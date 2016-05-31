import six


def extract_headers(response):
    """Extracts headers from httplib response or http.client response based on used version off Python."""
    return response.headers if six.PY2 else response.headers._headers
