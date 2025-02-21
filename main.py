import tkinter as tk
import customtkinter as ctk_l
from functools import partial
import sys, os, socket, subprocess
from PIL import Image, ImageFont

#ctk_l.set_default_color_theme("/data/interface_colors.json")

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
    start_window.destroy()


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
    print("Terminating application....")
    os._exit(0)




start_window.protocol("WM_DELETE_WINDOW", exit_application)
start_window.mainloop()
