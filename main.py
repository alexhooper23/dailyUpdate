import tkinter as tk
from tkinter import ttk, font
from functools import partial
import sys, os, socket, subprocess
from PIL import Image, ImageTk

onstart_window = tk.Tk()
onstart_window.title("DailyUpdate")
onstart_window.geometry("500x500")

def create_session(session_kind):
    if session_kind == 'p':
        machine_path = os.path.join(os.getcwd(), "machine_files", "primary","primary_machine.py")
    elif session_kind == 'v':
        machine_path = os.path.join(os.getcwd(), "machine_files", "client_viewer","client_viewer.py")
    elif session_kind == 'c':
        machine_path = os.path.join(os.getcwd(), "machine_files", "client_config","client_config.py")
    else:
        print("Session code not recognized.")
        return
    print("Running new session with session code", session_kind)
    subprocess.Popen([sys.executable, machine_path],
                     start_new_session=True,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    onstart_window.destroy()

onstart_window.columnconfigure((0,0),weight = 1,uniform = "a")
onstart_window.rowconfigure((0,6),weight = 1,uniform = "a")

window_img_import = Image.open("images/dailyUpdate_white.png")
window_img_import_sized = window_img_import.resize((400,100))
window_img_import_tk = ImageTk.PhotoImage(window_img_import_sized)
window_img = ttk.Label(master = onstart_window, image=window_img_import_tk)
window_img.grid(column = 0, row = 0)

window_header = ttk.Label(master = onstart_window, text = "Select your system type.")
window_header.grid(column = 0, row = 1)

window_hostname = ttk.Label(master = onstart_window, text = socket.gethostname())
window_hostname.grid(column = 0, row = 2)

button_executes = [
    ["Primary","p"],
    ["Client - Viewer","v"],
    ["Client - Configuration","c"]
]
for i in range(3):
    btn_crt = ttk.Button(master = onstart_window, text=button_executes[i][0], command=partial(create_session,button_executes[i][1]))
    btn_crt.grid(column = 0, row = i+3)

# Run GUI with close event handler
def exit_application():
    print("Terminating application....")
    os._exit(0)
onstart_window.protocol("WM_DELETE_WINDOW", exit_application)
onstart_window.mainloop()
