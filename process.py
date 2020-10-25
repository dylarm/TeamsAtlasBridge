import logging
from pathlib import Path

import pandas as pd

import constants as CONSTANT

logger = logging.getLogger(__name__)


def assignment_name(file: Path) -> str:
    """
    Get the name of an assignment from a Teams Assignment CSV

    :param file: Path
    :return: str
    """
    # TODO: get multiple assignments, if present
    logger.debug("Processing assignment name...")
    with open(file, "r") as f:
        line = f.readline()
    name = line.split(",")[3].strip('"')
    logger.info(f"Assignment name: {name}")
    return name


def class_period(file: Path) -> int:
    """
    Get the period of an assignment file
    
    :param file: Path
    :return: int
    """
    logger.debug("Extracting class period...")
    loc = file.name.find("P0")
    period = int(file.name[loc + 2])
    logger.info(f"Class period: {period}")
    return period


def assignment_file_name(assignment: str, period: int) -> str:
    """
    Generate the name of the assignment file to upload to ATLAS
    
    :param assignment: str
    :param period: int
    :return: str
    """
    logger.debug("Creating assignment file name for export...")
    name = f"{period} - {assignment}"
    logger.info(f"Output file name: {name}")
    return name


def generate_output(assignment_file: Path, student_list: Path, output: Path) -> None:
    """
    Match email addresses between the files and write out the result

    :param assignment_file: Path
    :param student_list: Path
    :param output: Path
    :return: None
    """
    logger.info("Generating matched file...")
    # TODO: If there are multiple files to export, how do we avoid loading the student list for each one?
    students = pd.read_excel(student_list, **CONSTANT.STUDENT_LOGINS)
    logger.debug("Student login file loaded")
    teams = pd.read_csv(assignment_file, **CONSTANT.TEAMS_CSV)
    logger.debug("Teams grade CSV file loaded")
    logger.info("Input files loaded, matching email addresses...")
    matched_file = teams.merge(
        students,
        how="left",
        left_on=teams.columns[0],
        right_on=CONSTANT.STUDENT_LOGINS["usecols"][1],
    )
    logger.info("Email addresses matched. Writing file(s) out")
    matched_file.to_excel(output, index=False)
    logger.info("File(s) finished writing")
