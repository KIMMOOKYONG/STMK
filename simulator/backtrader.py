# !pip install backtrader

import backtrader as bt
from backtrader import plot
import backtrader.feeds as btFeeds

"""
backtrader 시뮬레이션 실행
"""
def backtrader_run(data, strategy, init_cash=1_000_000, commission=0.0, stake=1):

    data = bt.feeds.PandasData(dataname=data)

    cerebro = bt.Cerebro()  
    cerebro.adddata(data) 
    cerebro.addstrategy(strategy) 
    cerebro.addsizer(bt.sizers.FixedSize,stake=stake)
    cerebro.broker.setcash(init_cash) 
    cerebro.broker.setcommission(commission=commission) 
    cerebro.run()

    return cerebro

"""
backtrader 시뮬레이션 결과를 이미지로 저장
"""
def saveplots(cerebro, numfigs=1, iplot=True, start=None, end=None,
             width=16, height=9, dpi=300, tight=True, use=None, file_path = '', **kwargs):

        if cerebro.p.oldsync:
            plotter = plot.Plot_OldSync(**kwargs)
        else:
            plotter = plot.Plot(**kwargs)

        figs = []
        for stratlist in cerebro.runstrats:
            for si, strat in enumerate(stratlist):
                rfig = plotter.plot(strat, figid=si * 100,
                                    numfigs=numfigs, iplot=iplot,
                                    start=start, end=end, use=use)
                figs.append(rfig)

        for fig in figs:
            for f in fig:
                f.savefig(file_path, bbox_inches='tight')
        return figs