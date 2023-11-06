"""
This entire app is crazily structured, for $REASONS. It's not a good example of
how to write Shiny apps!!
"""
import inspect

from faicons import icon_svg
from htmltools import css
from shiny import App, ui
from shiny.ui import fill
import example_inputs
import example_outputs
from codeutils import format_code, find_decorated_function_name

gap = "var(--bs-gutter-x)"
counter = 0

all_inputs = [
    getattr(example_inputs, name)
    for name in example_inputs.__all__
    if name.startswith("i_")
]
all_outputs = [
    getattr(example_outputs, name)
    for name in example_outputs.__all__
    if name.startswith("o_")
]


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


def preview_input(fn):
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


def preview_output(fn):
    local = dict()

    label = fn.__doc__.strip()
    code = inspect.getsource(fn)
    code = format_code(code)
    exec(
        # Need to add implied imports to the code
        "from shiny import render, reactive, ui\n" + code,
        dict(),
        local,
    )

    fn_name = find_decorated_function_name(code)

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


app_ui = ui.page_sidebar(
    ui.sidebar(open="always", width="0"),
    ui.include_css("styles.css"),
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
                *[preview_input(i) for i in all_inputs],
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
                *[preview_output(o) for o in all_outputs],
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
    [o() for o in all_outputs]


app = App(app_ui, server)
