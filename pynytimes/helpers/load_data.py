from requests.models import Response


def raise_for_status(res: Response):
    if res.status_code == 400:
        raise ValueError("Error 400: Invalid input")

    if res.status_code == 401:
        raise ValueError("Error 401: Invalid API Key")

    if res.status_code == 403:
        raise RuntimeError("Error 403: You don't have access to this page")

    if res.status_code == 404:
        raise RuntimeError("Error 404: This page does not exist")

    res.raise_for_status()
