"""Homepage for Datakoen."""

import streamlit as st
from pages.tools.assets import koen_footer, koen_header, set_homepage

koen_header()

# Content Start Here

with open(st.session_state["config"]["path"]["md"] + "home.md", "rb") as ctx:
    homepage_details = ctx.read().decode("UTF-8")
set_homepage(homepage_details)

# Content End Here

koen_footer()
