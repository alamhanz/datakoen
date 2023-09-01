"""Web page for hypothesis testing."""
import streamlit as st
import yaml
from pages.tools.utils import footer
from pages.tools.assets import set_assets
from pages.tools.calc import ztest_2prop

with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
# zippath = st.session_state['config']['zippath']

set_assets(st.session_state["config"])

st.title("Hypothesis Testing")
st.markdown("Tools to help you to hypothesis testing.")

testing_opt = st.selectbox(
    "Choose Statistical Test :",
    [
        "-",
        "Proportion Differences t-test of 2 samples",
        "Mean Differences t-test of 2 samples",
    ],
    key="testing_options",
)

if testing_opt == "-":
    st.markdown("Please Choose The Hytpothesis testing Method")
elif testing_opt == "Proportion Differences t-test of 2 samples":
    col1, col2 = st.columns(2)

    with col1:
        sample_size1 = st.number_input("Get the sample size group1: ", value=7)
        proportion_1 = st.number_input(
            "Proportion group1:",
            value=0.5,
            max_value=1.0,
            min_value=1e-5,
            step=0.0001,
            format="%.5f",
        )

    with col2:
        sample_size2 = st.number_input("Get the sample size group2: ", value=7)
        proportion_2 = st.number_input(
            "Proportion group2:",
            value=0.5,
            max_value=1.0,
            min_value=1e-5,
            step=0.0001,
            format="%.5f",
        )

    N0 = [sample_size1, sample_size2]
    prop = [proportion_1, proportion_2]
    alp = 0.06
    calcZ = ztest_2prop(N0, prop, 1)

    p_value, z_score = calcZ.calc_zscore()

    if p_value <= alp:
        output = "Difference is statistically significant"
    else:
        output = "It is NOT statistically significant different"
    output = output + " : dengan pvalue {} dan z_score {}".format(
        round(p_value, 3), round(z_score, 3)
    )
    st.markdown(output)
    calcZ.simulasi_sampel(250)


elif testing_opt == "Mean Differences t-test of 2 samples":
    sample_size1 = st.number_input("Get the sample size group1: ")
    sample_size2 = st.number_input("Get the sample size group2: ")
else:
    st.markdown("Please Choose The Hytpothesis testing Method")

footer()
