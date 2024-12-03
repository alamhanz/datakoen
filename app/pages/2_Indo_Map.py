"""Web page for chat page."""

import logging

import streamlit as st
import yaml
from pages.tools.assets import set_assets
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
st.title("COMING SOON ..")

# footer
footer()
