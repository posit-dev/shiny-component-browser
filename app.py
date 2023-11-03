"""
This entire app is crazily structured, for $REASONS. It's not a good example of
how to write Shiny apps!!
"""

import inspect
import re

from faicons import icon_svg

from shiny import App, reactive, render, ui
from shiny.ui import fill

gap = "2rem"
counter = 0


def strip_indent(code: str):
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
    while lines[0].strip().startswith("@"):
        lines.pop(0)
    assert lines[0].strip().startswith("def ")
    lines.pop(0)
    indent = min_indent(lines)
    code = "\n".join(lines)
    code = re.sub(f"^{indent}", "", code, flags=re.MULTILINE)
    return code


def format_code(code: str):
    import black

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


def demo_input(label):
    def wrapper(fn):
        code = inspect.getsource(fn)
        code = format_code(code)

        global counter
        counter += 1

        return ui.TagList(
            ui.navset_card_underline(
                ui.nav(
                    "View",
                    fill.as_fill_item(ui.div(eval(code), class_="demo")),
                ),
                ui.nav("Code", show_code(code)),
                title=label,
            )
        )

    return wrapper


# @demo_input("Select box (single value)")
# def i1():
#     ui.input_select(
#         "select_one",
#         label="Select box (single value)",
#         choices=["A", "B", "C"],
#     )


# @demo_input("Select box (multi value)")
# def i2():
#     ui.input_select(
#         "select_multi",
#         label="Select box (multi value)",
#         choices=["A", "B", "C"],
#         multiple=True,
#     )


@demo_input("Select input (single value)")
def i3():
    ui.input_selectize(
        "selectize_one",
        label="Selectize (single value)",
        choices=["A", "B", "C"],
    )


@demo_input("Select input (multi value)")
def i4():
    ui.input_selectize(
        "selectize_multi",
        label="Selectize (multi value)",
        choices=["A", "B", "C"],
        multiple=True,
    )


@demo_input("Slider (single value)")
def i5():
    ui.input_slider(
        "slider_single",
        label="Slider (single value)",
        min=0,
        max=1,
        value=0.5,
        step=0.05,
    )


@demo_input("Slider (range)")
def i6():
    ui.input_slider(
        "slider_range",
        label="Slider (range)",
        min=0,
        max=100,
        value=[35, 65],
    )


@demo_input("Date input")
def i7():
    ui.input_date(
        "date",
        label="Date input",
        value="1970-01-01",
    )


@demo_input("Date range input")
def i8():
    ui.input_date_range(
        "date_range",
        label="Date range input",
        start="1988-01-01",
        end="1988-12-31",
        format="mm/dd/yyyy",
    )


@demo_input("Checkbox input")
def i9():
    ui.input_checkbox(
        "checkbox",
        label="Checkbox input",
        value=True,
    )


@demo_input("Checkbox group input")
def i10():
    ui.input_checkbox_group(
        "checkbox_group",
        label="Checkbox group input",
        choices=["A", "B", "C"],
        selected="A",
    )


@demo_input("Switch input")
def i11():
    ui.input_switch("switch", label="Switch input", value=True)


@demo_input("Radio buttons")
def i12():
    ui.input_radio_buttons(
        "radio", label="Radio buttons", choices=["A", "B", "C"], selected="A"
    )


@demo_input("Numeric input")
def i13():
    ui.input_numeric("numeric", label="Numeric input", value=5)


@demo_input("Text input")
def i14():
    ui.input_text("text", label="Text input", value="Hello, world!")


@demo_input("Multi-line text input")
def i15():
    ui.input_text_area(
        "textarea",
        label="Multi-line text input",
        value="Hello, world!",
        height="125px",
    )


@demo_input("Password input")
def i16():
    ui.input_password("password", label="Password input")


@demo_input("Action button")
def i17():
    ui.input_action_button(
        "action_button",
        label="Recalculate",
    )


@demo_input("Action link")
def i18():
    ui.input_action_link(
        "action_link",
        label="Continue",
    )


local = locals()


def demo_output(fn_name, label):
    def wrapper(fn):
        code = inspect.getsource(fn)
        code = format_code(code)
        exec(code, globals(), local)
        func = local[fn_name]
        return ui.navset_card_underline(
            ui.nav("View", func),
            ui.nav("Code", show_code(code)),
            title=label,
        )

    return wrapper


# OUTPUTS


def o1():
    import matplotlib.pyplot as plt

    @render.plot(height=300)
    def plot_mpl():
        plt.scatter(x=[1, 2, 3], y=[3, 2, 1])


def o2():
    import seaborn as sns

    @render.plot(height=300)
    def plot_sns():
        sns.lineplot(x=[1, 2, 3], y=[12, 4, 8])


def o3():
    from datetime import datetime

    @render.text
    def text():
        reactive.invalidate_later(1)  # Update every second
        return f"The current time is {datetime.now().strftime('%H:%M:%S')}"


def o4():
    from datetime import datetime

    @render.ui
    def dynamic_ui():
        reactive.invalidate_later(1)  # Update every second
        return ui.TagList(
            "The current time is ",
            ui.strong(datetime.now().strftime("%H:%M:%S")),
        )


def o5():
    from palmerpenguins import load_penguins

    @render.data_frame
    def datatable():
        df = load_penguins()
        df = df[["species", "bill_length_mm", "bill_depth_mm"]]
        return render.DataTable(df, height="300px")


def o6():
    from palmerpenguins import load_penguins

    @render.data_frame
    def datagrid():
        return render.DataGrid(load_penguins(), height="300px", filters=True)


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
    ui.h1("Shiny Component Gallery", class_="display-3"),
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
                i17,  # Action button
                i18,  # Action link
                i9,  # Checkbox input
                i10,  # Checkbox group
                i7,  # Date input
                i8,  # Date range input
                i13,  # Numeric input
                # i1,  # Select box (single value)
                # i2,  # Select box (multi value)
                i12,  # Radio buttons
                i3,  # Selectize (single value)
                i4,  # Selectize (multi value)
                i5,  # Slider (single value)
                i6,  # Slider (range)
                i11,  # Switch input
                i14,  # Text input
                i15,  # Multi-line text input
                i16,  # Password input
                width=300,
                fill=False,
                heights_equal="all",
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
                demo_output("plot_mpl", "Plot (matplotlib)")(o1),
                demo_output("plot_sns", "Plot (Seaborn)")(o2),
                demo_output("datatable", "Data Table")(o5),
                demo_output("datagrid", "Data Grid")(o6),
                demo_output("text", "Text")(o3),
                demo_output("dynamic_ui", "UI objects/HTML")(o4),
                width=450,
                fill=False,
                heights_equal="row",
                gap=gap,
            ),
        ),
    ),
)


def server(input, output, session):
    o3()  # Data Table
    o4()  # Data Grid
    o1()  # Plot (matplotlib)
    o2()  # Plot (Seaborn)
    o5()  # Text
    o6()  # UI


app = App(app_ui, server)
