import sys
import re

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from core.executor import Executor
from core.tracer import PythonTracer
from core.execution_controller import ExecutionController


def run_code(code):
    executor = Executor()
    tracer = PythonTracer(executor)
    tracer.run(code)
    return executor.steps


# ============================================================
# 1. BASIC OBJECT CREATION
# ============================================================

# ============================================================
# MANDATORY TESTS A - F
# ============================================================

def test_a_addition():
    code = """a = 10
b = 20
c = a + b"""
    steps = run_code(code)
    last_step = steps[-1]
    assert last_step.variables["a"] == "Object #1"
    assert last_step.variables["b"] == "Object #2"
    assert last_step.variables["c"] == "Object #3"
    assert last_step.objects_snapshot["object_1"]["value"] == 10
    assert last_step.objects_snapshot["object_2"]["value"] == 20
    assert last_step.objects_snapshot["object_3"]["value"] == 30
    print("TEST A (Addition): PASSED")


def test_b_aliasing():
    code = """a = 10
b = a"""
    steps = run_code(code)
    last_step = steps[-1]
    assert last_step.variables["a"] == "Object #1"
    assert last_step.variables["b"] == "Object #1"
    assert len(last_step.objects_snapshot) == 1
    assert last_step.objects_snapshot["object_1"]["value"] == 10
    print("TEST B (Aliasing): PASSED")


def test_c_runtime_identity():
    code = """a = 10
b = 10"""
    steps = run_code(code)
    last_step = steps[-1]
    # CPython small integers share identity
    assert last_step.variables["a"] == "Object #1"
    assert last_step.variables["b"] == "Object #1"
    assert len(last_step.objects_snapshot) == 1
    print("TEST C (Runtime Identity): PASSED")


def test_d_reassignment_historical_isolation():
    code = """a = 10
a = 20"""
    steps = run_code(code)
    step1 = [s for s in steps if s.variables.get("a") == "Object #1"][0]
    step2 = [s for s in steps if s.variables.get("a") == "Object #2"][0]

    assert step1.variables["a"] == "Object #1"
    assert step1.objects_snapshot["object_1"]["value"] == 10

    assert step2.variables["a"] == "Object #2"
    assert step2.objects_snapshot["object_2"]["value"] == 20
    print("TEST D (Historical Snapshot Isolation): PASSED")


def test_e_user_defined_object_attributes():
    code = """class Person:
    def __init__(self, name):
        self.name = name

p = Person("Kowshik")"""
    steps = run_code(code)
    last_step = steps[-1]
    assert last_step.variables["p"] == "Object #1"
    p_obj = last_step.objects_snapshot["object_1"]
    assert p_obj["class_name"] == "Person"
    name_ref = p_obj["attributes"]["name"]
    name_key = "object_" + name_ref.removeprefix("Object #")
    name_obj = last_step.objects_snapshot[name_key]
    assert name_obj["class_name"] == "str"
    assert name_obj["value"] == "Kowshik"
    print("TEST E (User Defined Object Attributes): PASSED")


def test_f_function_arguments():
    code = """x = 10

def add(a):
    return a + 20

result = add(x)"""
    steps = run_code(code)
    func_step = [s for s in steps if s.frame_name == "add" and "a" in s.variables][0]
    assert func_step.variables["a"] == "Object #1", "Function parameter 'a' must refer to same Object #1 as 'x'"
    assert func_step.objects_snapshot["object_1"]["value"] == 10
    print("TEST F (Function Arguments): PASSED")


# ============================================================
# 1. BASIC OBJECT CREATION
# ============================================================

def test_basic_object_creation():
    code = """class Person:
    def __init__(self, name):
        self.name = name

p = Person("Kowshik")"""
    steps = run_code(code)
    assert len(steps) > 0

    last_step = steps[-1]
    assert "p" in last_step.variables, "p must be in variables"
    assert last_step.variables["p"] == "Object #1", "p must reference Object #1"
    assert "object_1" in last_step.objects_snapshot, "object_1 must exist in heap snapshot"

    obj = last_step.objects_snapshot["object_1"]
    assert obj["class_name"] == "Person", "Class name must be Person"
    name_ref = obj["attributes"].get("name")
    assert name_ref is not None
    name_key = "object_" + name_ref.removeprefix("Object #")
    assert last_step.objects_snapshot[name_key]["value"] == "Kowshik"
    print("Test 1 (Basic Object Creation): PASSED")


