class FrameModel:
    def __init__(self, name, variables=None):
        self.name = name
        self.variables = variables or {}

    def add_variable(self, name, value):
        self.variables[name] = value

    def __repr__(self):
        return f"FrameModel(name={self.name}, variables={self.variables})"