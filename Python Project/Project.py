import mysql.connector as mysql_con
import datetime
from tkinter import *
from tkinter import messagebox
import random
# -----------------------------------------------------------------
db = mysql_con.connect(host="localhost", user="root", passwd="1234", database="test")  # python ki database
con = db.cursor()  # giving connector to data
con.execute("USE test")
todaydate = datetime.date.today()
# ------------------------------------------------------------------
root = Tk()
root.geometry("600x560")
root.title("Python Project")

colors = ["black", "white", "cyan", "#856ff8", "#ffff00"]  # List of colors


def fun():
    root['background'] = random.choice(colors)  # picks up random color


# Creating a photoimage object to use image
photo = PhotoImage(file=r"C:\\Users\\j v v m syam prasad\\OneDrive\Desktop\\MANIT Logo.png")
# here, image option is used to
# set image on button
# Button(root, image = photo,command=lambda:(root.config(bg=random.choice(colors)))).grid(row=0,column=1)
Button(root, image=photo, command=lambda: (root.config(fun()))).grid(row=0, column=1)
# -----------------------------Notification----------------------------------
sql = "SELECT wname FROM WORK WHERE ddate = '{}'AND status='{}'".format(todaydate,0)
con.execute(sql)
pend = ""
pend_all = con.fetchall()
for i in range(0, len(pend_all)):
    for j in range(0, len(pend_all[i])):
        pend += str(pend_all[i][j]) + ","
if con.rowcount != 0:
    messagebox.showinfo("Due Today", "assignments :-" + pend + "is today")


# --------------------------------FUNCTIONS---------------------------------------
def nearest_search_result(subcode, subname):
    z = "No subject found. Nearest search results are:-\n\n"
    z += "Sub Code".ljust(19, ' ') + "Sub Name".ljust(19, ' ') + "Lab".ljust(19, ' ') + "Assigned date".ljust(19,' ') + "Due date".ljust(19, ' ') + "\n\n"
    x = "%" + subcode + "%"
    y = "%" + subname + "%"
    sql = 'SELECT subcode,wname,labno,adate,ddate FROM work WHERE subcode LIKE "{}" OR wname LIKE "{}"'.format(x, y)
    con.execute(sql)
    res = con.fetchall()
    for i in range(0, len(res)):
        for j in range(0, len(res[0])):
            z += res[i][j].ljust(22, ' ')
        z += "\n"
    return z


def add_entry():
    #  Toplevel(parameter) -->creates new window  ,parameter-->parent window
    NewWin = Toplevel(root)
    NewWin.geometry("600x400")
    NewWin.title("Add Assignment")
    Label(NewWin,text="Enter Subject Code, Subject Name, Lab Number, Assigned Date, Due Date\nDate Format:- YYYY-MM-DD").grid(row=0, column=1)
    Label(NewWin, text="Subject Code").grid()
    Label(NewWin, text="Subject Name").grid()
    Label(NewWin, text="Lab number").grid()
    Label(NewWin, text="Assigned Date").grid()
    Label(NewWin, text="Due Date").grid()

    sub_code = StringVar()
    sub_name = StringVar()
    lab_no = StringVar()
    assigned_date = StringVar()
    due_date = StringVar()

    Entry(NewWin, textvariable=sub_code).grid(row=1, column=1)
    Entry(NewWin, textvariable=sub_name).grid(row=2, column=1)
    Entry(NewWin, textvariable=lab_no).grid(row=3, column=1)
    Entry(NewWin, textvariable=assigned_date).grid(row=4, column=1)
    Entry(NewWin, textvariable=due_date).grid(row=5, column=1)

    def add(subcode, wname, labno, adate, ddate):
        # Here comes the hero(SQL)
        sql = "INSERT INTO work(subcode,wname,labno,adate,ddate) VALUES(%s,%s,%s,%s,%s)"
        val = (subcode, wname, labno, adate, ddate)
        con.execute(sql, val)
        db.commit()
        Label(NewWin, text="Assignment is added in schedule").grid(row=6, column=1)
        messagebox.showinfo("Notification", "New Assignment is added")

    Button(NewWin, text="Submit", command=lambda: add(sub_code.get(), sub_name.get(), lab_no.get(), assigned_date.get(),due_date.get())).grid()
    Button(NewWin, text="Exit", command=NewWin.destroy).grid()


