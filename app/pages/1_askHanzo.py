"""Web page for chat page."""

import logging

import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.utils import basicsidebar, footer, koen_logger, koenprep

koen_logger("askhanzo")
logger = logging.getLogger("askhanzo")
koenprep("1")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

basicsidebar()

# Opening
st.title("Chat me about Data and AI")
logger.info("start")

prompt = st.chat_input("Say something")
if prompt:
    logger.info("asking: %s", prompt)
    answer = st.session_state["1__hanzo"].streaming(input_query=prompt, stream=False)
    st.write(answer)

# footer
footer()
