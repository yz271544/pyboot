"""
预警类模型训练算子
"""

import pandas as pd
import numpy as np
from scipy.linalg import lstsq
from sklearn.neighbors.kde import KernelDensity

import lightgbm
import os
from sklearn.externals import joblib
import time
import traceback

## ====================自适应阈值计算部分=============================================
def kde_density(data, tag):
    """核密度估计"""
    kde = KernelDensity(kernel="gaussian", bandwidth=1).fit(data[tag].values.reshape(-1, 1))
    return kde

def probability_distribution(data, tag):
    """拟合概率密度分布函数"""
    kde = kde_density(data, tag)
    data_probability = pd.DataFrame()
    data_probability["list"] = np.linspace(data[tag].min(), data[tag].max(), 1000, endpoint=True)
    data_probability["score"] = np.exp(kde.score_samples(data_probability["list"].values.reshape(-1, 1)))
    return data_probability

def get_quantile(data, score, alfa):
    """根据置信度获取上下分位数"""
    sum_v = data[score].sum()
    n = data.shape[0]
    m = sum_v * (1-alfa) / 2
    a = 0
    for i in range(n-1):
        a += data[score][i]
        if a > m:
            lp = data["list"][i]
            break
    b = 0
    for i in range(1, n):
        b += data[score][n-i]
        if b > m:
            hp = data["list"][n-i]
            break
    return lp, hp

def get_throld(lp, hp, factor_list):
    """计算上下限阈值"""
    if factor_list[0]:
        llv = lp - (1 - factor_list[0]) * (hp - lp)
    else:
        llv = 0
    if factor_list[1]:
        lv = lp - (1 - factor_list[1]) * (hp - lp)
    else:
        lv = 0
    if factor_list[2]:
        hv = hp + (factor_list[2] - 1) * (hp - lp)
    else:
        hv = 0
    if factor_list[3]:
        hhv = hp + (factor_list[3] - 1) * (hp - lp)
    else:
        hhv = 0
    return [llv, lv, hv, hhv]

def adaptive_threshold(data, tag, timestamp, factor_list=[0, 0, 1, 1.1], confidence=0.95, distribution="gaussian"):
    """计算单个测点的自适应阈值"""
    data1 = data[[timestamp, tag]]
    # data_probability = probability_distribution(data2, tag)
    data_probability = probability_distribution(data1, tag)
    lp, hp = get_quantile(data_probability, "score", confidence)
    throld_list = get_throld(lp, hp, factor_list)
    threshold = {
        "llv": throld_list[0],
        "lv": throld_list[1],
        "hv": throld_list[2],
        "hhv": throld_list[3]
    }
    return threshold

## =====================趋势预警计算部分==========================================
def mad_outlier_detector(data, MAD_multiplier):
    """
    使用MAD找出离群点
    """
    median_value = np.median(data)
    bias_array = data - median_value # 绝对偏差集合
    mad = 1.4826 * np.median(list(map(abs,bias_array)))
    # 绝对偏差中位数, 1.4826 为Consistency Constant，这里假设数据分布为normal distribution
    reuslt_array = bias_array / mad
    outlier_array = np.asarray([i for i in reuslt_array if abs(i) > MAD_multiplier]) * mad + median_value  
    if len(outlier_array) > 0:
        pass
    else:
        return max(map(abs, data))
    return min(map(abs,outlier_array))

