import sqlite3 as sql

# # Create a database connection
# conn = sql.connect('grades.db')

# # Create a cursor object
# c = conn.cursor()

# # Create a table
# c.execute(""" CREATE TABLE microeconomics (
#     assignment_name text,
#     assignment_grade real,
#     possible_points real,
#     assignment_weight real
# )""")

# # Commit changes
# conn.commit()

# conn.close()
# ## 5 data types
# # null: no value
# # integer: whole number
# # real: decimal number
# # text: string
# # blob: binary data


# # Update the table
# c.execute(""" UPDATE microeconomics SET assignment_grade = 100 WHERE assignment_name = 'Midterm'
# """)

# Query the table and 
def show_table(database_name, table_name):
    conn = sql.connect(database_name)
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(table_name))
    table_elements = c.fetchall()
    conn.commit()
    conn.close()
    return table_elements

