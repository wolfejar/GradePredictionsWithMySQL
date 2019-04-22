import mysql.connector
import sys
from passlib.hash import pbkdf2_sha256


class SQL:
    def __init__(self, ):
        self.mydb = mysql.connector.connect(
            host=sys.argv[1],
            user=sys.argv[2],
            passwd=sys.argv[3],
            database="CollegeStateUniversity"
        )
        self.mydb.autocommit = True
        self.my_cursor = self.mydb.cursor()

    def get_all_course_students(self, how_many):
        self.my_cursor.execute('''Select CS.GradePoints, info.GPA as StudentGPA,
        info.TotalCreditHours as StudentTotalCreditHours, info.OnCampus as StudentOnCampus,
        info.IsWorking as StudentIsWorking, coalesce(AST.HasPosition, 0) as StudentHasActivityPosition,
        C.CreditHours as CourseCreditHours, C.CourseLevel,
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
            S.GPA, S.OnCampus, S.IsWorking
            from CourseStudent CS
            join Course C on C.CourseId = CS.CourseId
            join Student S on S.StudentId = CS.StudentId
            group by S.StudentId
        ) as info
        left join ActivityStudent AST on AST.StudentId = info.StudentId 
        join CourseStudent CS on CS.StudentId = info.StudentId
        join Course C on C.CourseId = CS.CourseId
        join CourseType CT on CT.CourseTypeId = C.CourseTypeId;''')
        return self.my_cursor.fetchmany(how_many)

    def sign_in(self, username, raw):
        return pbkdf2_sha256.verify(raw, self.get_hashed(username))

    def get_hashed(self, username):
        self.my_cursor.execute('''
            SELECT S.StudentPassword
            From Student S
            Where S.StudentId = '{}'
        '''.format(username))
        return self.my_cursor.fetchone()[0]

    def get_home_info(self, username):
        self.my_cursor.execute('''
            SELECT C.CourseName, C.CourseLevel, C.CreditHours, CT.CourseTypeName, concat(CS.GradePoints, '%') 
            FROM Student S
            Join CourseStudent CS on CS.StudentId = S.StudentId
            Join Course C on C.CourseId = CS.CourseId
            Join CourseType CT on C.CourseTypeId = CT.CourseTypeId
            Where S.StudentId = {}
            '''.format(username))
        return self.my_cursor.fetchall()

    def get_student_first_name(self, username):
        self.my_cursor.execute('''
            SELECT S.FirstName
            FROM Student S
            where S.StudentId = {}   
        '''.format(username))
        return self.my_cursor.fetchone()[0]

    def create_student(self, first_name, last_name, on_campus, is_working, gpa, password):
        self.my_cursor.execute('''
            INSERT INTO Student(FirstName, LastName, OnCampus, IsWorking, GPA, StudentPassword)
            VALUES ('{}' ,'{}', {}, {}, {}, '{}');
        '''.format(first_name, last_name, on_campus, is_working, gpa, password))
        self.my_cursor.execute('''
            SELECT LAST_INSERT_ID();
        ''')  # This wil be SELECT SCOPE_IDENTITY with SQLServer
        return self.my_cursor.fetchone()

    def get_student_info_by_id(self, student_id):
        self.my_cursor.execute('''
            Select S.FirstName, S.LastName, S.StudentId, S.GPA, S.OnCampus, S.IsWorking
            FROM Student S
            Where S.StudentId = {};
        '''.format(student_id))
        return self.my_cursor.fetchone()

    def get_student_grades_by_course(self, course_id):
        self.my_cursor.execute('''
            SELECT CS.GradePoints
            FROM CourseStudent CS
            WHERE CS.CourseId = {}
        '''.format(course_id))
        return self.my_cursor.fetchone()