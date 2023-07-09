import streamlit as st
import yaml
from pages.tools.utils import basicsidebar, footer
from pages.tools.assets import set_assets
from pages.tools.common import upload_data

with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
# zippath = st.session_state['config']['zippath']

set_assets(st.session_state["config"])
df = upload_data()

st.title("Hypothesis Testing")
st.markdown("Tools to help you to hypothesis testing.")

testing_opt = st.selectbox(
    "Choose Statistical Test :", 
    ["-",
    "Proportion Differences t-test of 2 samples", 
    "Mean Differences t-test of 2 samples"], key="testing_options"
)

if testing_opt == "-":
    st.markdown("Please Choose The Hytpothesis testing Method")
elif testing_opt == "Proportion Differences t-test of 2 samples":
    sample_size1 = st.number_input("Get the sample size group1: ")
    sample_size2 = st.number_input("Get the sample size group2: ")

elif testing_opt == "Mean Differences t-test of 2 samples":
    sample_size1 = st.number_input("Get the sample size group1: ")
    sample_size2 = st.number_input("Get the sample size group2: ")
else:
    st.markdown("Please Choose The Hytpothesis testing Method")

footer()