import re
import ast


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


def find_decorated_function_name(code):
    """Given valid Python source code, find the name of the first function that
    has one or more decorators."""

    tree = ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if len(node.decorator_list) > 0:
                return node.name
    raise ValueError("No decorated functions found in code")
