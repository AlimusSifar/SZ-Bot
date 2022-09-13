import re


def role_is_valid(role_name: str) -> bool:
    """
    Verifies the valid BRACU Course Codes
    """

    VALID_COURSE_NAMES: tuple[str] = (
        "ANT",
        "BUS",
        "CHE",
        "CSE",
        "ECO",
        "ENG",
        "ENV",
        "GEO",
        "MAT",
        "PHY",
        "POL",
        "SOC",
        "STA",
    )

    valid_course_codes = "|".join(VALID_COURSE_NAMES)
    pattern = f"({valid_course_codes})" + r"[0-9]{3}"

    if re.fullmatch(pattern, role_name):
        return True

    return False
