"""Web page for chat page."""

import logging

import lereng
import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.common import upload_data
from pages.tools.utils import footer, koen_logger, koenprep
from streamlit_extras.stylable_container import stylable_container

# from functools import partial

# from streamlit_extras.stylable_container import stylable_container

koen_logger("indomap")
logger = logging.getLogger("indomap")
koenprep("2")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

with open(st.session_state["config"]["asset"]["map-explain"], "rb") as ctx:
    read_md = ctx.read().decode("UTF-8")

with open("styles/map_container.css") as ctx:
    map_container_css = [i for i in ctx.read().split(".container") if len(i) > 0]


# opening
# st.write(
#     "Problem Statement: How easily to create heatmap
#       on indonesia map given cities/province name only?"
# )
st.title("Indonesia Choropleth map")
logger.info("start")

# output_container = stylable_container(key="map_container", css_styles=map_container_css)
input_container1 = st.container()

df_data = []
with input_container1:
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload Your CSV with Indonesia Area Name and One Metric Value.",
        key="indomap__binaries",
        type=["csv"],
    )
    df_data = upload_data(logger, uploaded_file)

tab1, tab2 = st.tabs(["Maps", "Table"])

# if st.session_state["indomap__binaries"] is not None:
if df_data is not None:
    with tab1:
        output_container = st.container()
        input_container2 = st.container()
        with input_container2:
            col1, col2 = st.columns(2)
            with col1:
                choosen_metric_col = st.selectbox(
                    "Select a metrics:",
                    options=df_data.select_dtypes(include=["number"]).columns,
                )

            with col2:
                col_opt = df_data.select_dtypes(include=["object", "category"]).columns
                choosen_area_col = st.selectbox(
                    "Select the column area:",
                    options=col_opt,
                )

            # identify
            identifier = lereng.areaname()
            area_type = identifier.identify_area(df_data, choosen_area_col)
            logger.info("area type : %s", area_type)

            # Normalize the name
            df_data = identifier.normalize(df_data, choosen_area_col)
            df_data["old_" + choosen_area_col] = df_data[choosen_area_col]
            df_data[choosen_area_col] = df_data["normalized_area"]
            # is_already_normalized

            # make the map
            map_maker = lereng.chrmap(level=area_type)
            map_maker.insert(
                df_data,
                metric_col=choosen_metric_col,
                area_col=choosen_area_col,
                store_path="app/temp_viz",
            )
            with open("app/temp_viz/lereng_viz.html", "r") as f:
                logger.info("read the html")
                html_content = f.read()

            bool_name_same = (
                df_data[~(df_data["is_already_normalized"])]["old_" + choosen_area_col]
                == df_data[~(df_data["is_already_normalized"])][choosen_area_col]
            ).mean()

            if bool_name_same > 0:
                with st.sidebar:
                    st.warning("Hugging Face API has reached limit today.")

        with output_container:
            with stylable_container(key="map_container", css_styles=map_container_css):
                st.components.v1.html(html_content, height=400, width=850)

    with tab2:
        st.dataframe(df_data)
        st.markdown(read_md)

# footer
footer()
