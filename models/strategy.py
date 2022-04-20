import backtrader as bt
import backtrader.feeds as btFeeds

class ta(bt.Strategy):
    def __init__(self):

        self.dataclose= self.datas[0].close
        bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        bt.indicators.WeightedMovingAverage(self.datas[0], period=25, subplot = False)
        bt.indicators.StochasticSlow(self.datas[0], subplot=True)
        bt.indicators.MACDHisto(self.datas[0])
        rsi = bt.indicators.RSI(self.datas[0])
        bt.indicators.SmoothedMovingAverage(rsi, period=10)
        bt.indicators.ATR(self.datas[0], plot = True)
