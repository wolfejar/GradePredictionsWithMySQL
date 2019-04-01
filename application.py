import sys
import numpy as np
from flask import Flask, render_template, request
import current_model

application = Flask(__name__)


@application.route('/')
@application.route('/index')
def home():
    model = current_model.get_model()
    data = model.__str__()
    return render_template('landing.html', data=data)


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
        input_data = [float(gpa) / 100.0, float(totalcreditcours) / 22.0, float(int(oncampus)), float(int(isworking)),
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
