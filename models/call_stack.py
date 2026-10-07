class CallStack:

    def __init__(self):

        self.frames = []

    def push(self, frame):

        self.frames.append(frame)

    def pop(self):

        if self.frames:
            return self.frames.pop()

        return None

    def current(self):

        if self.frames:
            return self.frames[-1]

        return None

    def get_frames(self):

        return self.frames.copy()

    def depth(self):

        return len(self.frames)