# ============================================================
# 2. MULTIPLE OBJECTS
# ============================================================

def test_multiple_objects():
    code = """class Person:
    def __init__(self, name):
        self.name = name

p1 = Person("Kowshik")
p2 = Person("Rahul")"""
    steps = run_code(code)
    last_step = steps[-1]

    assert last_step.variables.get("p1") == "Object #1"
    assert last_step.variables.get("p2") == "Object #3" # Object #2 is "Kowshik"
    assert "object_1" in last_step.objects_snapshot
    assert "object_3" in last_step.objects_snapshot

    obj1 = last_step.objects_snapshot["object_1"]
    obj2 = last_step.objects_snapshot["object_3"]
    ref1 = obj1["attributes"]["name"]
    ref2 = obj2["attributes"]["name"]
    key1 = "object_" + ref1.removeprefix("Object #")
    key2 = "object_" + ref2.removeprefix("Object #")
    assert last_step.objects_snapshot[key1]["value"] == "Kowshik"
    assert last_step.objects_snapshot[key2]["value"] == "Rahul"
    assert obj1["object_id"] != obj2["object_id"]
    print("Test 2 (Multiple Objects): PASSED")


# ============================================================
# 3. ALIASING
# ============================================================

def test_aliasing():
    code = """class Person:
    def __init__(self, name):
        self.name = name

p = Person("Kowshik")
q = p"""
    steps = run_code(code)
    last_step = steps[-1]

    assert last_step.variables.get("p") == "Object #1"
    assert last_step.variables.get("q") == "Object #1"
    assert "object_1" in last_step.objects_snapshot
    print("Test 3 (Aliasing): PASSED")


# ============================================================
# 4. ATTRIBUTE MUTATION
# ============================================================

def test_attribute_mutation():
    code = """class Person:
    def __init__(self, name):
        self.name = name

p = Person("Kowshik")
p.name = "Rahul" """
    steps = run_code(code)

    # Find step where name ref points to Kowshik object
    step_kowshik = None
    for s in steps:
        if "object_1" in s.objects_snapshot:
            ref = s.objects_snapshot["object_1"].get("attributes", {}).get("name")
            if ref:
                k = "object_" + ref.removeprefix("Object #")
                if s.objects_snapshot.get(k, {}).get("value") == "Kowshik":
                    step_kowshik = s
                    break
    assert step_kowshik is not None, "Snapshot with name='Kowshik' must exist"

    # Find later step where name ref points to Rahul object
    step_rahul = None
    for s in steps:
        if "object_1" in s.objects_snapshot:
            ref = s.objects_snapshot["object_1"].get("attributes", {}).get("name")
            if ref:
                k = "object_" + ref.removeprefix("Object #")
                if s.objects_snapshot.get(k, {}).get("value") == "Rahul":
                    step_rahul = s
                    break
    assert step_rahul is not None, "Snapshot with name='Rahul' must exist"

    # Verify deep-copy isolation
    ref_k = step_kowshik.objects_snapshot["object_1"]["attributes"]["name"]
    key_k = "object_" + ref_k.removeprefix("Object #")
    assert step_kowshik.objects_snapshot[key_k]["value"] == "Kowshik"

    ref_r = step_rahul.objects_snapshot["object_1"]["attributes"]["name"]
    key_r = "object_" + ref_r.removeprefix("Object #")
    assert step_rahul.objects_snapshot[key_r]["value"] == "Rahul"

    assert steps[-1].variables.get("p") == "Object #1"
    print("Test 4 (Attribute Mutation): PASSED")


# ============================================================
# 5. MULTIPLE ATTRIBUTES
# ============================================================

