# generic pulls
import os
# pulls tools for thread sequencing to improve time accuracy
import queue
import random
import socket
import sys
import threading
import time
from datetime import datetime

# gui handlers
import customtkinter as ctk_l

# Logging functionality
from shared.custom_logging import Log
# pulls from project files
from shared.data_processing import pref_pull

log_exec = Log()


def log(*args):
    """Simplifies logging call. Executes log_exec.log(), combining all comma separated arguments"""
    log_exec.log(' '.join(str(arg) for arg in args))


log("Session code p initiated")

main_window = ctk_l.CTk()
main_window.title("DailyUpdate")
main_window.geometry("1920x1080")

time_tk = ctk_l.StringVar()
access_code = ctk_l.IntVar()

update_time_based_functions = threading.Event()
all_prefs = pref_pull()

access_code.set(random.randint(10000, 99999))


# HEAD CALLING LOOP
def clock_run(q):
    while True:
        time_now = datetime.now()
        q.put(time_now.second)
        time.sleep(0.1)


def clock_update_response(q):
    while True:
        fetch_q = int(q.get())
        if fetch_q % 1 == 0 or fetch_q == 0:
            # Operations to run every 3 seconds
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
        time_string = time_string.replace(":", " ")
    time_tk.set(gui_time_pull.strftime(time_string))


def find_devices_on_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Set socket to allow broadcasting
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind to the specified port
    sock.bind(('', 50008))
    print(f"Listening for broadcasts on port {port}...")

    while True:
        # Receive data and sender address
        data, addr = sock.recvfrom(1024)
        print(f"Received message from {addr}: {data.decode()}")
        break
    sock.close()


find_devices_on_port(50008)


def server_start():
    global access_code
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        ip_addr = socket.gethostbyname(socket.gethostname())
        port = 50008
        s.bind((ip_addr, port))
        s.listen(1)
        log(f"Server at IP Address {ip_addr} listening on port {port}\nAccess code: {access_code.get()}")
        conn, addr = s.accept()
        with conn:
            log("Connected by", addr)
            conn.sendall("LOCKED OUT".encode())
            auth_response = conn.recv(1024).decode()
            log("Response:", auth_response)
            if auth_response != access_code:
                conn.sendall("DENIED".encode())
                return
            conn.sendall("AUTH SUCCESS".encode())
            log("Client authenticated.")
            connection_success_response = conn.recv(1024).decode()
            with open(os.path.dirname(os.path.dirname(os.getcwd())) + "/data/private/client_identifiers",
                      "a+") as client_identifiers_file:
                client_identifiers_file.seek(0)
                client_identifiers_file.find()
            while True:
                response = conn.recv(1024).decode()
                if response:
                    log("Message received:", response)
                    conn.sendall(b"Acknowledge\n")


server_start()

# GUI Elements
main_window.columnconfigure((5, 5), weight=3, uniform="a")
main_window.rowconfigure(0, weight=3, uniform="a")

# Temp code: write row/column labels
for i in range(5):
    main_window.columnconfigure(i, weight=1, minsize=50)
    main_window.rowconfigure(i, weight=1, minsize=50)

    for j in range(5):
        frame = ctk_l.CTkFrame(master=main_window)
        frame.grid(row=i, column=j, padx=0, pady=0, sticky="nsew")
        label = ctk_l.CTkLabel(master=frame, text=f"{i}, {j}")
        label.pack(padx=5, pady=5)

# TIME
curr_time_tk = ctk_l.CTkLabel(master=main_window, textvariable=time_tk)
curr_time_tk.grid(column=0, row=0)

access_code_tk = ctk_l.CTkLabel(master=main_window, textvariable=access_code)
access_code_tk.grid(column=1, row=0)

# Start time threads
if __name__ == "__main__":
    log("Class threads")
    q_updates = queue.Queue()

    time_func = threading.Thread(target=clock_run, args=(q_updates,))
    update_func = threading.Thread(target=clock_update_response, args=(q_updates,))

    # Start threads
    time_func.start()
    update_func.start()


# Run GUI with close event handler
def exit_application():
    log("Window closed. Terminating application.")
    # noinspection PyProtectedMember,PyUnresolvedReferences
    sys.exit(0)


main_window.protocol("WM_DELETE_WINDOW", exit_application)
main_window.mainloop()
