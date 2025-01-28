""" Slider Number Game Page """

import logging
from functools import partial

import dolphin
import numpy as np
import streamlit as st
import yaml
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

if st.session_state.get("3__game_start"):
    p1, col_sep, p2 = st.columns([1, 0.3, 1])
    slider_rl = dolphin.SliderNumber(human_render=False)
    slider_rl.auto_run()
    initial_state = slider_rl.initial_state
    slider_solution = slider_rl.steps
    slider_rl.get_html_template()

    initial_state = np.array2string(initial_state, separator=", ")
    st.write(
        "PS: The Reset will generate new random puzzle. "
        "Also, Dolphin sometimes stucks and can't solve the puzzle. "
        "Try to beat it."
    )

    with p1:
        html_human_slider = slider_rl.human_slider.render(inputArray=initial_state)
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
        html_auto_slider = slider_rl.auto_slider.render(
            inputArray=initial_state, slider_solution=slider_solution
        )
        st.components.v1.html(html_auto_slider, height=400)

    st.button("Reset")

else:
    with stylable_container(key="start_button", css_styles=startbutton_container_css):
        st.button("Start", on_click=partial(koen_change_bool, "3__game_start"))

# footer
footer()
