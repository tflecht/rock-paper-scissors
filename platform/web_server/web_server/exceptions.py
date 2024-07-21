
class CompatibilityError(Exception):
    def __init__(self, detail):
        self.detail = detail

    def __str__(self) -> str:
        return self.detail
