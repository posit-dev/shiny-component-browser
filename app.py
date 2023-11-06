"""
This entire app is crazily structured, for $REASONS. It's not a good example of
how to write Shiny apps!!
"""

import inspect
import re

from faicons import icon_svg
from htmltools import css
from shiny import App, reactive, render, ui
from shiny.ui import fill

gap = "var(--bs-gutter-x)"
counter = 0


def extract_code(code: str):
    """Get just the body of a function, without the signature or docstring."""

    lines = code.splitlines()
    # Remove decorators
    while lines[0].strip().startswith("@"):
        lines.pop(0)
    # Remove function signature
    assert lines[0].strip().startswith("def ")
    lines.pop(0)
    # Remove docstring
    if lines[0].strip().startswith('"') and lines[0].strip().endswith('"'):
        lines.pop(0)
        if lines[0].strip() == "":
            lines.pop(0)
    return "\n".join(lines)


def strip_indent(code: str):
    """Remove the most amount of indent possible from a block of code."""

    def min_indent(lines: list[str]):
        ws = [re.search(r"^\s*", line).group(0) for line in lines if line.strip() != ""]
        # Make sure it's either \t, or " ", not both
        space = False
        tab = False
        min = ""
        for x in ws:
            space = space or " " in x
            tab = tab or "\t" in x
            if min == "" or len(x) < len(min):
                min = x
        if space and tab:
            raise ValueError("Mixed tabs and spaces")
        return min

    lines = code.splitlines()
    indent = min_indent(lines)
    code = "\n".join(lines)
    code = re.sub(f"^{indent}", "", code, flags=re.MULTILINE)
    return code


def format_code(code: str):
    import black

    code = extract_code(code)
    code = strip_indent(code)

    mode = black.FileMode()
    mode.line_length = 50
    fast = False
    try:
        code = black.format_file_contents(code, fast=fast, mode=mode)
    except Exception:
        print(code)
        raise
    return re.sub(r"\n{3,}", "\n\n", code)


def show_code(code):
    return ui.TagList(
        ui.pre(code),
        ui.tags.button(
            icon_svg("copy", style="regular"),
            " Copy to clipboard",
            class_="btn btn-default btn-sm",
            onclick="navigator.clipboard.writeText(this.previousSibling.textContent);",
        ),
    )


def nav_link(label, href):
    return ui.nav_control(
        {"class": "nav-item"},
        ui.a(
            label,
            class_="nav-link",
            href=href,
            target="_blank",
        ),
    )


def demo_input(fn):
    code = inspect.getsource(fn)
    code = format_code(code)
    label = fn.__doc__.strip()

    global counter
    counter += 1

    return ui.TagList(
        ui.navset_card_underline(
            ui.nav(
                "View",
                fill.as_fillable_container(
                    fill.as_fill_item(
                        ui.div(
                            eval(code),
                            class_="demo",
                            style=css(
                                min_height="150px",
                                align_items="center",
                                justify_content="center",
                            ),
                        )
                    )
                ),
            ),
            ui.nav("Code", show_code(code)),
            title=label,
        )
    )


def i_native_select():
    "Select box (single value)"

    ui.input_select(
        "select_one",
        label="Select box (single value)",
        choices=["A", "B", "C"],
    )


def i_native_select_multi():
    "Select box (multi value)"

    ui.input_select(
        "select_multi",
        label="Select box (multi value)",
        choices=["A", "B", "C"],
        multiple=True,
    )


def i_selectize():
    "Select input (single value)"

    ui.input_selectize(
        "selectize_one",
        label="Selectize (single value)",
        choices=["A", "B", "C"],
    )


def i_selectize_multi():
    "Select input (multi value)"

    ui.input_selectize(
        "selectize_multi",
        label="Selectize (multi value)",
        choices=["A", "B", "C"],
        multiple=True,
    )


def i_slider_single():
    "Slider (single value)"

    ui.input_slider(
        "slider_single",
        label="Slider (single value)",
        min=0,
        max=1,
        value=0.5,
        step=0.05,
    )


def i_slider_range():
    "Slider (range)"

    ui.input_slider(
        "slider_range",
        label="Slider (range)",
        min=0,
        max=100,
        value=[35, 65],
    )


def i_date():
    "Date input"

    ui.input_date(
        "date",
        label="Date input",
        value="1970-01-01",
    )


def i_date_range():
    "Date range input"

    ui.input_date_range(
        "date_range",
        label="Date range input",
        start="1988-01-01",
        end="1988-12-31",
        format="mm/dd/yyyy",
    )


def i_checkbox():
    "Checkbox input"

    ui.input_checkbox(
        "checkbox",
        label="Checkbox input",
        value=True,
    )


def i_checkbox_group():
    "Checkbox group input"

    ui.input_checkbox_group(
        "checkbox_group",
        label="Checkbox group input",
        choices=["A", "B", "C"],
        selected="A",
    )


def i_switch():
    "Switch input"

    ui.input_switch("switch", label="Switch input", value=True)


def i_radio():
    "Radio buttons"

    ui.input_radio_buttons(
        "radio", label="Radio buttons", choices=["A", "B", "C"], selected="A"
    )


def i_numeric():
    "Numeric input"

    ui.input_numeric("numeric", label="Numeric input", value=5)


def i_text():
    "Text input"

    ui.input_text("text", label="Text input", value="Hello, world!")


def i_textarea():
    "Multi-line text input"

    ui.input_text_area(
        "textarea",
        label="Multi-line text input",
        value="Hello, world!",
        height="125px",
    )


def i_password():
    "Password input"

    ui.input_password("password", label="Password input")


