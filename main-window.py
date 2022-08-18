from tkinter import *
from tkinter import ttk

from tkcalendar import DateEntry

import ftplib
ftp = ftplib.FTP()


# FTP commands =====================
# Attempts to establish a connection to the ftp server with the given details
def connect_server():
    ip = "127.0.0.1"#ent_ip.get()
    port = 21#int(ent_port.get())
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
    user = "testUser"#ent_login.get()
    password = "Pa$$w0rd"#ent_pass.get()
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
    file = libox_serverdir.get(libox_serverdir.curselection())

    down = open(file, "wb")
    try:
        text_servermsg.insert(END, "\nDownloading " + file + "...\n")
        text_servermsg.insert(END, ftp.retrbinary("RETR " + file, down.write))
    except:
        text_servermsg.insert(END, "\nUnable to download file")
    display_dir()


# Downloads all files that were created on a given date
def download_files_from_date():
    pass

# Closes FTP server connection
def close_connection():
    try:
        text_servermsg.insert(END,"\nClosing connection...\n")
        text_servermsg.insert(END,ftp.quit())
    except:
        text_servermsg.insert(END,"\nUnable to disconnect")
# ==================================


# Scheduling Methods ===============
# Creates a new window with options for setting a scheduled task.
def create_schedule_window():
    schedule = Toplevel(window)
    schedule.title("FTP Client - Scheduler")
    schedule.geometry("300x200")

    # Defining Widgets ============
    lbl_start_date = Label(schedule, text="Start Date")
    dent_start_date = DateEntry(schedule, width=12, background="darkblue", foreground="white", borderwidth=2, textvariable=start_date)

    lbl_start_time = Label(schedule, text="Start Time")
    lbl_start_hour = Label(schedule, text="Hour")
    lbl_start_minute = Label(schedule, text="Min")
    spn_schedule_start_hour = Spinbox(schedule, width=2, wrap=True, from_=0, to=23, textvariable=start_hour)
    spn_schedule_start_minute = Spinbox(schedule, width=2, wrap=True, from_=0, to=59, textvariable=start_minute)

    lbl_repeat_delay = Label(schedule, text="Repeat Delay")
    cmb_repeat_delay = ttk.Combobox(schedule, values=["Daily", "Weekly", "Monthly"], width=8, textvariable=repeat_delay)
    cmb_repeat_delay.current(0) # Sets default value to "Daily"

    btn_schedule_submit = Button(schedule, text="Submit", command=submit_schedule)
    # =============================
    

    # Placing Widgets =============
    lbl_start_date.place(x=10, y=10)
    dent_start_date.place(x=10, y=30)

    lbl_repeat_delay.place(x=120, y=130)
    cmb_repeat_delay.place(x=200, y=130)

    lbl_start_time.place(x=120, y=10)
    lbl_start_hour.place(x=120, y=30)
    lbl_start_minute.place(x=200, y=30)
    spn_schedule_start_hour.place(x=155, y=30)
    spn_schedule_start_minute.place(x=230, y=30)

    btn_schedule_submit.place(x=240, y=160)
    # =============================


# Triggered when the user presses the submit button when setting up a schedule
def submit_schedule():
    print(start_date.get(), start_hour.get(), start_minute.get(), repeat_type.get(), repeat_delay.get())
    # If there is no batch file, create it. ?? I think (:
    # Then create the scheduled task using schtasks. https://docs.microsoft.com/en-us/windows/win32/taskschd/schtasks
    # os.system(f'SchTasks /Create /SC DAILY /TN "My Task" /TR "task.bat" /ST 09:00')
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
# ==========================================

# Connect
lbl_ip = Label(window, text="IP Address")
ent_ip = Entry(window)
lbl_port = Label(window, text="Port")
ent_port = Entry(window)
btn_connect = Button(window, text="Connect", command=connect_server)

# Server response text box
text_servermsg = Text(window)

# Login
lbl_login = Label(window, text="Username")
ent_login = Entry(window)
lbl_pass = Label(window, text="Password")
ent_pass = Entry(window)
btn_login = Button(window, text="Login", command=login_server)

# Directory listing
lbl_dir = Label(window, text="Directory listing:")
libox_serverdir = Listbox(window, width=40, height=16)

# Options
lbl_input = Label(window, text="Input")
ent_input = Entry(window)
btn_chdir = Button(window, text="Change Directory", command=change_directory,width=15)
btn_updir = Button(window, text="Step Up Directory", command=step_up_directory, width=15)
btn_downfile = Button(window, text="Download File", command=download_file,width=15)
btn_down_from_date = Button(window, text="Download Date", command=download_files_from_date, width=15)
btn_schedule = Button(window, text="Set Schedule", command=create_schedule_window, width=15)
btn_quit = Button(window, text="Disconnect", command=close_connection,width=15)

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
