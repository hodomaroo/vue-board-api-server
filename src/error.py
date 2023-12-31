class CustomDBError(Exception):
    err_type: Exception
    detail: str

    def __init__(self, err_type: Exception, detail: str, tag: str = "") -> None:
        self.err_type = err_type
        self.detail = detail
        self.tag = tag
