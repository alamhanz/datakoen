import streamlit as st


def basicsidebar():
    st.sidebar.success("Select the tool above.")
    st.sidebar.subheader("Navigation")
    st.sidebar.text("This is some text in the sidebar")


def footer():
    read_md = open("assets/markdowns/footer-sidebar.md", "rb")
    read_md = read_md.read().decode("UTF-8")
    st.sidebar.markdown(" ")
    st.sidebar.markdown(read_md, unsafe_allow_html=True)

    read_md = open("assets/markdowns/footer.md", "rb")
    read_md = read_md.read().decode("UTF-8")
    st.markdown(read_md, unsafe_allow_html=True)
