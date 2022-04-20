from IPython.display import display 
import pandas as pd
import numpy as np
import os
import preprocessing.download as dn
import simulator.backtrader as bt
import models.strategy as st
import argparse

import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = [15, 8]
plt.rcParams.update({'font.size': 12}) 

# 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser(description="종목코드를 입력하세요.")
# 입력받을 인자값 등록
parser.add_argument("--ticker", required=True, help="종목코드를 입력하세요.")
# 입력받은 인자값을 args에 저장 (type: namespace)
args = parser.parse_args()
ticker = args.ticker

save_results_path = os.getcwd()
save_results_path = os.path.join(save_results_path, "results")
save_results_path = os.path.join(save_results_path, ticker + ".png")

data = dn.s_download(ticker, "20210101", "20221231")

display(data)

# 전략 클래스
model = st.ta
# 백테스팅
cerebro = bt.backtrader_run(data, model)

# 백테스팅결과저장
bt.saveplots(cerebro, file_path=save_results_path)