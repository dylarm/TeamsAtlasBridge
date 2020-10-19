from pathlib import Path


def assignment_name(file: Path) -> str:
    """
    Get the name of an assignment from a Teams Assignment CSV

    :param file: Path
    :return: str
    """
    with open(file, "r") as f:
        line = f.readline()
    return line.split(",")[3].strip('"')


def class_period(file: Path) -> int:
    """
    Get the period of an assignment file
    
    :param file: Path
    :return: int
    """
    loc = file.name.find("P0")
    return int(file.name[loc + 2])


def assignment_file_name(assignment: str, period: int) -> str:
    """
    Generate the name of the assignment file to upload to ATLAS
    
    :param assignment: str
    :param period: int
    :return: str
    """
    return f"{period} - {assignment}"
