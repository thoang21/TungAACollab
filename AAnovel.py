"""
Tung Hoang - 03/12/20
The following program is the console of an book searching and adding application.
The user will be able to request a book report and add a new novel from existing author
Show that I know how to edit and commit my code

Citation:
Tabulate table: https://pypi.org/project/tabulate/#files
Adding variable to SQL: 
"""


import sqlite3 as sq
from datetime import datetime, date
from tabulate import tabulate

# MODEL:  the following functions can be used by ANY front end using the SQL Database
# identify location of database
con = sq.connect("../AAColab/AAnovel.db")
c = con.cursor()

def get_count_book():
    res = c.execute("SELECT COUNT(*) from Book")
    data = c.fetchall() # Gets the data from the table
    return data

def get_writers():
    res = c.execute("SELECT * from Writer")
    data = c.fetchall() # Gets the data from the table
    return data

def check_writer(wtid):
    res = c.execute("SELECT WriterID from Writer")
    writerIDs = c.fetchall() # Gets the data from the table
    for wt in writerIDs:
        if wtid in wt:
            return True
    return False

def check_book(t, g, w):
    dataSet = (str(t), str(g), int(w))
    res = c.execute("SELECT Title, Genre, WriterID from Book")
    bookData = c.fetchall() # Gets the data from the table
    
    if dataSet in bookData:
        return True
    else:
        return False
    
def get_books(key):
    res = c.execute("SELECT BookID, Title, Genre, Name FROM Book, Writer WHERE Book.WriterID = Writer.WriterID AND Book.Title LIKE ?;",('%' + str(key) + '%',))
    data = c.fetchall() # Gets the data from the table
    return data

def add_book(book, title, genre, writer):
    c.execute("INSERT INTO Book (BookID, Title, Genre, WriterID) Values (?, ?, ?, ?);",(str(book), str(title), str(genre), str(writer)))
            #DO THIS COMMIT ANY TIME YOU CHANGE THE DATABASE - after a complete transaction!!!


# The following VIEW functions are specific to a console based application
#main menu
def render_menu():
    # Welcome messgae
    print('\n"""\n-----------------------------------------')
    print("Welcome to our book searching and adding system")
    print('-----------------------------------------\n"""')

    print("1. Find a novel")
    print("2. Add a novel")
    print("3. Exit")

    choice = input("Choose an option:\t")
    
    if choice.isdigit():
        choice = int(choice)
        if choice == 1:
            render_book_report()
        elif choice == 2:
            render_adding_request()
        elif choice == 3:
            end_program()
            return False;
        else:
            print("<<<<<<Error. Please only enter interger number within choice>>>>>>")
        
    else:
        print("<<<<<<Error. Please only enter integer number>>>>>>")
        
    return True;


def end_program():
    print('\n"""\n----------------------------------')
    print("Thank you for your visit")
    print('----------------------------------\n"""')
    con.close()

"""
-----------------------------------------
This is the function that render a report
-----------------------------------------
"""
def render_book_report():
    # This report can be much prettier!!
    keyword = input("\n\nEnter a keyword for a specific search. If you want the full library, don't put any entry.\nPlease enter a keyword:\t\t")
    books = get_books(keyword)
    
    if books != []:
        print("\nReport results")
        print(tabulate(books, headers=['BookID','Title','Genre','Author'], tablefmt='orgtbl'))
    else:
        print("\n------\nSorry, we cannot find any book with that keyword\n------")
"""
-----------------------------------------
This is the set of function to add a book
-----------------------------------------
"""
def render_adding_request():
    # This will populate the author and  listbox
    writers = get_writers()
    writerchoice = writer_lb(writers)

    title = input("\n\nPlease enter the title:\t")
    genre = input("\n\nPlease enter the genre:\t")

    bookID = int(get_count_book()[0][0]) + 1
    
    check_and_enter_book(bookID, title, genre, writerchoice)
    
def writer_lb(writers):
    print("\n\nWriters\n")
    for row in writers:
        print(row)
    writer = input("\nChoose the writer by ID num:\t")
    
    while not(writer.isdigit() and check_writer(int(writer))):
        print("<<<<<<Error! Please try again!>>>>>>")
        writer = input("Choose the writer by ID num:\t")

    return writer

# The following CONTROLLER functions can be used by any front end and any database
def check_and_enter_book(bk, t, g, w):
    
    if not(check_book(t, g, w)):
        add_book(bk, t, g, w)
        print("Success!", "Your book has been added!")
    else:
        print("\nError! Try again!", "Possible errors:  \nThe book is already register \nYou choose an nonexisting writerID")
        return


"""
--------------------
Main code start here
--------------------
"""
# Start here: loop the main menu until the user choses the exit option
while(render_menu()):
    print('')
