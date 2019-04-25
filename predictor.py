from sql_scripts import SQL
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
import numpy as np

sql = SQL()

# normalizes data and creates a numpy matrix which can be fed into the model
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
            elif i == 16:
                # years teaching
                resulting_row.append(float(col) / 8.0)
            elif i == 18:
                # instructor degree
                resulting_row.append(float(col) / 8.0)
            else:
                resulting_row.append(float(col))
        inputs.append(resulting_row)
    return np.array(inputs), np.array(outputs)


# input for nn
# double gpa, bool double  total credit hours, bool on campus, bool working, bool student in activity position,
# int course credit hours, int course level,
# bool aesthetic, bool empirical, bool ethical, bool global issue, bool historical, bool human diversity,
# bool natural/physical sciences, bool social sciences
# int instructor_years_teaching, int instructor_tenured, int instructor_degree
# Should train on 40k samples, but we know the pattern can be learned almost exactly using only a small portion
input_rows, classifications = build_list(sql.get_all_course_students(4000))

model = keras.Sequential([
    keras.layers.Dense(18, activation=tf.nn.relu),
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

test_rows, test_classifications = build_list(sql.my_cursor.fetchmany(500))
test_predictions = model.predict(test_rows)

plt.scatter(test_classifications, test_predictions)
plt.xlabel('True Values [MPG]')
plt.ylabel('Predictions [MPG]')
plt.axis('equal')
plt.axis('square')
plt.xlim([0, plt.xlim()[1]])
plt.ylim([0, plt.ylim()[1]])
_ = plt.plot([-100, 100], [-100, 100])
plt.savefig('static/recent_model.png')
# plt.show()
model.save_weights('./most_recent_model')
