import sys


code = """def add(a, b):
    result = a + b
    return result

x = add(10, 20)

print(x)"""


def trace(frame, event, arg):

    if frame.f_code.co_filename == "<user_code>":

        print(
            "EVENT:",
            event,
            "LINE:",
            frame.f_lineno,
            "FUNCTION:",
            frame.f_code.co_name
        )

        if event == "return":

            print(
                "RETURN VALUE:",
                arg
            )

    return trace


sys.settrace(trace)

try:

    compiled_code = compile(
        code,
        "<user_code>",
        "exec"
    )

    exec(compiled_code, {})

finally:

    sys.settrace(None)