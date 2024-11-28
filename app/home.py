"""Homepage for Datakoen."""

import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.utils import footer
from streamlit_extras.stylable_container import stylable_container

with open("config.yaml", "r", encoding="utf-8") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

with open(st.session_state["config"]["asset"]["home-markdown"], "rb") as ctx:
    read_md = ctx.read().decode("UTF-8")

with open("styles/hanzo_container.css") as ctx:
    hanzo_container_css = [i for i in ctx.read().split(".container") if len(i) > 0]

st.markdown(
    """
    <h1 style='text-align: center; margin-bottom: -35px;'>
    Welcome to DataKoen
    </h1>
""",
    unsafe_allow_html=True,
)

st.caption(
    """
    <p style='text-align: center;margin-bottom: 35px;'>
    by <a href='https://alamhanz.xyz'>Hanz</a>
    </p>
""",
    unsafe_allow_html=True,
)

st.markdown(read_md)

# hanzo_container_css = [
#     """ {align-items: center;
#                        position: fixed;
#                        box-sizing: border-box;
#                        padding-top: 40px;}""",
#     """div {
#     text-align: center;
#     vertical-align: middle;}""",
# ]

with stylable_container(key="hanzo_container", css_styles=hanzo_container_css):
    #     st.caption("[Hanzo is left the office right now.]")
    k = 0
    with st.form("Hanzo Space"):
        text = st.text_area(
            "Hanzo Space",
            "what do you want to ask?",
        )
        submitted = st.form_submit_button("Submit")
        if submitted:
            k += 1
            if k == 1:
                st.info("I'm still learning. Give me another week to answer that.")
            elif k == 2:
                st.info(
                    "I'm sorry, I think i'm not clear enough. I still need sometime to learn. Please wait for another week."
                )
            elif k == 3:
                st.info("Did you read my previous answer? Geez..")
            elif k == 4:
                st.info(
                    "Sorry for the attitude. I didn't mean to be rude. But really, I need sometime to learn."
                )
            else:
                st.info("Okay. I'll ignore you now.")


footer()
