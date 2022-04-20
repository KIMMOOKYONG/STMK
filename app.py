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