import json, jicson, requests
from icalendar import Calendar, Event
from io import StringIO
import secrets
import os

cal_data_key = {
    "Location" : "LOCATION",
    "Summary" : "SUMMARY",
    "Start Time" : "DTSTART;TZID=America/New_York",
    "End Time" : "DTEND;TZID=America/New_York",
}

project_data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")

def pref_pull():
    with open(os.path.join(project_data_folder,"prefs.json"), 'r') as pref_read:
        return json.load(pref_read)

with open(os.path.join(project_data_folder,"prefs.json"),'r+') as pref_file:
    prefs = json.load(pref_file)
    def cal_pull(url,curr_file_name):
        response = requests.get(url)
        import_store = jicson.fromText(response.text)
        if curr_file_name:
            file_name = curr_file_name
        else:
            file_name = secrets.token_hex(8)
        with open(f"{project_data_folder}/private/{file_name}.json","w") as cal_import:
            json.dump(import_store, cal_import, indent=4)
            cal_import.close()
        return file_name, cal_import["VCALENDAR"]["X-WR-CALNAME"]

for currCal in prefs["calFeeds"]:
    currCal["cal_file"] = cal_pull(currCal["url"],currCal["cal_file"])

with open(os.path.join(project_data_folder,"prefs.json"), "w") as pref_file:
    json.dump(prefs, pref_file, indent=4)

class CalInfoPull:
    def info(self):
        print()
