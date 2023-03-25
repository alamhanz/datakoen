import streamlit as st
import yaml
from pages.tools.utils import head, basicsidebar
from pages.tools.assets import set_icon
import polars as pl

# read config
with open("config.yaml", "r") as f:
    st.session_state['config'] = yaml.load(f, Loader=yaml.FullLoader)
zippath = st.session_state['config']['zippath']

# First Part
set_icon('assets/kupasdata-icon.png')
# set_bg('assets/bg.jpeg')
head()

# Side bar
basicsidebar(st.session_state['config'])

