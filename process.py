from pathlib import Path

import pandas as pd

import constants as CONSTANT


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


def generate_output(assignment_file: Path, student_list: Path, output: Path) -> None:
    """
    Match email addresses between the files and write out the result

    :param assignment_file: Path
    :param student_list: Path
    :param output: Path
    :return: None
    """
    students = pd.read_excel(student_list, **CONSTANT.STUDENT_LOGINS)
    teams = pd.read_csv(assignment_file, **CONSTANT.TEAMS_CSV)
    matched_file = teams.merge(
        students,
        how="left",
        left_on=teams.columns[0],
        right_on=CONSTANT.STUDENT_LOGINS["usecols"][1],
    )
    matched_file.to_excel(output)