def test_multiple_attributes():
    code = """class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

student = Student("Kowshik", 23)"""
    steps = run_code(code)
    last_step = steps[-1]

    assert last_step.variables.get("student") == "Object #1"
    obj = last_step.objects_snapshot["object_1"]
    assert obj["class_name"] == "Student"
    name_ref = obj["attributes"].get("name")
    age_ref = obj["attributes"].get("age")
    name_key = "object_" + name_ref.removeprefix("Object #")
    age_key = "object_" + age_ref.removeprefix("Object #")
    assert last_step.objects_snapshot[name_key]["value"] == "Kowshik"
    assert last_step.objects_snapshot[age_key]["value"] == 23
    print("Test 5 (Multiple Attributes): PASSED")


# ============================================================
# 6. OBJECT INSIDE FUNCTION
# ============================================================

def test_object_inside_function():
    code = """class Person:
    def __init__(self, name):
        self.name = name

def create_person():
    p = Person("Kowshik")
    return p

person = create_person()"""
    steps = run_code(code)

    inside_func_step = None
    for s in steps:
        if s.frame_name == "create_person" and s.variables.get("p") == "Object #1":
            inside_func_step = s
            break
    assert inside_func_step is not None, "p -> Object #1 must be present inside create_person"

    last_step = steps[-1]
    assert last_step.variables.get("person") == "Object #1"
    assert "object_1" in last_step.objects_snapshot
    name_ref = last_step.objects_snapshot["object_1"]["attributes"]["name"]
    name_key = "object_" + name_ref.removeprefix("Object #")
    assert last_step.objects_snapshot[name_key]["value"] == "Kowshik"

    stack_frame_names = [f["name"] for f in last_step.stack_snapshot]
    assert "create_person" not in stack_frame_names
    print("Test 6 (Object Inside Function): PASSED")


# ============================================================
# 7. METHOD SELF REFERENCE
# ============================================================

def test_method_self_reference():
    code = """class Person:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(self.name)

p = Person("Kowshik")
p.display()"""
    steps = run_code(code)

    display_steps = [s for s in steps if s.frame_name == "Person.display"]
    assert len(display_steps) > 0, "Steps in Person.display must be captured"
    for s in display_steps:
        assert s.variables.get("self") == "Object #1", "self must reference Object #1"
    print("Test 7 (Method Self Reference): PASSED")


# ============================================================
# 8. INHERITANCE
# ============================================================

def test_inheritance():
    code = """class Person:
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

student = Student("Kowshik", 23)"""
    steps = run_code(code)
    last_step = steps[-1]

    assert last_step.variables.get("student") == "Object #1"
    obj = last_step.objects_snapshot["object_1"]
    assert obj["class_name"] == "Student"
    name_ref = obj["attributes"].get("name")
    age_ref = obj["attributes"].get("age")
    name_key = "object_" + name_ref.removeprefix("Object #")
    age_key = "object_" + age_ref.removeprefix("Object #")
    assert last_step.objects_snapshot[name_key]["value"] == "Kowshik"
    assert last_step.objects_snapshot[age_key]["value"] == 23

    for s in steps:
        if s.frame_name in ("Person.__init__", "Student.__init__"):
            assert s.variables.get("self") == "Object #1"
    print("Test 8 (Inheritance): PASSED")


# ============================================================
# 9. OBJECT PASSED INTO FUNCTION
# ============================================================

def test_object_passed_into_function():
    code = """class Person:
    def __init__(self, name):
        self.name = name

def rename(person):
    person.name = "Rahul"

p = Person("Kowshik")
rename(p)"""
    steps = run_code(code)

    rename_steps = [s for s in steps if s.frame_name == "rename"]
    assert len(rename_steps) > 0
    assert rename_steps[0].variables.get("person") == "Object #1"

    last_step = steps[-1]
    assert last_step.variables.get("p") == "Object #1"
    name_ref = last_step.objects_snapshot["object_1"]["attributes"]["name"]
    name_key = "object_" + name_ref.removeprefix("Object #")
    assert last_step.objects_snapshot[name_key]["value"] == "Rahul"
    print("Test 9 (Object Passed Into Function): PASSED")


