"""Common utilities."""

from io import BytesIO
from typing import Tuple, Type

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
