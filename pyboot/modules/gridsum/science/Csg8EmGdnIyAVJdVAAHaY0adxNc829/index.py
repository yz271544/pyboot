import json

import lightgbm
import numpy as np
import os
import pandas as pd
from sklearn.externals import joblib
import time
import traceback

from pyboot.conf import PYBOOT_HOME


def data_preprocess_wrapper(df):
    # column rename
    df = df.fillna(method='ffill').fillna(method='bfill')
    return df

class Multivariate:
    def __init__(self, init_path=None):

        if init_path is None:
            raise ValueError('Invalid init path')
        else:
            # load from existing model
            model = joblib.load(init_path)
            self.multivariate_feature = model.multivariate_feature
            self.threshold = model.threshold
            self.model_dict = model.model
            self.error_record = {}

    def test(self, data):
        for feature_key, feature_list in self.multivariate_feature.items():
            # predict one feature with other features
            data[feature_key + '_error'] = 0
            for i in range(len(feature_list)):
                temp = feature_list.copy()
                target = temp.pop(i)
                feature = temp
                x_test = data[feature]
                y_test = data[target]
                y_pred = self.model_dict[(feature_key, target)].predict(x_test)
                data[feature_key + '_error'] += np.array(abs((y_test - y_pred) / y_test * 100))
            data[feature_key + '_error'] /= len(feature_list)
            data[feature_key + '_multi_alarm'] = data[feature_key + '_error'] > self.threshold[feature_key]
        return data

    def test_for_dict(self, data):
        # get diagnostic results from dictionary data
        try:
            res = data_preprocess_wrapper(pd.DataFrame(data, index=[0]))
            res = self.test(res)
            res = dict(res.iloc[0, :])
            alarm_res = {
                "result": "NORMAL",
                "alarmType": "",
                "alarmLevel": "",
                "alarmValue": "",
                "alarmThreshold": "",
                "alarmTime": "",
                "alarmReason": "",
                "errorReason": ""
            }
            for i in res.keys():
                if '_multi_alarm' not in i:
                    continue
                if res[i]:
                    alarm_res['result'] = "ABNORMAL"
                    alarm_res['alarmType'] = "MULTIVARIATE_LINKAGE_WARNING"
                    alarm_res['alarmLevel'] = "HIGH_ALARM"
                    alarm_res['alarmValue'] = res[i.strip('_multi_alarm') + '_error']
                    alarm_res['alarmThreshold'] = self.threshold[i.strip('_multi_alarm')]
                    alarm_res['alarmTime'] = int(time.time())
                    alarm_res['alarmReason'] = "多变量数值组合超出正常范围"
                    alarm_res['errorReason'] = ""
                    break
        except Exception as e:
            alarm_res = {
                "result": "EXCEPTION",
                "alarmType": "",
                "alarmLevel": "",
                "alarmValue": "",
                "alarmThreshold": "",
                "alarmTime": "",
                "alarmReason": "",
                "errorReason": traceback.format_exc()
            }
        return alarm_res

def handler(event, content):
    data = event['model_data']
    # get the model path
    path = os.path.dirname(os.path.abspath(__file__))
    f_list = os.listdir(path)
    for f in f_list:
        if ".model" in f:
            filename = f
    model_file_path = os.path.join(path, filename)
    # generate agent
    Multi = Multivariate(init_path=model_file_path)
    # get diagnostic results
    event['alarmResult'] = Multi.test_for_dict(data=data)
    event['model_data'] = ""
    return event


# 本地测试
if __name__ == "__main__":
    input_data_filname = os.path.join(PYBOOT_HOME, 'tests/test_data/multi_var.json')

    with open(input_data_filname, encoding='UTF-8') as inputfile:
        data = json.load(inputfile)
    context = ""
    event = handler(data, context)
    print(event)
