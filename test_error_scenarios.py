import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from core.executor import Executor
from core.tracer import PythonTracer
from core.execution_controller import ExecutionController


def test_zero_division_error():
    print("\n--- TEST 1: ZeroDivisionError ---")
    code = """x = 10
y = 0
z = x / y"""
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except ZeroDivisionError as e:
        error_caught = e

    assert error_caught is not None, "Expected ZeroDivisionError to be raised"
    assert len(executor.steps) > 0, "Steps before error should be preserved"
    print(f"Preserved {len(executor.steps)} steps before ZeroDivisionError.")

    # Verify controller navigation
    controller = ExecutionController(executor.steps)
    step1 = controller.next()
    assert step1 is not None, "Controller next() should return first step"
    assert step1.step_number == 1

    # Verify variables snapshot
    last_step = executor.steps[-1]
    assert "x" in last_step.variables and last_step.variables["x"] == "Object #1"
    assert "y" in last_step.variables and last_step.variables["y"] == "Object #2"
    assert last_step.objects_snapshot["object_1"]["value"] == 10
    assert last_step.objects_snapshot["object_2"]["value"] == 0
    assert "z" not in last_step.variables, "z should not exist due to error"

    # Verify reset
    assert controller.reset() is None
    print("ZeroDivisionError validation passed.")


def test_name_error():
    print("\n--- TEST 2: NameError ---")
    code = "x = unknown_variable"
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except NameError as e:
        error_caught = e

    assert error_caught is not None, "Expected NameError to be raised"
    print(f"Preserved {len(executor.steps)} steps before NameError.")

    controller = ExecutionController(executor.steps)
    step = controller.next()
    assert step is not None
    # Reset test
    controller.reset()
    assert controller.get_current_step() is None
    print("NameError validation passed.")


def test_type_error():
    print("\n--- TEST 3: TypeError ---")
    code = "x = 10 + 'hello'"
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except TypeError as e:
        error_caught = e

    assert error_caught is not None, "Expected TypeError to be raised"
    assert len(executor.steps) > 0
    print(f"Preserved {len(executor.steps)} steps before TypeError.")

    controller = ExecutionController(executor.steps)
    assert controller.next() is not None
    print("TypeError validation passed.")


def test_attribute_error():
    print("\n--- TEST 4: AttributeError ---")
    code = """class Person:
    pass

p = Person()
print(p.name)"""
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except AttributeError as e:
        error_caught = e

    assert error_caught is not None, "Expected AttributeError to be raised"
    assert len(executor.steps) > 0
    print(f"Preserved {len(executor.steps)} steps before AttributeError.")

    # Verify object and heap snapshot
    last_step = executor.steps[-1]
    assert "p" in last_step.variables
    assert last_step.variables["p"] == "Object #1"
    assert "object_1" in last_step.objects_snapshot
    assert last_step.objects_snapshot["object_1"]["class_name"] == "Person"
    print("AttributeError with heap object validation passed.")


def test_syntax_error():
    print("\n--- TEST 5: SyntaxError ---")
    code = """if True
    print("hello")"""
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except SyntaxError as e:
        error_caught = e

    assert error_caught is not None, "Expected SyntaxError to be raised"
    assert len(executor.steps) == 0, "SyntaxError must produce 0 execution steps"
    print("SyntaxError cleanly raised with 0 execution steps.")


def test_empty_input():
    print("\n--- TEST 6: Empty Input ---")
    executor = Executor()
    tracer = PythonTracer(executor)
    steps = tracer.run("")
    assert len(steps) == 0, "Empty input should produce 0 steps"
    print("Empty input produces 0 steps cleanly.")


def test_invalid_input():
    print("\n--- TEST 7: Invalid Input ---")
    # Whitespace only
    executor = Executor()
    tracer = PythonTracer(executor)
    steps = tracer.run("   \n\t  ")
    assert len(steps) == 0, "Whitespace-only input should produce 0 steps"

    # Incomplete syntax
    error_caught = None
    try:
        tracer.run("def (")
    except SyntaxError as e:
        error_caught = e
    assert error_caught is not None
    assert len(executor.steps) == 0, "Invalid syntax should produce 0 steps"
    print("Invalid input validation passed.")


