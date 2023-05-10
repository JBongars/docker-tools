def cache_no_args(f: callable) -> callable:
    result = ""

    def wrapper():
        nonlocal result
        if result == "":
            result = f()
        return result

    return wrapper