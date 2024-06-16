"""Webpage for sample size."""
import streamlit as st
import scipy.stats as stat
import yaml
from pages.tools.assets import set_assets
from pages.tools.common import upload_data
from pages.tools.utils import footer

with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
# zippath = st.session_state['config']['zippath']

set_assets(st.session_state["config"])
df = upload_data()

st.title("Sample Size")
st.markdown("Tools to help you to calculate Sample Size.")
st.markdown("Under Development")

power_exp = 0.84
alpha_exp = 0.05

z_pow = stat.norm.ppf(power_exp)
z_alp = stat.norm.ppf(1 - (alpha_exp / 2))
n_group = 3
sample_ratio = 1 / (n_group)

metrics_mean = 150
metrics_std = 250
metrics_diff = 25

n_sample = ((sample_ratio + 1) * (z_pow + z_alp) * (metrics_std**2)) / (
    (sample_ratio) * (metrics_diff**2)
)


footer()
