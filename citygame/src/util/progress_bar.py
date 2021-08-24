class ProgressBar:
    def __init__(self):
        self.current_task = ""
        self.progress = 0.0

    def set_progress(self, progress: float, current_task: str):
        self.progress = progress
        self.current_task = current_task
