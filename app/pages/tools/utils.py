"""Common function used in the web page."""

import streamlit as st
from hanzo import talk, vectordb
from streamlit_extras.stylable_container import stylable_container

with open("styles/sidebar_footer.css") as ctx:
    sidebar_footer_css = [i for i in ctx.read().split(".container") if len(i) > 0]


def basicsidebar():
    """Set basic side bar."""
    st.sidebar.success("Select the tool above.")
    st.sidebar.subheader("Navigation")
    st.sidebar.text("This is some text in the sidebar")


def footer():
    """Set footer in for web page."""
    read_md = open("assets/markdowns/footer-sidebar.md", "rb")
    read_md = read_md.read().decode("UTF-8")
    with st.sidebar:
        with stylable_container(key="sidebar_footer", css_styles=sidebar_footer_css):
            st.markdown(read_md, unsafe_allow_html=True)

    read_md = open("assets/markdowns/footer.md", "rb")
    read_md = read_md.read().decode("UTF-8")
    st.markdown(read_md, unsafe_allow_html=True)


def koencounter(state_name):
    if state_name in st.session_state:
        st.session_state[state_name] += 1
    else:
        st.session_state[state_name] = 1


def koenprep(part):

    if part == "home":
        ## Hanzo Prep
        if "home__vdb" not in st.session_state:
            st.session_state["home__vdb"] = vectordb(
                model="BAAI/bge-large-en-v1.5",
                file="temp/Alamsyah_Koto_Hanza_Profile.txt",
                db_path="temp/about_alam/",
            )
            st.session_state["home__vdb"].load()

        if "home__hanzo" not in st.session_state:
            st.session_state["home__hanzo"] = talk(
                st.session_state["home__vdb"].db,
                model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
            )
