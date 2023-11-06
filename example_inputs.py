from shiny import ui
import inspect
import sys


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


__all__ = []
for name, obj in inspect.getmembers(sys.modules[__name__]):
    if not name.startswith("_"):
        __all__.append(name)
