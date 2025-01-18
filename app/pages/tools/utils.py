"""Common function used in the web page."""

import logging
import sys

import colorlog
import streamlit as st
from hanzo import talk, vectordb
from streamlit_extras.stylable_container import stylable_container

with open("styles/sidebar_footer.css") as ctx:
    sidebar_footer_css = [i for i in ctx.read().split(".container") if len(i) > 0]


# def basicsidebar():
#     """Set basic side bar."""
#     st.sidebar.success("Select the tool above.")
#     st.sidebar.subheader("Navigation")
#     st.sidebar.text("This is some text in the sidebar")


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


def koenprep(part):
    """initial state if needed

    Args:
        part (_type_): _description_
    """
    if part == "home":
        ## Hanzo Prep
        if "home__vdb" not in st.session_state:
            st.session_state["home__vdb"] = vectordb(
                model="BAAI/bge-large-en-v1.5",
                file="app/default/my_profile.txt",
                db_path="app/default/about_me/",
            )
            st.session_state["home__vdb"].load()

        if "home__hanzo" not in st.session_state:
            st.session_state["home__hanzo"] = talk(
                st.session_state["home__vdb"].db,
                model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                max_token=800,
                context_size=5,
            )
    elif part == "1":
        if "1__hanzo" not in st.session_state:
            st.session_state["1__hanzo"] = talk(
                model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
                max_token=800,
            )
    elif part == "2":
        if "indomap__dataset" not in st.session_state:
            st.session_state["indomap__dataset"] = None


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
