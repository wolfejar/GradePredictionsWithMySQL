import numpy as np
from flask import Flask, render_template, request, session, jsonify
import current_model
from sql_scripts import SQL
from passlib.hash import pbkdf2_sha256
from flask_bootstrap import Bootstrap

application = Flask(__name__)
Bootstrap(application)
sql = SQL()
application.app_context()


@application.route('/')
@application.route('/index')
def home():
    return render_template('index.html')


@application.route('/sign_up_get', methods=['GET'])
def sign_up_get():
    return render_template('sign_up.html')


@application.route('/sign_up_post', methods=['POST'])
def sign_up_post():
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    on_campus = request.form.get('oncampus') is not None
    is_working = request.form.get('isworking') is not None
    gpa = request.form.get('gpa')
    hashed_pass = pbkdf2_sha256.hash(request.form['password'])
    instution_id = request.form.get('institutionId')
    email = request.form.get('email')
    sql.create_student(hashed_pass, first_name, last_name, int(on_campus), int(is_working), float(gpa),
                       email, int(instution_id))
    session['email'] = email
    return account_home()


@application.route('/sign_in_get', methods=['GET'])
def sign_in_get():
    return render_template('sign_in.html')


@application.route('/sign_in_post', methods=['POST'])
def sign_in_post():
    if request.method == 'POST':
        email = request.form['email']
        raw = request.form['password']
        if sql.sign_in(email, raw):
            session['email'] = email
            return account_home()
        else:
            return sign_in_get()


@application.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email', None)
    return home()


@application.route('/edit_account_info_get', methods=['GET'])
def edit_account_info_get():
    course_data = sql.get_home_info(session['email'])
    first_name = sql.get_student_first_name(session['email'])
    student_info = sql.get_student_info_by_email(session['email'])
    return render_template('edit_account.html', data=course_data, first_name=first_name, student_info=student_info)


@application.route('/edit_account_student_info_post', methods=['POST'])
def edit_account_student_info_post():
    request.form.get('first_name')
    return account_home()


@application.route('/edit_account_course_info_post', methods=['POST'])
def edit_account_course_info_post():
    request.form.get()
    return account_home()


@application.route('/account_home', methods=['GET', 'POST'])
def account_home():
    data = sql.get_home_info(session['email'])
    firstname = sql.get_student_first_name(session['email'])
    block = 'style="display: block"'
    none = 'style="display: none"'
    return render_template('account_home.html', firstname=firstname, data=data)


@application.route('/course_report', methods=['POST'])
def course_report():
    course_id = int(request.form.get('course_id'))
    data = sql.get_student_info_by_course_id(course_id)
    grade_percentage_arr = []
    on_campus_arr = []
    is_working_arr = []
    gpa_arr = []
    institution_arr = []
    for student in data:
        grade_percentage_arr.append(student[2])
        on_campus_arr.append(student[8])
        # is_working_arr.append(student[])
    return account_home()


@application.route('/send', methods=['POST'])
def send():
    if request.method == 'POST':
        gpa = request.form['gpa']
        totalcreditcours = request.form['totalcredithours']
        oncampus = request.form.get('oncampus') is not None
        isworking = request.form.get('isworking') is not None
        hasposition = request.form.get('hasposition') is not None
        coursecredithours = request.form['coursecredithours']
        courselevel = request.form['courselevel']
        AestheticInterpetation = request.form.get('AestheticInterpetation') is not None
        EmpiricalandQuantitativeReasoning = request.form.get('EmpiricalandQuantitativeReasoning') is not None
        EthicalReasoningandResponsibility = request.form.get('EthicalReasoningandResponsibility') is not None
        GlobalIssuesandPerspectives = request.form.get('GlobalIssuesandPerspectives') is not None
        HistoricalPerspectives = request.form.get('HistoricalPerspectives') is not None
        HumanDiversitywithintheUS = request.form.get('HumanDiversitywithintheUS') is not None
        NaturalandPhysicalSciences = request.form.get('NaturalandPhysicalSciences') is not None
        SocialSciences = request.form.get('SocialSciences') is not None
        years_teaching = request.form.get('YearsTeaching')
        is_tenured = request.form.get('IsTenured') is not None
        degree = request.form.get('Degree')
        # normalize data as we enter it into input array
        input_data = [float(gpa) / 4.0, float(totalcreditcours) / 22.0, float(int(oncampus)), float(int(isworking)),
                      float(int(hasposition)), float(coursecredithours) / 6.0, float(courselevel) / 1000,
                      float(int(AestheticInterpetation)), float(int(EmpiricalandQuantitativeReasoning)),
                      float(int(EthicalReasoningandResponsibility)), float(int(GlobalIssuesandPerspectives)),
                      float(int(HistoricalPerspectives)), float(int(HumanDiversitywithintheUS)),
                      float(int(NaturalandPhysicalSciences)), float(int(SocialSciences)),
                      float(int(years_teaching)) / 8.0, float(int(is_tenured)), float(int(degree)) / 3.0]
        input_data = np.array([input_data])

        model = current_model.get_model()
        numerical_grade = model.predict(input_data)[0][0]
        integer_grade = int(numerical_grade)
        letter_grade = '?'
        if integer_grade < 60:
            letter_grade = 'F'
        elif integer_grade < 70:
            letter_grade = 'D'
        elif integer_grade < 80:
            letter_grade = 'C'
        elif integer_grade < 90:
            letter_grade = 'B'
        else:
            letter_grade = 'A'

        message = 'You grade will be' + letter_grade + ' ' + str(numerical_grade)

        return jsonify({'text':message})


if __name__ == '__main__':
    application.secret_key = 'super secret key'
    application.run(debug=True)
