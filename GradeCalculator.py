import tkinter as tk   # import tkinter library and alias it as tk
import databasefunctions as dbf   # import databasefunctions library and alias it as dbf
import sqlite3 as sql  # import sqlite3 library and alias it as sql
from functools import partial   # import partial function from functools library



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

    def back(self):
        self.window.destroy()
        root = HomePage()



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

        #create a back button
        self.backButton = tk.Button(self.window, text="Back", command = self.window.destroy)
        self.backButton.pack(padx=10, pady=10)

        # Create a button widget
        self.button = tk.Button(self.window, text="Exit", command=self.window.quit)

        # Add the button widget to the window
        self.button.pack(padx=10, pady=10)

        self.tableFrame = tk.Frame(self.window)
        self.tableFrame.config(width = 500)
        # Start the event loop
        self.window.mainloop()

    def viewGrades(self,selectedClass,semester):
        root = ViewGradesPage(selectedClass,semester)

    def semesterSelect(self, value):
        self.semester_dropdown.destroy()
        self.infolabel.destroy()
        self.button.destroy()
        self.backButton.destroy()
        self.classlist = []
        self.creditlist = []
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM classes WHERE semester = ?", (value,))
        class_tuple = cur.fetchall()
        for elements in class_tuple:
            self.classlist.append(elements[1])
            self.creditlist.append(elements[2])
        conn.commit()
        conn.close()
        # Create a table of buttons with the class names, and when clicked, call the viewGrades method, but also have labels next to them with their respective credits and grade percentage
        class_label = tk.Label(self.tableFrame, text="Class")
        credit_label = tk.Label(self.tableFrame, text="Credits")
        class_label.grid(row = 0, column = 0, sticky = tk.W, pady=5)
        credit_label.grid(row = 0, column = 1, sticky = tk.E, pady=5)
        count = 1
        for element in self.classlist:
            button = tk.Button(self.tableFrame, text=element, command=lambda elem = element, value = value: self.viewGrades(elem, value))
            button.grid(row = count, column = 0, sticky = tk.W, pady=5)
            count += 1
        
        count2 = 1
        for element in self.creditlist:
            creditlabel = tk.Label(self.tableFrame, text=element)
            creditlabel.grid(row = count2, column = 1, sticky = tk.E, pady=5)
            count2 += 1
        
        self.tableFrame.pack(pady = 10)
        ## Still need to add grade percentage labels

        back_button = tk.Button(self.window, text="Back", command=self.back)
        back_button.pack(padx=10, pady=10)
        # Create a button widget
        self.button = tk.Button(self.window, text="Exit", command=self.window.quit)

        # Add the button widget to the window
        self.button.pack(padx=10, pady=10)


            
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
            semester text,
            class_name text,
            credit_hours real
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

        #create a back button
        self.backButton = tk.Button(self.window, text="Back", command = self.window.destroy)
        self.backButton.pack(padx=10, pady=10)

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
        cur.execute("INSERT INTO classes VALUES (?, ?, ?)", (semester, className, creditHours))
        conn.commit()
        conn.close()
        root = ClassGradingPage(className, semester)


    def semesterEnter(self, selected_value):
        self.SemesterName = tk.StringVar(value = selected_value)
        print(self.SemesterName.get())


