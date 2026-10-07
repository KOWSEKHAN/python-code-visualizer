from models.execution_frame import ExecutionFrame
from models.execution_state import ExecutionState
from models.execution_step import ExecutionStep


class Executor:

    def __init__(self):

        self.state = ExecutionState()

        self.global_frame = ExecutionFrame(
            "Global Frame",
            frame_id="global"
        )

        self.state.push_frame(
            self.global_frame
        )

        self.steps = []

    # ========================================================
    # FIND FRAME USING PYTHON FRAME ID
    # ========================================================

    def find_frame(self, frame_id):

        for frame in reversed(
            self.state.get_frames()
        ):

            if frame.frame_id == frame_id:

                return frame

        return None

    # ========================================================
    # CREATE EXECUTION STEP
    # ========================================================

    def create_step(
        self,
        event_type,
        line_number,
        code,
        frame_name,
        variables,
        runtime_frame=None,
        objects=None
    ):

        # ====================================================
        # UNIQUE FRAME ID
        # ====================================================

        if frame_name == "<module>":

            frame_id = "global"

        elif runtime_frame is not None:

            frame_id = id(runtime_frame)

        else:

            frame_id = frame_name

        # ====================================================
        # FUNCTION CALL
        # ====================================================

        if event_type == "call":

            if frame_name != "<module>":

                new_frame = ExecutionFrame(
                    frame_name,
                    frame_id
                )

                new_frame.update(
                    variables
                )

                self.state.push_frame(
                    new_frame
                )

        # ====================================================
        # LINE
        # ====================================================

        elif event_type == "line":

            target_frame = self.find_frame(
                frame_id
            )

            if target_frame:

                target_frame.update(
                    variables
                )

        # ====================================================
        # RETURN
        # ====================================================

        elif event_type == "return":

            target_frame = self.find_frame(
                frame_id
            )

            if target_frame:

                target_frame.update(
                    variables
                )

        # ====================================================
        # CREATE COMPLETE STACK SNAPSHOT
        # ====================================================

        stack_snapshot = []

        for frame in self.state.get_frames():

            stack_snapshot.append({

                "frame_id":
                    frame.frame_id,

                "name":
                    frame.name,

                "variables":
                    frame.get_variables()

            })

        # ====================================================
        # CREATE EXECUTION STEP
        # ====================================================

        step_number = (
            len(self.steps) + 1
        )

        step = ExecutionStep(

            step_number=step_number,

            event_type=event_type,

            line_number=line_number,

            code=code,

            frame_name=frame_name,

            variables=variables,

            stack_snapshot=stack_snapshot,

            objects_snapshot=objects or {}

        )

        self.steps.append(step)

        # ====================================================
        # POP FUNCTION AFTER SNAPSHOT
        # ====================================================

        if event_type == "return":

            if frame_name != "<module>":

                target_frame = self.find_frame(
                    frame_id
                )

                if target_frame:

                    self.state.remove_frame(
                        target_frame
                    )

        return step