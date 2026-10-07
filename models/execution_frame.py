class ExecutionFrame:

    def __init__(self, name, frame_id=None):

        self.name = name

        self.frame_id = frame_id

        self.variables = {}

    def update(self, variables):

        self.variables = variables.copy()

    def get_variables(self):

        return self.variables.copy()