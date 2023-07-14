from zipfile import ZipFile
import polars as pl
import pandas as pd
import os
import shutil
from io import BytesIO
import streamlit as st
from collections import Counter

@st.cache_data
def readFiles(fn_root, path):
    print("new file is uploaded : ", fn_root)
    placeholder = st.empty()
    placeholder.info("reading files")
    if "zip" in st.session_state["dataset"].type:
        zObject = ZipFile(st.session_state["dataset"], "r")
        zObject.extractall(path=path + fn_root + "/")
        data_list = []
        for fn in os.listdir(path + fn_root):
            print(path + fn_root + "/" + fn)
            try:
                data_temp = pl.read_excel(path + fn_root + "/" + fn)
                data_list.append(data_temp)
            except:
                data_list = []
                # shutil.rmtree(path+fn_root+'/')
                break

        if len(data_list) == 0:
            df = pl.DataFrame()
            placeholder.error("Unrecognizeable Format. Excel Only inside zip.")
            st.session_state["file_readable"] = False
        else:
            df = pl.concat(data_list)
            st.session_state["file_readable"] = True
            placeholder.empty()
            shutil.rmtree(path + fn_root + "/")

    elif "spreadsheet" in st.session_state["dataset"].type:
        df = pl.read_excel(st.session_state["dataset"])
        st.session_state["file_readable"] = True
        placeholder.empty()

    elif "csv" in st.session_state["dataset"].type:
        df = pl.read_csv(st.session_state["dataset"])
        st.session_state["file_readable"] = True
        placeholder.empty()

    else:
        df = None
        placeholder.error("Unrecognizeable Format. Excel or Zip format.")
        st.session_state["file_readable"] = False

    return df


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="xlsxwriter")
    df.to_excel(writer, index=False, sheet_name="Sheet1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet1"]
    format1 = workbook.add_format({"num_format": "0.00"})
    worksheet.set_column("A:A", None, format1)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def upload_data():
    with st.sidebar:
        uploaded_file = st.file_uploader("upload your data", key="dataset")
        if uploaded_file:
            fn_uploaded = st.session_state["dataset"].name
            df_polars = readFiles(fn_uploaded, 
                                st.session_state["config"]["zippath"])
        else:
            df_polars = None
    return df_polars


def config_types(df):
    """
    Do Data type changes capability.

    Return df after data type changes.
    """
    with st.expander('Data Edit'):
        if df is not None:
            default_types = dict(zip(df.columns, df.dtypes))
            base_types = list(set([pl.Decimal, pl.Float64, pl.Int64,
                                   pl.UInt64, pl.Date,
                                   pl.Datetime, pl.Boolean, pl.Binary,
                                   pl.Categorical, pl.Utf8]+df.dtypes))
            col_types = {}

            for colm in default_types:
                st.write(colm)
                col_types[colm] = st.selectbox("types :", base_types,
                                               index=base_types
                                               .index(default_types[colm]),
                                               key=colm+"_types")

                if default_types[colm] != col_types[colm]:
                    df = df.with_columns(pl.col(colm)
                                        .cast(col_types[colm]))
        else:
            st.write('Error Data Load')
        
        return df


# def data_clean(df):
#     """
#     Return Cleaner df.

#     task:
#     1. Rename the Duplicate Column Name
#     """
#     all_cols = df.columns
#     if len(all_cols) == len(set(all_cols)):
#         df_update = df.copy()
#     else:
#         col_cnt = Counter(all_cols)
#         high_col_cnt = dict((k, v) for k, v in col_cnt.items() if v > 1)
#         print(high_col_cnt)
#         for k in high_col_cnt:
#             for i in range(high_col_cnt[k]):




#     return df_update


## missing value handle

