class GamersServiceException(Exception):
    def __init__(self, detail: str=''):
        self.detail = detail


class BadRequest(GamersServiceException):
    def __init__(self, detail: str):
        super().__init__(detail)
