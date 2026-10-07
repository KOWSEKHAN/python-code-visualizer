import sys
import io

from models.object_model import ObjectModel


class PythonTracer:
    """Trace user Python code and convert runtime values into visualizer models."""

    def __init__(self, executor):

        self.executor = executor
        self.source_lines = []

        # Used to capture a line AFTER it has executed.
        self.pending_line = None
        self.pending_frame = None

        # Runtime objects known to the visualizer.
        # key   -> Python id() of the real object
        # value -> ObjectModel
        self.objects = {}

        self._next_object_id = 1

        self._ignored_class_frames = set()

        # Program output
        self.output = ""

    # ========================================================
    # TRACE FUNCTION
    # ========================================================

    def trace(self, frame, event, arg):

        # Trace only code compiled by this tracer.
        if frame.f_code.co_filename != "<user_code>":
            return self.trace

        # Python executes class bodies in temporary frames.
        # We do not want those implementation frames to appear
        # as runtime call-stack frames.
        frame_id = id(frame)

        if event == "call":

            if self.is_class_definition_call(frame):

                self._ignored_class_frames.add(frame_id)

                return self.trace

            self.register_object_from_call(frame)

            self.capture_event(
                frame,
                "call"
            )

            return self.trace

        if frame_id in self._ignored_class_frames:

            if event == "return":

                self._ignored_class_frames.discard(
                    frame_id
                )

            return self.trace

        if event == "line":

            # The previous line has now finished executing.
            if (
                self.pending_line is not None
                and self.pending_frame is not None
            ):

                self.capture_state(
                    self.pending_frame,
                    self.pending_line
                )

            self.pending_line = frame.f_lineno
            self.pending_frame = frame

        elif event == "return":

            if (
                self.pending_line is not None
                and self.pending_frame is not None
            ):

                self.capture_state(
                    self.pending_frame,
                    self.pending_line
                )

            self.pending_line = None
            self.pending_frame = None

            self.capture_event(
                frame,
                "return",
                arg
            )

        return self.trace

    # ========================================================
    # CLASS FRAME DETECTION
    # ========================================================

    def is_class_definition_call(self, frame):

        code = self.get_source_line(
            frame.f_lineno
        ).lstrip()

        return (
            code.startswith("class ")
            or code.startswith("class\t")
        )

    # ========================================================
    # OBJECT TRACKING
    # ========================================================

    def register_object_from_call(self, frame):

        """Create an ObjectModel when an instance method receives self."""

        obj = frame.f_locals.get("self")

        if obj is None:
            return

        # Only track user-defined instances
        # that have an instance dictionary.
        if not hasattr(obj, "__dict__"):
            return

        python_object_id = id(obj)

        if python_object_id not in self.objects:

            class_name = type(obj).__name__

            object_id = (
                f"object_{self._next_object_id}"
            )

            self._next_object_id += 1

            self.objects[python_object_id] = ObjectModel(
                object_id,
                class_name
            )

        self.sync_object(obj)

    def sync_object(self, obj):

        """Copy current instance attributes into ObjectModel."""

        python_object_id = id(obj)

        model = self.objects.get(
            python_object_id
        )

        if (
            model is None
            or not hasattr(obj, "__dict__")
        ):
            return

        for name, value in obj.__dict__.items():

            model.set_attribute(
                name,
                self.format_value(value)
            )

    def sync_all_objects(self):

        """Refresh all tracked objects after a traced line executes."""

        for python_object_id, model in list(
            self.objects.items()
        ):

            obj = self.find_runtime_object(
                python_object_id
            )

            if obj is not None:

                self.sync_object(obj)

    def find_runtime_object(
        self,
        python_object_id
    ):

        """Find a tracked object through active runtime frames."""

        frame = self.pending_frame

        if frame is not None:

            found = self.find_in_frame_chain(
                frame,
                python_object_id
            )

            if found is not None:
                return found

        return None

    def find_in_frame_chain(
        self,
        frame,
        python_object_id
    ):

        current = frame

        while current is not None:

            for value in current.f_locals.values():

                if id(value) == python_object_id:

                    return value

            for value in current.f_globals.values():

                if id(value) == python_object_id:

                    return value

            current = current.f_back

        return None

    # ========================================================
    # VALUE FORMATTING
    # ========================================================

    def format_value(self, value):

        if value is None:

            return "None"

        if isinstance(value, type):

            return f"Class {value.__name__}"

        if callable(value):

            module = getattr(
                value,
                "__module__",
                None
            )

            qualname = getattr(
                value,
                "__qualname__",
                None
            )

            if qualname:

                return (
                    f"{module + '.' if module else ''}"
                    f"{qualname}()"
                )

            return "<callable>"

        python_object_id = id(value)

        if python_object_id in self.objects:

            object_id = (
                self.objects[
                    python_object_id
                ].object_id
            )

            display_id = (
                object_id.removeprefix(
                    "object_"
                )
            )

            return f"Object #{display_id}"

        if isinstance(
            value,
            (
                str,
                int,
                float,
                bool,
                complex
            )
        ):

            class_name = type(value).__name__

            object_id = f"object_{self._next_object_id}"

            self._next_object_id += 1

            model = ObjectModel(
                object_id,
                class_name,
                value=value
            )

            self.objects[python_object_id] = model

            display_id = object_id.removeprefix("object_")

            return f"Object #{display_id}"

        if isinstance(
            value,
            (list, tuple, set)
        ):

            class_name = type(value).__name__

            object_id = f"object_{self._next_object_id}"

            self._next_object_id += 1

            elements = [
                self.format_value(item)
                for item in value
            ]

            model = ObjectModel(
                object_id,
                class_name,
                elements=elements
            )

            self.objects[python_object_id] = model

            display_id = object_id.removeprefix("object_")

            return f"Object #{display_id}"

        if isinstance(value, dict):

            class_name = "dict"

            object_id = f"object_{self._next_object_id}"

            self._next_object_id += 1

            elements = {
                str(self.format_value(k)):
                self.format_value(v)
                for k, v in value.items()
            }

            model = ObjectModel(
                object_id,
                class_name,
                elements=elements
            )

            self.objects[python_object_id] = model

            display_id = object_id.removeprefix("object_")

            return f"Object #{display_id}"

        if hasattr(value, "__dict__"):

            class_name = type(value).__name__

            object_id = f"object_{self._next_object_id}"

            self._next_object_id += 1

            model = ObjectModel(
                object_id,
                class_name
            )

            self.objects[python_object_id] = model

            self.sync_object(value)

            display_id = object_id.removeprefix("object_")

            return f"Object #{display_id}"

        return repr(value)

    def get_formatted_variables(
        self,
        frame
    ):

        self.sync_all_objects()

        return {

            name: self.format_value(value)

            for name, value
            in frame.f_locals.items()

            if not name.startswith("__")
        }

    def get_object_snapshot(self):

        return {

            model.object_id:
            model.to_dict()

            for model in self.objects.values()
        }

    # ========================================================
    # CAPTURE NORMAL LINE EXECUTION
    # ========================================================

    def capture_state(
        self,
        frame,
        line_number
    ):

        variables = self.get_formatted_variables(
            frame
        )

        code = self.get_source_line(
            line_number
        )

        self.executor.create_step(

            event_type="line",

            line_number=line_number,

            code=code,

            frame_name=frame.f_code.co_qualname,

            variables=variables,

            runtime_frame=frame,

            objects=self.get_object_snapshot()
        )

    # ========================================================
    # CAPTURE CALL / RETURN
    # ========================================================

    def capture_event(
        self,
        frame,
        event_type,
        return_value=None
    ):

        if event_type == "call":

            self.register_object_from_call(
                frame
            )

        if event_type == "return":

            obj = frame.f_locals.get(
                "self"
            )

            if obj is not None:

                self.sync_object(obj)

        line_number = frame.f_lineno

        code = self.get_source_line(
            line_number
        )

        variables = self.get_formatted_variables(
            frame
        )

        self.executor.create_step(

            event_type=event_type,

            line_number=line_number,

            code=code,

            frame_name=frame.f_code.co_qualname,

            variables=variables,

            runtime_frame=frame,

            objects=self.get_object_snapshot()
        )

    # ========================================================
    # GET SOURCE LINE
    # ========================================================

    def get_source_line(
        self,
        line_number
    ):

        if (
            1 <= line_number
            <= len(self.source_lines)
        ):

            return self.source_lines[
                line_number - 1
            ]

        return ""

    # ========================================================
    # RUN USER PROGRAM
    # ========================================================

    def run(self, code):

        if not code or not code.strip():
            self.source_lines = []
            self.output = ""
            return []

        self.source_lines = code.splitlines()

        self.pending_line = None
        self.pending_frame = None

        self.objects = {}

        self._next_object_id = 1

        self._ignored_class_frames = set()

        self.output = ""

        compiled_code = compile(
            code,
            "<user_code>",
            "exec"
        )

        # ----------------------------------------------------
        # Capture print() output
        # ----------------------------------------------------

        original_stdout = sys.stdout

        captured_output = io.StringIO()

        sys.stdout = captured_output

        sys.settrace(self.trace)

        try:

            exec(
                compiled_code,
                {
                    "__name__": "__main__"
                }
            )

        finally:

            sys.settrace(None)

            sys.stdout = original_stdout

            self.output = captured_output.getvalue()

            self.pending_line = None
            self.pending_frame = None

        return self.executor.steps