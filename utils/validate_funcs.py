from re import sub, match


def validate_year(year_str: str) -> str or None:
    """
    Validates a year string according to a specific pattern.

    Parameters:
    year_str (str): The year string to validate.

    Returns:
    str or None: The validated year string if it matches the pattern, or None otherwise.
    """
    pattern = r"^(19|20)\d{2}(\s{0,1}-\s{0,1}(19|20)\d{2}\s{0,1})?$"
    return sub(r"\s+", "", year_str) if bool(match(pattern, year_str)) else None


def validate_rating(rating_str: str, min_rating: int, max_rating: int) -> str or None:
    """
    Validates a rating string according to a specific pattern and checks if it falls within a given range.

    Parameters:
    rating_str (str): The rating string to validate.
    min_rating (int): The minimum allowed rating value.
    max_rating (int): The maximum allowed rating value.

    Returns:
    str or None: The validated rating string if it matches the pattern and falls within the range, or None otherwise.
    """
    pattern = r"^\s{0,2}\d{1,2}\s{0,2}(-\s{0,2}\d{1,2}\s{0,2})?$"
    rating = rating_str.split("-") if bool(match(pattern, rating_str)) else None
    if rating:
        start = int(rating[0])
        if len(rating) == 2:
            end = int(rating[-1])
            return (
                "-".join(rating)
                if (
                    min_rating <= start < max_rating
                    and min_rating < end <= max_rating
                    and start < end
                )
                else None
            )
        return rating[0] if min_rating <= start <= max_rating else None
    return rating


def check_card(card: dict) -> bool:
    """
    Checks if a card dictionary meets certain conditions.

    Parameters:
    card (dict): The card dictionary to check.

    Returns:
    bool: True if the card meets all conditions, False otherwise.
    """
    try:
        condition = all(
            [
                card.get("ageRating"),
                card.get("description"),
                card.get("budget").get("value") > 1,
                card.get("rating").get("kp") > 1,
                card.get("poster").get("url"),
            ]
        )
    except AttributeError:
        condition = False
    return condition


def check_named_card(card: dict) -> bool:
    """
    Checks if a named card dictionary meets certain conditions.

    Parameters:
    card (dict): The named card dictionary to check.

    Returns:
    bool: True if the named card meets all conditions, False otherwise.
    """
    try:
        condition = all(
            [
                card.get("description"),
                card.get("rating").get("kp") > 1,
                card.get("poster").get("url"),
            ]
        )
    except AttributeError:
        condition = False
    return condition
