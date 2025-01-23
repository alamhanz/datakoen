"""Web page for chat page."""

import logging
from functools import partial

import lereng
import streamlit as st
import yaml
from pages.tools.assets import set_assets
from pages.tools.common import change_boolean_status, upload_data
from pages.tools.utils import basicsidebar, footer, koen_logger, koenprep
from streamlit_extras.stylable_container import stylable_container

koen_logger("indomap")
logger = logging.getLogger("indomap")
koenprep("2")

# asset prep and get data
with open("config.yaml", "r") as f:
    st.session_state["config"] = yaml.load(f, Loader=yaml.FullLoader)
set_assets(st.session_state["config"])

with open(st.session_state["config"]["asset"]["map-explain"], "rb") as ctx:
    read_md = ctx.read().decode("UTF-8")

with open("styles/map_container.css") as ctx:
    map_container_css = [i for i in ctx.read().split(".container") if len(i) > 0]


basicsidebar()

# opening
# st.write(
#     "Problem Statement: How easily to create heatmap
#       on indonesia map given cities/province name only?"
# )
st.title("Indonesia Choropleth map")
logger.info("start")

# output_container = stylable_container(key="map_container", css_styles=map_container_css)
input_container1 = st.container()

with input_container1:
    # File uploader
    uploaded_file = st.file_uploader(
        """ """,
        key="2__file_binaries",
        type=["csv"],
        on_change=partial(change_boolean_status, state="2__not_normalize"),
    )
    df_data = upload_data(logger, uploaded_file)

tab1, tab2 = st.tabs(["Maps", "Table"])
with st.sidebar:
    use_sample = None
    if uploaded_file is None:
        use_sample = st.selectbox(
            "Choose Sample Here",
            (None, "nation_sample_population", "jabar_sample_data_kemiskinan"),
            index=0,
        )

if (use_sample is not None) & (df_data is None):
    logger.info("sample used")
    df_data = lereng.datasample(f"{use_sample}.csv")

if df_data is None:
    st.markdown(
        """Upload Your CSV with :

* at least one Indonesia Area Name Column (Province, Kecamatan, or Kabupaten Kota) and
* at least one Numeric Column.
            """
    )

if df_data is not None:
    with tab1:
        output_container = st.container()
        input_container2 = st.container()
        with input_container2:
            col1, col2 = st.columns(2)
            with col1:
                numeric_col_names = df_data.select_dtypes(include=["number"]).columns
                if len(numeric_col_names) < 1:
                    st.error("zero numeric column")
                choosen_metric_col = st.selectbox(
                    "Select a metrics:",
                    options=numeric_col_names,
                )

            with col2:
                col_opt = df_data.select_dtypes(include=["object", "category"]).columns
                if len(col_opt) < 1:
                    st.error("zero dimension column")
                choosen_area_col = st.selectbox(
                    "Select the column area:",
                    options=col_opt,
                )

            # identify
            identifier = lereng.areaname()
            area_type = identifier.identify_area(df_data, choosen_area_col)
            logger.info("area type : %s", area_type)

            with st.spinner("Normalizing Area Name."):
                logger.info("normalizing process")
                original_columns = df_data.columns
                # Normalize the name
                df_data = identifier.normalize(df_data, choosen_area_col)
                df_data["old_" + choosen_area_col] = df_data[choosen_area_col]
                df_data[choosen_area_col] = df_data["normalized_area"]
                other_columns = ["old_" + choosen_area_col, "is_already_normalized"]
                shown_columns = other_columns + list(original_columns)
                logger.info("normalizing process done")

            # make the map
            map_maker = lereng.chrmap(level=area_type)
            map_maker.insert(
                df_data,
                metric_col=choosen_metric_col,
                area_col=choosen_area_col,
                store_path="app/temp_viz",
            )
            html_content = map_maker.rendered_html

            bool_name_same = (
                df_data[~(df_data["is_already_normalized"])]["old_" + choosen_area_col]
                == df_data[~(df_data["is_already_normalized"])][choosen_area_col]
            ).mean()

            if bool_name_same > 0:
                with st.sidebar:
                    if identifier.area_db.api_status == 504:
                        st.warning(
                            "Timeout. The Hugging Face API for the model may just started. Please Retry."
                        )
                        logger.info("Timeout API")
                    elif identifier.area_db.api_status == 429:
                        st.warning("Error. Hugging Face API has reached limit today.")
                        logger.info("Limited API")
                    else:
                        st.warning("Error. Unidentify problem.")
                        logger.info("Another Problem")

        with output_container:
            with stylable_container(key="map_container", css_styles=map_container_css):
                st.components.v1.html(html_content, height=400, width=850)

    with tab2:
        csv_data = (
            df_data[shown_columns]
            .sort_values("is_already_normalized")
            .to_csv(index=False)
        )
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name="datakoen__indomap.csv",
            mime="text/csv",
        )
        st.dataframe(df_data[shown_columns].sort_values("is_already_normalized"))
        st.markdown(read_md)

# footer
footer()
