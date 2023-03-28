# HCI Studio Orchestration Scripts
Scripts to orchestrate the creation of documents for HCI Studio. 

## Setup
1. Make sure you have [Python 3.x](https://www.python.org/downloads/) (we use 3.9) and [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/#install-pipenv-today) installed.
2. Clone the repo to your local machine.
3. Install dependencies using `pipenv install`. To run scripts, start a virtual environment using `pipenv shell`. 
4. Generate a `credentials.json` for the [Google Drive v3 API](https://developers.google.com/drive/api/v3/quickstart/python) and a `service_account.json` for the [Google Spreadsheet API](https://gspread.readthedocs.io/en/latest/oauth2.html#for-bots-using-service-account). Place both of these files at the root of the cloned repo. _Note: these can be under the same project. See the instructions for [setting up gspread](https://gspread.readthedocs.io/en/latest/oauth2.html#enable-api-access-for-a-project) to learn more._

## Available Scripts and Usage

### roster_to_json.py
This script is used to extract information from a Studio Database Google Spreadsheet for other scripts and tools. When run from the command line, it will download information from the Studio Database Spreadsheet, and parse it into a JSON file.

The script is run as follows: 
```commandline
python roster_to_json.py <studio_db_url> <student_info_sheet_name> <team_info_sheet_name>
```

For example: 
```commandline
python roster_to_json.py "https://docs.google.com/spreadsheets/d/1xr9MWxBWHXcRyjeBXvF4tP6c9JNct1ckRgQqJHXxfl4/edit#gid=0" "Student Info" "Team Info"
```

### create_ipm.py
This script is used to create Individual Progress Maps (IPMs) for a list of students specified in the command line argument, given an IPM template and an output directory.

The script is run as follows:
```commandline
python create_ipm.py <ipm_template_url> <ipm_folder_url> "[\"list\", \"of\", \"students\"]"
```

For example:
```commandline
python create_ipm.py "https://docs.google.com/spreadsheets/d/1XTuvjEtIgFuvNZ5MzrYH6WlphnYaprOC-7BUJiT0mWU/edit?usp=sharing" "https://drive.google.com/drive/u/1/folders/1gWcW29cheuDxEhImg-gwnwhGRmItWfez" "[\"John Doe\", \"Jane Doe\"]"
```

### create_weekly_templates.py
This script is used to create Weekly Project Templates for a list of Project Teams.

The script is run as follows:
```commandline
python create_weekly_templates.py <template_name> <weekly_template_template_url> <weekly_template_folder_url> "[\"list\", \"of\", \"project team names\"]"
```

For example:
```commandline
python create_weekly_templates.py "Template 01: Needfinding and Analysis On Your Own" "https://docs.google.com/presentation/d/1eSLR344A5C2dt4ICQPzv5VjlUwgNBHCdCHRtYDzP5bs/edit?usp=share_link" "https://drive.google.com/drive/u/1/folders/1jRnumZWdL_2fq0g0dUPOO-leYFJfGRz3" "[\"Milky Way\", \"Andromeda\",  \"Cigar\",  \"Triangulum\",  \"Sombrero\",  \"Whirlpool\",  \"Pinwheel\",  \"Sculptor\",  \"Cartwheel\",  \"Tadpole\"]"
```

### create_self_assessments.py
This script is used to create end-of-quarter self-assessments for each student, given a self-assessment template, output directory, true/false for if Basic Info should be filled from the studio roster, a link to the studio roster, the name of the sheet with student info, and the name of the sheet with team info.

The script is run as follows: 
```commandline
python create_self_assessments.py <self_assessment_template_url> <self_assessment_folder_url> <should_populate_boolean> <studio_db_url> <student_info_sheet_name> <team_info_sheet_name>
```

For example:
```commandline
python create_self_assessments.py "https://docs.google.com/spreadsheets/d/1sP-kMXQlKvqPOOTgA3M1Qp3FXvJ9DSRO2ZjaWVem0bg/edit?usp=sharing" "https://drive.google.com/drive/u/1/folders/1Zrqjo1yI-twQpzZRxC_MLWKu_XoUFbMJ" "true" "https://docs.google.com/spreadsheets/d/1xr9MWxBWHXcRyjeBXvF4tP6c9JNct1ckRgQqJHXxfl4/edit#gid=0" "Student Info" "Team Info"
```

"[\"Milky Way\", \"Andromeda\",  \"Cigar\",  \"Triangulum\",  \"Sombrero\",  \"Whirlpool\",  \"Pinwheel\",  \"Sculptor\",  \"Cartwheel\",  \"Tadpole\"]"