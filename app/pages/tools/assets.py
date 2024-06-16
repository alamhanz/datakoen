"""Streamlit web asset."""

import base64
import copy

import streamlit as st
import yaml


def get_base64(bin_file):
    """Read byte file and decode.

    Args:
        bin_file (_type_): _description_

    Returns:
        _type_: decoded content.
    """
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_bg(png_file):
    """Set background given png file.

    Args:
        png_file (_type_): _description_
    """
    bin_str = get_base64(png_file)
    page_bg_img = (
        """
            <style>
            .stApp {
            background-image: url("data:image/png;base64,%s");
            background-size: cover;
            }
            </style>
        """
        % bin_str
    )
    st.markdown(page_bg_img, unsafe_allow_html=True)


def set_icon(icon_file="assets/icon.png", layout=None):
    """Set icon

    Args:
        icon_file (str, optional): _description_. Defaults to "assets/icon.png".
    """
    if layout is None:
        layout = "centered"

    st.set_page_config(page_title="DataKoen", page_icon=icon_file, layout=layout)


def set_assets(config, layout=None):
    """Set assets.

    Args:
        config (_type_): _description_
    """
    set_icon(config["asset"]["icon"], layout)
    set_bg(config["asset"]["background"])


def set_color_theme(config):
    color = config["theme"]["sidebar_color"]
    st.markdown(
        """
        <style>
            [data-testid=stSidebar] {
                background-color: """
        + color
        + """;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def basicsidebar():
    """Set basic side bar."""
    with st.sidebar:
        st.success("Select the tool above.")
        st.subheader("Navigation")
        st.text("This is some text in the sidebar")


def footer():
    """Set footer in for web page."""
    read_md = open("assets/markdowns/footer-sidebar.html", "rb")
    read_md = read_md.read().decode("UTF-8")
    with st.sidebar:
        st.markdown(" ")
        st.markdown(read_md, unsafe_allow_html=True)

    read_md = open("assets/markdowns/footer.html", "rb")
    read_md = read_md.read().decode("UTF-8")
    st.markdown(read_md, unsafe_allow_html=True)


def koen_header(layout=None):
    with open("config.yaml", "r", encoding="utf-8") as f:
        st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
    cfg = copy.copy(st.session_state["config"])
    set_assets(cfg, layout=layout)
    set_color_theme(cfg)


def koen_footer():
    basicsidebar()
    footer()


def set_homepage(details):
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: -35px;'>
        Welcome to Datakoen
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

    st.markdown(details)
