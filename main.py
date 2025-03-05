import json
import os
import socket
import subprocess
import sys
import secrets
from functools import partial
from wsgiref.simple_server import software_version

import customtkinter as ctk_l
from PIL import Image, ImageFont

# Logging functionality
from shared.custom_logging import Log

log_exec = Log()


def log(*args):
    """Simplifies logging call. Executes log_exec.log(), combining all comma separated arguments"""
    log_exec.log(' '.join(str(arg) for arg in args))


# ctk_l.set_default_color_theme("/data/interface_color_defaults.json")

# System Identifier Registration
identifier_path = "data/private/sys_identifiers"
sf_version = "0.0.05"


def gen_identifier_info():
    identifier_key = secrets.token_hex(16)
    log("Machine identifier key was corrupt or nonexistent. New key generated -->", identifier_key)
    log("MACHINE SHORTNAME -->", identifier_key[-5:-1])
    return [identifier_key + "\n", sf_version]


if not os.path.exists(identifier_path):
    with open(identifier_path, "w+") as f:
        f.writelines(gen_identifier_info())
else:
    with (open(identifier_path, "r+") as f):
        f_lines = f.readlines()
        if f_lines[0] == '\n' or not len(f_lines[0]) == 33:
            f_lines = gen_identifier_info()
        else:
            f_lines[1] = sf_version
        log("MACHINE SHORTNAME  -->", f_lines[0][-5:-1])
        f.seek(0)
        f.truncate()
        f.writelines(f_lines)


start_window = ctk_l.CTk()
start_window.title("DailyUpdate")
window_offset_x = int((start_window.winfo_screenwidth() / 2) - 250)
window_offset_y = int((start_window.winfo_screenheight() / 3) - 150)
start_window.geometry(f"500x300+{window_offset_x}+{window_offset_y}")

bg_tk = ctk_l.CTkImage(Image.open("images/du-bg.png"))
bg_label = ctk_l.CTkLabel(start_window, image=bg_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_tk

ImageFont.truetype("/fonts/SF-Pro-Rounded-Black.otf")
ImageFont.truetype("/fonts/SF-Pro-Rounded-Regular.otf")
f_sf_black_ttl_tk = ctk_l.CTkFont(family="SF Pro Rounded Bold", size=50)
f_sf_reg_opt_tk = ctk_l.CTkFont(family="SF Pro Rounded Regular", size=15)


def find_ip():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('8.8.8.8', 80))
    local_ip = sock.getsockname()[0]
    sock.close()
    return local_ip


def register_identifier(kind):
    with open("data/private/machine_identifiers.json", "r+") as f:
        identifiers = json.load(f)
        machine_hostname = socket.gethostname()
        data = identifiers.setdefault(machine_hostname, {})

        # Update the dictionary with the desired values.
        data.update({
            "hostname": machine_hostname,
            "common_name": machine_hostname,
            "ip_addr": find_ip(),
            "sessions_since_last_connection": data.get("sessions_since_last_connection", 0),
            "kind": kind,
        })
        f.seek(0)
        json.dump(identifiers, f, indent=4)
        f.truncate()


def create_session(session_kind):
    with open("data/private/machine_identifiers.json", "r+") as machine_identifiers:
        json_identifiers = json.load(machine_identifiers)
        print(json_identifiers)
        print(type(json_identifiers))
        for key, each in json_identifiers.items():
            print(type(each))
            each["sessions_since_last_connection"] += 1
        machine_identifiers.seek(0)
        json.dump(json_identifiers, machine_identifiers, indent=4)
        machine_identifiers.truncate()
        machine_identifiers.close()
    if session_kind == 'p':
        machine_path = os.path.join(os.getcwd(), "machine_files", "primary", "primary_machine.py")
    elif session_kind == 'v':
        machine_path = os.path.join(os.getcwd(), "machine_files", "client_viewer", "client_viewer.py")
        register_identifier("v")
    elif session_kind == 'c':
        machine_path = os.path.join(os.getcwd(), "machine_files", "client_config", "client_config.py")
        register_identifier("c")
    else:
        log("Session code not recognized.")
        return
    log("Running new session with session code", session_kind)
    """subprocess.Popen([sys.executable, machine_path],
                     start_new_session=True,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    start_window.destroy()"""

create_session("c")

start_window.columnconfigure((0, 0), weight=1)
start_window.rowconfigure((0, 6), weight=1)

window_header = ctk_l.CTkLabel(master=start_window, text="DailyUpdate", font=f_sf_black_ttl_tk)
window_header.grid(column=0, row=0)

window_option = ctk_l.CTkLabel(master=start_window, text="Select your system type.", font=f_sf_reg_opt_tk)
window_option.grid(column=0, row=1)

window_hostname = ctk_l.CTkLabel(master=start_window, text=socket.gethostname(), font=f_sf_reg_opt_tk)
window_hostname.grid(column=0, row=2)

button_executes = [
    ["Primary", "p"],
    ["Client - Viewer", "v"],
    ["Client - Configuration", "c"]
]
for i in range(3):
    btn_crt = ctk_l.CTkButton(master=start_window, text=button_executes[i][0],
                              command=partial(create_session, button_executes[i][1]))
    btn_crt.grid(column=0, row=i + 3)


# Run GUI with close event handler
def exit_application():
    log("Window closed; terminating application")
    sys.exit(0)


start_window.protocol("WM_DELETE_WINDOW", exit_application)
start_window.mainloop()