def Submit_Assignment():
    NewWin = Toplevel(root)
    NewWin.geometry("900x550")
    NewWin.title("Change Assignment Status")
    Label(NewWin, text="Enter subject code and Lab no").grid(row=0, column=1)
    Label(NewWin, text="Subject Code").grid(row=1, column=0)
    Label(NewWin, text="Lab number").grid(row=1, column=3)

    sub_code = StringVar()
    lab_no = StringVar()

    Entry(NewWin, textvariable=sub_code).grid(row=1, column=1)
    Entry(NewWin, textvariable=lab_no).grid(row=1, column=4)
    Button(NewWin, text="Turn in", command=lambda: status(sub_code.get(), lab_no.get(), "1")).grid(row=1, column=6)
    Button(NewWin, text="Undo Turn in", command=lambda: status(sub_code.get(), lab_no.get(), "0")).grid(row=1, column=7)

    def status(subcode, labno, x):
        sql = "UPDATE work SET status = '{}' WHERE subcode = '{}' and labno = '{}'".format(x, subcode, labno)
        con.execute(sql)
        db.commit()
        res = ""
        if con.rowcount == 0:
            res += nearest_search_result(subcode, "blank_space")
        else:
            if x == "1":
                res += "Successfully Turned in"
            else:
                res += "Turned out :("
        text = Text(NewWin, font="Calibri 12", height=25, width=100)
        text.insert(INSERT, res)
        text.grid(row=2, column=0, padx=20, columnspan=20)


def search_entry():
    NewWin = Toplevel(root)
    NewWin.geometry("900x550")
    NewWin.title("Search Assignment")
    val = StringVar()
    Label(NewWin, text="Enter subject code or subject name").grid(row=0, column=0)
    Entry(NewWin, textvariable=val).grid(row=0, column=1, padx=20)
    text = Text(NewWin, font=("Calibri 12"), width=100, height=25)
    Button(NewWin, text="Search", command=lambda: search(val.get())).grid(row=0, column=2, padx=20)
    Button(NewWin, text="Clear", command=lambda: text.delete(1.0, END)).grid(row=0, column=3, padx=20)

    def search(val):
        sql = 'SELECT subcode,wname,labno,adate,ddate,status FROM work WHERE subcode = "{}" OR wname = "{}"'.format(val,val)
        con.execute(sql)
        res = con.fetchall()  # res-->many tuples
        x = "Sub Code".ljust(20, ' ') + "Sub Name".ljust(20, ' ') + "Lab".ljust(20, ' ') + "Assigned date".ljust(20,' ') + "Due date".ljust(20, ' ') + "Status".ljust(20, ' ') + '\n'
        for i in range(0, len(res)):  # how many tuples
            for j in range(0, len(res[0]) - 1):  # no. of var in each tuple
                x += res[i][j].ljust(22, ' ')
            if res[i][5] == 0:
                x += "\tNot submitted\n"
            else:
                x += "\tSubmitted\n"
        if con.rowcount == 0:
            x = nearest_search_result(val, val)
        text.insert(INSERT, x)
        text.grid(row=2, column=0, columnspan=30, padx=20)


def completed_and_pending(option):
    NewWin = Toplevel(root)
    NewWin.title("Completed or Pending Assignments")
    NewWin.geometry("900x550")
    x = ""  # empty
    sql = 'SELECT subcode,wname,labno,adate,ddate FROM work WHERE status = {}'.format(option)
    con.execute(sql)
    res = con.fetchall()
    if option == 0:
        x += "Total No. of Pending Assignements are {}\n\n".format(con.rowcount)
    else:
        x += "Total No. of Completed Assignements are {}\n\n".format(con.rowcount)
    x += "Sub Code".ljust(22, ' ') + "Sub Name".ljust(22, ' ') + "Lab".ljust(22, ' ') + "Assigned date".ljust(22,' ') + "Due date" + '\n'
    for i in range(0, len(res)):
        for j in range(0, len(res[0])):
            x += res[i][j].ljust(26, ' ')
        x += "\n"
    text = Text(NewWin, font=("Calibri 12"), height=25, width=100)
    text.insert(INSERT, x)
    text.grid(row=2, column=1, padx=20, pady=30)
    text.config(state="disabled")


