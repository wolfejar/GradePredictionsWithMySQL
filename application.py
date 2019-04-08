import numpy as np
from flask import Flask, render_template, request
import current_model
from sql_scripts import SQL

application = Flask(__name__)

sql = SQL()


@application.route('/')
@application.route('/index')
def home():
    return render_template('landing.html')


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
    password = request.form.get('password')
    username = sql.create_student(first_name, last_name, bool(on_campus), bool(is_working), float(gpa), password)[0]
    return account_home(username, password)


@application.route('/sign_in_get', methods=['GET'])
def sign_in_get():
    return render_template('sign_in.html')


@application.route('/sign_in_post', methods=['POST'])
def sign_in_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if sql.sign_in(username, password):
            return account_home(username, password)
        else:
            return sign_in_get()


@application.route('/edit_account_info_get', methods=['GET'])
def edit_account_info_get():
    return render_template('edit_account.html')


@application.route('/account_home', methods=['GET', 'POST'])
def account_home(username, password):
    data = sql.get_home_info(username, password)
    firstname = sql.get_student_first_name(username, password)[0]
    return render_template('account_home.html', firstname=firstname, data=data)


@application.route('/send', methods=['GET', 'POST'])
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

        # normalize data as we enter it into input array
        input_data = [float(gpa) / 4.0, float(totalcreditcours) / 22.0, float(int(oncampus)), float(int(isworking)),
                      float(int(hasposition)), float(coursecredithours) / 6.0, float(courselevel) / 1000,
                      float(int(AestheticInterpetation)), float(int(EmpiricalandQuantitativeReasoning)),
                      float(int(EthicalReasoningandResponsibility)), float(int(GlobalIssuesandPerspectives)),
                      float(int(HistoricalPerspectives)), float(int(HumanDiversitywithintheUS)),
                      float(int(NaturalandPhysicalSciences)), float(int(SocialSciences))]
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

        return render_template('result.html', numerical_grade=numerical_grade, letter_grade=letter_grade)


if __name__ == '__main__':
    application.run(debug=True)
