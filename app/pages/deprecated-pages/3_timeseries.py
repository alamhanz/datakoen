"""Web page for timeseries."""

import plotly.express as px
import streamlit as st
import yaml
from annotated_text import annotated_text
from pages.tools.assets import set_assets
from pages.tools.calc import add_ts, run_all_ts
from pages.tools.common import (
    config_types,
    custom_legend_name,
    split_col_types,
    upload_data,
)
from pages.tools.utils import footer

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
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Prediction Model",
            "Model Evaluation",
            "Time Series Analysis",
            "Data Types Edit",
        ]
    )
    with tab4:
        df = config_types(df)

    with st.sidebar:
        dshape = df.shape
        show = st.checkbox("show the data raw")
        st.success(f"Your total observation is {dshape[0]}")

    with tab1:
        mylayout0 = st.columns(1)
        mylayout1 = st.columns(1)
        mylayout2 = st.columns(1)
        all_dimensions, all_measures = split_col_types(df)

        if (len(all_dimensions) == 0) | (len(all_measures) == 0):
            placeholder.error("There is no 'Date/Time Type' or no 'Numeric Type'")
        else:
            placeholder.empty()
            # Preprocessing
            with mylayout0[0]:
                annotated_text(
                    "Your data source: ", (st.session_state["dataset"].name, "")
                )
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

                max_rnu = 1500
                min_rnu = max(int(len(df) * 0.1), 10)
                default_rnu = min(int(len(df) * 0.8), max_rnu)
                row_number_used = st.number_input(
                    "Number of Rows (get x last number of timeseries)",
                    value=default_rnu,
                    min_value=min_rnu,
                    max_value=max_rnu,
                    step=1,
                    key="n_used",
                )

                df_ts = df[[col_time, col_value]].sort(col_time, descending=False)
                df_ts = df_ts[-row_number_used:]
                if "ts_lines" not in st.session_state:
                    st.session_state["ts_lines"] = {"actual": df_ts[col_value]}
                else:
                    st.session_state["ts_lines"]["actual"] = df_ts[col_value]

                st.divider()

            with mylayout2[0]:
                curr_y = run_all_ts(st.session_state["ts_lines"])
                st.button("Add TS Model", on_click=add_ts)

            all_model_name = st.session_state["ts_lines"].keys()
            fig = px.line(x=df_ts[col_time], y=curr_y)
            fig = custom_legend_name(fig, all_model_name)
            if "number_test" in st.session_state:
                n_test = st.session_state["number_test"]
                vline = max(df_ts[:-n_test][col_time])
                fig.add_vline(
                    x=vline, line_width=3, line_dash="dash", line_color="goldenrod"
                )
            with mylayout1[0]:
                st.plotly_chart(fig, theme="streamlit", use_container_width=False)
                st.divider()

    with tab2:
        st.markdown("Under Development")

    with tab3:
        st.markdown("Under Development")

    if show:
        st.caption("Sample of Raw Data Below")
        st.table(df.to_pandas().sample(10))

# footer
footer()
