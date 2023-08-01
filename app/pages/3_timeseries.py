"""Web page for timeseries."""
import streamlit as st
import yaml
from annotated_text import annotated_text
from pages.tools.assets import set_assets
from pages.tools.common import upload_data, config_types, split_col_types
from pages.tools.utils import footer
import plotly.express as px

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])
df = upload_data()

# opening
st.title("Timeseries Prediction")
st.markdown("Predicting the time series data.")
st.markdown("\nCompare time series methods. Try Now.")


## processing
if df is not None:
    placeholder = st.empty()
    tab1, tab2 = st.tabs(["Workspace", "Data Types Edit"])
    with tab2:
        df = config_types(df)

    with st.sidebar:
        dshape = df.shape
        show = st.checkbox("show the data raw")
        st.success(f"Your total observation is {dshape[0]}")

    with tab1:
        ## TODO all processing here
        all_dimensions, all_measures = split_col_types(df)
        annotated_text("Your data source: ", (st.session_state["dataset"].name, ""))

        if (len(all_dimensions) == 0) | (len(all_measures) == 0):
            placeholder.error("There is no 'Date/Time Type' or no 'Numeric Type'")
        else:
            placeholder.empty()

            col_time = st.selectbox(
                "column of the time / day",
                all_dimensions,
                # index=,
                key="col_time_ts",
            )

            col_value = st.selectbox(
                "column of the value",
                all_measures,
                # index=,
                key="col_value_ts",
            )

            df_ts = df[[col_time, col_value]]
            curr_y = [df_ts[col_value]]
            fig = px.line(x=df_ts[col_time], y=curr_y)
            st.plotly_chart(fig, theme="streamlit", use_container_width=False)

    if show:
        st.caption("Sample of Raw Data Below")
        st.table(df.to_pandas().sample(10))

# footer
footer()
