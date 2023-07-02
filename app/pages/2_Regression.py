import streamlit as st
import polars as pl
import yaml
from pages.tools.utils import basicsidebar, footer
from pages.tools.assets import set_assets
from pages.tools.common import upload_data

from pages.tools.calc import RunRegression

with open("config.yaml", "r") as f:
    st.session_state['config'] = yaml.load(f, Loader=yaml.FullLoader)
# zippath = st.session_state['config']['zippath']

set_assets(st.session_state['config'])
df = upload_data()

## opening
st.title("Regression")
st.markdown("drag and drop regression")


## processing
if df is not None:
    all_dimensions = df.select([pl.col(pl.Boolean),pl.col(pl.Binary),pl.col(pl.Categorical),pl.col(pl.Utf8)]).columns
    all_measures = df.select([pl.col(pl.Decimal),pl.col(pl.Float32),pl.col(pl.Float64)
           ,pl.col(pl.Int8),pl.col(pl.Int16),pl.col(pl.Int32),pl.col(pl.Int64)]).columns
    dshape = df.shape

    target_opt = st.selectbox("target variable:",all_measures,key='target_reg')
    features_opt = st.multiselect('dependent variable:',all_measures,key='feature_reg')
    add_c = st.checkbox('with bias',value=True,key='add_constantd')

    # show = st.checkbox('standardize',key='is_standardized')
    reg_result = RunRegression(df)

footer()