"""
This script is used to create Mid-Auarter Self-Assessments for each student in HCI Studio, given a template,
output directory and a list of student names.
"""

import sys
import helpers.imports as helpers
import roster_to_json as studio_db
from copy_gdrive_file import copy_file


def generate_self_assessment(
    studio_db_dict,
    gdrive_service,
    gspreadsheets_service,
    template_url,
    target_folder_url,
    should_populate,
):
    """
    Generates a Self-Assessment worksheet for each student. Data is populated if should_populate is True.

    :param studio_db_dict: dict containing all information for the studio database
    :param gdrive_service: Google Drive v3 authentication object.
    :param template_url: string url of original file to copy.
    :param target_folder_url: string url of folder to copy file to.
    :param should_populate: boolean whether student info from the studio_db_dict should be used to pre-populate
        the generated self-assessment.
    :return: None
    """
    # iterate over each student in the studio_db_dict, and create a self-assessment for them
    for student_name, student_info in studio_db_dict.items():
        # generate a filename using the student's first name and last initial
        student_name_split = student_name.split(" ")
        student_filename = "{first} {lasti}. -- Mid-Quarter Self-Assessment".format(
            first=student_name_split[0], lasti=student_name_split[-1][0]
        )

        # copy original file for each project using student_filename
        curr_copied_file = copy_file(
            gdrive_service, template_url, target_folder_url, student_filename
        )

        # generate a file URL for copied file
        curr_file_id = curr_copied_file["id"]
        curr_file_url = "https://docs.google.com/spreadsheets/d/{id}/edit".format(
            id=curr_file_id
        )

        # populate with data
        if should_populate:
            populate_self_assessment(
                gspreadsheets_service, curr_file_url, student_name, student_info
            )

        # print generated file
        print(
            "{filename}: {fileurl}".format(
                filename=student_filename, fileurl=curr_file_url
            )
        )


def populate_self_assessment(
    gspreadsheet_service, self_assessment_url, student_name, student_info_dict
):
    """
    Pre-populates the generated self-assessment with info from the Studio Roster, where applicable.

    :param gspreadsheet_service:
    :param self_assessment_url:
    :param student_name:
    :param student_info_dict:
    :return:
    """
    # get the generated spreadsheet
    generated_spreadsheet = gspreadsheet_service.open_by_url(self_assessment_url)

    # populate basic info
    basic_info_worksheet = generated_spreadsheet.worksheet("Basic Info")
    populate_basic_info(basic_info_worksheet, student_name, student_info_dict)


def populate_basic_info(worksheet, student_name, student_info_dict):
    """
    Populates the Basic Info tab with the student's: name; email; team color (and members); individual progress map.

    :param worksheet: gspread worksheet object that points to the Basic Info tab.
    :param student_name: string name of student.
    :param student_info_dict: dict info related to student.
    :return:
    """
    # generate update list with student's: name; email; team color (and members); individual progress map link
    student_email = student_info_dict["email_address"]
    student_learning_goal = student_info_dict["learning_goals"]
    student_team = "{teamname} ({teammembers})".format(
        teamname=student_info_dict["team_info"]["team_name"],
        teammembers="; ".join(student_info_dict["team_info"]["team_members"]),
    )
    student_design_log = "design log link"
    student_ipm = student_info_dict["individual_progress_map_link"]
    student_latest_proj_template = student_info_dict["team_info"]["weekly_templates"][
        4
    ]["link"]
    update_list = [
        [student_name],
        [student_email],
        [student_learning_goal],
        [student_team],
        [student_design_log],
        [student_ipm if student_ipm != "" else "individual progress map link"],
        [student_latest_proj_template],
    ]

    # update worksheet
    worksheet.update("B2:B8", update_list)


def main(
    template_file_url,
    target_folder_url,
    should_populate,
    roster_spreadsheet_url,
    student_info_sheet_name,
    team_info_sheet_name,
):
    """
    Fetches info from Studio Roster, and uses it to generate self-assessment sheets for each student.

    :param template_file_url: string url of original file to copy.
    :param target_folder_url: string url of folder to copy file to.
    :param should_populate: boolean should the copied sheet be populated with the known information (e.g., name; email).
    :param roster_spreadsheet_url: string url of Studio Roster Google Spreadsheet.
    :param student_info_sheet_name: string name of sheet where Student Information is stored.
    :param team_info_sheet_name: string name of sheet where Team Information is stored.
    :return: None
    """
    # authenticate for Google Drive v3 and Google Spreadsheets APIs
    gdrive_service = helpers.auth_gdrive()
    gspreadsheets_service = helpers.auth_gsheets()

    # generate studio database from roster
    studio_db_dict = studio_db.main(
        roster_spreadsheet_url, student_info_sheet_name, team_info_sheet_name
    )

    # generate IPMs for each student
    generate_self_assessment(
        studio_db_dict,
        gdrive_service,
        gspreadsheets_service,
        template_file_url,
        target_folder_url,
        should_populate,
    )


if __name__ == "__main__":
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 6:
        raise Exception(
            "Invalid number of arguments. Expected 6 "
            "(Self-Assessment template URL, Self-Assessment target folder URL, Should Populate (boolean), "
            "Studio Roster URL, Student Info sheet name, Team Info sheet name) got {}.".format(
                arg_count
            )
        )

    # inputs for creating self-assessments
    input_template_file_url = sys.argv[1]
    input_folder_url = sys.argv[2]
    input_should_populate = True if sys.argv[3] == "true" else False

    # inputs for generating studio database
    input_studio_db_url = sys.argv[4]
    input_student_info_sheet_name = sys.argv[5]
    input_team_info_sheet_name = sys.argv[6]

    main(
        input_template_file_url,
        input_folder_url,
        input_should_populate,
        input_studio_db_url,
        input_student_info_sheet_name,
        input_team_info_sheet_name,
    )
