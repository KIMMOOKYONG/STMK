import numpy as np

import backtrader as bt
import backtrader.feeds as btFeeds

class ta(bt.Strategy):
    def __init__(self):

        self.dataclose= self.datas[0].close
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot = False)
        # bt.indicators.StochasticSlow(self.datas[0], subplot=True)
        bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot = True)

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)

# Create a Stratey
optimization = False
class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 20),
    )

    def log(self, txt, optimization=False, dt=None):
        if optimization:
            return
        
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        self.hma = bt.indicators.HullMovingAverage(
            self.datas[0], period=self.params.maperiod)

    def notify_order(self, order):
        global lastBuy
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                lastBuy = self.datas[0].datetime.date(0)
                self.log(
                    'BUY EXECUTED, Price: $%.2f, Cost: $%.2f ($Comm %.2f)' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm), optimization=optimization)

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: $%.2f, Cost: $%.2f (Comm $%.2f)' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm), optimization=optimization)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected', optimization=optimization)

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION GROSS $%.2f, NET $%.2f, PROFIT %.2f%%' %
                 (trade.pnl, trade.pnlcomm, trade.pnlcomm/trade.price*100), optimization=optimization)
        

    def next(self):
        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            # check for HMA trend reversal
            if self.hma[-2] >= self.hma[-1] and \
               self.hma[-1] < self.hma[0]:

                self.log('BUY CREATE, $%.2f' % self.dataclose[0], optimization=optimization)

                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:
            # check for HMA trend reversal
            if self.hma[-2] <= self.hma[-1] and \
               self.hma[-1] > self.hma[0]:

                self.log('SELL CREATE, $%.2f' % self.dataclose[0], optimization=optimization)

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()

    def stop(self):
        self.log('(MA Period %2d) Ending Value %.2f' %
                 (self.params.maperiod, self.broker.getvalue()), optimization=optimization)
        
        # keep track of results for each period backtest
        strategyResults[self.params.maperiod] = self.broker.getvalue()


from sklearn import linear_model

class LinearRegressionModel(bt.Strategy):
    # params = (
    #     ("linear_reg_length", 20),
    # )
       
    def __init__(self):
        self.dataclose = self.datas[0].close
        self.datalow = self.datas[0].low
        self.LR_low_trend = LinearRegression(self.datalow, len=20)

    def next(self):
        if self.LR_low_trend < self.data.close and (not self.long):
            self.size_to_buy = self.broker.getvalue()/ self.dataclose[0]
            self.order = self.buy(exectype=bt.Order.Market, size=self.size_to_buy)
        elif self.LR_low_trend > self.data.close and self.long:
            self.order = self.sell(exectype=bt.Order.Market, size=self.size_to_buy)

class LinearRegression(bt.Indicator):
    alias = ("LR")

    lines = ("linear_regression", "ma")
    params = (
        ("len", 300)
    )
    iter = 0

    def changeLen(self, length):
        self.params.len = length


    def next(self):
        if (self.iter > self.params.len):
            raw_prices = self.data.get(size=self.params.len)
            prices = np.array(raw_prices).reshape(-1, 1)
            x_line = np.array([i for i in range(0, self.params.len)]).reshape(-1, 1)

            # create linear regression object
            regr = linear_model.LinearRegression()

            # train the model using the training sets
            regr.fit(x_line, prices)
            prediction = regr.predict(np.array([self.params.len]).reshape(-1, 1))
            self.lines.linear_regression[0] = prediction

        self.iter += 1

        