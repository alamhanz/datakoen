"""Slider Number Game Page"""

import logging
import os
from functools import partial

import numpy as np
import requests
import streamlit as st
import yaml
from jinja2 import Template
from pages.tools.assets import set_assets
from pages.tools.utils import (
    basicsidebar,
    footer,
    koen_change_bool,
    koen_logger,
    koenprep,
)
from streamlit_extras.stylable_container import stylable_container

koen_logger("slidernumb")
logger = logging.getLogger("slidernumb")
koenprep("3")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

with open("styles/start_button.css") as ctx:
    startbutton_container_css = [
        i for i in ctx.read().split(".container") if len(i) > 0
    ]

basicsidebar()
st.title("Slider Number Game. Beat Me.")
logger.info("start")

st.write(
    """[Dolphin](https://github.com/alamhanz/dolphin) is my partner to do RL sandbox. 
    It can play Slider Number game quite well. 
    Press the `Start` button below and try to beat Dolphin in this Puzzle Game 
    by **Solving it with lesser number** (do not need to become the faster one). 
    Dolphin is using simple DQN Reinforcement Learning to mastering this one."""
)

if st.session_state.get("3__game_start", False):
    p1, col_sep, p2 = st.columns([1, 0.3, 1])
    k = 0
    while k <= 5:
        try:
            response = requests.get(
                "https://dolp-dive-467815982612.asia-southeast1.run.app/generate-random-slider-game",
                headers={
                    "accept": "application/json",
                    "Authorization": os.getenv("KOEN_TOKEN"),
                },
                timeout=0.5,
            )
            status = 200
            k = 10
        except requests.exceptions.ReadTimeout:
            status = 504
            k += 1

    # Prepare The Game
    if status == 200:
        game_data = response.json()
        auto_slider_path = st.session_state["config"]["asset"]["templates-auto-slider"]
        with open(auto_slider_path, "r") as file:
            auto_slider_template = Template(file.read())
        auto_slider = auto_slider_template

        human_slider_path = st.session_state["config"]["asset"][
            "templates-human-slider"
        ]
        with open(human_slider_path, "r") as file:
            human_slider_template = Template(file.read())
        human_slider = human_slider_template
    else:
        logger.error("Failed to fetch game data")
        human_slider = ""
        auto_slider = ""
        game_data = {}

    # Start The Game
    if len(game_data) > 0:
        initial_state = game_data.get("initial_state", None)
        slider_solution = game_data.get("slider_solution", None)
        initial_state = np.array2string(np.array(initial_state), separator=", ")
        st.write(
            "PS: The Reset will generate new random puzzle. "
            "Also, Dolphin sometimes stucks and can't solve the puzzle. "
            "Try to beat it."
        )

        with p1:
            html_human_slider = human_slider.render(inputArray=initial_state)
            st.components.v1.html(html_human_slider, height=400)

        with col_sep:
            st.markdown(
                """
                <style>
                .separator {
                    border-left: 2px solid #ccc;
                    height: 400px;
                    position: absolute;
                    left: 50%;
                    top: 50%;
                }
                </style>
                <div class="separator"></div>
                """,
                unsafe_allow_html=True,
            )

        with p2:
            html_auto_slider = auto_slider.render(
                inputArray=initial_state, slider_solution=slider_solution
            )
            st.components.v1.html(html_auto_slider, height=400)

        st.button("Reset")
    else:
        st.write(
            "There is a Problem with the API. This is maybe the fresh start. Let Refresh it."
        )
        st.button("Refresh")

else:
    with stylable_container(key="start_button", css_styles=startbutton_container_css):
        st.button("Start", on_click=partial(koen_change_bool, "3__game_start"))

# footer
footer()
