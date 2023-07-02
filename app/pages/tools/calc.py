import numpy as np
import streamlit as st

import statsmodels.api as sm


def RunRegression(df):

    df = df.to_pandas()
    x = df[st.session_state['feature_reg']].fillna(0)
    y = df[st.session_state['target_reg']].fillna(0)

    if st.session_state['add_constant']:
        x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    return model

## Standardize