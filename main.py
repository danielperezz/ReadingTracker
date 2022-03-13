import tkinter as tk
from PIL import Image, ImageTk
import mysql.connector
from tkcalendar import *
from datetime import date
from tkinter import ttk
import customtkinter as ctk

COL_NUM = 10
ROW_NUM = 5
GREY = "#595959"
BLUE = "#8FAADC"

# connect to DB
db_connect = mysql.connector.connect(
  host="localhost",
  user="root",
  password="@0406sbhtk2001prz55",
  database="mybooks"
)

# kind of pointer to the db, used to execute related commands
mycursor = db_connect.cursor()

# mycursor.execute("CREATE TABLE books (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), author VARCHAR(255), startDate DATE, endDate DATE, ranking INT(255), commonplace CHAR)")


# ~~~~~~~~~~~~ functions ~~~~~~~~~~~~~~~ #
def add_book():
    global open_start_date
    global open_end_date
    global commonplace_cb
    # label = tk.Label(root, text="hello")
    # label.grid(column=1, row=2)
    sql = "INSERT INTO books (name, author, startDate, endDate, ranking, commonplace) VALUES (%s, %s, %s, %s, %s, %s)"
    # gett all the info from the entry's
    name = input_name.get()
    author = input_author.get()
    ranking = input_rank.get()
    if ranking == '':
        ranking = None
    start_date = open_start_date.cget("text")
    if start_date == "Set Start Date":
        start_date = None
    end_date = open_end_date.cget("text")
    if end_date == "Set End Date":
        end_date = None
    commonplace = ''
    if is_checked.get():
        commonplace = 'V'
    # update the database
    mycursor.execute(sql, (name, author, start_date, end_date, ranking, commonplace))
    db_connect.commit()
    added_id = mycursor.lastrowid
    # update the treeview
    books_list.insert('', 'end', values=(added_id, name, author, start_date, end_date, ranking, commonplace))

    clear_entrys()


def clear_entrys():
    input_name.delete(0, 'end')
    input_author.delete(0, 'end')
    open_start_date.config(text="Set Start Date")
    open_end_date.config(text="Set End Date")
    input_rank.delete(0, 'end')
    commonplace_cb.deselect()


def open_start_date_calender(event):
    global open_start_date
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    win = tk.Tk()
    win.geometry("250x230")
    win.config(bg=GREY)
    start_date_cal = Calendar(win, selectmode="day", year=year, month=month, day=day, date_pattern="dd/mm/yy")
    start_date_cal.grid(column=0, row=0, rowspan=3, columnspan=3)
    set_date_button = ctk.CTkButton(master=win, width=120, height=35, border_width=2, corner_radius=8, text="Set Date",
                               command=lambda: [open_start_date.config(text=start_date_cal.get_date()), win.destroy()],
                                    fg_color=GREY, text_color="white", border_color=BLUE,
                               text_font=("Roboto Medium",), hover_color=BLUE)
    set_date_button.grid(column=1, row=4)


def open_end_date_calender(event):
    global open_end_date
    today = date.today()
    year = today.year
    month = today.month
    day = today.day
    win = tk.Tk()
    win.geometry("250x230")
    win.config(bg=GREY)
    end_date_cal = Calendar(win, selectmode="day", year=year, month=month, day=day, date_pattern="dd/mm/yy")
    end_date_cal.grid(column=0, row=0, rowspan=3, columnspan=3)
    set_date_button = ctk.CTkButton(master=win, width=120, height=35, border_width=2, corner_radius=8, text="Set Date",
                               command=lambda: [open_end_date.config(text=end_date_cal.get_date()), win.destroy()],
                                    fg_color=GREY, text_color="white", border_color=BLUE,
                               text_font=("Roboto Medium",), hover_color=BLUE)
    set_date_button.grid(column=1, row=4)


def update_table():
    mycursor.execute("SELECT id, name, author, DATE_FORMAT(startDate, '%d/%m/%y'), DATE_FORMAT(endDate, '%d/%m/%y'),"
                     " ranking, commonplace FROM books")
    rows = mycursor.fetchall()
    for data in rows:
        books_list.insert('', 'end', values=data)


