import streamlit as st

# Set the title and description
st.title("Welcome to Datakoen! 🌟")
st.write(
    """
**Datakoen** is a **simple web app** designed to provide powerful **data tools** and showcase my expertise in **data science**. Whether you're a seasoned data professional or just starting your journey, my platform is designed to help you harness the full potential of your data.
"""
)

# Create sections with headers and descriptions
st.header("🔧 Explore My Tools")
st.write(
    """
Dive into my suite of data analytics tools crafted to simplify and enhance your data processes. While many of the tools are still under development, you can start exploring and using the ones that are ready:
- **📊 Data visualization** that brings your data to life
- **🛠️ Data wrangling tools** that streamline your workflow
"""
)

st.header("💡 Showcase of Excellence")
st.write(
    """
Datakoen is not just a collection of tools—it's also a window into **my world of data science**. Here, you'll find a portfolio of my latest projects, showcasing my skills in data analytics, machine learning, and beyond. Each project is a testament to my **passion for data** and my commitment to delivering **high-quality, impactful results**.
"""
)

st.header("👥 Private Data Consultation")
st.write(
    """
If you're interested in private data consultation, check out my other project, [**Lyceum**](https://alamhanz.xyz/lyceum). Lyceum offers personalized, one-on-one sessions tailored to help you with a wide range of data challenges, from analyzing and automating data to tackling specific technical concerns. Whether you're looking to enhance your statistical understanding or streamline your workflows, **Lyceum provides the in-depth assistance you need**.
"""
)

st.header("🌍 Future Vision")
st.write(
    """
While Datakoen is currently a personal project, my vision is to **eventually make it open source**, inviting collaboration and contributions from the data community.
"""
)

# Add a call to action
st.write(
    "Thank you for visiting Datakoen. **Let's unlock the power of data, one project at a time**."
)

# Add some interactive elements
if st.button("Explore Tools"):
    st.write("Redirecting to tools... (link to tools page)")

if st.button("View Projects"):
    st.write("Redirecting to projects... (link to projects page)")

if st.button("Contact Me"):
    st.write("Redirecting to contact form... (link to contact form)")
