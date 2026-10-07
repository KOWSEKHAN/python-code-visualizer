from models.call_stack import CallStack


class ExecutionState:

    def __init__(self):

        self.frames = []

    def push_frame(self, frame):

        self.frames.append(frame)

    def pop_frame(self):

        if self.frames:

            return self.frames.pop()

        return None

    def remove_frame(self, frame):

        if frame in self.frames:

            self.frames.remove(frame)

    def current_frame(self):

        if self.frames:

            return self.frames[-1]

        return None

    def get_frames(self):

        return self.frames.copy()