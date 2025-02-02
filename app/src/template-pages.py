"""Template"""

import logging

import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.utils import basicsidebar, footer, koen_logger, koenprep

koen_logger("xx")
logger = logging.getLogger("xx")
koenprep("-1")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

basicsidebar()

# footer
footer()