def select_record():
    clear_entrys()
    selected = books_list.focus()
    selected_values = books_list.item(selected, 'values')
    # insert the values of the selected item to the entry's
    input_name.insert(0, selected_values[1])
    input_author.insert(0, selected_values[2])
    open_start_date.config(text=selected_values[3])
    open_end_date.config(text=selected_values[4])
    input_rank.insert(0, selected_values[5])
    if selected_values[6] == 'V':
        commonplace_cb.select()


def update_record():
    update_selected = books_list.focus()
    update_selected_values = books_list.item(update_selected, 'values')
    update_selected_id = update_selected_values[0]

    name = input_name.get()
    author = input_author.get()
    ranking = input_rank.get()
    start_date = open_start_date.cget("text")
    end_date = open_end_date.cget("text")
    commonplace = ''
    if is_checked.get():
        commonplace = 'V'
    update_sql_command = "UPDATE books SET name=%s, author=%s, startDate=%s, endDate=%s," \
                         " ranking=%s, commonplace=%s WHERE id=%s"
    mycursor.execute(update_sql_command, (name, author, start_date, end_date, ranking, commonplace, update_selected_id))
    db_connect.commit()

    books_list.item(update_selected, text="", values=(update_selected_values[0], name, author, start_date, end_date,
                                                      ranking, commonplace))
    clear_entrys()


def delete_record():
    delete_selected = books_list.focus()
    delete_selected_values = books_list.item(delete_selected, 'values')
    delete_selected_id = delete_selected_values[0]

    mycursor.execute("DELETE FROM books WHERE id=%s", (delete_selected_id,))
    db_connect.commit()

    books_list.delete(delete_selected)


# ~~~~~~~~~~~ start the main window ~~~~~~~~~~ #
# a kind of pointer to the window
root = tk.Tk()
root.title(" My Reading Tracker")
root.rowconfigure(15)
root.columnconfigure(10)
root.configure(bg=GREY)
root.geometry("1920x1080")

for col in (0, 10):
    root.grid_columnconfigure(col, minsize=50)

for row in (0, 15):
    root.grid_rowconfigure(row, minsize=80)

# ~~~~ logo ~~~~~ #
root.iconbitmap('C:/Users/danie/PycharmProjects/readingTracker/logo.ico')
# ~~~~ heading ~~~~~ #
img_canvas = tk.Canvas(bg=GREY)
img_canvas.grid(column=0, row=0, columnspan=15, rowspan=2)
logo = ImageTk.PhotoImage(Image.open('anotherlogo.png'))
logo_label = tk.Label(img_canvas, image=logo, bg=GREY)
logo_label.image = logo
logo_label.grid(column=0, row=0, rowspan=8, columnspan=2)

# ~~~~~ buttons ~~~~~ #
addBook_button = ctk.CTkButton(master=root, width=150, height=40, border_width=2, corner_radius=8, text="Add a New Book",
                               command=add_book, fg_color=GREY, text_color="white", border_color=BLUE,
                               text_font=("Roboto Medium",), hover_color=BLUE)
addBook_button.grid(column=8, row=6)

select_button = ctk.CTkButton(master=root, width=70, height=30, border_width=2, corner_radius=8, text="Edit",
                               command=select_record, fg_color=GREY, text_color="white", border_color=BLUE,
                               text_font=("Roboto Medium",), hover_color=BLUE)
select_button.grid(column=8, row=5, sticky='W')

update_button = ctk.CTkButton(master=root, width=70, height=30, border_width=2, corner_radius=8, text="Update",
                               command=update_record, fg_color=GREY, text_color="white", border_color=BLUE,
                               text_font=("Roboto Medium",), hover_color=BLUE)
update_button.grid(column=8, row=5, sticky='E')

delete_button = ctk.CTkButton(master=root, width=70, height=30, border_width=2, corner_radius=8, text="Delete",
                               command=delete_record, fg_color=GREY, text_color="white", border_color=BLUE,
                               text_font=("Roboto Medium",), hover_color=BLUE)
delete_button.grid(column=8, row=15, sticky='E')

# ~~~~ input textbox ~~~~ #
name_label = tk.Label(root, font=("Roboto Medium",), text="Book Name", bg=GREY, fg="white")
name_label.grid(row=5, column=1, sticky='W')

# input_name = tk.Entry(root, font="TheSansSemiLight-", width=15)
input_name = ctk.CTkEntry(master=root, placeholder_text="Enter Name", width=200, height=35, border_width=2,
                          corner_radius=10, text_font=("Roboto Medium",), border_color=BLUE)
