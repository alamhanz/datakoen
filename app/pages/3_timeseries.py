"""Web page for timeseries."""
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
st.title("Timeseries Prediction")
st.markdown("Predicting the time series data.")
st.markdown("\nCompare time series methods")


## processing
if df is not None:
    df = config_types(df)
    all_dimensions, all_measures = split_col_types(df)
    annotated_text("Your data source: ", (st.session_state["dataset"].name, ""))
    dshape = df.shape

    with st.sidebar:
        show = st.checkbox("show the data raw")
        st.success(f"Your total observation is {dshape[0]}")

    col_time = st.selectbox(
        "column of the time / day",
        all_dimensions,
        # index=,
        key="col_time_ts",
    )

    col_value = st.selectbox(
        "column of the value",
        all_dimensions,
        # index=,
        key="col_value_ts",
    )
    ## TODO all processing here

    if show:
        st.caption("Sample of Raw Data Below")
        st.table(df.to_pandas().sample(10))

# footer
footer()