def test_exception_inside_function():
    print("\n--- TEST 8: Runtime Exception inside a Function ---")
    code = """def divide(a, b):
    return a / b

x = divide(10, 0)"""
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except ZeroDivisionError as e:
        error_caught = e

    assert error_caught is not None
    assert len(executor.steps) > 0

    # Verify that a step inside the function frame 'divide' was captured
    function_frame_steps = [s for s in executor.steps if s.frame_name == "divide"]
    assert len(function_frame_steps) > 0, "Steps inside function frame should be recorded"

    # Verify stack snapshot contains function frame
    has_func_in_stack = any(
        any(f["name"] == "divide" for f in s.stack_snapshot)
        for s in executor.steps
    )
    assert has_func_in_stack, "Function frame must be in stack snapshot before return/unwind"

    # Verify controller navigation
    controller = ExecutionController(executor.steps)
    step1 = controller.next()
    step2 = controller.next()
    assert step2 is not None
    prev_step = controller.previous()
    assert prev_step.step_number == step1.step_number
    print("Exception inside function validation passed.")


def test_exception_inside_object_method():
    print("\n--- TEST 9: Runtime Exception inside an Object Method ---")
    code = """class Calculator:
    def __init__(self, factor):
        self.factor = factor

    def divide(self, val):
        return val / 0

calc = Calculator(5)
calc.divide(10)"""
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except ZeroDivisionError as e:
        error_caught = e

    assert error_caught is not None
    assert len(executor.steps) > 0

    # Verify method call frame exists
    method_steps = [s for s in executor.steps if s.frame_name == "Calculator.divide"]
    assert len(method_steps) > 0, "Method frame must be captured"

    # Verify heap has Calculator object with factor=5
    factor_ref = None
    for s in executor.steps:
        if "object_1" in s.objects_snapshot:
            factor_ref = s.objects_snapshot["object_1"]["attributes"].get("factor")
            if factor_ref:
                break
    assert factor_ref is not None
    obj_key = "object_" + factor_ref.removeprefix("Object #")
    calc_step = [s for s in executor.steps if obj_key in s.objects_snapshot and s.objects_snapshot[obj_key].get("value") == 5]
    assert len(calc_step) > 0, "Heap must contain Calculator object with factor attribute"
    print("Exception inside object method validation passed.")


def test_exception_after_object_created():
    print("\n--- TEST 10: Runtime Exception after Object Creation ---")
    code = """class Person:
    def __init__(self, name):
        self.name = name

p = Person("Alice")
print("Person created")
1 / 0"""
    executor = Executor()
    tracer = PythonTracer(executor)
    error_caught = None
    try:
        tracer.run(code)
    except ZeroDivisionError as e:
        error_caught = e

    assert error_caught is not None
    assert len(executor.steps) > 0

    # Verify stdout before error was captured
    assert "Person created" in tracer.output, "Stdout before error must be preserved"

    # Verify object p exists on heap with name 'Alice'
    last_step = executor.steps[-1]
    assert "object_1" in last_step.objects_snapshot
    name_ref = last_step.objects_snapshot["object_1"]["attributes"]["name"]
    name_key = "object_" + name_ref.removeprefix("Object #")
    assert last_step.objects_snapshot[name_key]["value"] == "Alice"
    print("Exception after object creation validation passed.")


def test_stale_state_and_sequence_isolation():
    print("\n--- TEST: Stale State and Sequence Isolation ---")
    # Run 1: Valid code
    ex1 = Executor()
    tr1 = PythonTracer(ex1)
    tr1.run("a = 1; b = 2")
    assert len(ex1.steps) > 0

    # Run 2: Erroneous code - should not reuse or be corrupted by Run 1
    ex2 = Executor()
    tr2 = PythonTracer(ex2)
    try:
        tr2.run("x = 1 / 0")
    except ZeroDivisionError:
        pass

    assert len(ex2.steps) > 0
    # ex2 steps must NOT have 'a' or 'b'
    for s in ex2.steps:
        assert "a" not in s.variables and "b" not in s.variables, "Run 2 must be isolated from Run 1"

    # Run 3: Valid code again
    ex3 = Executor()
    tr3 = PythonTracer(ex3)
    tr3.run("msg = 'success'")
    assert len(ex3.steps) > 0
    assert ex3.steps[-1].variables.get("msg") == "Object #1"
    assert ex3.steps[-1].objects_snapshot["object_1"]["value"] == "success"
    assert "x" not in ex3.steps[-1].variables
    print("Sequence isolation and state purity verified.")


if __name__ == "__main__":
    test_zero_division_error()
    test_name_error()
    test_type_error()
    test_attribute_error()
    test_syntax_error()
    test_empty_input()
    test_invalid_input()
    test_exception_inside_function()
    test_exception_inside_object_method()
    test_exception_after_object_created()
    test_stale_state_and_sequence_isolation()
    print("\n========================================")
    print("ALL 10 ERROR SCENARIO TESTS PASSED (100%)")
    print("========================================")
