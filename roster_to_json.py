"""
This script is used to extract information from the Studio Roster Google Spreadsheet for other scripts and tools.
"""

import sys
import json
import re
import helpers.imports as helpers


def fetch_student_info(spreadsheet, sheet_name):
    """
    Fetches information for each student from the Studio Roster Google Spreadsheet.

    :param spreadsheet:  gspread spreadsheet object for the Studio Roster.
    :param sheet_name: string name of sheet where Student Info is stored.
    :return: dict of students with info relevant specifically to them.
    """
    # open correct worksheet and get all values to parse
    student_info_worksheet = spreadsheet.worksheet(sheet_name)
    values = student_info_worksheet.get_all_values()

    # create header mapping object
    header = values[0]
    header_mapping = {
        "Name": "student_name",
        "Email": "email_address",
        "Team Name": "team_name",
        "Mysore Availability": "mysore_availability",
        "Individual Progress Map": "individual_progress_map_link",
        "Self-Assessment": "self_assessment_link"
    }

    # create a header index to lookup header_mapping keys by index number
    # track any header vals not including in mapping
    exclude_list = []
    header_index = {}

    for curr_index, curr_val in enumerate(header):
        if curr_val in header_mapping:
            header_index[curr_index] = curr_val
        else:
            exclude_list.append(curr_val)

    if len(exclude_list) > 0:
        print("The following columns were included in the Studio Roster Spreadsheet, but not in the header_mapping. "
              "They will not be included in the parsed Studio Database: {}".format(exclude_list))

    # iterate over each row and parse data
    output = {}
    for student in values[1:]:
        # hold the current student's name to use as a dict key later
        curr_student_name = ""

        # setup an object for holding current project information
        curr_student = {
            "email_address": "",
            "team_name": "",
            "mysore_availability": [],
            "individual_progress_map_link": "",
            "self_assessment_link": ""
        }

        # parse each individual info field
        for index, student_info in enumerate(student):
            # check if index is in header_index before proceeding
            if index not in header_index:
                continue

            # if Name, get current student's name
            if header_index[index] == "Name":
                curr_student_name = student_info
            # if Mysore Availability, parse comma-separated string into a list
            elif header_index[index] == "Mysore Availability":
                mysore_availability_list = [mysore_time.strip() for mysore_time in student_info.split(",")]
                curr_student[header_mapping[header_index[index]]].extend(mysore_availability_list)
            # else, add to appropriate field
            else:
                curr_student[header_mapping[header_index[index]]] = student_info.strip()

        # add to output
        output[curr_student_name] = curr_student

    # output data
    return output


def fetch_team_info(spreadsheet, sheet_name):
    """
    Fetches Team Information from Studio Roster.

    :param spreadsheet: gspread spreadsheet object for the Studio Database.
    :param sheet_name: string name of sheet where Team Information is stored.
    :return: dict of parsed Team Information.
    """
    # open correct worksheet and get all values to parse
    studio_info_worksheet = spreadsheet.worksheet(sheet_name)
    values = studio_info_worksheet.get_all_values()

    # create header mapping object
    header = values[0]
    header_mapping = {
        "Team Name": "team_name",
        "Week 1 Template": "week_1_template_link",
        "Week 2 Template": "week_2_template_link",
        "Week 3 Template": "week_3_template_link",
        "Week 4 Template": "week_4_template_link",
        "Week 5 Template": "week_5_template_link",
        "Week 6 Template": "week_6_template_link",
        "Week 7 Template": "week_7_template_link",
        "Week 8 Template": "week_8_template_link",
        "Week 9 Template": "week_9_template_link"
    }

    # create a header index to lookup header_mapping keys by index number
    # track any header vals not including in mapping
    exclude_list = []
    header_index = {}

    for curr_index, curr_val in enumerate(header):
        if curr_val in header_mapping:
            header_index[curr_index] = curr_val
        else:
            exclude_list.append(curr_val)

    if len(exclude_list) > 0:
        print("The following columns were included in the Studio Roster Spreadsheet, but not in the header_mapping. "
              "They will not be included in the parsed Studio Database: {}".format(exclude_list))

    # iterate over each row and parse data
    output = {}
    for team in values[1:]:
        # hold the current team's name to use as a dict key later
        curr_team_name = ""

        # setup an object for holding current team information
        curr_team = {
            "weekly_templates": []
        }

        # parse each individual info field
        for index, sig_info in enumerate(team):
            # check if index is in header_index before proceeding
            if index not in header_index:
                continue

            # check if a weekly template column
            pattern = re.compile(r'Week \d+ Template')
            if pattern.match(header_index[index]):
                curr_team["weekly_templates"].append({
                    "name": header_index[index],
                    "link": sig_info.strip()
                })
            # check if team name column
            elif header_index[index] == "Team Name":
                curr_team_name = sig_info.strip()
            # else, add to appropriate field
            else:
                curr_team[header_mapping[header_index[index]]] = sig_info.strip()

        # add to output
        output[curr_team_name] = curr_team

    # output data
    return output


