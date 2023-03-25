import streamlit as st
import yaml
from utils import head, sidebar, sidebar_df, readFiles, polars_csv, update_w_recipe, to_excel
from assets import set_bg, set_icon
import polars as pl

# read config
with open("config.yaml", "r") as f:
    st.session_state['config'] = yaml.load(f, Loader=yaml.FullLoader)
col_date = st.session_state['config']['column_maps']['date']
col_demand = st.session_state['config']['column_maps']['demand']
col_hue = st.session_state['config']['column_maps']['hue']
zippath = st.session_state['config']['zippath']

is_food_service = True
st.session_state['config']['industry'] = 'food'
st.session_state['df'] = None

# First Part
set_icon('assets/icon.jpeg')
set_bg('assets/bg.jpeg')
head()

# Side bar
sidebar(st.session_state['config'])

# Main
if st.session_state['dataset']:
    fn_uploaded = st.session_state['dataset'].name
    df_polars = readFiles(fn_uploaded,zippath)
    df_polars = df_polars.with_columns([
            pl.col(col_date).str.strptime(pl.Date, fmt="%m-%d-%y").cast(pl.Date)                                         
        ])

    if is_food_service:
        df_recipe = polars_csv(st.session_state['config']['recipepath'])
        df_polars = update_w_recipe(df_polars,df_recipe)
        col_hue = st.session_state['config']['column_maps']['hue'] ## update hue
        col_demand = st.session_state['config']['column_maps']['demand'] ## update demand

    st.session_state['df'] = df_polars.to_pandas()
    sidebar_df(st.session_state['config'])

if st.session_state['df'] is not None:
    if st.session_state['box']=='all':
        data_for_visual = st.session_state['df'].copy()
    else:
        data_for_visual = st.session_state['df'][st.session_state['df'][col_hue]==st.session_state['box']]

    data_for_visual = data_for_visual.groupby([col_date])[col_demand].sum().reset_index().sort_values(col_date)
    data_for_visual.columns = [col_date,col_demand]

    if is_food_service:
        st.caption('Here is the Menu list with no Recipe :')
        df_no_ingredient = df_polars.filter(pl.col(col_hue).is_null()).to_pandas()
        st.dataframe(df_no_ingredient[['Description','Quantity']].drop_duplicates().sort_values('Quantity',ascending=False))
    st.dataframe(st.session_state['df'])
    st.line_chart(
        data=data_for_visual,
        x=col_date,
        y=col_demand,
        use_container_width=True
    )

if st.session_state.get('run',False):
    df_run = st.session_state['df'].groupby(col_hue)[col_demand].sum().reset_index()
    df_run.columns = ['ingredient','weekly_amount']
    df_run['weekly_amount'] = (df_run['weekly_amount']/4)*st.session_state['factor']
    df_run = to_excel(df_run)

    st.download_button(label='📥 Download The Result',
                        data=df_run ,
                        file_name= 'result.xlsx')
