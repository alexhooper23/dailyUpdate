# ©2025 Alex Hooper Projects

import inspect
import jicson
import json
import os
import requests
import secrets

# Logging functionality
from shared.custom_logging import Log

log_exec = Log()


def log(*args):
    """Simplifies logging call. Executes log_exec.log(), combining all comma separated arguments"""
    log_exec.log(' '.join(str(arg) for arg in args))


cal_data_key = {
    "Location": "LOCATION",
    "Summary": "SUMMARY",
    "Start Time": "DTSTART;TZID=America/New_York",
    "End Time": "DTEND;TZID=America/New_York",
}


class Dummy:
    print()


project_data_folder = os.path.dirname(os.path.dirname(inspect.getfile(Dummy))) + "/data/private/"


def pref_pull():
    with open(project_data_folder + "prefs.json", 'r') as pref_read:
        log("Reading preference file...")
        return json.load(pref_read)


with open(os.path.join(project_data_folder, "prefs.json"), 'r') as pref_file:
    prefs = json.load(pref_file)

    def cal_pull(url, curr_file_name):
        response = requests.get(url)
        import_store = jicson.fromText(response.text)
        if curr_file_name:
            file_name = curr_file_name
        else:
            file_name = secrets.token_hex(8)
            log(f"No file present for calendar from url {url}. Generating new file with name {file_name}.json")
        with open(f"{project_data_folder}/calendars/{file_name}.json","w") as cal_import:
            json.dump(import_store, cal_import, indent=4)
            log(f"Calendar data dumped to file {file_name}.json")
            cal_import.close()
        return file_name

for currCal in prefs["calFeeds"]:
    log(f"Pulling calendar {currCal["cal_file"]}")
    currCal["cal_file"] = cal_pull(currCal["url"], currCal["cal_file"])

with open(os.path.join(project_data_folder, "prefs.json"), "w") as pref_file:
    json.dump(prefs, pref_file, indent=4)
    pref_file.close()


class CountdownWidgetData:
    def __init__(self):
        self.identifier = ""

    def new(self, label_input, date_input):
        with open(os.path.join(project_data_folder, "prefs.json"), "r+") as int_pref_file:
            editable_prefs = json.load(int_pref_file)
            self.identifier = secrets.token_hex(8)
            editable_prefs["countdowns"][self.identifier]["label"] = label_input
            editable_prefs["countdowns"][self.identifier]["date"] = date_input
            json.dump(editable_prefs, int_pref_file, indent=4)
            int_pref_file.close()
        return self.identifier

    def update(self, label, date):
        with open(os.path.join(project_data_folder, "prefs.json"), "r+") as int_pref_file:
            editable_prefs = json.load(int_pref_file)
            editable_prefs["countdowns"][self.identifier]["label"] = label
            editable_prefs["countdowns"][self.identifier]["date"] = date


    def retrieve(self):
        with open(os.path.join(project_data_folder, "prefs.json"), "r+") as int_pref_file:
            editable_prefs = json.load(int_pref_file)
            return [self.label, self.date]

    def remove(self, identifier):
        print()
