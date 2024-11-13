"""Web page for table pivot."""

import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.utils import footer

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

# opening
st.title("Pivot")
st.markdown("pivoting your data for your exploration.")
st.markdown("\nUpload Your data first.")

# footer
footer()
