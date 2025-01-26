"""Template"""

import logging

import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.utils import basicsidebar, footer, koen_logger, koenprep

koen_logger("slidernumb")
logger = logging.getLogger("slidernumb")
koenprep("3")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

basicsidebar()
st.title("Slider Number Game. Beat Me.")
logger.info("start")

st.write(
    "Press the start button below. Try to beat Dolphin in Slider Number Puzzle Game. Dolphin is using simple DQN Reinforcement Learning to mastering the game."
)

p1, col_sep, p2 = st.columns([1, 0.3, 1])

with p1:
    with open("assets/human_slider.html", "r", encoding="utf-8") as file:
        html_content1 = file.read()
    st.components.v1.html(html_content1, height=400)

with col_sep:
    st.markdown(
        """
        <style>
            .separator {
                border-left: 2px solid #ccc;
                height: 500px;
                position: absolute;
                left: 50%;
            }
        </style>
        <div class="separator"></div>
        """,
        unsafe_allow_html=True,
    )

with p2:
    with open("assets/human_slider.html", "r", encoding="utf-8") as file:
        html_content2 = file.read()
    st.components.v1.html(html_content2, height=400)

# footer
footer()
