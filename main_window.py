from calendar import timegm
from datetime import date
from operator import truediv
from tkinter import *
from tkinter import ttk

from tkcalendar import Calendar, DateEntry

import csv_checker as csv_checker

import os
import shutil
import ftplib
ftp = ftplib.FTP()

import logging
from csv_checker import *

# sets up logging in file csv.log
logging.basicConfig(filename='csv.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)



# FTP commands =====================
# Attempts to establish a connection to the ftp server with the given details
def connect_server():
    ip = ent_ip.get()
    port = int(ent_port.get())
    try:
       msg = ftp.connect(ip,port)
       text_servermsg.insert(END, "\n" + msg)
       lbl_login.place(x=150,y=20)
       ent_login.place(x=150,y=40)
       lbl_pass.place(x=150,y=60)
       ent_pass.place(x=150,y=80)
       btn_login.place(x=182,y=110)
    except:
       text_servermsg.insert(END,"\nUnable to connect")


# Logs the user in with the given credentials
def login_server():
    user = ent_login.get()
    password = ent_pass.get()
    try:
        msg = ftp.login(user,password)
        text_servermsg.insert(END, "\n" + msg)
        display_dir()
        lbl_login.place_forget()
        ent_login.place_forget()
        lbl_pass.place_forget()
        ent_pass.place_forget()
        btn_login.place_forget()
    except:
        text_servermsg.insert(END, "\nUnable to login")


# Each time the active directory changes, the list is cleared and the new files are displayed
def display_dir():
    libox_serverdir.delete(0, END)
    libox_serverdir.insert(0,"--------------------------------------------")
    dirlist = ftp.nlst()
    dirlist.reverse() # Sorts directory listing to descending alphabetical
    for item in dirlist:
        libox_serverdir.insert(0, item)


# Changes the active server directory currently being viewed
def change_directory():
    try:
        directory = libox_serverdir.get(libox_serverdir.curselection())
    except:
        directory = ""

    try:
        msg = ftp.cwd(directory)
        text_servermsg.insert(END, "\n" + msg)
    except:
        text_servermsg.insert(END, "\nUnable to change directory")
    display_dir()


# Steps up to the parent server directory
def step_up_directory():
    directory = ".."
    try:
        msg = ftp.cwd(directory)
        text_servermsg.insert(END, "\n" + msg)
    except:
        text_servermsg.insert(END, "\nUnable to change directory")
    display_dir()


# Downloads the single file selected in the server directory listing
def download_file():
    download = True
    try:
        file = libox_serverdir.get(libox_serverdir.curselection())
        text_servermsg.insert(END, "\nDownloading " + file + "...\n")
        os.chdir(os.getcwd() + '/Temp_Files')
        with open(file, "wb") as newfile:
            ftp.retrbinary(f"RETR {file}", newfile.write)
    except:
        download = False
        logging.warning(f'File could not be found')
        text_servermsg.insert(END, "\nUnable to download file")
    display_dir()
    if (download):
        os.chdir('..')
        if(csv_checker.total_valid(file)):
            print(os.getcwd() + "/Valid_Files" + file)
            if (not os.path.exists(os.getcwd() + "/Valid_Files/" + file)):
                text_servermsg.insert(END, "\nSuccessfully downloaded file to Valid_Files")
                shutil.move('Temp_Files/%s' % file, 'Valid_Files/')
        else:
            text_servermsg.insert(END, "\nInvalid File, check the log file for more details")
    wipe_temp()
    

# Downloads all files that were created on a given date
def download_files_from_date():
    check_date = [download_date.get()[0:2], download_date.get()[3:5], download_date.get()[6:10]]
    csv_files = []
    os.chdir(os.getcwd() + '/Temp_Files')

    for f in ftp.nlst():
        csv_files.append(f)
        with open(f, "wb") as newfile:
                ftp.retrbinary(f"RETR {f}", newfile.write)
    os.chdir('..')
    for file in csv_files:
        if (csv_checker.total_valid(file)):
            file_date = [file[15:17], file[13:15], file[9:13]]
            if (file_date[2] >= check_date[2] and file_date[1] >= check_date[1] and file_date[0] >= check_date[0]):
                if (not os.path.exists(os.getcwd() + "/Valid_Files/" + file)):
                    text_servermsg.insert(END, "\nSuccessfully downloaded file to Valid_Files")
                    shutil.move(os.getcwd() + '/Temp_Files/%s' % file, os.getcwd() +'/Valid_Files/%s' % file)
    wipe_temp()

def download_all_files():
    csv_files = []
    os.chdir(os.getcwd() + '/Temp_Files')
    for f in ftp.nlst():
        csv_files.append(f)
        with open(f, "wb") as newfile:
                ftp.retrbinary(f"RETR {f}", newfile.write)
    os.chdir('..')
    for file in csv_files:
        if (csv_checker.total_valid(file)):
            if (not os.path.exists(os.getcwd() + "/Valid_Files/" + file)):
                text_servermsg.insert(END, "\nSuccessfully downloaded file to Valid_Files")
                shutil.move('Temp_Files/%s' % file, 'Valid_Files/')
    wipe_temp()
        
def validate_file(file):
    if (not csv_checker.filename_check(file)):
        return False
    if (not csv_checker.check_empty_files(file)):
        return False
    if (not csv_checker.check_batch_ids(file)):
        return False
    if (not csv_checker.check_missing_entries(file)):
        return False
    if (not csv_checker.check_time_entry(file)):
        return False
    if (not csv_checker.check_headers(file)):
        return False
    if (not csv_checker.invalid_entries(file)):
        return False
    return True

def wipe_temp():
    shutil.rmtree(os.getcwd() + '/Temp_Files')
    os.mkdir(os.getcwd() + '/Temp_Files')

# Closes FTP server connection
def close_connection():
    try:
        text_servermsg.insert(END,"\nClosing connection...\n")
        text_servermsg.insert(END,ftp.quit())
    except:
        text_servermsg.insert(END,"\nUnable to disconnect")
# ==================================

# Downloading From Date ============
# Creates a new window, prompting the user to enter a date to download the files from.
def create_date_download_window():
    date_download_window = Toplevel(window)
    date_download_window.title("FTP Client - Download from Date")
    
    # Defining widgets
    dent_download_date = DateEntry(date_download_window, width=12, bg="darkblue", fg="white", borderwidth=2, textvariable=download_date)
    #clndr_download_date = Calendar(date_download_window)
    btn_submit_date = Button(date_download_window, text="Download all files from Date", bg="#37c92c", command=download_files_from_date, padx=5, pady=5)

    dent_download_date.grid(padx=10, pady=5)
    #clndr_download_date.grid()
    btn_submit_date.grid(padx=10, pady=10)
# ==================================


# Scheduling Methods ===============
# Creates a new window with options for setting a scheduled task.
def create_schedule_window():
    schedule = Toplevel(window)
    schedule.title("FTP Client - Scheduler")
    schedule.geometry("280x140")

    # Defining Widgets ============
    lbl_start_date = Label(schedule, text="Start Date")
    dent_start_date = DateEntry(schedule, width=12, bg="darkblue", fg="white", borderwidth=2, textvariable=start_date)

    lbl_start_time = Label(schedule, text="Start Time")
    lbl_start_hour = Label(schedule, text="Hour")
    lbl_start_minute = Label(schedule, text="Min")
    spn_schedule_start_hour = Spinbox(schedule, width=3, wrap=True, from_=0, to=23, textvariable=start_hour)
    spn_schedule_start_minute = Spinbox(schedule, width=3, wrap=True, from_=0, to=59, textvariable=start_minute)

    lbl_repeat_delay = Label(schedule, text="Repeat Delay")
    cmb_repeat_delay = ttk.Combobox(schedule, values=["Daily", "Weekly"], width=8, textvariable=repeat_delay)
    cmb_repeat_delay.current(0) # Sets default value to "Daily"

    btn_schedule_submit = Button(schedule, text="Submit", command=submit_schedule, width=15, bg="#37c92c", padx=5, pady=5, anchor=CENTER)
    # =============================
    

    # Placing Widgets =============
    lbl_start_date.place(x=10, y=10)
    dent_start_date.place(x=10, y=30)

    lbl_repeat_delay.place(x=115, y=60)
    cmb_repeat_delay.place(x=195, y=60)

    lbl_start_time.place(x=120, y=10)
    lbl_start_hour.place(x=120, y=30)
    lbl_start_minute.place(x=200, y=30)
    spn_schedule_start_hour.place(x=155, y=30)
    spn_schedule_start_minute.place(x=230, y=30)

    btn_schedule_submit.place(x=140, y=95)
    # =============================


# Triggered when the user presses the submit button when setting up a schedule
def submit_schedule():
    time = ""
    if (len(start_hour.get()) != 2):
        time += "0"
    time += start_hour.get() + ":"
    if (len(start_minute.get()) != 2):
        time += "0"
    time += start_minute.get()


    if (repeat_delay.get() == "Daily"):
        os.system(f'schtasks /Create /SC DAILY /TN "My Task" /TR "task.bat" /SD %s /ST %s' % (start_date.get(), time))
    else:
        os.system(f'schtasks /Create /SC MONTHLY /TN "My Task" /TR "task.bat" /SD %s /ST %s' % (start_date.get(), time))
    
    # If there is no batch file, create it. ?? I think (:
    # Then create the scheduled task using schtasks. https://docs.microsoft.com/en-us/windows/win32/taskschd/schtasks
    # os.system(f'schtasks /Create /SC DAILY /TN "My Task" /TR "task.bat" /ST 09:00')
# ==================================


# ======== MAIN WINDOW SETUP ========
window = Tk()
window.title("FTP Client")
window.geometry("970x560")

# Defining Variables =======================
start_date = StringVar()
start_hour = StringVar()
start_minute = StringVar()
repeat_type = StringVar()
repeat_delay = StringVar()

download_date = StringVar()
# ==========================================

# Connect
lbl_ip = Label(window, text="IP Address")
ent_ip = Entry(window)
lbl_port = Label(window, text="Port")
ent_port = Entry(window)
btn_connect = Button(window, text="Connect", command=connect_server, bg="#37c92c")

# Server response text box
text_servermsg = Text(window)

# Login
lbl_login = Label(window, text="Username")
ent_login = Entry(window)
lbl_pass = Label(window, text="Password")
ent_pass = Entry(window)
btn_login = Button(window, text="Login", command=login_server, bg="#37c92c")

# Directory listing
lbl_dir = Label(window, text="Directory listing:")
libox_serverdir = Listbox(window, width=40, height=16)

# Options
lbl_input = Label(window, text="Input")
ent_input = Entry(window)
btn_chdir = Button(window, text="Change Directory", command=change_directory,width=15)
btn_updir = Button(window, text="Step Up Directory", command=step_up_directory, width=15)
btn_downfile = Button(window, text="Download File", command=download_file,width=15)
btn_down_from_date = Button(window, text="Download Date", command=create_date_download_window, width=15)
btn_schedule = Button(window, text="Set Schedule", command=create_schedule_window, width=15)
btn_quit = Button(window, text="Disconnect", command=close_connection, width=15, bg="#bd2626", fg="white")

# Place widgets
lbl_ip.place(x=20,y=20)
ent_ip.place(x=20,y=40)
lbl_port.place(x=20,y=60)
ent_port.place(x=20,y=80)
btn_connect.place(x=52,y=110)
text_servermsg.place(x=20,y=150)

lbl_dir.place(x=700,y=143)
libox_serverdir.place(x=700,y=165)

btn_downfile.place(x=700,y=450)
btn_down_from_date.place(x=700,y=480)
btn_schedule.place(x=700, y=510)

btn_updir.place(x=830, y=450)
btn_chdir.place(x=830,y=480)
btn_quit.place(x=830,y=510)
# ==========================================


# Create
window.mainloop()