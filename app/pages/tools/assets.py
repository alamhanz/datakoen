"""Streamlit web asset."""
import base64
import streamlit as st


def get_base64(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_bg(png_file):
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
    st.set_page_config(page_title="KupasData", page_icon=icon_file)


def set_assets(config):
    set_icon(config["asset"]["icon"])
    set_bg(config["asset"]["background"])