# ============================================================
# 10. SNAPSHOT ISOLATION
# ============================================================

def test_snapshot_isolation():
    code = """class Person:
    def __init__(self, name):
        self.name = name

p = Person("A")
p.name = "B"
p.name = "C" """
    steps = run_code(code)

    names_recorded = []
    for s in steps:
        if "object_1" in s.objects_snapshot:
            ref = s.objects_snapshot["object_1"]["attributes"].get("name")
            if ref:
                k = "object_" + ref.removeprefix("Object #")
                val = s.objects_snapshot.get(k, {}).get("value")
                if val and (not names_recorded or names_recorded[-1] != val):
                    names_recorded.append(val)

    assert "A" in names_recorded, "Snapshot with name='A' must exist"
    assert "B" in names_recorded, "Snapshot with name='B' must exist"
    assert "C" in names_recorded, "Snapshot with name='C' must exist"
    print("Test 10 (Snapshot Isolation): PASSED")


# ============================================================
# 11. REFERENCE DELETION BEHAVIOR
# ============================================================

def test_reference_deletion():
    code = """class Person:
    def __init__(self, name):
        self.name = name

p = Person("Kowshik")
q = p
del p"""
    steps = run_code(code)
    last_step = steps[-1]

    assert "p" not in last_step.variables, "p must not exist after del p"
    assert last_step.variables.get("q") == "Object #1", "q must still reference Object #1"
    assert "object_1" in last_step.objects_snapshot, "object_1 must remain on heap"
    name_ref = last_step.objects_snapshot["object_1"]["attributes"]["name"]
    name_key = "object_" + name_ref.removeprefix("Object #")
    assert last_step.objects_snapshot[name_key]["value"] == "Kowshik"
    print("Test 11 (Reference Deletion): PASSED")


# ============================================================
# 12. NO RAW CPYTHON MEMORY ADDRESSES
# ============================================================

def test_no_raw_cpython_memory_addresses():
    test_programs = [
        "x = 10\ny = 'hello'",
        "class Person: pass\np = Person()",
        "class Person:\n    def __init__(self, n): self.n = n\np = Person('Kowshik')",
        "class A:\n    def __init__(self): self.val = 1\na = A()\nb = a",
        "def f(x): return x\ny = f(42)",
    ]

    addr_pattern = re.compile(r"0x[0-9a-fA-F]{6,}")

    for prog in test_programs:
        steps = run_code(prog)
        for s in steps:
            for v_name, v_val in s.variables.items():
                val_str = str(v_val)
                assert not addr_pattern.search(val_str), f"Found raw address in variable {v_name}={val_str}"
                assert "object at 0x" not in val_str

            for o_id, o_data in s.objects_snapshot.items():
                for a_name, a_val in o_data.get("attributes", {}).items():
                    val_str = str(a_val)
                    assert not addr_pattern.search(val_str), f"Found raw address in attribute {a_name}={val_str}"
                    assert "object at 0x" not in val_str

            for frame in s.stack_snapshot:
                for v_name, v_val in frame.get("variables", {}).items():
                    val_str = str(v_val)
                    assert not addr_pattern.search(val_str), f"Found raw address in stack frame variable {v_name}={val_str}"
                    assert "object at 0x" not in val_str

    print("Test 12 (No Raw CPython Memory Addresses): PASSED")


if __name__ == "__main__":
    test_a_addition()
    test_b_aliasing()
    test_c_runtime_identity()
    test_d_reassignment_historical_isolation()
    test_e_user_defined_object_attributes()
    test_f_function_arguments()
    print("------------------------------------------------------------")
    test_basic_object_creation()
    test_multiple_objects()
    test_aliasing()
    test_attribute_mutation()
    test_multiple_attributes()
    test_object_inside_function()
    test_method_self_reference()
    test_inheritance()
    test_object_passed_into_function()
    test_snapshot_isolation()
    test_reference_deletion()
    test_no_raw_cpython_memory_addresses()
    print("\n============================================================")
    print("ALL MANDATORY (A-F) AND 12 REFERENCE MODEL TESTS PASSED (100%)")
    print("============================================================")
