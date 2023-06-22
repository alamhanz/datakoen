import streamlit as st

def head():
    read_md = open('assets/markdowns/home.md','rb')
    read_md = read_md.read().decode("UTF-8")
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: -35px;'>
        Welcome to KupasData
        </h1>
    """, unsafe_allow_html=True
    )
    
    st.caption("""
        <p style='text-align: center'>
        by <a href='https://alamhanz.xyz'>Hanz</a>
        </p>
    """, unsafe_allow_html=True
    )

    st.markdown(read_md)

def basicsidebar():
    st.sidebar.success("Select the tool above.")
    st.sidebar.subheader("Navigation")
    st.sidebar.text("This is some text in the sidebar")

def footer():
    read_md = open('assets/markdowns/footer-sidebar.md','rb')
    read_md = read_md.read().decode("UTF-8")
    st.sidebar.markdown(' ')
    st.sidebar.markdown(read_md, unsafe_allow_html=True)

    read_md = open('assets/markdowns/footer.md','rb')
    read_md = read_md.read().decode("UTF-8")
    st.markdown(read_md,unsafe_allow_html=True)