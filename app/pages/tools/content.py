import streamlit as st


def set_homepage(details):
    st.markdown(
        """
        <h1 style='text-align: center; margin-bottom: -35px;'>
        Welcome to Datakoen
        </h1>
    """,
        unsafe_allow_html=True,
    )

    st.caption(
        """
        <p style='text-align: center'>
        by <a href='https://alamhanz.xyz'>Hanz</a>
        </p>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(details)
