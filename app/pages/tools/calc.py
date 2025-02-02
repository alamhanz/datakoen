"""Calculation Capability

Contains all calculation
"""

import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl
import seaborn as sns
import statsmodels.api as sm
import streamlit as st
from scipy.stats import norm
from statsmodels.tsa.arima.model import ARIMA

# import uuid


def RunRegression(df):
    """Run regression given dataframe.

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    df = df.to_pandas()
    x = df[st.session_state["feature_reg"]].fillna(0)
    y = df[st.session_state["target_reg"]].fillna(0)

    if st.session_state["add_constant"]:
        x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model


# Standardize


def zscore_calc_proportion(N, proporsi, tailed):
    """
    Return zcore.

    N --> list dari banyaknya data di dua grup [N1, N2]
    proporsi --> list dari proporsi di dua grup [p1, p2]
    """
    N1 = N[0]
    N2 = N[1]
    p1 = proporsi[0]
    p2 = proporsi[1]

    N_all = (1 / N1) + (1 / N2)
    p_all = ((N1 * p1) + (N2 * p2)) / (N1 + N2)

    z_score = (p1 - p2) / np.sqrt(p_all * (1 - p_all) * (N_all))
    if tailed == 2:
        p_value = norm.pdf(z_score)
    else:
        p_value = norm.pdf(z_score) / 2

    return p_value, z_score


class ztest_2prop:
    """Run ztest from 2 sets.

    ztest class
    """

    def __init__(self, N, proporsi, tailed):
        """init

        ztest class
        """
        self.ukuran_sampel = N
        self.proporsi = proporsi
        # self.alpha = alp
        self.tailed = tailed
        self.pval = 1.0
        self.zscore = 0.0
        self.df_group = pd.DataFrame()

    def calc_zscore(self):
        """zscore

        zscore is calculated
        """
        self.pval, self.zscore = zscore_calc_proportion(
            self.ukuran_sampel, self.proporsi, self.tailed
        )
        return self.pval, self.zscore

    def simulasi_sampel(self, sampel_simulasi):
        """simulation

        sample simulation
        """
        mean_group1 = self.proporsi[0]
        stddev_group1 = np.sqrt(
            (mean_group1 * (1 - mean_group1)) / self.ukuran_sampel[0]
        )
        distribution_group1 = norm.rvs(
            size=sampel_simulasi, loc=mean_group1, scale=stddev_group1
        )

        mean_group2 = self.proporsi[1]
        stddev_group2 = np.sqrt(
            (mean_group2 * (1 - mean_group2)) / self.ukuran_sampel[1]
        )
        distribution_group2 = norm.rvs(
            size=sampel_simulasi, loc=mean_group2, scale=stddev_group2
        )

        dg1 = pd.DataFrame({"data": distribution_group1})
        dg1["groups"] = "group1"
        dg2 = pd.DataFrame({"data": distribution_group2})
        dg2["groups"] = "group2"
        self.df_group = pd.concat([dg1, dg2])

        # fig = plt.figure(figsize=(30, 25))
        sns.displot(data=self.df_group, x="data", hue="groups", kind="kde")
        st.pyplot(plt.gcf())


## timeseries
def set_ts_config(method_name, model_name, n_test):
    """set config for a ts model

    Args:
        method_name (str): name of timeseries method
        model_name (str): name of the model
        n_test (int): number of test

    Returns:
        grid : streamlit object
    """
    config = {}
    config["method"] = method_name
    config["n_test"] = n_test
    if method_name == "arima":
        p0 = st.number_input(
            "p", value=1, min_value=0, max_value=60, step=1, key="p_" + model_name
        )
        d0 = st.number_input(
            "d", min_value=0, max_value=2, step=1, key="d_" + model_name
        )
        q0 = st.number_input(
            "q", min_value=0, max_value=60, step=1, key="q_" + model_name
        )
        config["order"] = (p0, d0, q0)

        is_seasonal = st.checkbox("is seasonal", key="is_seasonal_" + model_name)

        if is_seasonal:
            periode = st.number_input(
                "Periode",
                value=7,
                min_value=0,
                max_value=365 * 2,
                step=1,
                key="periode_" + model_name,
            )
            p1 = st.number_input(
                "P", value=1, min_value=0, max_value=60, step=1, key="P_" + model_name
            )
            d1 = st.number_input(
                "D", min_value=0, max_value=2, step=1, key="D_" + model_name
            )
            q1 = st.number_input(
                "Q", min_value=0, max_value=60, step=1, key="Q_" + model_name
            )
            config["order_seasonal"] = (p1, d1, q1, periode)

        config["is_seasonal"] = is_seasonal

    elif method_name == "rolling":
        config["window_size"] = st.number_input(
            "window_size",
            value=2,
            min_value=2,
            max_value=100,
            step=1,
            key="win_size_" + model_name,
        )
        config["roll_method"] = st.selectbox(
            "Method:", ["mean", "median"], key="roll_method_" + model_name
        )

    else:
        config["test"] = 1

    return config


class timeseries_model:
    """Run timeseries model.

    ts class
    """

    def __init__(self, actual, config):
        """init

        initial all config
        """
        self.actual_ts = actual
        self.init_config = config
        self.n_test = self.init_config["n_test"]
        self.ts_pred_data = pl.Series([])

    def run(self):
        """run timeseries model

        start the prediction
        """
        train_part = self.actual_ts[: -self.n_test].to_numpy()
        # test_part = self.actual_ts[-self.n_test :].to_numpy()

        if self.init_config["method"] == "arima":
            if self.init_config["is_seasonal"]:
                model_ = ARIMA(
                    train_part,
                    order=self.init_config["order"],
                    seasonal_order=self.init_config["order_seasonal"],
                )
            else:
                model_ = ARIMA(train_part, order=self.init_config["order"])
            model_fit_ = model_.fit()

            train_part_pred = model_fit_.get_prediction().predicted_mean
            test_part_pred = model_fit_.forecast(steps=self.n_test)

            ts_pred_data_array = np.append(train_part_pred, test_part_pred, 0)
            self.ts_pred_data = pl.Series(ts_pred_data_array)

        elif self.init_config["method"] == "rolling":
            # dt["Temp"].rolling_mean(window_size=10)
            w_size = self.init_config["window_size"]
            if self.init_config["roll_method"] == "mean":
                self.ts_pred_data = self.actual_ts.rolling_mean(window_size=w_size)
            elif self.init_config["roll_method"] == "median":
                self.ts_pred_data = self.actual_ts.rolling_median(window_size=w_size)
            else:
                self.ts_pred_data = self.actual_ts.rolling_mean(window_size=w_size)
        else:
            # self.ts_pred_data = self.actual_ts + random.randint(9, 25)
            m_train = train_part.mean()
            v_train = train_part.std()
            test_part_pred = np.array(
                [
                    m_train + random.uniform(-1 * v_train * 1.5, v_train * 1.5)
                    for i in range(self.n_test)
                ]
            )

            ts_pred_data_array = np.append(train_part, test_part_pred, 0)
            self.ts_pred_data = pl.Series(ts_pred_data_array)

        return self.ts_pred_data

    def evaluate(self):
        """time series evaluation

        evaluating the time series
        """
        return 1


def add_ts():
    """adding ts

    add time series model
    """
    max_id = str(len(st.session_state["ts_lines"].keys()))
    st.session_state["ts_lines"]["predict_{}".format(max_id)] = []


def ts_pred(actual_ts, name, n_test):
    """one model time series run

    running time series model
    """
    method_opt = ["arima", "rolling", "random"]

    ts_container = st.empty()
    ts_columns = ts_container.columns((3, 2))
    ts_method = ts_columns[0].selectbox("Method:", method_opt, key=name)
    with ts_columns[1].expander("{}-config".format(name)):
        st.write(f"depends on the {ts_method}")
        config = set_ts_config(ts_method, name, n_test)
        # config = {}
        # config["method"] = ts_method
        # config["n_test"] = 15
        ts_model = timeseries_model(actual_ts, config)

    return ts_model.run()


def run_all_ts(data_ts, n_test=4):
    """all run

    running all time series model
    """
    all_ts = []
    if len(data_ts.keys()) > 1:
        max_test = int(len(data_ts["actual"]) * 0.4)
        default_test = int(len(data_ts["actual"]) * 0.2)
        n_test = st.number_input(
            "Number of Test",
            value=default_test,
            min_value=1,
            max_value=max_test,
            step=1,
            key="number_test",
        )

    for method_name in data_ts.keys():
        if method_name != "actual":
            pred_ts = ts_pred(data_ts["actual"], method_name, n_test)
        else:
            pred_ts = data_ts["actual"]
        all_ts.append(pred_ts)
    return all_ts
