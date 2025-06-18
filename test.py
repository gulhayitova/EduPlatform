from main import *

teach1 = Teacher(100, "Samantha White", 'samantha.white203@gmail.com', 'teacher', ["Math", "Physics"], '998901112233')
stu1 = Student(200, 'Dori Kalil', 'dorikal1l@gmail.com', 'student200', '9A')
admin1 = Admin(1000, "Bob Marley", 'bob-marley@gmail.com', 'bobm@rley', ['add_user', 'remove_user']) # adding admin manually; permissions
USERS[admin1._id] = admin1
ADMINS[admin1._id] = admin1

admin1.add_user(teach1) # admin can directly add users
admin1.add_user(stu1)

parent1 = Parent(300, "Meryl Kalil", 'meryl.kalil@gmail.com', 'dorismother', [200], '998754323221')
admin1.add_user(parent1)

teach1.create_assignment("Reflection essay", "Reflection essay on Shakespeare's poem of choice, words limit: 300", '2025/06/20', 'Literature', '9A', 'Medium')
stu1.view_notifications()
parent1.receive_child_notifications(200)

stu1.submit_assignment(1, 'kgk')
teach1.grade_assignment(1, 200, 4)

monday_9a = Schedule(400, '9A', 'Monday')
monday_9a.add_lesson('9:00', 'Physics', 100)
# monday_9a.view_schedule()
tuesday_9a = Schedule(401, '9A', 'Tuesday')
stu1.view_schedule()

admin1.export_to_csv()
admin1.export_to_xlsx()
admin1.export_to_sql()

monday_10a = Schedule(402, '10A', 'Monday')
# monday_10a.add_lesson('9:00', 'Physics', 100)
print(SCHEDULES)
monday_10a.add_lesson('10:00', 'Math', 100)