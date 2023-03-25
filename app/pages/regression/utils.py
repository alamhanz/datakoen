import streamlit as st
from zipfile import ZipFile
import polars as pl
import os
import shutil
from io import BytesIO
import pandas as pd

def head():
    st.markdown("""
        <h1 style='text-align: center; margin-bottom: -35px;'>
        Banana Pealer
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
        "Wants to know next demand?",
        "Try this apps.",
        "It will help you to calculate your next week demand."
        "Just start by adding your data file to this app \U0001F642."
    )


def sidebar(config):
    with st.sidebar:
        add_radio = st.radio(
            "Choose Predictor",
            ("Base Predictor", "Method A", "Method B"),
            key='predictor'
        )

        uploaded_file = st.file_uploader("Upload File", key = 'dataset')

def sidebar_df(config):
    with st.sidebar:
        if config['column_maps']['hue']:
            huelist = list(st.session_state['df'].groupby(config['column_maps']
                                    ['hue'])[config['column_maps']
                                    ['demand']].sum().sort_values(ascending=False).index)
        else:
            huelist = []

        huelist = ['all'] + huelist
        add_selectbox = st.selectbox(
            "Choose Element?",
            huelist,
            index=0,
            key='box'
        )

        st.number_input('factor multiplier',value=1.0, min_value=0.5, max_value=2.5,key='factor')

        run_program = st.button('predict', key='run')

@st.cache_data
def readFiles(fn_root,path):
    print('new file is uploaded : ', fn_root)
    placeholder = st.empty()
    placeholder.info('reading files')
    if 'zip' in st.session_state['dataset'].type:
        zObject = ZipFile(st.session_state['dataset'], 'r')
        zObject.extractall(path=path+fn_root+'/')
        data_list = []
        for fn in os.listdir(path+fn_root):
            print(path+fn_root+'/'+fn)
            try:
                data_temp = pl.read_excel(path+fn_root+'/'+fn)
                data_list.append(data_temp)
            except:
                data_list = []
                # shutil.rmtree(path+fn_root+'/')
                break

        if len(data_list)==0:
            df = pl.DataFrame()
            placeholder.error('Unrecognizeable Format. Excel Only inside zip.')
            st.session_state['file_readable'] = False
        else:
            df = pl.concat(data_list)
            st.session_state['file_readable'] = True
            placeholder.empty()
            shutil.rmtree(path+fn_root+'/')

    elif 'spreadsheet' in st.session_state['dataset'].type:
        df = pl.read_excel(st.session_state['dataset'])
        st.session_state['file_readable'] = True
        placeholder.empty()

    else:
        df = pl.DataFrame()
        placeholder.error('Unrecognizeable Format. Excel or Zip format.')
        st.session_state['file_readable'] = False

    return df

@st.cache_data
def polars_csv(path):
    return pl.read_csv(path)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data