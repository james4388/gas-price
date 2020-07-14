"""Headers related handling
"""

RATELIMIT_HEADERS = {
    'x-ratelimit-limit',
    'x-ratelimit-remaining',
    'x-ratelimit-reset',
    'retry-after',
    'ratelimit-limit',
    'ratelimit-remaining',
    'ratelimit-reset',
    'x-rate-limit-limit',
    'x-rate-limit-remaining',
    'x-rate-limit-reset',
}


def allow_headers(headers: dict, allow_set: set) -> dict:
    """Only allow headers key from allow_set
    """
    clean_header = {}
    for key, value in headers.items():
        if key.lower() in allow_set:
            clean_header[key] = value

    return clean_header


def allow_ratelimit_headers(headers: dict):
    return allow_headers(headers, RATELIMIT_HEADERS)