def create_studio_db_dict(student_info_dict, team_info_dict):
    """
    Creates a studio database dict that combines the parsed Student and Team Information worksheets.

    :param student_info_dict: dict of parsed Student Info from Studio Roster.
    :param team_info_dict: dict of parsed Team Info from Studio Roster.
    :return: dict of each student with all individual and team info.
    """
    # create a placeholder output object
    output = json.loads(json.dumps(student_info_dict))

    # construct list of team members
    team_members = {team_names: [] for team_names in team_info_dict.keys()}
    for student_name, student_info  in student_info_dict.items():
        team_members[student_info["team_name"]].append(student_name)

    # add team info to student info
    for student_name, student_info  in output.items():
        # get team info for student
        curr_team_name = student_info["team_name"]
        curr_team_info = team_info_dict[curr_team_name]

        # add team name and members
        curr_team_info["team_name"] = curr_team_name
        curr_team_info["team_members"] = team_members[curr_team_name]

        # remove team_name from student info, and add in team_info
        output[student_name].pop("team_name", None)
        output[student_name]["team_info"] = curr_team_info

    # output studio database dict
    return output


def export_studio_db_as_json(studio_db_dict, output_file):
    """
    Exports Studio Database dict as a json object for other tools.
    For convenience, the exported json uses a list of students rather than a dictionary where each student is a key.

    :param studio_db_dict: dict containing all information for the studio database
    :param output_file: string filepath to output json to.
    :return: json string of studio database dict with correct formatting for external tools.
    """
    # create output object
    output = []

    for student_name, student_info in studio_db_dict.items():
        # create a dict with all student info, and add the student's name to it
        curr_student = student_info
        curr_student["name"] = student_name

        # add to output
        output.append(curr_student)

    # output json to specified file
    with open(output_file, "w") as outfile:
        json.dump(output, outfile, indent=4)

    # return json string
    return json.dumps(output, indent=4)


def main(spreadsheet_url, student_info_sheet_name, team_info_sheet_name):
    """
    Generates a Studio Database dict, given a Studio Database spreadsheet.

    :param spreadsheet_url: string url of Studio Roster Google Spreadsheet.
    :param student_info_sheet_name: string name of sheet where Student Information is stored.
    :param team_info_sheet_name: string name of sheet where Team Information is stored.
    :return: dict of parsed studio database.
    """
    # authenticate gspread
    gc = helpers.auth_gsheets()

    # get spreadsheet
    curr_spreadsheet = gc.open_by_url(spreadsheet_url)

    # fetch student and team info
    curr_student_info = fetch_student_info(curr_spreadsheet, student_info_sheet_name)
    curr_team_info = fetch_team_info(curr_spreadsheet, team_info_sheet_name)

    # create and output a studio database dict
    return create_studio_db_dict(curr_student_info, curr_team_info)


if __name__ == '__main__':
    # get command line args
    arg_count = len(sys.argv) - 1

    # check for correct number of arguments
    if arg_count != 3:
        raise Exception("Invalid number of arguments. Expected 3 "
                        "(Studio Roster URL, Student Info sheet name, Team Info sheet name) got {}."
                        .format(arg_count))

    # parse each argument
    input_spreadsheet_url = sys.argv[1]
    input_student_info_sheet_name = sys.argv[2]
    input_team_info_sheet_name = sys.argv[3]
    json_output_filepath = "hci_studio_db.json"

    # generate studio database dict
    studio_database_dict = main(input_spreadsheet_url, input_student_info_sheet_name, input_team_info_sheet_name)

    # export as json and print exported json
    export_studio_db_as_json(studio_database_dict, json_output_filepath)
    print("Studio Roster successfully parsed and exported to {}".format(json_output_filepath))
