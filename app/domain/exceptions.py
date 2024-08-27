from starlette import status


class HTTPException(Exception):
    def __init__(self, title: str, message: str, status_code: int):
        self.title = title
        self.message = message
        self.status_code = status_code


class StudentNotFound(HTTPException):
    def __init__(self, title="Not Found", message="Student not Found", status_code=status.HTTP_404_NOT_FOUND):
        super().__init__(title, message, status_code)