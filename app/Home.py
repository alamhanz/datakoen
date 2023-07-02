import streamlit as st
import yaml
from pages.tools.utils import basicsidebar, footer
from pages.tools.assets import set_assets

with open("config.yaml", "r") as f:
    st.session_state['config'] = yaml.load(f, Loader=yaml.FullLoader)

set_assets(st.session_state['config'])

read_md = open(st.session_state['config']['asset']['home-markdown'],'rb')
read_md = read_md.read().decode("UTF-8")
st.markdown("""
    <h1 style='text-align: center; margin-bottom: -35px;'>
    Welcome to KupasData
    </h1>
""", unsafe_allow_html=True
)

st.caption("""
    <p style='text-align: center'>
    by <a href='https://alamhanz.xyz'>Hanz</a>
    </p>
""", unsafe_allow_html=True
)

st.markdown(read_md)

basicsidebar()
footer()