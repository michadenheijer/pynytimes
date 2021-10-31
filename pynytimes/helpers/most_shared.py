def most_shared_check_method(method: str):
    method_options = ["email", "facebook"]
    # Raise error if method isn't a str
    if not isinstance(method, str):
        raise TypeError("Method needs to be str")

        # Raise error if days, or method aren't in options
    if method not in method_options:
        raise ValueError("Shared option does not exist")


def most_shared_check_days(days: int):
    # Check if options are valid
    days_options = [1, 7, 30]

    # Raise error if days isn't an int
    if not isinstance(days, int):
        raise TypeError("Days needs to be int")

    if days not in days_options:
        raise ValueError("You can only select 1, 7 or 30 days")


def most_shared_get_url():
    pass
