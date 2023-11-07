import re
import ast
import textwrap


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


def format_code(code: str):
    import black

    code = extract_code(code)
    code = textwrap.dedent(code)

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
