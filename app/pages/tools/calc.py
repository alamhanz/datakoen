"""Calculate OLS regression."""
import statsmodels.api as sm
import streamlit as st


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
