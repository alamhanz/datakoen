"""Homepage for Datakoen."""

from functools import partial

import streamlit as st
import yaml
from dotenv import load_dotenv
from hanzo import talk, vectordb
from pages.tools.assets import set_assets
from pages.tools.utils import footer, koencounter
from streamlit_extras.stylable_container import stylable_container

load_dotenv()

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


## Hanzo part
koen_part_func = partial(koencounter, "home__submitted-form")

## Hanzo Prep
if "home__vdb" not in st.session_state:
    st.session_state["home__vdb"] = vectordb(
        model="BAAI/bge-large-en-v1.5",
        file="temp/Alamsyah_Koto_Hanza_Profile.txt",
        db_path="temp/about_alam/",
    )
    st.session_state["home__vdb"].load()

if "home__hanzo" not in st.session_state:
    st.session_state["home__hanzo"] = talk(
        st.session_state["home__vdb"].db,
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
    )

with stylable_container(key="hanzo_container", css_styles=hanzo_container_css):
    #     st.caption("[Hanzo is left the office right now.]")
    with st.form(key="home__hanzospace", clear_on_submit=True):
        text = st.text_area(
            "Hanzo Space",
            "what do you want to ask?",
        )
        submitted = st.form_submit_button("Submit", on_click=koen_part_func)

        if submitted:
            hanzo_response = st.session_state["home__hanzo"].invoking(text)
            if isinstance(hanzo_response, dict):
                st.info(hanzo_response["answer"])

footer()
