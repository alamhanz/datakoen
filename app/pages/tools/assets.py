"""Streamlit web asset."""

import base64

import streamlit as st


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


def set_icon(icon_file="assets/icon.png"):
    """Set icon

    Args:
        icon_file (str, optional): _description_. Defaults to "assets/icon.png".
    """
    st.set_page_config(page_title="KupasData", page_icon=icon_file)


def set_assets(config):
    """Set assets.

    Args:
        config (_type_): _description_
    """
    set_icon(config["asset"]["icon"])
    set_bg(config["asset"]["background"])
