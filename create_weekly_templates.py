"""
This script is used to create Weekly Templates for each project team in HCI Studio.
"""

import sys
import json
import helpers.imports as helpers
from copy_gdrive_file import copy_file


def generate_weekly_templates(
    project_team_names_list, gdrive_service, template_name, template_url, folder_url
):
    """
    Generates an Weekly Template for each project team.

    :param project_team_names_list: list of project team names to generate Weekly Template for.
    :param gdrive_service: Google Drive v3 authentication object.
    :param template_name: name of weekly template.
    :param template_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :return: None
    """
    # iterate over project team nameslist and create an Weekly Template for each project team
    for project_team in project_team_names_list:
        # generate a filename using the project team name
        weekly_template_filename = "[{team_name}] {template_name}".format(
            team_name=project_team, template_name=template_name
        )

        # copy original file for each project using weekly_template_filename
        curr_copied_file = copy_file(
            gdrive_service, template_url, folder_url, weekly_template_filename
        )

        # generate a file URL for copied file, and print out
        curr_file_id = curr_copied_file["id"]
        print(
            "{filename}: https://docs.google.com/spreadsheets/d/{id}/edit".format(
                filename=weekly_template_filename, id=curr_file_id
            )
        )


def main(template_name, template_file_url, folder_url, project_team_names_list):
    """
    Generates Weekly Templates based on command-line arguments.

    :param template_name: name of weekly template.
    :param template_file_url: string url of original file to copy.
    :param folder_url: string url of folder to copy file to.
    :param project_team_names_list: list of project team names to create files for.
    :return: None
    """
    # authenticate for Google Drive v3 and Google Spreadsheets APIs
    gdrive_service = helpers.auth_gdrive()
    gspreadsheets_service = helpers.auth_gsheets()

    # generate Weekly Templates for each project team
    generate_weekly_templates(
        project_team_names_list,
        gdrive_service,
        template_name,
        template_file_url,
        folder_url,
    )


if __name__ == "__main__":
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 4:
        raise Exception(
            "Invalid number of arguments. Expected 4 "
            "(Template Name, Weekly Template URL, Destination Folder URL, "
            "Project Team Names List) got {}.".format(arg_count)
        )

    # inputs for creating Weekly Templates
    input_template_file_name = sys.argv[1]
    input_template_file_url = sys.argv[2]
    input_folder_url = sys.argv[3]
    input_project_team_names_list = json.loads(sys.argv[4])

    main(
        input_template_file_name,
        input_template_file_url,
        input_folder_url,
        input_project_team_names_list,
    )
