"""Web page for table pivot."""
import streamlit as st
import yaml
from annotated_text import annotated_text
from pages.tools.assets import set_assets
from pages.tools.common import upload_data, config_types, split_col_types
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
    df = config_types(df)
    all_dimensions, all_measures = split_col_types(df)
    annotated_text("Your data source: ", (st.session_state["dataset"].name, ""))
    dshape = df.shape

    all_fun = ["sum", "first", "max", "min", "mean", "median", "count"]
    with st.sidebar:
        show = st.checkbox("show the data raw")
        st.success(f"Your current data shape is {dshape[0]} x {dshape[1]}")
        val_opt = st.selectbox("measure name :", all_measures, key="mea_pivot")
        fun_opt = st.selectbox("function name :", all_fun, key="fun_pivot")

    row_opt = st.selectbox("row name :", all_dimensions, key="row_pivot")
    col_opt = st.selectbox("column name :", all_dimensions, key="col_pivot")

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
