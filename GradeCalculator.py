import PySimpleGUI as sg   # import PySimpleGUI library and alias it as sg
import tkinter as tk   # import tkinter library and alias it as tk
import databasefunctions as dbf   # import databasefunctions library and alias it as dbf
import sqlite3 as sql  # import sqlite3 library and alias it as sql
import os  # import os library



# Define a class named HomePage
class HomePage:
    def __init__(self):   # Constructor function for the HomePage class 
        # Create the database if it does not exist
        database = "GradeCalculator.db"
        conn = sql.connect(database)
        # create a cursor object
        cur = conn.cursor()
        # committing changes and closing the connection to the database file
        conn.commit()
        # close the database connection
        conn.close()

        # Create the window
        window = tk.Tk()
        window.title("Grade Calculator")

        # Class list creation
        class_list = []

        # Create a label widget
        label = tk.Label(window, text="Grade Calculator")

        # Add the label widget to the window
        label.pack(padx=10, pady=10)

        # Create a button widget
        button = tk.Button(window, text="Exit", command=window.quit)

        add_class_button = tk.Button(window, text="Add Class", command=self.addClassViewer)   # Create a button widget with the given text and command
        add_class_button.pack(padx=10, pady=10)   # Add the button widget to the window with the given padding values

        view_class_button = tk.Button(window, text="View Classes", command=self.classViewer)   # Create a button widget with the given text and command
        view_class_button.pack(padx=10, pady=10)   # Add the button widget to the window with the given padding values

        # Add the button widget to the window
        button.pack(padx=10, pady=10)

        # Start the event loop
        window.mainloop()

    # Define a method called addClassViewer
    def addClassViewer(self):
        root = AddClassPage()
        root.mainloop()
        

    # Define a method called classViewer
    def classViewer(self):
        root = ViewClassesPage()
        root.mainloop()


# Class for the view classes page
class ViewClassesPage(HomePage):
    def __init__(self):

        # Create the window
        window = tk.Tk()
        window.title("View Classes")

        # Create a label widget
        label = tk.Label(window, text="View Classes")

        # Add the label widget to the window
        label.pack(padx=10, pady=10)


        # for i in range(len(class_list)):
        #     #create a button widget
        #     button = tk.Button(window, text= class_list(i), command=viewGrades)


        # Create a button widget
        button = tk.Button(window, text="Exit", command=window.quit)

        # Add the button widget to the window
        button.pack(padx=10, pady=10)

        # Start the event loop
        window.mainloop()

        def viewGrades(self):
            print("View Grades")


class AddClassPage(HomePage):
    def __init__(self):
        # Connect to database and add a new table if it does not exist
        database = "GradeCalculator.db"
        conn = sql.connect(database)
        # create a cursor object
        cur = conn.cursor()

        cur.execute(""" CREATE TABLE IF NOT EXISTS classes (
            class_name text,
            credit_hours integer
            )
        """)
        # committing changes and closing the connection to the database file
        conn.commit()
        # close the database connection
        conn.close()
    
        # Create the window
        self.window = tk.Tk()
        self.window.title("Add Class")

        # Create a label widget
        self.label = tk.Label(self.window, text="Add Class")

        # Add the label widget to the window
        self.label.pack(padx=10, pady=10)

        # Create a ClassName Variable to hold the new class name
        self.ClassName = tk.StringVar()

        self.name_label = tk.Label(self.window, text= "Enter Name of Class")
        self.name_label.pack(padx=10)


        # Create a Name entry widget
        self.name_entry = tk.Entry(self.window, width=20, textvariable=self.ClassName)
        self.name_entry.pack(padx=10, pady=5)

        # Create an entry button
        self.entryButton = tk.Button(self.window, text="Enter", command = self.nameEnter)
        self.entryButton.pack(padx=10, pady=10)

        # Create a CreditHours Variable to hold the credit hours
        self.CreditHours = tk.StringVar()

        self.credit_label = tk.Label(self.window, text= "Enter Credit Hours")
        self.credit_label.pack(padx=10)

        # Create a CreditHours entry widget
        self.credit_entry = tk.Entry(self.window, width=20, textvariable=self.CreditHours)
        self.credit_entry.pack(padx=10, pady=5)

        # Create an entry button
        self.entryButton2 = tk.Button(self.window, text="Enter", command = self.creditEnter)
        self.entryButton2.pack(padx=10, pady=10)

        # Create a button widget
        self.button = tk.Button(self.window, text="Exit", command=self.window.quit)

        # Add the button widget to the window
        self.button.pack(padx=10, pady=10)
       
        # Start the event loop
        self.window.mainloop()
        


    def nameEnter(self):
        print(self.name_entry.get())## CHECK OVER THIS LATER FUNCTIONS ON INPUT TEXT VARIABLES
    
    def creditEnter(self):
        print(self.credit_entry.get())


if __name__=='__main__':
    my_gui = HomePage()