input_name.grid(column=1, row=6, sticky='W')

author_label = tk.Label(root, font=("Roboto Medium",), text="Author Name", bg=GREY, fg="white")
author_label.grid(row=5, column=2, sticky='W')

input_author = ctk.CTkEntry(master=root, placeholder_text="Enter Author", width=200, height=35, border_width=2,
                          corner_radius=10, text_font=("Roboto Medium",), border_color=BLUE)
input_author.grid(column=2, row=6, sticky='W')


open_start_date = tk.Label(root, font=("Roboto Medium",), text="Set Start Date", bg=GREY, fg="white")
open_start_date.bind("<Button-1>", open_start_date_calender)
open_start_date.grid(column=3, row=6, sticky='W')

open_end_date = tk.Label(root, text="Set End Date", font=("Roboto Medium",), height=2, width=15, bg=GREY, fg="white")
open_end_date.bind("<Button-1>", open_end_date_calender)
open_end_date.grid(column=4, row=6, sticky='W')

input_rank = ctk.CTkEntry(master=root, placeholder_text="Enter Rank", width=200, height=35, border_width=2,
                          corner_radius=10, text_font=("Roboto Medium",), border_color=BLUE)
input_rank.grid(column=5, row=6, sticky='W')

rank_label = tk.Label(root, font=("Roboto Medium",), text="Book Rank", bg=GREY, fg="white")
rank_label.grid(row=5, column=5, sticky='W')

empty_row = tk.Label(root, text="", bg=GREY).grid(row=7, column=0)

# ~~~~~ commonplace checkbox ~~~~~ #
commonplace_label = tk.Label(root, font=("Roboto Medium",), text="CP", bg=GREY, fg="white")
commonplace_label.grid(row=5, column=6, sticky='W')

is_checked = tk.IntVar()
commonplace_cb = ctk.CTkCheckBox(root, fg_color=BLUE, onvalue=1, offvalue=0, bg=GREY, variable=is_checked, text="")
commonplace_cb.grid(column=6, row=6)

# ~~~~ Treeview Frame ~~~~ #
treeview_frame = tk.Frame(root, bg="white")
treeview_frame.grid(row=8, column=1, columnspan=8, rowspan=6)

# ~~~~~~~ scrollbar ~~~~~~ #
tree_scroll = tk.Scrollbar(treeview_frame, orient="vertical", background=GREY)
tree_scroll.grid(row=1, column=7, rowspan=6, sticky='ns')

# ~~~~~ setting the treeview ~~~~~ #
books_list = ttk.Treeview(treeview_frame, columns=("id", "book name", "author", "start date", "end date", "rank", "commonplace"),
                          show='headings', height=10, yscrollcommand=tree_scroll.set)
books_list.grid(row=0, column=0, columnspan=7, rowspan=6, sticky='W')
books_list.column("# 1", anchor='center', width=100)
books_list.heading("# 1", text="ID")
books_list.column("# 2", anchor='center', width=220)
books_list.heading("# 2", text="Book Name")
books_list.column("# 3", anchor='center', width=220)
books_list.heading("# 3", text="Author")
books_list.column("# 4", anchor='center')
books_list.heading("# 4", text="Start Date")
books_list.column("# 5", anchor='center')
books_list.heading("# 5", text="End Date")
books_list.column("# 6", anchor='center', width=100)
books_list.heading("# 6", text="Rank")
books_list.column("# 7", anchor='center', width=100)
books_list.heading("# 7", text="CP")

# ~~~~ Treeview Style ~~~~~ #
style = ttk.Style()
style.theme_use("winnative")
style.configure("Treeview", background="white", foreground="white", rowheight=30, fieldbackground="white",
                font=("Roboto Light",12))
style.configure("Treeview.Heading", font=("Roboto Medium",14), height=50)
style.map('Treeview', background=[('selected', BLUE)])

# ~~~ configure the scrollbar ~~~ #
books_list.config(yscrollcommand=tree_scroll.set)
tree_scroll.config(command=books_list.yview)

# ~~~ Empty Row ~~~ #
# space_label = tk.Label(root, text="", bg=GREY).grid(row=14, column=0)

update_table()

root.mainloop()
db_connect.close()
