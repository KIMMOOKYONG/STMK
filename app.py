from IPython.display import display 
import pandas as pd
import numpy as np
import os
import preprocessing.create_logistic_regression_data as lrdata

load_data_path = os.getcwd()
load_data_path = os.path.join(load_data_path, "datasets")
load_data = os.path.join(load_data_path, "000270")
data = pd.read_csv(load_data)
data["date"] = pd.to_datetime(data["date"])
data = data.reset_index(drop=True)

# 날짜 인덱스로 변환
data = data.set_index("date")

data = lrdata.create_training_data_using_lag(data, 50)
display(data)