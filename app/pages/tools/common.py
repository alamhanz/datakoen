"""Common utilities."""

import os
import shutil
from io import BytesIO
from typing import Tuple, Type
from zipfile import ZipFile

import pandas as pd
import streamlit as st


def upload_data(_logger, text="upload your data", key="dataset"):
    """Upload user data.

    Returns:
        _type_: _description_
    """
    uploaded_file = st.file_uploader(text, key=key, type=["csv"])
    if uploaded_file:
        _logger.info("uploading the data")
        # Read the first 10 rows to check the structure
        partial_data = pd.read_csv(uploaded_file, nrows=10)
        num_columns = len(partial_data.columns)

        # Check if the column count exceeds x
        max_columns = 7
        if num_columns > max_columns:
            with st.sidebar:
                st.error(
                    f"The file has {num_columns} columns, but the maximum allowed is {max_columns}."
                )
            return None

        # Reset file pointer to re-read the full file
        uploaded_file.seek(0)

        # Check the row count
        # total_rows = sum(1 for _ in open(uploaded_file.name)) - 1  # Minus header row
        chunk_size = 1000
        total_rows = 0
        for chunk in pd.read_csv(uploaded_file, chunksize=chunk_size):
            total_rows += len(chunk)
            max_rows = 5000
            if total_rows > max_rows:
                with st.sidebar:
                    st.error(
                        f"The file has more than {max_rows} rows (current count: {total_rows})."
                    )
                return None

        # Reset file pointer again to load the data after validation
        uploaded_file.seek(0)
        df_data = pd.read_csv(uploaded_file)

        # Display data
        st.sidebar.success("File uploaded successfully!")

        return df_data


## Unused
def custom_legend_name(fig, new_names):
    """create custom legerd.

    Args:
        fig (figure): figure object
        new_names (list): list of new names

    Returns:
        figure: figure with new legend names
    """
    for i, new_name in enumerate(new_names):
        fig.data[i].name = new_name
    return fig


# def findMaxAverage(self, nums: List[int], k: int) -> float:
def make_grid(cols: int, rows: int) -> Tuple[Type[st.columns]]:
    """make grid from streamlit

    Args:
        cols (int): number of columns
        rows (int): number of rows

    Returns:
        grid : streamlit object
    """
    grid = []
    for i in range(cols):
        print(i)
        with st.container():
            grid.append(st.columns(rows))
    return tuple(grid)


@st.cache_data
def readFiles(fn_root, path):
    """Read user input file.

    Args:
        fn_root (_type_): _description_
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
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
    """Export from dataframe to excel.

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
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


def config_types(df):
    """
    Do Data type changes capability.

    Return df after data type changes.
    """
    # with st.expander("Data Edit"):
    if df is not None:
        default_types = dict(zip(df.columns, df.dtypes))
        base_types = list(
            set(
                [
                    pl.Decimal,
                    pl.Float64,
                    pl.Int64,
                    pl.UInt64,
                    pl.Date,
                    pl.Datetime,
                    pl.Boolean,
                    pl.Binary,
                    pl.Categorical,
                    pl.Utf8,
                ]
                + df.dtypes
            )
        )
        col_types = {}

        for colm in default_types:
            st.write(colm)
            col_types[colm] = st.selectbox(
                "types :",
                base_types,
                index=base_types.index(default_types[colm]),
                key=colm + "_types",
            )

            if default_types[colm] != col_types[colm]:
                if col_types[colm] in [pl.Date, pl.Datetime]:
                    format_date = st.text_input(
                        "format datetime [default : %Y-%m-%d]", "%Y-%m-%d"
                    )
                    df = df.with_columns(
                        pl.col(colm)
                        .str.strptime(pl.Date, fmt=format_date)
                        .cast(pl.Datetime)
                    )
                else:
                    df = df.with_columns(pl.col(colm).cast(col_types[colm]))
            st.divider()

    else:
        st.write("Error Data Load")

    return df


def split_col_types(df):
    """
    List down all columns based on types.

    Return 2 list of column name.
    """
    all_dimensions = df.select(
        [
            pl.col(pl.Boolean),
            pl.col(pl.Binary),
            pl.col(pl.Categorical),
            pl.col(pl.Utf8),
            pl.col(pl.Date),
            pl.col(pl.Datetime),
            pl.col(pl.Time),
        ]
    ).columns
    all_measures = df.select(
        [
            pl.col(pl.Decimal),
            pl.col(pl.Float32),
            pl.col(pl.Float64),
            pl.col(pl.Int8),
            pl.col(pl.Int16),
            pl.col(pl.Int32),
            pl.col(pl.Int64),
        ]
    ).columns

    return all_dimensions, all_measures