class ClassGradingPage(AddClassPage):
    def __init__(self,className, semesterName):
        self.entryCount = 0
        # Connect to database and add a new table if it does not exist
        database = "GradeCalculator.db"
        conn = sql.connect(database)
        # create a cursor object
        cur = conn.cursor()
        cur.execute(""" CREATE TABLE IF NOT EXISTS grading (
            semester_name text,
            class_name text,
            category text,
            weight real
            )
        """)
        conn.commit()
        conn.close()

        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute(f""" CREATE TABLE IF NOT EXISTS "{className}" (
            category text,
            assignment_name text,
            grade real,
            total_points real
            )"""
        )
        
        #create lists to hold completed items in order to build labels
        self.categories = []
        self.weights = []

        self.window = tk.Tk()
        self.window.title(className)
        self.window.geometry("800x800")

        # Create the instructions for how to use this page
        self.classLabel = tk.Label(self.window, text=className)
        self.label = tk.Label(self.window, text="Grading Scheme:")
        self.instructionLabel = tk.Label(self.window, text="Enter the assignment categories, and the percentage weight as a decimal")
        self.exampleLabel = tk.Label(self.window, text="Example: 10% = 0.1")
        self.warningLabel = tk.Label(self.window, text="All fields must be filled out.", fg="red", font=("Helvetica", 20))
        self.instructions = tk.Label(self.window, text="Add Category button will send the current category and allow for another entry.")
        self.instructionsContinued = tk.Label(self.window, text= " Enter will finish adding categories, once either button is pressed they are final")
        self.classLabel.pack(padx=10, pady=10)
        self.label.pack(padx=10, pady=10)
        self.instructionLabel.pack(padx=10, pady=10)
        self.exampleLabel.pack(padx=10, pady=10)
        self.warningLabel.pack(padx=10, pady=10)
        self.instructions.pack(padx=10, pady=10)
        self.instructionsContinued.pack(padx=10, pady=10)

        # create a button that adds a grading category
        self.addCategoryButton = tk.Button(self.window, text="Add Category", command = partial(self.addCategory, semesterName = semesterName, className = className))
        self.addCategoryButton.pack(padx=10, pady=10)

        # create a back button
        self.backButton = tk.Button(self.window, text="Back", command = self.window.destroy)
        self.backButton.pack(padx=10, pady=10)

        # create an exit button
        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)



    def addCategory(self, semesterName, className):
        # remove buttons to add them to the end
        self.addCategoryButton.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        # create a frame that holds all the entry buttons and labels
        self.frame = tk.Frame(self.window)
        self.categoryName = tk.StringVar()
        self.categoryWeight = tk.DoubleVar()
        self.nameLabel = tk.Label(self.frame, text="Category Name")
        self.weightLabel = tk.Label(self.frame, text="Category Weight")
        self.nameLabel.grid(row=0, column=0, sticky = tk.W)
        self.weightLabel.grid(row=0, column=1, sticky = tk.W)
        self.nameEntry = tk.Entry(self.frame, textvariable=self.categoryName, width=20)
        self.weightEntry = tk.Entry(self.frame, textvariable=self.categoryWeight, width=20)
        self.nameEntry.grid(row=1, column=0, sticky = tk.W)
        self.weightEntry.grid(row=1, column=1, sticky = tk.E)
        self.frame.pack(padx=10, pady=10)
        self.addCategoryButton = tk.Button(self.window, text="Add another Category", command = partial(self.addMoreCategory,semesterName = semesterName, className = className, categoryName = self.categoryName, weight = self.categoryWeight))
        self.addCategoryButton.pack(padx=10, pady=10)
        self.enterButton = tk.Button(self.window, text="Enter and go Back", command = partial(self.enterCategory, semesterName = semesterName, className = className))
        self.enterButton.pack(padx=10, pady=10)
        self.backButton = tk.Button(self.window, text="Back", command = self.window.destroy)
        self.backButton.pack(padx=10, pady=10)
        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack()
        

    def enterCategory(self, semesterName, className):
        categoryName = self.nameEntry.get()
        categoryWeight = self.weightEntry.get()
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO grading VALUES (?, ?, ?, ?)", (semesterName, className, categoryName, categoryWeight))
        conn.commit()
        conn.close()
        self.window.destroy()
    
    ## work on adding the grid above the entry fields but below the labels
    def addMoreCategory(self, semesterName, className, categoryName, weight):
        self.addCategoryButton.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        self.enterButton.destroy()
        categoryName = self.nameEntry.get()
        weight = self.weightEntry.get()
        # entering into database 
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO grading VALUES (?, ?, ?, ?)", (semesterName, className, categoryName, weight))
        conn.commit()
        conn.close()
        self.entryCount += 1
        self.frame.destroy()
        # Add a new Frame for the labels and entries
        self.newFrame = tk.Frame(self.window)
        self.nameLabel = tk.Label(self.newFrame, text="Category Name")
        self.weightLabel = tk.Label(self.newFrame, text="Category Weight")
        self.nameLabel.grid(row=0, column=0, sticky = tk.W)
        self.weightLabel.grid(row=0, column=1, sticky = tk.W)
        self.enteredName = tk.Label(self.newFrame, text=categoryName)
        self.enteredWeight = tk.Label(self.newFrame, text=weight)
        self.enteredName.grid(row=1, column=0, sticky = tk.W)
        self.enteredWeight.grid(row=1, column=1, sticky = tk.W)
        self.newFrame.pack(padx=10, pady=10)
        #frame for the entry
        self.entryFrame = tk.Frame(self.window)
        self.name = tk.StringVar()
        self.weight = tk.DoubleVar()
        self.nameEntry = tk.Entry(self.entryFrame, textvariable=self.name, width=20)
        self.weightEntry = tk.Entry(self.entryFrame, textvariable=self.weight, width=20)
        self.nameEntry.grid(row=0, column=0, sticky = tk.W)
        self.weightEntry.grid(row=0, column=1, sticky = tk.E)
        self.entryFrame.pack(padx=10, pady=10)
        self.addCategoryButton = tk.Button(self.window, text="Add Category", command = partial(self.add3rdCategory,semesterName = semesterName, className = className, name = self.name,weight = self.weight))
        self.addCategoryButton.pack(padx=10, pady=10)
        self.enterButton = tk.Button(self.window, text="Enter and go Back", command = partial(self.enterCategory, semesterName = semesterName, className = className))
        self.enterButton.pack(padx=10, pady=10)
        self.backButton = tk.Button(self.window, text="Back", command = self.window.destroy)
        self.backButton.pack(padx=10, pady=10)
        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)

    def add3rdCategory(self, semesterName, className, name, weight):
        self.addCategoryButton.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        self.enterButton.destroy()
        name = self.nameEntry.get()
        weight = self.weightEntry.get()
        # entering into database
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO grading VALUES (?, ?, ?, ?)", (semesterName, className, name, weight))
        conn.commit()
        conn.close()
        # destroying entry Frame, adding to the list of labels
        self.entryCount += 1
        self.entryFrame.destroy()
        self.newLabel = tk.Label(self.newFrame, text=name)
        self.weightLabel = tk.Label(self.newFrame, text=weight)
        self.newLabel.grid(row=self.entryCount, column=0, sticky = tk.W)
        self.weightLabel.grid(row=self.entryCount, column=1, sticky = tk.W)
        self.newFrame.pack(padx=10, pady=10)
        # frame for more entries
        self.entryFrame = tk.Frame(self.window)
        self.name = tk.StringVar()
        self.weight = tk.DoubleVar()
        self.nameEntry = tk.Entry(self.entryFrame, textvariable=self.name, width=20)
        self.weightEntry = tk.Entry(self.entryFrame, textvariable=self.weight, width=20)
        self.nameEntry.grid(row=0, column=0, sticky = tk.W)
        self.weightEntry.grid(row=0, column=1, sticky = tk.E)
        self.entryFrame.pack(padx=10, pady=10)
        self.addCategoryButton = tk.Button(self.window, text="Add Category", command = partial(self.add3rdCategory, className =className, semesterName = semesterName, name = self.name, weight = self.weight))
        self.addCategoryButton.pack(padx=10, pady=10)
        self.enterButton = tk.Button(self.window, text="Enter and go Back", command = partial(self.enterCategory, semesterName = semesterName, className = className))
        self.enterButton.pack(padx=10, pady=10)
        self.backButton = tk.Button(self.window, text="Back", command = self.window.destroy)
        self.backButton.pack(padx=10, pady=10)
        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)


