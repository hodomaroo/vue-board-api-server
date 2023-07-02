from requests import Session

session = Session()
session.headers.update({"accept": "application/json"})
