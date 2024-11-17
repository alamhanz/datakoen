"""Web page for table pivot."""

import streamlit as st
import yaml
from annotated_text import annotated_text
from pages.tools.assets import set_assets
from pages.tools.common import config_types, split_col_types, upload_data
from pages.tools.utils import footer

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])
df = upload_data()

# opening
st.title("Pivot")
st.markdown("pivoting your data for your exploration.")
st.markdown("\nUpload Your data first.")

# processing
if df is not None:
    tab1, tab2 = st.tabs(["Workspace", "Data Types Edit"])
    with tab2:
        df = config_types(df)

    with st.sidebar:
        dshape = df.shape
        show = st.checkbox("show the data raw")
        st.success(f"Your current data shape is {dshape[0]} x {dshape[1]}")

    with tab1:
        all_dimensions, all_measures = split_col_types(df)
        annotated_text("Your data source: ", (st.session_state["dataset"].name, ""))

        all_fun = ["sum", "first", "max", "min", "mean", "median", "count"]

        row_opt = st.selectbox("row name :", all_dimensions, key="row_pivot")
        col_opt = st.selectbox("column name :", all_dimensions, key="col_pivot")

        with st.sidebar:
            val_opt = st.selectbox("measure name :", all_measures, key="mea_pivot")
            fun_opt = st.selectbox("function name :", all_fun, key="fun_pivot")

        df_pivot = df.pivot(
            values=val_opt, index=row_opt, columns=col_opt, aggregate_function=fun_opt
        )
        if dshape[0] >= 25:
            st.warning("It only shows first 25 elements of rows", icon="⚠️")
            st.table(df_pivot.to_pandas().head(25))

        else:
            st.table(df_pivot.to_pandas())

    if show:
        st.caption("Sample of Raw Data Below")
        st.table(df.to_pandas().sample(10))

# footer
footer()