def Existing_lab_details():
    NewWin = Toplevel(root)
    NewWin.geometry("490x500")
    NewWin.title("All assignments details")
    sql = "SELECT DISTINCT subcode,wname,labno FROM work"
    con.execute(sql)
    res = con.fetchall()
    x = ""
    x += "Code".ljust(20, ' ') + "Name".ljust(20, ' ') + "Lab No".ljust(20, ' ') + '\n'
    for i in range(0, len(res)):
        for j in range(0, len(res[0])):
            x += res[i][j].ljust(20, ' ')
        x += "\n"
    text = Text(NewWin, font="Calibri 12", height=25, width=50)
    text.insert(INSERT, x)
    text.grid(row=2, column=1, padx=40, columnspan=30)
    text.config(state="disabled")


def remove_completed():
    sql = "DELETE FROM work WHERE status = 1"
    con.execute(sql)
    db.commit()
    Label(root, text="Assignments are removed").grid(row=6, column=1, columnspan=2)


def update_entry(option):
    NewWin = Toplevel(root)
    NewWin.geometry("550x500")
    NewWin.title("Change Assignment Details")
    Label(NewWin, text="Enter subject code and Lab no").grid(row=0, column=1)
    Label(NewWin, text="Subject Code").grid(row=1, column=0)
    Label(NewWin, text="Lab number").grid(row=1, column=3)

    sub_code = StringVar()
    lab_no = StringVar()

    Entry(NewWin, textvariable=sub_code).grid(row=1, column=1)
    Entry(NewWin, textvariable=lab_no).grid(row=1, column=4)

    def update(subcode, labno, option):
        sql = "DELETE FROM work WHERE subcode='{}' AND labno='{}'".format(subcode, labno)
        con.execute(sql)
        db.commit()
        if con.rowcount != 0:
            if option == 0:
                Label(NewWin, text="Assignment is deleted Enter new values", font="Arial 10").grid(row=3, columnspan=10)
                add_entry()
            else:
                Label(NewWin, text="Assignment is deleted", font="Arial 10").grid(row=3, columnspan=10)
        else:
            Label(NewWin, text="No assignment is found", font="Arial 10").grid(row=3, columnspan=10)
            messagebox.showwarning("Error", "No Assignment is found")

    if option==0 :
        Button(NewWin, text="Update", command=lambda: update(sub_code.get(), lab_no.get(), option)).grid(row=1, column=6)
    else :
        Button(NewWin, text="Delete", command=lambda: update(sub_code.get(), lab_no.get(), option)).grid(row=1, column=6)


root.config(bg="white")

label = Label(root, text="Assignments", font=("25"))
label.grid(row=1, column=1)

bn1 = Button(root, text="Add Assignment", font=("Arial", "10"), command=lambda: add_entry())
bn1.grid(row=2, column=0, padx=50, pady=30)

bn2 = Button(root, text="Search Assignments", font=("Arial", "10"), command=lambda: search_entry())
bn2.grid(row=2, column=2)

bn3 = Button(root, text="Submit Assignment", font=("Arial", "10"), command=lambda: Submit_Assignment())
bn3.grid(row=3, column=0, padx=50, pady=30)

bn4 = Button(root, text="Pending Assignments", font=("Arial", "10"), command=lambda: completed_and_pending(0))
bn4.grid(row=3, column=2)

bn5 = Button(root, text="Completed Assignments", font=("Arial", "10"), command=lambda: completed_and_pending(1))
bn5.grid(row=4, column=0, padx=50, pady=30)

bn6 = Button(root, text="Update Assignment Details", font=("Arial", "10"), command=lambda: update_entry(0))
bn6.grid(row=4, column=2)

bn7 = Button(root, text="Existing lab details", font=("Arial", "10"), command=lambda: Existing_lab_details())
bn7.grid(row=5, column=0, padx=50, pady=30)

bn8 = Button(root, text="Remove completed Assignments", font=("Arial", "10"), command=lambda: remove_completed())
bn8.grid(row=5, column=2)

bn9 = Button(root, text="Remove Assignment", font=("Arial", "10"), command=lambda: update_entry(1))
bn9.grid(row=6, column=0, padx=50, pady=30)

root.mainloop()