import pandas as pd
import json
from sklearn.externals import joblib
import os
import numpy as np
from scipy.linalg import lstsq

from pyboot.conf import PYBOOT_HOME


def model_loader(model_path):
    model = joblib.load(model_path)
    long_window_threshold = model["long_window_threshold"]
    short_window_threshold = model["short_window_threshold"]
    long_window_length = model["long_window_length"]
    short_window_length = model["short_window_length"]
    tolerance = model["tolerance"]
    pointName_input = model['pointName']
    return long_window_threshold, short_window_threshold, long_window_length, short_window_length, tolerance, pointName_input

def input_data_slope_fitting(data_datetime, data_param, window_length, tolerance):
    """
    data_datetime: list_like, record down to milliseconds
    data_param: list_like, parameter value
    window_length: int down to hours
    tolerance: accepted time span rate， 0.1 denote 6 * (1-0.1) = 5.4 hours if window_lenth is 6 hours
    """
    
    try:
        df = pd.DataFrame({"datetime": data_datetime, "param": data_param})
    except Exception as e:
        return e
    df.reset_index(drop=True, inplace=True)
    target_data_point_time = df["datetime"][df.shape[0]-1]
    accepted_duration = int( (pd.Timedelta(str(window_length)+"hours") * (1-tolerance)).total_seconds() * 1000)
    start_position = target_data_point_time - pd.Timedelta(str(window_length)+"hours").total_seconds() * 1000
    df_temp = df.loc[df["datetime"]>=start_position]
    df_temp.reset_index(drop=True, inplace=True)

    if df_temp["datetime"][df_temp.shape[0]-1] - df_temp["datetime"][0] < accepted_duration:
        return "More data is required, the current length of data is less than {} hours\
         and current window length is {} hours ".format((1-tolerance)*window_length, window_length)
    x = np.asarray(df_temp["datetime"].tolist())
    y = np.asarray(df_temp["param"].tolist())
    fitted_slope = (np.cov(x,y)[0][1]) / (np.var(x,ddof=1))
    return fitted_slope

def trend_warning(data_datetime, data_param, window_type):

    window_threshold = None
    window_length = None
    window_type_cn = ""

    path = os.path.dirname(os.path.abspath(__file__))
    f_list = os.listdir(path)
    for f in f_list:
        if ".model" in f:
            filename = f

    model_file_path = os.path.join(path, filename)
    long_window_threshold, short_window_threshold, long_window_length, short_window_length, tolerance, pointName_input = model_loader(model_file_path)
    if window_type == "long":
        window_threshold = long_window_threshold
        window_length = long_window_length
        window_type_cn = "长"
    elif window_type == "short":
        window_threshold = short_window_threshold
        window_length = short_window_length
        window_type_cn = "短"

    fitted_slope = input_data_slope_fitting(data_datetime, data_param, window_length, tolerance)

    if isinstance(fitted_slope, str):
        result = "EXCEPTION"
        pointName = pointName_input
        alarmType = "TYPE_TREND_WARNING"
        alarmLevel = ""
        alarmValue = ""
        alarmThreshold = ""
        alarmTime = ""
        alarmReason = ""
        errorReason = fitted_slope
    elif fitted_slope >= window_threshold:
        result = "ABNORMAL"
        pointName = pointName_input
        alarmType = "TYPE_TREND_WARNING"
        alarmLevel = "HIGH_ALARM"
        alarmValue = fitted_slope
        alarmThreshold = window_threshold
        alarmTime = data_datetime[-1]
        alarmReason = "{}窗口趋势阈值超过高限".format(window_type_cn)
        errorReason = ""
    else:
        result = "NORMAL"
        pointName = pointName_input
        alarmType = ""
        alarmLevel = ""
        alarmValue = ""
        alarmThreshold = ""
        alarmTime = ""
        alarmReason = ""
        errorReason = ""


    result = {"result": result, "pointName": pointName, "alarmType": alarmType, "alarmLevel": alarmLevel, 
              "alarmValue": alarmValue, "alarmThreshold": alarmThreshold, 
              "alarmTime": alarmTime, "alarmReason": alarmReason, "errorReason": errorReason}
    return result


def handler(event, context):

    data_datetime_list = []
    data_param_list =[]
    window_type = event["model_data"]["window"]
    for item in event["model_data"]["trend_model_data"]:
        data_datetime_list.append(item[0])
        data_param_list.append(item[1])

    event["alarmResult"] = trend_warning(data_datetime_list, data_param_list, window_type)
    event["model_data"]["trend_model_data"] =  ""
    return event


# 本地测试
if __name__ == "__main__":
    input_data_filname = os.path.join(PYBOOT_HOME, 'tests/test_data/theshld.json')

    with open(input_data_filname, encoding='UTF-8') as inputfile:
        data = json.load(inputfile)
    context = ""
    event = handler(data, context)
    print(event)
