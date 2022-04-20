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
입력 데이터 프레임 구조
date,open,high,low,close,volume

반환 데이터 프레임 구조(lag_range=5)
date,today,lag_1,lag_2,lag_3,lag_4,lag_5,volume,direction
"""
def create_training_data(data, lag_range=5):
    """
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

    # 전일 보다 주가가 상승했으면 up, 하락했으면 down으로 라벨링
    df["direction"] = [1 if i > 0 else 0 for i in df["today"]]

    return df
   