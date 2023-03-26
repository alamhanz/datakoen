import streamlit as st
import yaml
from pages.tools.utils import head, basicsidebar, footer
from pages.tools.assets import set_assets

with open("config.yaml", "r") as f:
    st.session_state['config'] = yaml.load(f, Loader=yaml.FullLoader)
# zippath = st.session_state['config']['zippath']

set_assets(st.session_state['config'])
basicsidebar(st.session_state['config'])
footer()

st.title("Pivot")