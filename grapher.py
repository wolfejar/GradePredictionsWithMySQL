import matplotlib.pyplot as plt


def plot_student_grades_vs_on_campus(x_label, y_label, grade_percentage_arr, on_campus_arr, dest):
    x = on_campus_arr
    y = grade_percentage_arr
    plt.plot(x, y, 'o', color='orange')
    plt.xlabel = x_label
    plt.ylabel = y_label
    plt.xticks(ticks=[0, 1], labels=['Off Campus', 'On Campus'])

    plt.title("Student performance off/on campus")
    plt.savefig(dest)
    plt.close()


def plot_student_grades_vs_is_working(x_label, y_label, grade_percentage_arr, is_working_arr, dest):
    x = is_working_arr
    y = grade_percentage_arr
    plt.plot(x, y, 'o', color='orange')
    plt.xlabel = x_label
    plt.ylabel = y_label
    plt.xticks(ticks=[0, 1], labels=['Not Working', 'Is Working'])

    plt.title("Student performance Working vs. Not Working")
    plt.savefig(dest)
    plt.close()


def plot_student_grades_vs_gpa(x_label, y_label, grade_percentage_arr, gpa_arr, dest):
    x = gpa_arr
    y = grade_percentage_arr
    plt.plot(x, y, 'o', color='orange')
    plt.xlabel = x_label
    plt.ylabel = y_label

    plt.title("Student Performance vs GPA")
    plt.savefig(dest)
    plt.close()


def plot_student_grades_vs_institution(x_label, y_label, grade_percentage_arr, gpa_arr, dest):
    x = gpa_arr
    y = grade_percentage_arr
    plt.plot(x, y, 'o', color='orange')
    plt.xlabel = x_label
    plt.ylabel = y_label
    plt.xticks(ticks=[1, 2, 3, 4, 5], labels=['Kansas State University', 'University of Kansas',
                                              'Wichita State University', 'Emporia State University',
                                              'Fort Hays State University'], rotation='vertical')
    plt.title("Student Performance vs Student Institution")
    plt.savefig(dest)
    plt.close()


def plot_student_grades_vs_position(x_label, y_label, grade_percentage_arr, pos_arr, dest):
    x = pos_arr
    y = grade_percentage_arr
    plt.plot(x, y, 'o', color='orange')
    plt.xlabel = x_label
    plt.ylabel = y_label
    plt.xticks(ticks=[0, 1], labels=['No Position', 'Has Position'])
    plt.title("Student Performance vs Position In Club")
    plt.savefig(dest)
    plt.close()


def plot_student_grades_vs_department(x_label, y_label, grade_percentage_arr, dept_arr, dest):
    x = dept_arr
    y = grade_percentage_arr
    plt.plot(x, y, 'o', color='orange')
    plt.xlabel = x_label
    plt.ylabel = y_label
    plt.title("Student Performance vs Department")
    plt.savefig(dest)
    plt.close()
