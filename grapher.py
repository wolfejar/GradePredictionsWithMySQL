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
