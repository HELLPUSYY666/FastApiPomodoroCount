class SyncContManager:
    def __init__(self):
        self.a = 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


with SyncContManager() as manager:
    manager.a
