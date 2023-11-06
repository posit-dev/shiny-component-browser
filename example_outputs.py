import inspect
import sys
from shiny import render, reactive, ui


def o_plt():
    "Plot (matplotlib)"

    import matplotlib.pyplot as plt

    @render.plot(height=300)
    def plot_mpl():
        plt.scatter(x=[1, 2, 3], y=[3, 2, 1])


def o_sns():
    "Plot (Seaborn)"

    import seaborn as sns

    @render.plot(height=300)
    def plot_sns():
        sns.lineplot(x=[1, 2, 3], y=[12, 4, 8])


def o_plotly():
    "Plot (Plotly)"

    from shinywidgets import render_widget
    import plotly.express as px

    @render_widget
    def plot_plotly():
        # From https://plotly.com/python/distplot/

        df = px.data.tips()
        fig = px.histogram(
            df,
            x="total_bill",
            y="tip",
            color="sex",
            marginal="rug",
            hover_data=df.columns,
        )
        fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
        return fig


def o_txt():
    "Text"

    from datetime import datetime

    @render.text
    def text():
        reactive.invalidate_later(1)  # Update every second
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"


def o_ui():
    "UI objects/HTML"

    from datetime import datetime

    @render.ui
    def dynamic_ui():
        reactive.invalidate_later(1)  # Update every second
        return ui.TagList(
            "The current time is ",
            ui.strong(datetime.now().strftime("%H:%M:%S")),
        )


def o_df_tbl():
    "Data Table"

    from palmerpenguins import load_penguins

    @render.data_frame
    def datatable():
        df = load_penguins()
        df = df[["species", "bill_length_mm", "bill_depth_mm"]]
        return render.DataTable(df, height="300px")


def o_df_grid():
    "Data Grid"

    from palmerpenguins import load_penguins

    @render.data_frame
    def datagrid():
        return render.DataGrid(load_penguins(), height="300px", filters=True)


def o_leaflet():
    "Map (ipyleaflet)"

    from shinywidgets import render_widget
    import ipyleaflet
    import json

    # From http://eric.clst.org/Stuff/USGeoJSON and
    # https://en.wikipedia.org/wiki/List_of_United_States_counties_and_county_equivalents
    with open("nycounties.geojson") as f:
        nycounties = json.load(f)

    # Build {id: population} choropleth data
    pop = {
        id: props["pop"]
        for id, props in [
            (feat["id"], feat["properties"]) for feat in nycounties["features"]
        ]
    }

    @render_widget
    def leaflet_map():
        m = ipyleaflet.Map(center=[42.8920, -76.0692], zoom=6)
        choro = ipyleaflet.Choropleth(
            geo_data=nycounties,
            choro_data=pop,
        )
        m.add_layer(choro)

        return m


__all__ = []
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if not name.startswith("_"):
        __all__.append(name)
