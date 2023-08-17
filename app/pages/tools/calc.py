"""Calculation Capability

Contains all calculation 
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import polars as pl
import seaborn as sns
import statsmodels.api as sm
import streamlit as st
from scipy.stats import norm
import random
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
def set_config(model_name):
    if model_name == "arima":
        xxx
    else:
        xxx


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

    def run(self):
        """run timeseries model

        start the prediction
        """
        ts_pred_data = []
        if self.init_config["method"] == "arima":
            train_part = self.actual_ts[self.n_test :].to_numpy()
            # test_part = self.actual_ts[: self.n_test]

            model_ = ARIMA(train_part, order=(2, 1, 1), seasonal_order=(1, 0, 0, 14))
            model_fit_ = model_.fit()

            train_part_pred = model_fit_.get_prediction().predicted_mean
            test_part_pred = model_fit_.forecast(steps=self.n_test)

            print(train_part_pred)
            print(test_part_pred)

            ts_pred_data_array = np.append(train_part_pred, test_part_pred, 0)
            self.ts_pred_data = pl.Series(ts_pred_data_array)

        else:
            self.ts_pred_data = self.actual_ts + random.randint(9, 25)

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


def ts_pred(actual_ts, name):
    """one model time series run

    running time series model
    """
    method_opt = ["arima", "not_arima"]

    ts_container = st.empty()
    ts_columns = ts_container.columns((3, 2))
    ts_method = ts_columns[0].selectbox("Method:", method_opt, key=name)
    with ts_columns[1].expander("{}-config".format(name)):
        st.write(f"depends on the {ts_method}")
        config = {}
        config["method"] = ts_method
        config["n_test"] = 15
        ts_model = timeseries_model(actual_ts, config)

    return ts_model.run()


def run_all_ts(data_ts):
    """all run

    running all time series model
    """
    all_ts = []
    for method_name in data_ts.keys():
        if method_name != "actual":
            pred_ts = ts_pred(data_ts["actual"], method_name)
        else:
            pred_ts = data_ts["actual"]
        all_ts.append(pred_ts)
    return all_ts
