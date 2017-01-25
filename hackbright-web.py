from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)

@app.route("/")
def index():
    print "entered route"
    projects = hackbright.get_all_projects()
    print 'got projects'

    students=hackbright.get_all_students()
    print 'got students'

    return render_template("index.html", students=students, projects=projects)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github', 'jhacks')
    if "drop table" in github:
        return "GO AWAY"
    first, last, github = hackbright.get_student_by_github(github)

    project_list = hackbright.get_grades_by_github(github)   # e.g. [('Blockly', 2), ('Pandas', 1000)]

    return render_template("student_info.html", github=github, first=first, last=last, projects=project_list)

@app.route("/new-student")
def new_student():
    """Displays form for new student information"""

    return render_template("new_student.html")

@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student"""

    first_name=request.form.get('first-name')
    last_name=request.form.get('last-name')
    github=request.form.get('github').lower()     # Think about stripping out full link info

    if first_name and last_name and github:
        hackbright.make_new_student(first_name, last_name, github)   # Adds student to database
        return render_template("student_add.html", first_name=first_name, 
                                                    last_name=last_name, 
                                                    github=github)

    else:
        return redirect("/new-student")

@app.route("/project")
def show_project():
    """Takes a GET request with a project title, displays info."""


    title = request.args.get('title')

    title, description, max_grade = hackbright.get_project_by_title(title)  # doesn't return id!!

    graded_students = hackbright.get_grades_by_title(title)
    return render_template("project_info.html", title=title,
                                                description=description,
                                                max_grade=max_grade,
                                                graded_students=graded_students
                                                )

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
