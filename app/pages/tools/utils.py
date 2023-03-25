import streamlit as st

def head():
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
    
    st.write(
        "Welcome.",
        "This all in one data tools will help you to data wrangling and getting insight.",
        "Just start by choose your tools and add your data file to this app \U0001F642."
    )

    st.markdown(
    """
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
            forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
            Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


def basicsidebar(config):
    # with st.sidebar:
    #     choose_kupas = st.selectbox(
    #         "Toolbox",
    #         ("Home", "Regression", "Timeseries"),
    #         key='toolbox'
    #     )
    
    st.sidebar.success("Select the tool above.")
