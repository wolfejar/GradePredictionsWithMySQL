import sys
import os
import matplotlib.pyplot as plt
import mysql.connector
import tensorflow as tf
from tensorflow import keras
import numpy as np

mydb = mysql.connector.connect(
    host=sys.argv[1],
    user=sys.argv[2],
    passwd=sys.argv[3],
    auth_plugin='mysql_native_password',
    database=sys.argv[4]
)

print(mydb)

my_cursor = mydb.cursor()

my_cursor.execute('''Select CS.GradePoints, info.GPA as StudentGPA, info.TotalCreditHours as StudentTotalCreditHours,
info.OnCampus as StudentOnCampus, info.IsWorking as StudentIsWorking,
coalesce(AST.HasPosition, 0) as StudentHasActivityPosition, C.CreditHours as CourseCreditHours,
C.CourseLevel,
case when CT.CourseTypeId = 1 then 1 else 0 end as AestheticInterpretation,
case when CT.CourseTypeId = 2 then 1 else 0 end as EmpiricalandQuantitativeReasoning,
case when CT.CourseTypeId = 3 then 1 else 0 end as EthicalReasoningandResponsibility,
case when CT.CourseTypeId = 4 then 1 else 0 end as GlobalIssuesandPerspectives,
case when CT.CourseTypeId = 5 then 1 else 0 end as HistoricalPerspectives,
case when CT.CourseTypeId = 6 then 1 else 0 end as HumanDiversitywithintheUS,
case when CT.CourseTypeId = 7 then 1 else 0 end as NaturalandPhysicalSciences,
case when CT.CourseTypeId = 8 then 1 else 0 end as SocialSciences
from (
    Select S.StudentId, S.FirstName, S.LastName, SUM(C.CreditHours) as TotalCreditHours,
    (SUM(CS.GradePoints * C.CreditHours) / SUM(C.CreditHours)) as GPA, S.OnCampus, S.IsWorking
    from CourseStudent CS
    join Course C on C.CourseId = CS.CourseId
    join Student S on S.StudentId = CS.StudentId
    group by S.StudentId
) as info
left join ActivityStudent AST on AST.StudentId = info.StudentId 
join CourseStudent CS on CS.StudentId = info.StudentId
join Course C on C.CourseId = CS.CourseId
join CourseType CT on CT.CourseTypeId = C.CourseTypeId;''')


def build_list(arr):
    inputs = []
    outputs = []
    for entry in arr:
        resulting_row = []
        for i, col in enumerate(entry):
            if i == 0:
                outputs.append(float(col))
            elif i == 1:
                resulting_row.append(float(col)/4.0)
            elif i == 2:
                resulting_row.append(float(col) / 22.0)
            elif i == 6:
                resulting_row.append(float(col) / 6.0)
            elif i == 7:
                resulting_row.append(float(col) / 1000.0)
            else:
                resulting_row.append(float(col))
        inputs.append(resulting_row)
    return np.array(inputs), np.array(outputs)


# input for nn
# double gpa, bool double  total credit hours, bool on campus, bool working, bool student in activity position,
# int course credit hours, int course level,
# bool aesthetic, bool empirical, bool ethical, bool global issue, bool historical, bool human diversity,
# bool natural/physical sciences, bool social sciences
input_rows, classifications = build_list(my_cursor.fetchmany(4500))

model = keras.Sequential([
    keras.layers.Dense(15, activation=tf.nn.relu),
    keras.layers.Dense(20, activation=tf.nn.relu),
    keras.layers.Dense(1)
  ])

optimizer = tf.keras.optimizers.RMSprop(0.001)

model.compile(loss='mean_squared_error',
              optimizer=optimizer,
              metrics=['mean_absolute_error', 'mean_squared_error'])

'''if os.path.isfile('./checkpoint'):
    model.load_weights('./most_recent_model')
else:'''
model.fit(
        input_rows, classifications,
        epochs=1000, validation_split=0.2, verbose=0)

loss, mae, mse = model.evaluate(input_rows, classifications, verbose=0)

print('Mean abs error:', mae)
print('Mean square error: ', mse)

test_rows, test_classifications = build_list(my_cursor.fetchmany(500))
test_predictions = model.predict(test_rows)

plt.scatter(test_classifications, test_predictions)
plt.xlabel('True Values [MPG]')
plt.ylabel('Predictions [MPG]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])
plt.show()

model.save_weights('./most_recent_model')