def fitted_slope_threshold(data, para_type, timestamp, window_length, tolerance, window_shift_length=0):
    """
    用给定的时间窗口拟合各时间点的线性变化斜率
    data 连续时间区间内的数据集(因剔除离群点造成数据点间有一定间隔), dataframe格式, 包含时间字段 'datetime',
    由于斜率的拟合是要用到历史数据, 因此会存在一部分数据无法拟合其斜率, 因此在返回时用np.nan插入斜率值
    window_length 时间窗口长度 '6hours' 或者 '6 hours' 均可以
    para_type 热力参数类型
    window_shift_length 窗口滑动长度, 若长度为0 则窗口按索引号依次滑动
    """
    
    # if data.shape[0] <= 1:
    #     raise Exception('the length of input size must be at least two (find_fitted_slope)')
    
    slope_list = []
    data_copy = data[[timestamp, 'datetime_num', para_type]].copy()
    start_position = data_copy[timestamp].min() + pd.Timedelta(window_length)
    data_candidate = data_copy.loc[data_copy[timestamp] >= start_position].copy().reset_index(drop=True)
    if data_candidate.shape[0] == 0:
        return np.nan

    duration = int((pd.Timedelta(window_length) * (1-tolerance)).total_seconds()) # 可容忍历史区间, 该区间保证提取的历史数据跨度不会过小
    
    
    if window_shift_length == 0:
        for dt in data_candidate[timestamp].sort_values():
            df_temp = data_copy.loc[(data_copy[timestamp] <= dt) & (data_copy[timestamp] >= dt - pd.Timedelta(window_length))].reset_index(drop=True)
            if df_temp.shape[0] <= 1:
                slope_list.append(np.nan)
            elif (df_temp['datetime_num'].max() - df_temp['datetime_num'].min() )< duration:
                slope_list.append(np.nan)
            else:
                x = np.asarray(df_temp['datetime_num'].tolist())
                y = np.asarray(df_temp[para_type].tolist())
                p, _, _, _ = lstsq(x[:, np.newaxis] ** [0,1], y, lapack_driver='gelsy')
                slope_list.append(p[1])
    else:
        dt = data_candidate[timestamp].min()
        while dt <= data_candidate[timestamp].max():
            df_temp = data_copy.loc[(data_copy[timestamp] <= dt) & (data_copy[timestamp] >= dt - pd.Timedelta(window_length))].reset_index(drop=True)
            if df_temp.shape[0] <= 1:
                slope_list.append(np.nan)
            elif (df_temp['datetime_num'].max() - df_temp['datetime_num'].min() )< duration:
                slope_list.append(np.nan)
            else:
                x = np.asarray(df_temp['datetime_num'].tolist())
                y = np.asarray(df_temp[para_type].tolist())
                p, _, _, _ = lstsq(x[:, np.newaxis] ** [0,1], y, lapack_driver='gelsy')
                slope_list.append(p[1])

            next_shift = dt + pd.Timedelta(window_length) * window_shift_length
            next_point = data_copy.loc[data_copy[timestamp]>dt][timestamp].min()
            if next_point >= next_shift:
                dt = next_point
            else:
                dt = next_shift
            
    ser = list(pd.Series(slope_list).dropna())
    if len(ser) == 0:
        threshold = np.nan
    else:
        threshold = mad_outlier_detector(ser, 3)
    return threshold

## ===================多变量联动预警计算部分==================================
def data_preprocess_wrapper(df):
    # column rename
    df = df.fillna(method='ffill').fillna(method='bfill')
    return df


class MultiRes:
    def __init__(self, feature, threshold, model):
        self.multivariate_feature = feature
        self.threshold = threshold
        self.model = model


