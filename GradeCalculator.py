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
        self.window = tk.Tk()
        self.window.title("Grade Calculator")
        self.window.geometry("800x800")


        # Create a label widget
        self.label = tk.Label(self.window, text="Grade Calculator")

        # Add the label widget to the window
        self.label.pack(padx=10, pady=10)

        # Create a button widget
        self.button = tk.Button(self.window, text="Exit", command=self.window.quit)

        self.add_class_button = tk.Button(self.window, text="Add Class", command=self.addClassViewer)   # Create a button widget with the given text and command
        self.add_class_button.pack(padx=10, pady=10)   # Add the button widget to the window with the given padding values

        self.view_class_button = tk.Button(self.window, text="View Classes", command=self.classViewer)   # Create a button widget with the given text and command
        self.view_class_button.pack(padx=10, pady=10)   # Add the button widget to the window with the given padding values

        self.add_sem_button = tk.Button(self.window, text="Add Semester", command=self.semesterViewer)   # Create a button widget with the given text and command
        self.add_sem_button.pack(padx=10, pady=10)   # Add the button widget to the window with the given padding values

        # Add the button widget to the window
        self.button.pack(padx=10, pady=10)

        # Start the event loop
        self.window.mainloop()

    # Define a method called addClassViewer
    def addClassViewer(self):
        root = AddClassPage()
        

    # Define a method called classViewer
    def classViewer(self):
        root = ViewClassesPage()

    def semesterViewer(self):
        self.SemesterName = tk.StringVar()
        self.semester_enter = tk.Entry(self.window, width=20, textvariable=self.SemesterName)
        self.semester_enter.pack(padx=10, pady=5)
        self.sem_enter_button = tk.Button(self.window, text="Enter", command=self.semesterEnter)
        self.sem_enter_button.pack(padx=10, pady=10)

    def semesterEnter(self):
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS semesters (
            semester_name text UNIQUE
            )""")
        semester_name = self.SemesterName.get()
        cur.execute("SELECT COUNT(*) FROM semesters WHERE semester_name = ?", (semester_name,))
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO semesters VALUES (?)", (semester_name,))
            conn.commit()
        conn.close()
        self.semester_enter.destroy()
        self.sem_enter_button.destroy()



# Class for the view classes page
class ViewClassesPage(HomePage):
    def __init__(self):

        # Create the window
        self.window = tk.Tk()
        self.window.title("View Classes")
        self.window.geometry("800x800")

        # Create a label widget
        self.label = tk.Label(self.window, text="View Classes")

        # Add the label widget to the window
        self.label.pack(padx=10, pady=10)

        self.infolabel = tk.Label(self.window, text="Select a class to view grades in detail.")
        self.infolabel.pack(padx=10, pady=10)

        # Creates the semester list
        self.semesters = []
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM semesters")
        sem_tuple = cur.fetchall()
        for elements in sem_tuple:
            self.semesters.append(elements[0])
        conn.commit()
        conn.close()

        self.selectSemester()

        # for i in range(len(class_list)):
        #     #create a button widget
        #     button = tk.Button(window, text= class_list(i), command=viewGrades)


        # Create a button widget
        self.button = tk.Button(self.window, text="Exit", command=self.window.quit)

        # Add the button widget to the window
        self.button.pack(padx=10, pady=10)

        # Start the event loop
        self.window.mainloop()

    def viewGrades(self):
        print("View Grades")

    def semesterSelect(self, value):
        self.semester_dropdown.destroy()
        self.infolabel.destroy()
        self.classlist = []
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM classes WHERE semester = ?", (value,))
        class_tuple = cur.fetchall()
        for elements in class_tuple:
            self.classlist.append(elements[0])
        conn.commit()
        conn.close()
        # Create a table of buttons with the class names, and when clicked, call the viewGrades method, but also have labels next to them with their respective credits and grade percentage
        for element in self.classlist:
            button = tk.Button(self.window, text=element, command=self.viewGrades)
            button.pack(padx=10, pady=10)
            
    def selectSemester(self):
        self.selectedSemester = tk.StringVar(self.window)
        self.selectedSemester.set("Select a semester")
        self.semester_dropdown = tk.OptionMenu(self.window, self.selectedSemester, *self.semesters, command=self.semesterSelect)
        self.semester_dropdown.pack(padx=10, pady=10)


class AddClassPage(HomePage):
    def __init__(self):
        # Connect to database and add a new table if it does not exist
        database = "GradeCalculator.db"
        conn = sql.connect(database)
        # create a cursor object
        cur = conn.cursor()

        cur.execute(""" CREATE TABLE IF NOT EXISTS classes (
            class_name text,
            credit_hours integer,
            semester text
            )
        """)
        # committing changes and closing the connection to the database file
        conn.commit()
        # close the database connection
        cur.execute("SELECT * FROM semesters")  # Select all the rows from the semesters table
        self.semesters = []
        semester_tuple = cur.fetchall() # Fetch all the rows from the semesters table
        for elements in semester_tuple: # For each row in the semesters table
            self.semesters.append(elements[0]) # Append the first element of the row to the semesters list
        conn.commit()
        conn.close()
    
        # Create the window
        self.window = tk.Tk()
        self.window.title("Add Class")
        self.window.geometry("800x800")

        # Create a label widget
        self.label = tk.Label(self.window, text="Add Class")
        self.warningLabel = tk.Label(self.window, text="All fields must be filled out.", fg="red", font=("Helvetica", 20))

        # Add the label widget to the window
        self.label.pack(padx=10, pady=10)
        self.warningLabel.pack(padx=10, pady=10)

        # Create a ClassName Variable to hold the new class name
        self.ClassName = tk.StringVar()

        self.name_label = tk.Label(self.window, text= "Enter Name of Class")
        self.name_label.pack(padx=10)


        # Create a Name entry widget
        self.name_entry = tk.Entry(self.window, width=20, textvariable=self.ClassName)
        self.name_entry.pack(padx=10, pady=5)

        # Create a CreditHours Variable to hold the credit hours
        self.CreditHours = tk.StringVar()

        self.credit_label = tk.Label(self.window, text= "Enter Credit Hours")
        self.credit_label.pack(padx=10)

        # Create a CreditHours entry widget
        self.credit_entry = tk.Entry(self.window, width=20, textvariable=self.CreditHours)
        self.credit_entry.pack(padx=10, pady=5)


        # Create a SemesterName Variable to hold the semester name
        self.SemesterName = tk.StringVar(self.window)
        self.SemesterName.set("Select Semester")
        self.sem_entry = tk.OptionMenu(self.window, self.SemesterName , *self.semesters, command = self.semesterEnter)
        self.sem_entry.pack(padx=10, pady=5)

        # Create an entry button
        self.entryButton2 = tk.Button(self.window, text="Enter", command = self.classEnter)
        self.entryButton2.pack(padx=10, pady=10)

        # Create a button widget
        self.button = tk.Button(self.window, text="Exit", command=self.window.quit)

        # Add the button widget to the window
        self.button.pack(padx=10, pady=10)
       
        # Start the event loop
        self.window.mainloop()
        

    
    def classEnter(self):
        className = self.name_entry.get()
        creditHours = self.credit_entry.get()
        semester = self.SemesterName.get()
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO classes VALUES (?, ?, ?)", (className, creditHours, semester))

    def semesterEnter(self, selected_value):
        self.SemesterName = tk.StringVar(value = selected_value)
        print(self.SemesterName.get())




if __name__=='__main__':
    my_gui = HomePage()

