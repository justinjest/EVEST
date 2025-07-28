import time
import requests
from functools import wraps


def retry_api_call(retries=3, delay=1):
    """
    Decorator to retry an API call function if it fails.

    Args:
        retries (int): How many times to retry the request.
        delay (int): Seconds to wait between retries.

    Returns:
        The JSON response if successful, or raises an error.
    """

    def decorator(api_function):
        @wraps(api_function)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    response = api_function(*args, **kwargs)
                    if response.error is not None:
                        raise ValueError(
                            response.error
                        )  # raises HTTPError if status is 4xx or 5xx
                    return response
                except Exception as e:
                    print(f"[Attempt {attempt}] Error: {e}")
                    if attempt < retries:
                        time.sleep(delay)
                    else:
                        print(f"API failed after {retries} attempts")
                        print("Servers may be down, or other known issue")
                        print("Leaving call")
                        exit(1)

        return wrapper

    return decorator
