"""Hackbright Project Tracker.

A front-end for a database that allows users to work with students, class
projects, and the grades students receive in class projects.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hackbright'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


def get_student_by_github(github):
    """Given a github account name, print information about the matching student."""

    QUERY = """
        SELECT first_name, last_name, github
        FROM students
        WHERE github = :github
        """
    db_cursor = db.session.execute(QUERY, {'github': github})
    row = db_cursor.fetchone()
    print "Student: %s %s\nGithub account: %s" % (row[0], row[1], row[2])

    return row


def make_new_student(first_name, last_name, github):
    """Add a new student and print confirmation.

    Given a first name, last name, and GitHub account, add student to the
    database and print a confirmation message.
    """
    
    QUERY = """
            INSERT INTO students
                VALUES(:first_name, :last_name, :github)
    """

    db.session.execute(QUERY, {'first_name': first_name,
                                'last_name': last_name,
                                'github': github})

    db.session.commit()

    print "Successfully added student: %s %s" % (first_name,
                                                 last_name)



def get_project_by_title(title):
    """Given a project title, print information about the project."""
    
    QUERY = """ 
            SELECT * FROM projects
            WHERE title = :title """

    db_cursor = db.session.execute(QUERY, {'title': title})
    project_id, project_title, description, max_grade = db_cursor.fetchone()

    print """Here's the information about %s: 
                Description: %s
                Maximum Grade: %s """ % (project_title, description, max_grade)


def get_grade_by_github_title(github, title):
    """Print grade student received for a project."""
    
    QUERY = """SELECT grade FROM grades
    WHERE student_github = :github AND project_title = :title
            """

    db_cursor = db.session.execute(QUERY, {'title': title, 'github': github})
    grade = db_cursor.fetchone()[0]

    print """Student %s received a grade of %s on the project %s""" % (github,
                                                                    grade, title)


def assign_grade(github, title, grade):
    """Assign a student a grade on an assignment and print a confirmation."""
    pass


def handle_input():
    """Main loop.

    Repeatedly prompt for commands, performing them, until 'quit' is received as a
    command."""

    command = None

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            github = args[0]
            get_student_by_github(github)

        elif command == "new_student":
            first_name, last_name, github = args   # unpack!
            make_new_student(first_name, last_name, github)

        elif command == "project":
            title = args[0]
            get_project_by_title(title)

        elif command == "grade":
            github = args[0]
            title = args[1]
            get_grade_by_github_title(github, title)

        else:
            if command != "quit":
                print "Invalid Entry. Try again."

if __name__ == "__main__":
    app = Flask(__name__)
    connect_to_db(app)

    handle_input()

    db.session.close()
