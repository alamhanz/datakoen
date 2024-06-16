"""Webpage for regression model."""

import sys
from io import StringIO

import streamlit as st
import yaml
from annotated_text import annotated_text
from pages.tools.assets import set_assets
from pages.tools.calc import RunRegression
from pages.tools.common import config_types, split_col_types, upload_data
from pages.tools.utils import footer

# with open("config.yaml", "r") as f:
#     st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
# zippath = st.session_state['config']['zippath']

set_assets(st.session_state["config"])
df = upload_data()

## opening
st.title("Regression")
st.markdown("drag and drop regression")

## processing
if df is not None:
    tab1, tab2 = st.tabs(["Workspace", "Data Types Edit"])
    with tab2:
        df = config_types(df)

    with st.sidebar:
        dshape = df.shape
        show = st.checkbox("show the data raw")
        st.success(f"Your total observation is {dshape[0]}")
        add_c = st.checkbox("with bias", value=True, key="add_constant")

    with tab1:
        all_dimensions, all_measures = split_col_types(df)
        annotated_text("Your data source: ", (st.session_state["dataset"].name, ""))

        target_opt = st.selectbox("target variable:", all_measures, key="target_reg")
        all_feats = [i for i in all_measures if i != target_opt]
        features_opt = st.multiselect(
            "dependent variable:", all_feats, key="feature_reg"
        )

        # show = st.checkbox('standardize',key='is_standardized')
        reg_model = RunRegression(df)

        # st.caption(reg_model.summary())
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()

        print(reg_model.summary())

        sys.stdout = old_stdout
        st.text(mystdout.getvalue())

    if show:
        st.caption("Sample of Raw Data Below")
        st.table(df.to_pandas().sample(10))

# footer
footer()
