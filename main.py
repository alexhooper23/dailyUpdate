import tkinter as tk
from tkinter import ttk, font
from functools import partial
import sys, os, socket, subprocess
from PIL import Image, ImageTk, ImageFont

onstart_window = tk.Tk()
onstart_window.title("DailyUpdate")
window_offset_x = int((onstart_window.winfo_screenwidth() / 2) - 250)
window_offset_y = int((onstart_window.winfo_screenheight() / 3) - 150)
onstart_window.geometry(f"500x300+{window_offset_x}+{window_offset_y}")

image = Image.open("images/du-bg.png")
bg_tk = ImageTk.PhotoImage(image)
bg_label = tk.Label(onstart_window, image=bg_tk)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
bg_label.image = bg_tk


ImageFont.truetype("/fonts/SF-Pro-Rounded-Black.otf")
ImageFont.truetype("/fonts/SF-Pro-Rounded-Regular.otf")
f_sf_black_ttl_tk = font.Font(family="SF Pro Rounded Bold", size=50)
f_sf_reg_opt_tk = font.Font(family="SF Pro Rounded Regular", size=15)


def create_session(session_kind):
    if session_kind == 'p':
        machine_path = os.path.join(os.getcwd(), "machine_files", "primary", "primary_machine.py")
    elif session_kind == 'v':
        machine_path = os.path.join(os.getcwd(), "machine_files", "client_viewer", "client_viewer.py")
    elif session_kind == 'c':
        machine_path = os.path.join(os.getcwd(), "machine_files", "client_config", "client_config.py")
    else:
        print("Session code not recognized.")
        return
    print("Running new session with session code", session_kind)
    subprocess.Popen([sys.executable, machine_path],
                     start_new_session=True,
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    onstart_window.destroy()


onstart_window.columnconfigure((0, 0), weight=1)
onstart_window.rowconfigure((0, 6), weight=1)

window_header = ttk.Label(master=onstart_window, text="DailyUpdate", font=f_sf_black_ttl_tk,background="")
window_header.grid(column=0, row=0)

window_option = ttk.Label(master=onstart_window, text="Select your system type.", font=f_sf_reg_opt_tk)
window_option.grid(column=0, row=1)

window_hostname = ttk.Label(master=onstart_window, text=socket.gethostname(), font=f_sf_reg_opt_tk)
window_hostname.grid(column=0, row=2)

button_executes = [
    ["Primary", "p"],
    ["Client - Viewer", "v"],
    ["Client - Configuration", "c"]
]
for i in range(3):
    btn_crt = ttk.Button(master=onstart_window, text=button_executes[i][0],
                         command=partial(create_session, button_executes[i][1]))
    btn_crt.grid(column=0, row=i + 3)


# Run GUI with close event handler
def exit_application():
    print("Terminating application....")
    os._exit(0)




onstart_window.protocol("WM_DELETE_WINDOW", exit_application)
onstart_window.mainloop()