def i_action_btn():
    "Action button"

    ui.input_action_button(
        "action_button",
        label="Recalculate",
    )


def i_action_link():
    "Action link"

    ui.input_action_link(
        "action_link",
        label="Continue",
    )


local = locals()


def demo_output(fn_name, label, fn):
    code = inspect.getsource(fn)
    code = format_code(code)
    exec(code, globals(), local)
    func = local[fn_name]
    return ui.navset_card_underline(
        ui.nav(
            "View",
            func,
        ),
        ui.nav(
            "Code",
            show_code(code),
        ),
        title=label,
    )


# OUTPUTS


def o_plt():
    import matplotlib.pyplot as plt

    @render.plot(height=300)
    def plot_mpl():
        plt.scatter(x=[1, 2, 3], y=[3, 2, 1])


def o_sns():
    import seaborn as sns

    @render.plot(height=300)
    def plot_sns():
        sns.lineplot(x=[1, 2, 3], y=[12, 4, 8])


def o_plotly():
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
    from datetime import datetime

    @render.text
    def text():
        reactive.invalidate_later(1)  # Update every second
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"


def o_ui():
    from datetime import datetime

    @render.ui
    def dynamic_ui():
        reactive.invalidate_later(1)  # Update every second
        return ui.TagList(
            "The current time is ",
            ui.strong(datetime.now().strftime("%H:%M:%S")),
        )


def o_df_tbl():
    from palmerpenguins import load_penguins

    @render.data_frame
    def datatable():
        df = load_penguins()
        df = df[["species", "bill_length_mm", "bill_depth_mm"]]
        return render.DataTable(df, height="300px")


def o_df_grid():
    from palmerpenguins import load_penguins

    @render.data_frame
    def datagrid():
        return render.DataGrid(load_penguins(), height="300px", filters=True)


def o_leaflet():
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


app_ui = ui.page_sidebar(
    ui.sidebar(open="always", width="0"),
    ui.tags.style(
        ui.HTML(
            # ".demo>.shiny-input-container>label, h3.label { font-size: 1.2em; margin-bottom: 1.2em; }"
            ".demo>.shiny-input-container>label { display: none; }"
            "h3.label { font-size: 1.2em; margin-bottom: 1.2em; }"
            ".demo-output { background-color: var(--bs-gray-100); }"
            "aside { display: none; }"
            ".bslib-sidebar-layout>.main { grid-column: unset; }"
            "hr { visibility: hidden; }"
        )
    ),
    ui.h1("Shiny Components", class_="display-3"),
    ui.row(
        ui.column(
            9,
            ui.markdown(
                """
                [Shiny](https://shiny.posit.co/py/) is a Python library that's
                designed to help data scientists easily build interactive web
                apps.

                This page demonstrates Shiny's built-in input and output
                controls. Each component is shown with a live example and the
                code used to generate it.
                """
            ),
            style="font-size: 1.2em;",
        )
    ),
    ui.hr(),
    ui.h2("Inputs", id="inputs"),
    ui.row(
        ui.column(
            3,
            ui.markdown(
                """
                Use inputs to accept information from the user.
                
                The first argument to each input function should be a unique
                identifier, which is used to refer to the input's value in
                output code.

                For example, if you create a checkbox using code like this:
                ```
                ui.input_checkbox(
                    "enable",
                    label="Enable?"
                )
                ```
                then you can access its
                value in output code using `input.enable()`.
                """
            ),
        ),
        ui.column(
            9,
            ui.layout_column_wrap(
                demo_input(i_action_btn),
                demo_input(i_action_link),
                demo_input(i_checkbox),
                demo_input(i_checkbox_group),
                demo_input(i_date),
                demo_input(i_date_range),
                demo_input(i_numeric),
                demo_input(i_radio),
                demo_input(i_native_select),
                demo_input(i_native_select_multi),
                demo_input(i_selectize),
                demo_input(i_selectize_multi),
                demo_input(i_slider_single),
                demo_input(i_slider_range),
                demo_input(i_switch),
                demo_input(i_text),
                demo_input(i_textarea),
                demo_input(i_password),
                width=300,
                fill=False,
                heights_equal="row",
                gap=gap,
            ),
        ),
    ),
    ui.hr(),
    ui.h2("Outputs", id="outputs"),
    ui.row(
        ui.column(
            3,
            ui.markdown(
                """
                Use outputs to display information to the user, usually
                reflecting choices they've made using inputs.

                Each output is a function that is adorned with a render
                decorator, like `@render.plot` or `@render.data_frame`. The
                function should return an object to be displayed; each render
                decorator expects a different type of object.
                """
            ),
        ),
        ui.column(
            9,
            ui.layout_column_wrap(
                demo_output("plot_mpl", "Plot (matplotlib)", o_plt),
                demo_output("plot_sns", "Plot (Seaborn)", o_sns),
                demo_output("plot_plotly", "Plot (Plotly)", o_plotly),
                demo_output("datatable", "Data Table", o_df_tbl),
                demo_output("datagrid", "Data Grid", o_df_grid),
                demo_output("leaflet_map", "Map (ipyleaflet)", o_leaflet),
                demo_output("text", "Text", o_txt),
                demo_output("dynamic_ui", "UI objects/HTML", o_ui),
                width=450,
                fill=False,
                heights_equal="row",
                gap=gap,
            ),
        ),
    ),
    window_title="Shiny Components",
)


def server(input, output, session):
    o_txt()
    o_ui()
    o_plt()
    o_sns()
    o_plotly()
    o_df_tbl()
    o_df_grid()
    o_leaflet()


app = App(app_ui, server)
