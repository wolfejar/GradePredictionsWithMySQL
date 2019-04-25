import matplotlib.pyplot as plt


def plot_student_grades_vs_on_campus(grade_percentage_arr, on_campus_arr):
    plt.scatter(grade_percentage_arr, on_campus_arr)
    plt.xlabel('Grade Percentage')
    plt.ylabel('On Campus (Y/N)')
    plt.axis('equal')
    plt.axis('square')
    plt.xlim([0, plt.xlim()[1]])
    plt.ylim([0, plt.ylim()[1]])
    _ = plt.plot([-100, 100], [-100, 100])
    plt.savefig('static/course_report.png')
