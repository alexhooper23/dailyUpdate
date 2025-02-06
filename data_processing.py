import json, jicson, requests
from icalendar import Calendar, Event
from io import StringIO
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

with open(os.path.join(project_data_folder,"prefs.json"),'r+') as prefFile:
    prefs = json.load(prefFile)
    def cal_pull(url):
        response = requests.get(url)
        import_store = jicson.fromText(response.text)
        file_name = import_store["VCALENDAR"][0]["X-WR-CALNAME"]
        with open(f"{project_data_folder}/{file_name}.json","w") as cal_import:
            json.dump(import_store, cal_import, indent=4)
        return file_name

for currCal in prefs["calFeeds"]:
    currCal["calFile"] = cal_pull(currCal["url"])

with open(os.path.join(project_data_folder,"prefs.json"), "w") as pref_file:
    json.dump(prefs, pref_file, indent=4)

def fetch_ui_cal_events(num_events):

    print("X")