class ViewGradesPage(ViewClassesPage):
    def __init__(self, className, semesterName):
        self.window = tk.Tk()
        self.window.geometry("800x800")
        self.window.title("View Grades for " + className + " during " + semesterName)
        self.className = className
        self.semesterName = semesterName

        ## Create a visual table of the weights and the categories with grades 
        self.frame = tk.Frame(self.window)
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM grading WHERE semester_name = ? AND class_name = ?", (semesterName, className))
        data = cur.fetchall()
        conn.commit()
        conn.close()
        self.categoryName = []
        self.categoryWeight = []
        for element in data: 
            self.categoryName.append(element[2])
            self.categoryWeight.append(element[3]) 
        for i in range(len(self.categoryName)):
            self.categoryLabel = tk.Label(self.frame, text=self.categoryName[i])
            self.categoryLabel.grid(row=i, column=0, sticky = tk.W)
            self.categoryLabel = tk.Label(self.frame, text=self.categoryWeight[i])
            self.categoryLabel.grid(row=i, column=1, sticky = tk.W)
            self.gradeLabel = tk.Label(self.frame, text= self.getGrade(self.categoryName[i]))
            self.gradeLabel.grid(row= i, column=2, sticky = tk.E)
        self.finalgradeLabel = tk.Label(self.frame, text="Final Grade: " + str(self.getFinalGrade()))
        self.finalgradeLabel.grid(row=len(self.categoryName), column=0, sticky = tk.W)
        self.frame.pack(padx=10, pady=10)

        self.addAssignmentButton = tk.Button(self.window, text="Add Assignment Grade", command = self.addAssignment)
        self.addAssignmentButton.pack(padx=10, pady=10)

        self.simulateAssignmentButton = tk.Button(self.window, text="Test an Assignment Grade", command = self.simulateAssignment)
        self.simulateAssignmentButton.pack(padx=10, pady=10)

        self.calculateNeededGradesButton = tk.Button(self.window, text="Calculate What I need", command = self.calculateNeededGrades)
        self.calculateNeededGradesButton.pack(padx=10, pady=10)

        self.backButton = tk.Button(self.window, text="Back", command = self.window.destroy)
        self.backButton.pack(padx=10, pady=10)

        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)


        self.window.mainloop()

    def addAssignment(self):
        self.addAssignmentButton.destroy()
        self.simulateAssignmentButton.destroy()
        self.calculateNeededGradesButton.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        self.selectedCategory = tk.StringVar()
        self.selectedCategory.set("Select a Category")
        self.selectCategoryMenu = tk.OptionMenu(self.window, self.selectedCategory,*self.categoryName, command = self.fillGradeEntry)
        self.selectCategoryMenu.pack(padx=10, pady=10)

        self.backButton = tk.Button(self.window, text="Back", command = self.backToGrades)
        self.backButton.pack(padx=10, pady=10)

        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)



    def fillGradeEntry(self, value): 
        self.selectCategoryMenu.destroy()
        self.categoryLabel = tk.Label(self.window, text=value)
        assignmentNames = []
        assignmentPoints = []
        assignmentTotalPoints = []
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM `{self.className}` WHERE category = ?", (value,))
        data = cur.fetchall()
        conn.commit()
        conn.close()

        for element in data:
            assignmentNames.append(element[1])
            assignmentPoints.append(element[2])
            assignmentTotalPoints.append(element[3])

        self.assignmentName = tk.StringVar()
        self.assignmentPoints = tk.DoubleVar()
        self.assignmentTotalPoints = tk.DoubleVar()

        self.labelEntryFrame = tk.Frame(self.window)

        self.nameLabel = tk.Label(self.labelEntryFrame, text="Assignment Name")
        self.pointsLabel = tk.Label(self.labelEntryFrame, text="Points Earned")
        self.totalPointsLabel = tk.Label(self.labelEntryFrame, text="Total Points")
        self.nameLabel.grid(row=0, column=0, sticky = tk.W)
        self.pointsLabel.grid(row=0, column=1, sticky = tk.W)
        self.totalPointsLabel.grid(row=0, column=2, sticky = tk.W)


        self.assignmentNameEntry = tk.Entry(self.labelEntryFrame, width=20, textvariable=self.assignmentName)
        self.assignmentPointsEntry = tk.Entry(self.labelEntryFrame, width=20, textvariable=self.assignmentPoints)    
        self.assignmentTotalPointsEntry = tk.Entry(self.labelEntryFrame, width=20, textvariable=self.assignmentTotalPoints)
        self.enter = tk.Button(self.window, text="Enter", command = self.enterAssignment)

        self.assignmentNameEntry.grid(row=1, column=0, sticky = tk.W)
        self.assignmentPointsEntry.grid(row=1, column=1, sticky = tk.W)
        self.assignmentTotalPointsEntry.grid(row=1, column=2, sticky = tk.W)
        self.labelEntryFrame.pack(padx=10, pady=10)
        self.enter.pack(padx=10, pady=10)

        if len(assignmentNames) != 0:    
            priorGradeLabel = tk.Label(self.window, text="Prior Grades:")
            priorGradeLabel.pack(padx=10, pady=10)
            i = 0
            self.entryGrid = tk.Frame(self.window)
            for i in range(len(assignmentNames)):
                self.assignmentNameLabel = tk.Label(self.entryGrid, text=assignmentNames[i])
                self.assignmentNameLabel.grid(row=i, column=0, sticky = tk.W)
                self.assignmentPointsLabel = tk.Label(self.entryGrid, text=assignmentPoints[i])
                self.assignmentPointsLabel.grid(row=i, column=1, sticky = tk.W)
                self.assignmentTotalPointsLabel = tk.Label(self.entryGrid, text=assignmentTotalPoints[i])
                self.assignmentTotalPointsLabel.grid(row=i, column=2, sticky = tk.E)
    
            self.entryGrid.pack(padx=10, pady=10)

    def enterAssignment(self):
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute(f"INSERT INTO `{self.className}` VALUES (?, ?, ?, ?)", (self.selectedCategory.get(), self.assignmentNameEntry.get(), self.assignmentPointsEntry.get(), self.assignmentTotalPointsEntry.get()))
        conn.commit()
        conn.close()
        self.window.destroy()
        my_gui = ViewGradesPage(self.className, self.semesterName)

    def getGrade(self, categoryName):
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM `{self.className}` WHERE category = ?", (categoryName,))
        data = cur.fetchall()
        conn.commit()
        conn.close()
        points = 0
        totalPoints = 0
        if len(data) == 0:
            return "No Inputted Grades"
        for element in data:
            points += element[2]
            totalPoints += element[3]
        result = (points/totalPoints) * 100
        return round(result, 2)
    
    def getFinalGrade(self):
        grades = []
        finalgrades = []
        for i in range(len(self.categoryName)):
            grade = self.getGrade(self.categoryName[i])
            if grade == "No Inputted Grades":
                grade = 100 
            grades.append(grade)
        for i in range(len(grades)):
            finalgrades.append(grades[i] * float(self.categoryWeight[i]))
        return round(sum(finalgrades), 2)

    def simulateAssignment(self):
        self.addAssignmentButton.destroy()
        self.simulateAssignmentButton.destroy()
        self.calculateNeededGradesButton.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        self.selectedCategory = tk.StringVar()
        self.selectedCategory.set("Select a Category")
        self.selectCategoryMenu = tk.OptionMenu(self.window, self.selectedCategory,*self.categoryName, command = self.fillSimulateEntry)
        self.selectCategoryMenu.pack(padx=10, pady=10)

        self.backButton = tk.Button(self.window, text="Back", command = self.backToGrades)
        self.backButton.pack(padx=10, pady=10)

        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)

    def backToGrades(self):
        self.window.destroy()
        my_gui = ViewGradesPage(self.className, self.semesterName)

    def fillSimulateEntry(self, value):
        self.selectCategoryMenu.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        self.categoryLabel = tk.Label(self.window, text=value)
        self.categoryLabel.pack(padx=10, pady=10)
        self.simulateLabel = tk.Label(self.window, text="Simulate Assignment Grade")
        self.simulateLabel.pack(padx=10, pady=10)
        self.simulateCategory = tk.Label(self.window, text="Category: " + value)

        self.simulatePoints = tk.DoubleVar()
        self.simulateTotalPoints = tk.DoubleVar()

        self.simulateEntryFrame = tk.Frame(self.window)
        self.simulatePointsLabel = tk.Label(self.simulateEntryFrame, text="Points Earned")
        self.simulateTotalPointsLabel = tk.Label(self.simulateEntryFrame, text="Total Points")
        self.simulatePointsLabel.grid(row=0, column=0, sticky = tk.W)
        self.simulateTotalPointsLabel.grid(row=0, column=1, sticky = tk.W)
        self.simulatePointsEntry = tk.Entry(self.simulateEntryFrame, width=20, textvariable=self.simulatePoints)
        self.simulateTotalPointsEntry = tk.Entry(self.simulateEntryFrame, width=20, textvariable=self.simulateTotalPoints)
        self.simulatePointsEntry.grid(row=1, column=0, sticky = tk.W)
        self.simulateTotalPointsEntry.grid(row=1, column=1, sticky = tk.W)
        self.simulateEntryFrame.pack(padx=10, pady=10)

        self.simulateButton = tk.Button(self.window, text="Simulate", command = partial(self.simulate, category = value))
        self.simulateButton.pack(padx=10, pady=10)

        self.backButton = tk.Button(self.window, text="Back", command = self.backToGrades)
        self.backButton.pack(padx=10, pady=10)

        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)


    def simulate(self, category):
        self.simulateButton.destroy()
        pointsEarned = float(self.simulatePointsEntry.get())
        totalassignmentPoints = float(self.simulateTotalPointsEntry.get())
        self.simulateEntryFrame.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM `{self.className}` WHERE category = ?", (category,))
        data = cur.fetchall()
        conn.commit()
        conn.close()
        points = 0
        totalPoints = 0
        if len(data) == 0:
            categoryGrade = (pointsEarned/totalassignmentPoints) * 100
        else: 
            for element in data:
                points += element[2]
                totalPoints += element[3]
            categoryGrade = ((points + pointsEarned)/(totalPoints + totalassignmentPoints)) * 100 
        
        
        self.inputtedGradeLabel = tk.Label(self.window, text="Inputted Grade:")
        self.inputtedGradeLabel.pack(padx=10, pady=10)

        self.inputtedGradeFrame = tk.Frame(self.window)
        self.inputtedPointsLabel = tk.Label(self.inputtedGradeFrame, text="Points Earned: " + str(pointsEarned))
        self.inputtedTotalPointsLabel = tk.Label(self.inputtedGradeFrame, text="Total Points: " + str(totalassignmentPoints))
        self.inputtedPointsLabel.grid(row=0, column=0, sticky = tk.W)
        self.inputtedTotalPointsLabel.grid(row=0, column=1, sticky = tk.W)
        self.inputtedGradeFrame.pack(padx=10, pady=10)

        self.simulatedGradeLabel = tk.Label(self.window, text="Category Grade After Inputted Assignment: " + str(round(categoryGrade, 2)))
        self.simulatedGradeLabel.pack(padx=10, pady=10)
        self.finalGradeSimulationLabel = tk.Label(self.window, text="Final Grade After Inputted Assignment: " + str(self.getSimulatedGrade(category, categoryGrade)))
        self.finalGradeSimulationLabel.pack(padx=10, pady=10)

        self.backButton = tk.Button(self.window, text="Back", command = self.backToGrades)
        self.backButton.pack(padx=10, pady=10)

        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)
        
    def getSimulatedGrade(self, category, categoryGrade):
        grades = []
        finalgrades = []
        for i in range(len(self.categoryName)):
            if self.categoryName[i] == category:
                grade = categoryGrade
            else:
                grade = self.getGrade(self.categoryName[i])
                if grade == "No Inputted Grades":
                    grade = 100
            grades.append(grade)

        for i in range(len(grades)):
            finalgrades.append(grades[i] * float(self.categoryWeight[i]))
        simulatedGrade = round(sum(finalgrades), 2)
        return round(simulatedGrade, 2)
    
    def calculateNeededGrades(self):
        self.addAssignmentButton.destroy()
        self.simulateAssignmentButton.destroy()
        self.calculateNeededGradesButton.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        self.selectedCategory = tk.StringVar()
        self.desiredGrade = tk.DoubleVar()
        self.pointsAvailable = tk.DoubleVar()
        self.desiredGradeLabel = tk.Label(self.window, text="Desired Grade:")
        self.desiredGradeLabel.pack(padx=10, pady=10)
        self.desiredGradeEntry = tk.Entry(self.window, width=20, textvariable=self.desiredGrade)
        self.desiredGradeEntry.pack(padx=10, pady=10)
        self.pointsAvailableLabel = tk.Label(self.window, text="Points Available:")
        self.pointsAvailableLabel.pack(padx=10, pady=10)
        self.pointsAvailableEntry = tk.Entry(self.window, width=20, textvariable=self.pointsAvailable)
        self.pointsAvailableEntry.pack(padx=10, pady=10)
        self.selectedCategory.set("Select a Category to Calculate Needed Grade")
        self.selectCategoryMenu = tk.OptionMenu(self.window, self.selectedCategory,*self.categoryName, command = self.fillCalculateNeededEntry)
        self.selectCategoryMenu.pack(padx=10, pady=10)

        self.backButton = tk.Button(self.window, text="Back", command = self.backToGrades)
        self.backButton.pack(padx=10, pady=10)

        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)

    def fillCalculateNeededEntry(self, category):
        self.selectCategoryMenu.destroy()
        self.backButton.destroy()
        self.exitButton.destroy()
        desiredGrade = float(self.desiredGradeEntry.get())
        pointsAvailable = float(self.pointsAvailableEntry.get())
        self.currentGradeLabel = tk.Label(self.window, text="Current Grade: "+ str(self.getFinalGrade()))
        self.newDesiredGradeLabel = tk.Label(self.window, text="Desired Grade: " + str(desiredGrade))
        self.desiredGradeEntry.destroy()
        self.pointsAvailableLabel.destroy()
        self.pointsAvailableEntry.destroy()
        self.desiredGradeLabel.destroy()
        
        self.pointsAvailableLabel = tk.Label(self.window, text="Points Available: " + str(pointsAvailable))
        self.currentGradeLabel.pack(padx=10, pady=10)
        self.newDesiredGradeLabel.pack(padx=10, pady=10)

        gradeNeeded = self.calculateGradeNeeded(category, desiredGrade, pointsAvailable)

        self.newergradeNeededLabel = tk.Label(self.window, text="Grade Needed in " + category + ": " + str(gradeNeeded))
        self.newergradeNeededLabel.pack(padx=10, pady=10)

        self.backButton = tk.Button(self.window, text="Back", command = self.backToGrades)
        self.backButton.pack(padx=10, pady=10)

        self.exitButton = tk.Button(self.window, text="Exit", command = self.window.quit)
        self.exitButton.pack(padx=10, pady=10)

    def calculateGradeNeeded(self, category, desiredGrade, availablePoints):
        # Connect to the database
        conn = sql.connect('GradeCalculator.db')
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM `{self.className}`")
        data = cur.fetchall()
        cur.execute(f"SELECT weight FROM grading WHERE semester_name = ? AND class_name = ? AND category = ?", (self.semesterName, self.className, category,))
        weight = cur.fetchone()[0]

        # Close the database connection
        conn.close()

        grades = []
        finalgrades = []
        for i in range(len(self.categoryName)):
            if self.categoryName[i] != category:
                grade = self.getGrade(self.categoryName[i])
                if grade == "No Inputted Grades":
                    grade = 100 
                grades.append(grade)
            else:
                grades.append(0)
        for i in range(len(grades)):
            finalgrades.append(grades[i] * float(self.categoryWeight[i]))
        
        currentGrade = sum(finalgrades) 
        print(currentGrade)
        neededCategoryGrade = (desiredGrade - currentGrade) / float(weight)
        print(neededCategoryGrade)

        conn = sql.connect("GradeCalculator.db")
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM `{self.className}` WHERE category = ?", (category,))
        data = cur.fetchall()
        conn.commit()
        conn.close()
        points = 0
        totalPoints = 0
        if len(data) == 0:
            return "No Inputted Grades"
        for element in data:
            points += element[2]
            totalPoints += element[3]
        
        totalPoints += availablePoints
        neededPoints = neededCategoryGrade * (totalPoints - points)
        return neededPoints/availablePoints



        



if __name__=='__main__':
    my_gui = HomePage()

