from tkinter import *
import ftplib
ftp = ftplib.FTP()


def connect_server():
    pass
    ip = ent_ip.get()
    port = int(ent_port.get())
    try:
       msg = ftp.connect(ip,port)
       text_servermsg.insert(END,"\n")
       text_servermsg.insert(END,msg)
       lbl_login.place(x=150,y=20)
       ent_login.place(x=150,y=40)
       lbl_pass.place(x=150,y=60)
       ent_pass.place(x=150,y=80)
       btn_login.place(x=182,y=110)
    except:
       text_servermsg.insert(END,"\n")
       text_servermsg.insert(END,"Unable to connect")


def login_server():
    user = ent_login.get()
    password = ent_pass.get()
    try:
        msg = ftp.login(user,password)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,msg)
        display_dir()
        lbl_login.place_forget()
        ent_login.place_forget()
        lbl_pass.place_forget()
        ent_pass.place_forget()
        btn_login.place_forget()
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to login")

        
def display_dir():
    libox_serverdir.delete(0, END)
    libox_serverdir.insert(0,"--------------------------------------------")
    dirlist = []
    dirlist = ftp.nlst()
    for item in dirlist:
        libox_serverdir.insert(0, item)


#FTP commands
def change_directory():
    directory = ent_input.get()
    try:
        msg = ftp.cwd(directory)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,msg)
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to change directory")
    display_dir()


def create_directory():
    directory = ent_input.get()
    try:
        msg = ftp.mkd(directory)
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,msg)
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to create directory")
    display_dir()


def download_file():
    file = ent_input.get()
    down = open(file, "wb")
    try:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Downloading " + file + "...")
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,ftp.retrbinary("RETR " + file, down.write))
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to download file")
    display_dir()


def create_schedule_window():
    # ======== SCHEDULE WINDOW SETUP ========
    schedule = Toplevel(window)
    schedule.title("FTP Client - Set up Schedule")
    schedule.geometry("300x200")

    # Repeat Options
    # repeate_type: 0-Days | 1-Weeks | 2-Months
    repeat_type = 0

    spn_repeat_value = Spinbox(schedule, width=5)
    lbl_repeatmsg1 = Label(schedule, text="Repeat every: ")
    lbl_repeatmsg2 = Label(schedule, text="days")

    # IDK where the combobox went but i need it so ill need to find out where the fuck it went and who took it then find their house and intimidate them with my towering stature and greek god like physique into putting the comboboxes back into tkinter
    # cmb_repeat_type = Combobox(schedule, values=["days", "weeks", "months"])
    
    # rad_daily = Radiobutton(schedule, text="Daily", variable=repeat_type, value=0, command=lbl_repeatmsg2.config(text="days"))
    # rad_weekly = Radiobutton(schedule, text="Weekly", variable=repeat_type, value=1, command=lbl_repeatmsg2.config(text="weeks"))
    # rad_monthly = Radiobutton(schedule, text="Monthly", variable=repeat_type, value=2, command=lbl_repeatmsg2.config(text="months"))

    # Placing Widgets
    # rad_daily.place(x=20, y=40)
    # rad_weekly.place(x=20, y=60)
    # rad_monthly.place(x=20, y=80)
    
    
    # cmb_repeat_type.place(x=100, y=100)
    spn_repeat_value.place(x=180, y=160)
    lbl_repeatmsg1.place(x=100, y=160)
    lbl_repeatmsg2.place(x=230, y=160)
    # ==========================================


def set_schedule():
    create_schedule_window()

    
    # If there is no batch file, create it.
    # Then create the scheduled task using schtasks.
    # os.system(f'SchTasks /Create /SC DAILY /TN "My Task" /TR "task.bat" /ST 09:00')


def update_repeat_text(label_name, value):
    label_name.text=value


def close_connection():
    try:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Closing connection...")
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,ftp.quit())
    except:
        text_servermsg.insert(END,"\n")
        text_servermsg.insert(END,"Unable to disconnect")




# ======== MAIN WINDOW SETUP ========
window = Tk()
window.title("FTP Client")
window.geometry("1000x600")

#Connect
lbl_ip = Label(window, text="IP Address")
ent_ip = Entry(window)
lbl_port = Label(window, text="Port")
ent_port = Entry(window)
btn_connect = Button(window, text="Connect", command=connect_server)

#Server response text box
text_servermsg = Text(window)

#Login
lbl_login = Label(window, text="Username")
ent_login = Entry(window)
lbl_pass = Label(window, text="Password")
ent_pass = Entry(window)
btn_login = Button(window, text="Login", command=login_server)

#Directory listing
lbl_dir = Label(window, text="Directory listing:")
libox_serverdir = Listbox(window,width=40,height=14)

#Options
lbl_input = Label(window, text="Input")
ent_input = Entry(window)
btn_chdir = Button(window, text="Change Directory", command=change_directory,width=15)
btn_crdir = Button(window, text="Create Directory", command=create_directory,width=15)
btn_downfile = Button(window, text="Download File", command=download_file,width=15)
btn_schedule = Button(window, text="Set Schedule", command=set_schedule, width=15)
btn_quit = Button(window, text="Disconnect", command=close_connection,width=15)

#Place widgets
lbl_ip.place(x=20,y=20)
ent_ip.place(x=20,y=40)
lbl_port.place(x=20,y=60)
ent_port.place(x=20,y=80)
btn_connect.place(x=52,y=110)
text_servermsg.place(x=20,y=150)

lbl_dir.place(x=700,y=143)
libox_serverdir.place(x=700,y=165)

btn_schedule.place(x=700,y=510)

lbl_input.place(x=700,y=400)
ent_input.place(x=700,y=420)
btn_chdir.place(x=700,y=450)
btn_crdir.place(x=700,y=480)

btn_downfile.place(x=850,y=450)
btn_quit.place(x=850,y=510)
# ==========================================









#Create
window.mainloop()
