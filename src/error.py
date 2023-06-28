class CustomDBError(Exception):
    err_type: Exception
    detail: str
