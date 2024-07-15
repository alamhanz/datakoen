"""Streamlit web asset."""

import copy

import streamlit as st
import yaml

from .common import get_base64


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


def set_page(icon_file=None, layout=None):
    """Set icon

    Args:
        icon_file (str, optional): _description_. Defaults to "assets/icon.png".
    """
    if layout is None:
        layout = "centered"

    st.set_page_config(page_title="DataKoen", page_icon=icon_file, layout=layout)
    with st.sidebar:
        st.success("Select the tool above.")

    hover_style = """
        <style>
        a:link , a:visited{
        color: #DB8F8F;
        background-color: transparent;
        text-decoration: underline;
        }

        a:hover,  a:active {
        color: red;
        background-color: transparent;
        text-decoration: underline;
        }"""
    st.markdown(hover_style, unsafe_allow_html=True)


def footer(config):
    """Set footer in for web page."""
    read_md = open(config["path"]["md"] + "footer-sidebar.html", "rb")
    read_md = read_md.read().decode("UTF-8")
    with st.sidebar:
        st.markdown(" ")
        st.markdown(read_md, unsafe_allow_html=True)

    read_md = open(config["path"]["md"] + "footer.html", "rb")
    read_md = read_md.read().decode("UTF-8")
    st.markdown(read_md, unsafe_allow_html=True)


def koen_header(layout=None):
    with open("asset_config.yaml", "r", encoding="utf-8") as f:
        st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
    cfg = copy.copy(st.session_state["config"])
    set_page(cfg["asset"]["icon"], layout)
    set_bg(cfg["asset"]["background"])


def koen_footer():
    cfg = copy.copy(st.session_state["config"])
    footer(cfg)
