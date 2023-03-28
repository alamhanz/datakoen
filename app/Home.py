import streamlit as st
import yaml
from pages.tools.utils import head, basicsidebar, footer
from pages.tools.assets import set_assets

with open("config.yaml", "r") as f:
    st.session_state['config'] = yaml.load(f, Loader=yaml.FullLoader)

set_assets(st.session_state['config'])
head()
basicsidebar()

footer()