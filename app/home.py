"""Homepage for kupasdata."""
import streamlit as st
import yaml
from pages.tools.utils import basicsidebar, footer
from pages.tools.assets import set_assets

with open("config.yaml", "r", encoding="utf-8") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)

set_assets(st.session_state["config"])

with open(st.session_state["config"]["asset"]["home-markdown"], "rb") as ctx:
    read_md = ctx.read()

read_md = read_md.read().decode("UTF-8")
st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: -35px;'>
    Welcome to KupasData
    </h1>
""",
    unsafe_allow_html=True,
)

st.caption(
    """
    <p style='text-align: center'>
    by <a href='https://alamhanz.xyz'>Hanz</a>
    </p>
""",
    unsafe_allow_html=True,
)

st.markdown(read_md)

basicsidebar()
footer()