class Multivariate:
    def __init__(self, multivariate_feature, params, init_path=None):

        if init_path is None or not os.path.exists(init_path):
            # model save
            self.model_dict = {}
            # error store
            self.error_record = {}
            # threshold store
            self.threshold = {}
            self.params = params
            self.multivariate_feature = multivariate_feature
        else:
            # load from existing model
            model = joblib.load(open(os.path.join(init_path, 'multivariate.model'), 'rb'))
            self.multivariate_feature = model.multivariate_feature
            self.threshold = model.threshold
            self.model_dict = model.model
            self.error_record = {}

    def training_wrapper(self, data, save_path=None):
        trn_data = data[:int(self.params["train_test_ratio"]["exact"] * len(data))].copy()
        for feature_key, feature_list in self.multivariate_feature.items():
            # predict one feature with other features
            for i in range(len(feature_list)):
                temp = feature_list.copy()
                target = temp.pop(i)
                feature = temp
                x_train = trn_data[feature]
                y_train = trn_data[target]
                self.model_dict[(feature_key, target)] = self.training(x_train, y_train)
        # calculate error
        self.error_test_data(data)
        # get threshold
        self.get_threshold()
        # model save
        if save_path is None:
            save_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'model')
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        res = MultiRes(feature=self.multivariate_feature,
                       threshold=self.threshold,
                       model=self.model_dict)
        # joblib.dump(res, open(os.path.join(save_path, 'multivariate.model'), 'wb'))
        return res

    def training(self, X, y):
        gbm = lightgbm.LGBMRegressor(
            objective='regression',
            learning_rate=self.params["learning_rate"]["exact"],
            n_estimators=self.params["n_estimators"]["exact"])
        gbm.fit(X, y)
        res = gbm
        return res

    def error_test_data(self, data):
        test_data = data[int(self.params["train_test_ratio"]["exact"] *
                             len(data)):].copy()
        for feature_key, feature_list in self.multivariate_feature.items():
            # predict one feature with other features
            self.error_record[feature_key] = np.zeros(shape=len(test_data))
            for i in range(len(feature_list)):
                temp = feature_list.copy()
                target = temp.pop(i)
                feature = temp
                x_test = test_data[feature]
                y_test = test_data[target]
                y_pred = self.model_dict[(feature_key, target)].predict(x_test)
                self.error_record[feature_key] += np.array(
                    abs((y_test - y_pred) / y_test * 100))
            self.error_record[feature_key] /= len(feature_list)

    def get_threshold(self):
        # get threshold used to judge if there is a fault
        for i in self.error_record.keys():
            self.threshold[i] = np.percentile(self.error_record[i], self.params["upper_limit"]["exact"]) \
                                + self.params["window_ratio"]["exact"] * (
                np.percentile(self.error_record[i], self.params["upper_limit"]["exact"]) -
                np.percentile(self.error_record[i], self.params["lower_limit"]["exact"]))

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
        except:
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


def multivariate_linkage_alarm_train(file_, multivariate_feature, params):
    # load data
    df = file_
    # data preprocess
    df = data_preprocess_wrapper(df)
    # generate agent
    Multi = Multivariate(multivariate_feature=multivariate_feature,
                         params=params)
    model = Multi.training_wrapper(data=df)
    return model

## =========================智能预警模型部分=============================

class alarm_base(object):
    def new_column_drop_duplicate(self, new_column, org_columns):
        is_cycle = True
        count = 0
        while (is_cycle):
            if count == 100:
                raise Exception(" Repeating limit (100 times) exceeded")
            new_column, org_columns, is_cycle = self.drop_duplicate(new_column, org_columns)
            count += 1
        return new_column

    def drop_duplicate(self, a, b_list):
        cycle = False
        b_list_copy = b_list.copy()
        for b in b_list_copy:
            if a == b:
                b_list_copy.remove(b)
                a += "_1"
                cycle = True
                break
        return a, b_list_copy, cycle

class adaptive_threshold_alarm(alarm_base):
    """自适应阈值"""
    def __init__(self):
        self.func_name = "adaptive_threshold_alarm"
        self.info = {}

    def apply(self, input_, field, params):
        file_ = None
        for input_object in input_:
            if input_object["input_index"] == 0:
                file_ = input_object["value"]

        for field_object in field:
            if field_object["input_index"] == 0:
                for setting in field_object["settings"]:
                    if setting["name"] == "特征列":
                        feature = setting["columns"][0]
                    if setting["name"] == "时间列":
                        timestamp = setting["columns"][0]

        distribution = params["probability_density"]["options"][0]
        confidence = params["confidence_coefficient"]["exact"]
        factor_llv = params["ampification_coefficient_llv"]["exact"]
        factor_lv = params["ampification_coefficient_lv"]["exact"]
        factor_hv = params["ampification_coefficient_hv"]["exact"]
        factor_hhv = params["ampification_coefficient_hhv"]["exact"]
        factor_list = [factor_llv, factor_lv, factor_hv, factor_hhv]

        threshold = adaptive_threshold(file_, feature, timestamp, factor_list=factor_list, confidence=confidence, distribution=distribution)
        # threshold = {"threshold_list": threshold_list}

        output = [
            {
                "output_index": 0,
                "type": "dict",
                "value": threshold
            },
            {
                "output_index": 1,
                "type": "model",
                "value": threshold
            }
        ]

        return output


