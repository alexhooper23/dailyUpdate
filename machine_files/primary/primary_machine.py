# generic pulls
from datetime import datetime
import time, os, sys

# pulls from project files
from data_processing import fetch_ui_cal_events, pref_pull

# pulls tools for thread sequencing to improve time accuracy
import threading, queue

# gui handlers
import customtkinter as ctk_l

import random
import socket

print("Session code p initiated")

main_window = ctk_l.CTk()
main_window.title("DailyUpdate")
main_window.geometry("1920x1080")

time_tk = ckt_l.StringVar()
access_code = tk.IntVar()

update_time_based_functions = threading.Event()
all_prefs = pref_pull()

access_code.set(random.randint(00000,99999))

# HEAD CALLING LOOP
def clock_run(q):
    while True:
        time_now = datetime.now()
        q.put(time_now.second)
        time.sleep(1)

def clock_update_response(q):
    while True:
        fetch_q = int(q.get())
        if fetch_q % 1 == 0 or fetch_q == 0:
            #operations to run every 3 seconds
            curr_time = datetime.now()
            gui_clock_update(curr_time)
            # OPERATIONS TO RUN EVERY MINUTE
            # if time_now.second == 0:
            # OPERATIONS TO RUN EVERY HOUR
            # if time_now.minute == 0:
            # OPERATIONS TO RUN EVERY DAY
        q.task_done()

def gui_clock_update(gui_time_pull):
    time_prefs = all_prefs["time"]
    time_string = ""
    if time_prefs["format"] == 12:
        time_string = "%I"
    else:
        time_string = "%H"
    time_string += ":%M"
    if time_prefs["seconds"]:
        time_string += ":%S"
    if time_prefs["am_pm"]:
        time_string += " %p"
    if time_prefs["flash_col"] and gui_time_pull.second % 2 == 0:
        time_string = time_string.replace(":"," ")
    time_tk.set(gui_time_pull.strftime(time_string))

# GUI Elements

main_window.columnconfigure((5,5),weight = 3,uniform = "a")
main_window.rowconfigure(0,weight = 3,uniform = "a")

#Temp code: write row/column labels
for i in range(5):
    main_window.columnconfigure(i, weight=1, minsize=50)
    main_window.rowconfigure(i, weight=1, minsize=50)

    for j in range(5):
        frame = ctk_l.Frame(
            master=main_window,
            relief=ctk_l.SOLID,
            borderwidth=1
        )
        frame.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
        label = ctk_l.Label(master=frame, text=f"{i}, {j}")
        label.pack(padx=5, pady=5)

# TIME
curr_time_tk = ttk.Label(master = main_window, textvariable = time_tk)
curr_time_tk.grid(column = 0, row = 0)


access_code_tk = ttk.Label(master = main_window, textvariable = access_code)
access_code_tk.grid(column = 1, row = 0)

#Start time threads
if __name__ == "__main__":
    print("Class threads")
    q_updates = queue.Queue()

    time_func = threading.Thread(target=clock_run, args=(q_updates,))
    update_func = threading.Thread(target=clock_update_response, args=(q_updates,))

    # Start threads
    time_func.start()
    update_func.start()



# Run GUI with close event handler
def exit_application():
    print("Terminating application....")
    os._exit(0)

main_window.protocol("WM_DELETE_WINDOW", exit_application)
main_window.mainloop()