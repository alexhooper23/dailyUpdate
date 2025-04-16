# ©2025 Alex Hooper Projects

import json

# Logging functionality
from shared.custom_logging import Log

log_exec = Log()


def log(*args):
    """Simplifies logging call. Executes log_exec.log(), combining all comma separated arguments"""
    log_exec.log(' '.join(str(arg) for arg in args))
# End logging functionality


def pull_widget():
    with open("../data/private/widget_layout.json", "r") as wgt_lo:
        wgt_lo_json = json.load(wgt_lo)
        head_data = []
        x = 0
        for unique_widget in wgt_lo_json:
            # x, y, w, l, id
            head_data[x] = [unique_widget["pos"], unique_widget["size"], str(unique_widget)]
        return head_data