class trend_detection_alarm(alarm_base):
    """趋势预警"""
    def __init__(self):
        self.func_name = "trend_detection_alarm"
        self.info = {}

    def apply(self, input_, field, params):
        file_ = None
        for input_object in input_:
            if input_object["input_index"] == 0:
                file_ = input_object["value"]

        for field_object in field:
            if field_object["input_index"] == 0:
                for setting in field_object["settings"]:
                    if setting["name"] == "特征列":
                        feature = setting["columns"][0]
                    if setting["name"] == "时间列":
                        timestamp = setting["columns"][0]
                    if setting["name"] == "开停机区间列":
                        territory = setting["columns"][0]
        file_[timestamp] = pd.to_datetime(file_[timestamp])
        file_['datetime_num'] = file_[timestamp].apply(lambda s: int(s.timestamp()))
        # 去掉数据中有NaN或者infs的行
        file_ = file_.replace([np.inf, -np.inf], np.nan).dropna()

        long_window = str(params["long_window"]["exact"]) + 'hours'
        short_window = str(params["short_window"]["exact"]) + 'hours'
        tolerance = params["tolerance"]["exact"]
        window_shift_length = params["window_shift_length"]["exact"]
        
        territory_list = file_[territory].value_counts().reset_index(drop=False)['index'].tolist()
        territory_list.sort()

        lw_threshold_list=[]
        sw_threshold_list =[]
        for ter in territory_list:
            print('territory number: {}'.format(ter))
            file_temp_ = file_.loc[file_[territory]==ter].copy()
            file_temp_.reset_index(inplace=True)
            if file_temp_.shape[0] < 20:
                pass
            else:
                lw_threshold_ = fitted_slope_threshold(file_temp_, feature, timestamp, long_window, tolerance, window_shift_length)
                sw_threshold_ = fitted_slope_threshold(file_temp_, feature, timestamp, short_window, tolerance, window_shift_length)
                lw_threshold_list.append(lw_threshold_)
                sw_threshold_list.append(sw_threshold_)
        
        if (len(lw_threshold_list)==0) or (len(sw_threshold_list)==0):
            raise Exception('Model training failed due to data shortage(less than 20 records) in each run-stop cycle.')
        threshold = {'long_window_threshold':max(lw_threshold_list), 'short_window_threshold': max(sw_threshold_list)} 
        threshold["long_window_length"] = params["long_window"]["exact"]
        threshold["short_window_length"] = params["short_window"]["exact"]
        threshold["tolerance"] = params["tolerance"]["exact"]
        # 加入测点名称
        threshold["pointName"] = feature

        output = [
            {
                "output_index": 0,
                "type": "model",
                "value": threshold
            }
        ]

        return output


class MultivariateLinkageAlarm(alarm_base):
    """多变量联合报警"""
    def __init__(self):
        self.func_name = "multivariate_linkage_alarm"
        self.info = {}

    def apply(self, input_, field, params):
        file_, setting = None, None
        for input_object in input_:
            if input_object["input_index"] == 0:
                file_ = input_object["value"]

        for field_object in field:
            if field_object["input_index"] == 0:
                setting_list = field_object["settings"]
        multivariate_feature = {}
        for feature in ['特征组合1', '特征组合2', '特征组合3']:
            for setting in setting_list:
                if feature == setting['name']:
                    multivariate_feature[feature] = setting['columns']
        model = multivariate_linkage_alarm_train(file_, multivariate_feature, params)

        output = [
            {
                "output_index": 0,
                "type": "model",
                "value": model
            }
        ]
        return output


class Alarm_operator(object):
    def __init__(self):
        self.operation_to_class = {
            "AdaptiveThresholdAlarm": adaptive_threshold_alarm(),
            "TrendDetectionAlarm": trend_detection_alarm(),
            "MultivariateLinkageAlarm": MultivariateLinkageAlarm(),
        }

    def train_v2(self, function_setting, function_name):
        input_ = function_setting["input"]
        field_ = function_setting["field"]
        param_ = function_setting["params"]
        operator = self.operation_to_class[function_name]
        output = operator.apply(input_, field_, param_)
        return output
