class ExecutionController:

    def __init__(self, steps):

        self.steps = steps

        # 0 means before the first execution step
        self.current_step = 0

    def next(self):

        if self.current_step < len(self.steps):
            self.current_step += 1

        return self.get_current_step()

    def previous(self):

        if self.current_step > 0:
            self.current_step -= 1

        return self.get_current_step()

    def reset(self):

        self.current_step = 0

        return self.get_current_step()

    def run(self):

        self.current_step = len(self.steps)

        return self.get_current_step()

    def get_current_step(self):

        if self.current_step == 0:
            return None

        return self.steps[self.current_step - 1]