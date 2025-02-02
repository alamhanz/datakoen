"""Common function used in the web page."""

import logging
import sys

import colorlog
import streamlit as st
from hanzo import Talk, Vectordb
from streamlit_extras.stylable_container import stylable_container

with open("styles/sidebar_footer.css") as ctx:
    sidebar_footer_css = [i for i in ctx.read().split(".container") if len(i) > 0]


def basicsidebar():
    """basic sidebar function"""

    koen_version = "v0.3.0"
    st.sidebar.text(koen_version)


def footer():
    """Set footer in for web page."""
    read_md = open("assets/markdowns/footer-sidebar.md", "rb")
    read_md = read_md.read().decode("UTF-8")
    with st.sidebar:
        with stylable_container(key="sidebar_footer", css_styles=sidebar_footer_css):
            st.markdown(read_md, unsafe_allow_html=True)

    read_md = open("assets/markdowns/footer.md", "rb")
    read_md = read_md.read().decode("UTF-8")
    st.markdown(read_md, unsafe_allow_html=True)


def koencounter(state_name):
    """create counter

    Args:
        state_name (_type_): _description_
    """
    if state_name in st.session_state:
        st.session_state[state_name] += 1
    else:
        st.session_state[state_name] = 1


def koen_change_bool(state: str):
    """Change Boolean Session State

    Args:
        state (str): state name that contain boolean only
    """
    st.session_state[state] = not st.session_state[state]


def koenprep(part):
    """initial state if needed

    Args:
        part (_type_): _description_
    """
    if part == "home":
        koenprep_home()
    elif part == "1":
        koenprep_1()
    elif part == "2":
        koenprep_2()
    elif part == "3":
        koenprep_3()


def koenprep_home():
    """Initial state for home"""
    if "home__vdb" not in st.session_state:
        st.session_state["home__vdb"] = Vectordb(
            model="BAAI/bge-large-en-v1.5",
            file="default/my_profile.txt",
            db_path="default/about_me/",
        )
        st.session_state["home__vdb"].load()

    if "home__hanzo" not in st.session_state:
        st.session_state["home__hanzo"] = Talk(
            st.session_state["home__vdb"].db,
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            max_token=800,
            context_size=5,
        )
    if "3__game_start" in st.session_state:
        st.session_state["3__game_start"] = False


def koenprep_1():
    """Initial state for part 1"""
    if "1__hanzo" not in st.session_state:
        st.session_state["1__hanzo"] = Talk(
            model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            max_token=800,
        )
    if "3__game_start" in st.session_state:
        st.session_state["3__game_start"] = False


def koenprep_2():
    """Initial state for part 2"""
    if "2__dataset" not in st.session_state:
        st.session_state["2__dataset"] = None

    if "2__not_normalize" not in st.session_state:
        st.session_state["2__not_normalize"] = False

    if "3__game_start" in st.session_state:
        st.session_state["3__game_start"] = False


def koenprep_3():
    """Initial state for part 3"""
    if "3__game_start" not in st.session_state:
        st.session_state["3__game_start"] = False

    if "3__game_rerun" not in st.session_state:
        st.session_state["3__game_rerun"] = True


loggers = {}


def koen_logger(module_name: str):
    """Logger Obejct

    Args:
        name (string): Name of the module
    """
    if loggers.get(module_name):

        return loggers.get(module_name)

    logger = logging.getLogger(module_name)
    # Set the threshold logging level of the logger to INFO
    logger.setLevel(logging.INFO)
    # Create a stream-based handler that writes the log entries
    # into the standard output stream
    handler = logging.StreamHandler(sys.stdout)
    # Create a formatter for the logs
    formatter = colorlog.ColoredFormatter(
        f"%(log_color)s%(levelname)-2s%(reset)s\t: %(asctime)s - {module_name}\t- %(message)s",
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "INFO": "blue",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
        secondary_log_colors={
            "message": {
                "DEBUG": "white",
                "INFO": "white",
                "WARNING": "white",
                "ERROR": "white",
                "CRITICAL": "white",
            }
        },
        style="%",
    )
    # Set the created formatter as the formatter of the handler
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    loggers.update({module_name: logger})
    return logger
