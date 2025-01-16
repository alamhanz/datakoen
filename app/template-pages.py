"""Web page for timeseries."""

import streamlit as st
import yaml
from annotated_text import annotated_text
from pages.tools.assets import set_assets
from pages.tools.common import config_types, split_col_types, upload_data
from pages.tools.utils import footer

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])
df = upload_data()

# opening
st.title("Title")
st.markdown("This is a template")

## processing

# footer
footer()
