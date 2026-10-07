import copy


class ExecutionStep:

    def __init__(
        self,
        step_number,
        event_type,
        line_number,
        code,
        frame_name,
        variables,
        stack_snapshot,
        objects_snapshot=None
    ):
        self.step_number = step_number
        self.event_type = event_type
        self.line_number = line_number
        self.code = code
        self.frame_name = frame_name
        self.variables = copy.deepcopy(variables)
        self.stack_snapshot = copy.deepcopy(stack_snapshot)
        self.objects_snapshot = copy.deepcopy(objects_snapshot or {})
