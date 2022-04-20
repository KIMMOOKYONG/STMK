import datetime as dt
import requests
import json
import pandas as pd
from pandas import DataFrame
import numpy as np
import time

"""
# -------------------------------------
네이버 금융에서 주가 데이터 다운로드 받기
# -------------------------------------
@ticker: 종목코드, 001440
@start: 시작일, 20200101
@end: 종료일, 20201231
"""
def s_download(ticker, start, end):
    time.sleep(0.2)
    url = f"https://fchart.stock.naver.com/siseJson.nhn?symbol={ticker}&requestType=1&startTime={start}&endTime={end}&timeframe=day"
    result = requests.post(url)

    data1 = result.text.replace("'",  '"').strip()
    data1 = json.loads(data1)

    data2 = DataFrame(data1[1:], columns=data1[0])
    data2 = data2.reset_index()
    data2["날짜"] = pd.to_datetime(data2["날짜"])

    df = data2[["날짜","시가", "고가", "저가", "종가", "거래량"]].copy()
    df.columns = ["date", "open", "high", "low", "close", "volume"]
    df = df.set_index("date")
    df = df.dropna()
    df.loc[:,["open", "high", "low", "close", "volume"]] = df.loc[:,["open", "high", "low", "close", "volume"]].astype(int)
    df = df.loc[:,["open", "high", "low", "close", "volume"]]       
    return df

   
"""
#--------------------------------------------------------------------------
네이버에서 주가 데이터 다운로드 받는 예시
#--------------------------------------------------------------------------
%%writefile app.py
from IPython.display import display 
import pandas as pd
import numpy as np
import os
import preprocessing.download as dn

import argparse

# 인자값을 받을 수 있는 인스턴스 생성
parser = argparse.ArgumentParser(description="종목코드를 입력하세요.")
# 입력받을 인자값 등록
parser.add_argument("--ticker", required=True, help="종목코드를 입력하세요.")
# 입력받은 인자값을 args에 저장 (type: namespace)
args = parser.parse_args()
ticker = args.ticker

save_data_path = os.getcwd()
save_data_path = os.path.join(save_data_path, "datasets")
save_data = os.path.join(save_data_path, ticker)

data = dn.s_download(ticker, "20210101", "20211232")
display(data)
"""
