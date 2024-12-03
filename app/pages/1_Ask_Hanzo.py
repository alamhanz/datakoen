"""Web page for chat page."""

import logging

import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.utils import footer, koen_logger, koenprep

# from functools import partial

# from streamlit_extras.stylable_container import stylable_container

koen_logger("askhanzo")
logger = logging.getLogger("askhanzo")
koenprep("1")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

# opening
st.title("Chat me about Data and AI")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"I know your input: {prompt}")
    st.write("But sorry, I still need time to learn.")

# footer
footer()
