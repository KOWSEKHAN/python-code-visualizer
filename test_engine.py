import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from core.executor import Executor
from core.tracer import PythonTracer
from core.execution_controller import ExecutionController


# ============================================================
# PROGRAM TO TRACE
# ============================================================

code = code = """
class Person:

    def __init__(self, name):
        self.name = name

    def display(self):
        print(self.name)


class Student(Person):

    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

    def show_age(self):
        print(self.age)


student1 = Student("Kowshik", 23)
student2 = Student("Livetha", 20)

student1.display()
student2.display()

student1.show_age()
student2.show_age()
"""


# ============================================================
# CREATE EXECUTION ENGINE
# ============================================================

executor = Executor()

tracer = PythonTracer(executor)


# ============================================================
# EXECUTE / TRACE PROGRAM
# ============================================================

tracer.run(code)


# ============================================================
# CREATE CONTROLLER
# ============================================================

controller = ExecutionController(
    executor.steps
)


# ============================================================
# PRINT COMPLETE EXECUTION HISTORY
# ============================================================

print("\n========== COMPLETE EXECUTION HISTORY ==========")

for step in executor.steps:

    print("\n--------------------")

    print("STEP:", step.step_number)

    print("EVENT:", step.event_type)

    print("FRAME:", step.frame_name)

    print("LINE:", step.line_number)

    print("CODE:", step.code)

    # ========================================================
    # CURRENT FRAME VARIABLES
    # ========================================================

    print("VARIABLES:")

    for name, value in step.variables.items():

        print(
            f"    {name} → {value}"
        )

    # ========================================================
    # CALL STACK
    # ========================================================

    print("\nCALL STACK:")

    for frame in step.stack_snapshot:

        print(
            f"    [{frame['name']}]"
        )

        for name, value in frame["variables"].items():

            print(
                f"        {name} → {value}"
            )

    # ========================================================
    # OBJECTS
    # ========================================================

    print("\nOBJECTS:")

    if step.objects_snapshot:

        for object_id, obj in step.objects_snapshot.items():

            print(
                f"    {object_id} "
                f"({obj['class_name']})"
            )

            if obj["attributes"]:

                for name, value in obj["attributes"].items():

                    print(
                        f"        {name} → {value}"
                    )

            else:

                print(
                    "        No attributes"
                )

    else:

        print(
            "    No objects"
        )


# ============================================================
# TOTAL STEPS
# ============================================================

print("\n========== TOTAL STEPS ==========")

print(
    len(executor.steps)
)


# ============================================================
# CONTROLLER TEST
# ============================================================

print("\n========== CONTROLLER TEST ==========")


# ============================================================
# NEXT
# ============================================================

print("\nNEXT")

step = controller.next()

if step:

    print(
        "STEP:",
        step.step_number
    )

    print(
        "EVENT:",
        step.event_type
    )

    print(
        "FRAME:",
        step.frame_name
    )

    print(
        "CODE:",
        step.code
    )

else:

    print("None")


# ============================================================
# NEXT AGAIN
# ============================================================

print("\nNEXT")

step = controller.next()

if step:

    print(
        "STEP:",
        step.step_number
    )

    print(
        "EVENT:",
        step.event_type
    )

    print(
        "FRAME:",
        step.frame_name
    )

    print(
        "CODE:",
        step.code
    )

else:

    print("None")


# ============================================================
# PREVIOUS
# ============================================================

print("\nPREVIOUS")

step = controller.previous()

if step:

    print(
        "STEP:",
        step.step_number
    )

    print(
        "EVENT:",
        step.event_type
    )

    print(
        "FRAME:",
        step.frame_name
    )

    print(
        "CODE:",
        step.code
    )

else:

    print("None")


# ============================================================
# RUN
# ============================================================

print("\nRUN")

step = controller.run()

if step:

    print(
        "STEP:",
        step.step_number
    )

    print(
        "EVENT:",
        step.event_type
    )

    print(
        "FRAME:",
        step.frame_name
    )

    print(
        "CODE:",
        step.code
    )

else:

    print("None")


# ============================================================
# RESET
# ============================================================

print("\nRESET")

print(
    controller.reset()
)