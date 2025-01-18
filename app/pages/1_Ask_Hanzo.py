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
# st.write(
#     "Problem Statement: How easily get information about Data and AI technique or professional?"
# )
st.title("Chat me about Data and AI")
logger.info("start")

prompt = st.chat_input("Say something")
if prompt:
    logger.info("asking: %s", prompt)
    answer = st.session_state["1__hanzo"].streaming(input_query=prompt, stream=False)
    st.write(answer)

# footer
footer()
