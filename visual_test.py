import pandas as pd
import sql_scripts
import matplotlib.pyplot as plt

sql = sql_scripts.SQL()

df = pd.read_sql('''select *  
                 from Student S
                 join CourseStudent CS on CS.StudentId = S.StudentId
                 join ActivityStudent AST on AST.StudentId = S.StudentId
                 join Course C on C.CourseId = CS.CourseId
                 join CourseInstructor CI on CI.CourseId = C.CourseId
                 join Instructor I on I.InstructorId = CI.InstructorId''', sql.mydb)

print(df.describe())

df.hist(bins=50, figsize=(20, 15))

plt.show()





