"""Homepage for Datakoen."""

from pages.tools.assets import koen_footer, koen_header
from pages.tools.common import default_data
from pygwalker.api.streamlit import StreamlitRenderer

koen_header("wide")

df = default_data(to_pandas=True)
pyg_app = StreamlitRenderer(df)
pyg_app.explorer()

koen_footer()
