import os
import pandas as pd
import numpy as np
from scipy.signal import argrelextrema

import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (14,6)
plt.rcParams["lines.linewidth"] = 1
plt.rcParams["lines.color"] = "r"
plt.rcParams["axes.grid"] = True

"""
#--------------------------------------------------------------------------
일정 기간의 과거 주가 변동폭이 현재 주가의 방향성을 결정한다는 가정을 반영한
데이터셋을 만드는 함수 
#--------------------------------------------------------------------------

#--------------------------------------------------------------------------
참고
#--------------------------------------------------------------------------
입력 데이터 프레임 구조
date,open,high,low,close,volume

반환 데이터 프레임 구조(lag_range=5)
date,today,lag_1,lag_2,lag_3,lag_4,lag_5,volume,direction
"""
def create_training_data_using_lag(data, lag_range=5):
    """
    lag_range 설정 기간만큼의 lag 데이터 생성
    @data: 입력 데이터 프레임
    @lag_range: 분석시 참조할 주가 변화(시차) 기간 설정
    """

    # 전일 종가와 현재 종가의 주가 차이(변화율)
    df = data["close"].pct_change() * 100
    df = df.rename("today")
    df = df.reset_index()

    # 현재일 기준 5일간의 주가 변화(lag:시차) 데이터 생성
    for i in range(1, lag_range + 1):
        df["lag " + str(i)] = df["today"].shift(i)

    # 전일 거래량
    df["volume"] = data.volume.shift(1).values / 1000_000_000
    df = df.dropna()

    # 데이터 라벨링
    # 전일 보다 주가가 상승했으면 up, 하락했으면 down으로 라벨링    
    df["direction"] = [1 if i > 0 else 0 for i in df["today"]]

    return df

"""
#--------------------------------------------------------------------
create_training_data_using_lag(data, lag_range=5) 사용예시
#--------------------------------------------------------------------

%%writefile app.py
from IPython.display import display 
import pandas as pd
import numpy as np
import os
import preprocessing.create_logistic_regression_data as lrdata

import argparse

# 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser(description="종목코드를 입력하세요.")
# 입력받을 인자값 등록
parser.add_argument("--ticker", required=True, help="종목 코드를 입력하세요.")
# 입력받은 인자값을 args에 저장 (type: namespace)
args = parser.parse_args()
ticker = args.ticker

load_data_path = os.getcwd()
load_data_path = os.path.join(load_data_path, "datasets")
load_data = os.path.join(load_data_path, ticker)
data = pd.read_csv(load_data)
data["date"] = pd.to_datetime(data["date"])
data = data.reset_index(drop=True)

# 날짜 인덱스로 변환
data = data.set_index("date")

data = lrdata.create_training_data_using_lag(data, 50)
display(data)
# data.to_csv(ticker + "_preprocessing")
"""
  
   