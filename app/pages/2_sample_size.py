import streamlit as st
import yaml
from pages.tools.utils import basicsidebar, footer
from pages.tools.assets import set_assets
from pages.tools.common import upload_data

with open("config.yaml", "r") as f:
    st.session_state['config'] = yaml.load(f, Loader=yaml.FullLoader)
# zippath = st.session_state['config']['zippath']

set_assets(st.session_state['config'])
df = upload_data()

st.title("Sample Size")
st.markdown("Tools to help you to calculate Sample Size.")
st.markdown("Differentiate 2 independent means")





footer()