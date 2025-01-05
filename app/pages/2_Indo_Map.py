"""Web page for chat page."""

import logging

import lereng
import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.common import upload_data
from pages.tools.utils import footer, koen_logger, koenprep

# from functools import partial

# from streamlit_extras.stylable_container import stylable_container

koen_logger("indomap")
logger = logging.getLogger("indomap")
koenprep("2")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

# opening
# st.title("COMING SOON ..")
st.title("Indonesia Choropleth map")

# File uploader
logger.info("test")
df_data = upload_data(
    logger,
    "Upload Your CSV with Indonesia Area Name and One Metric Value.",
    "indomap__binaries",
)

if st.session_state["indomap__binaries"] is not None:
    # # Create two columns in a single row
    # col1, col2 = st.columns(2)

    # # Dropdown in the second column for selecting a value
    # with col1:
    #     selected_value = st.selectbox(
    #         "Select a value:", options=["val1", "val2", "val3"]
    #     )

    # # Dropdown in the first column for selecting a DataFrame column
    # with col2:
    #     selected_column = st.selectbox("Select a metrics:", options=df.columns)

    # logger.info("generating map")
    map_maker = lereng.chrmap(level="provinsi")
    map_maker.insert(df_data, metric="2022", path="app/temp_viz")
    with open("app/temp_viz/lereng_viz.html", "r") as f:
        logger.info("read the html")
        html_content = f.read()
    st.components.v1.html(html_content, height=400, width=800)

# footer
footer()
