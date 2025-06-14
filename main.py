from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum
import uuid
from typing import Literal


class Assignment:
    def __init__(self, id: int, title: str, description: str, deadline: str, subject: str, teacher_id: int, class_id: str):
        self.id = id
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id

        self.submissions: dict[int, str] = {} # {student id: content}
        self.grades: dict[int, Grade] = {} # {student id: assignment grade}

        ASSIGNMENTS[self.id] = self # adding to the dictionary
    
    def add_submissions(self, student_id: int, content: str): # CONTENT
        if student_id in self.submissions:
            print(f"Student {student_id} vazifani allaqachon topshirgan. Ustidan yozilmaydi.")
            return
        self.submissions[student_id] = content
        print("Vazifa {student_id} tomonidan qabul qilindi.")


    def set_grade(self, student_id: int, grade: float):
        if student_id in self.submissions:
            if grade >= 0 and grade <= 100:
                self.grades[student_id] = grade
                print(f"{student_id}ga {grade} ball qo'yildi.")
            else:
                raise ValueError("Ball 0 - 100 shkalada emas.")
        else:
            print(f"{student_id}ning topshirgan vazifasi topilmadi.")

    def get_status(self):
        now = datetime.now().isocalendar()
        if now < self.deadline:
            print("Vazifalar qabul qilinmoqda.")
        print("Dedlayn tugadi. Vazifalar qabul qilinmaydi.")





class User_role(Enum): #For User
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"

class AbstractRole(ABC):
    def __init__(self, _id: int, _full_name: str, _email: str, _password_hash: str, _created_at: str = None):
        self._id = _id
        self._full_name = _full_name
        self._email = _email
        self._password_hush = _password_hash
        self._created_at = _created_at or datetime.now().isoformat()

    @abstractmethod
    def get_profile(self):
        pass

    @abstractmethod
    def update_profile(self):
        pass

class User(AbstractRole):
    def __init__(self, _id: int, _full_name: str, _email: str, _password_hash: str, role: User_role, _notifications = None,_created_at: str = None):
        super().__init__(_id, _full_name, _email, _password_hash, _created_at)
        self.role = role
        if _notifications is None:
            self._notifications = []
        else:
            self._notifications = _notifications

    def get_profile(self):
        return {
            "id": self._id,
            "full name": self._full_name,
            "email": self._email,
            "role": self.role.value,
            "created at": self._created_at
        }

    def update_profile(self, full_name = None, email = None, password_hash = None):
        if full_name:
            self._full_name = full_name
        if email:
            self._email = email
        if password_hash:
            self._password_hush = password_hash

    def add_notification(self, notification_message: str):
        notification = {
            "id": uuid.uuid4, # every notification should have a unique id
            "message": notification_message
        }
        self._notifications.append(notification)

    def view_notifications(self):
        return self._notifications

    def delete_notification(self, id: str):
        self._notifications = [i for i in self._notifications if i["id"] != id]

class Student(User):
    def __init__(self, _id: int, _full_name: str, _email: str, _password_hash: str,  
                grade: str, _notifications = None, _created_at: str = None):
        super().__init__(_id, _full_name, _email, _password_hash, User_role.STUDENT, _notifications, _created_at)
        self.grade = grade
        self.subjects: dict[str, int] = {} # {Subject Name: Teacher ID}
        self.assignments: dict[str, str] = {} # {Assignment ID: status}
        self.grades: dict[str, list[float]] = {} # {Subject: grades}

    def submit_assignment(self, assignment_id, content):
        self.assignments[assignment_id] = 'submitted'
        return f"Vazifa {assignment_id} muvaffaqiyatli qabul qilindi."
        # WHERE TO STORE THE CONTENT?

    def view_grades(self, subject=None):
        if subject:
            return self.grades.get(subject, [])
        return self.grades

    def calculate_average_grade(self):
        total = 0
        count = 0
        for grade_list in self.grades.values():
            total += sum(grade_list)
            count += len(grade_list)
        if count == 0:
            return 0.0
        return round(total / count, 2)

class Teacher(User):
    def __init__(self, _id: int, _full_name: str, _email: str, _password_hash: str, _notifications = None,_created_at: str = None):
        super().__init__(_id, _full_name, _email, _password_hash, User_role.TEACHER, _notifications, _created_at)
        self.subjects : list[str] = [] # [subject name 1, subject name 2, ...]
        self.classes: list[str] = [] # [class id 1, class id 2, ...]
        self.assignments: dict[str, Assignment] = {} # {assignment id: Assignment}
        
    def create_assignment(self, title: str, description: str, deadline: str, subject: str, class_id: str):
        assignment_id = len(self.assignments) + 1
        assignment = Assignment(assignment_id, title, description, deadline, subject, class_id)
        self.assignments[assignment_id] = assignment
        print("Vazifa muvaffaqiyatli qo'shildi.")
    
    def grade_assignment(self, assignment_id: int, student_id: int, grade: float):
        assignment = self.assignments.get(assignment_id)
        if assignment:
            assignment.set_grade(student_id, grade)
            assignment.set_grade(student_id, grade)
        else:
            print(f"Vazifa {assignment_id} topilmadi.")
        
    def view_student_progress(self, student_id):
        student = STUDENTS.get(student_id)
        if student:
            progress = {
                subj: grades
                for subj, grades in student.grades.items()
                if subj in self.subjects
            }
            return progress
        raise ValueError(f"O'quvchi {student_id} topilmadi.")

class Parent(User):
    def __init__(self, _id: int, _full_name: str, _email: str, _password_hash: str, children: list[int], _notifications = None,_created_at: str = None):
        super().__init__(_id, _full_name, _email, _password_hash, User_role.PARENT , _notifications, _created_at)
        self.children = children # list of student ids

    def view_child_grades(self, child_id: int):
        child = STUDENTS.get(child_id)
        if child:
            if child_id in self.children:
                print(f"Sizda o'quvchi {child_id}ning ma'lumotlarini ko'rishga ruxsat yo'q.")
                return
            return child.grades
        else:
            raise ValueError(f"O'quvchi {child_id} topilmadi.")
    
    def view_child_assignments(self, child_id: int):
        child = STUDENTS.get(child_id)
        if child:
            if child_id in self.children:
                print(f"Sizda o'quvchi {child_id}ning ma'lumotlarini ko'rishga ruxsat yo'q.")
                return
            return child.assignments
        else:
            raise ValueError(f"O'quvchi {child_id} topilmadi.")

    def receive_child_notifications(self, child_id: int):
        child = STUDENTS.get(child_id)
        if child:
            if child_id in self.children:
                print(f"Sizda o'quvchi {child_id}ning baholarini ko'rishga ruxsat yo'q.")
                return
            return child._notifications
        else:
            raise ValueError(f"O'quvchi {child_id} topilmadi.")

class Admin(User):
    def __init__(self,  _id: int, _full_name: str, _email: str, _password_hash: str, permissions: list[str], _notifications = None,_created_at: str = None):
        super().__init__(_id, _full_name, _email, _password_hash, User_role.PARENT , _notifications, _created_at)
        self.permissions = permissions # list of permissions
    
    def add_user(self, user: User): # A PERENT CLASS, MIGHT CLASH
        USERS[user._id] = user
        match user.role.name:
            case "Teacher":
                TEACHERS[user._id] = user
            case "Student":
                STUDENTS[user._id] = user
            case "Parent":
                PARENTS[user._id] = user
            case "Admin":
                ADMINS[user._id] = user

    def remove_user(self, user_id):
        if user_id in USERS:
            match USERS[user_id].role.name:
                case "Teacher":
                    del TEACHERS[user_id]
                case "Student":
                    del STUDENTS[user_id]
                case "Parent":
                    del PARENTS[user_id]
            del USERS[user_id]
            print(f"Foydalanuvchi {user_id} bazadan o'chirildi.")
        else:
            print(f"Foydalanuvchi {user_id} bazada topilmadi.")
    
    def generate_report(self):
        report = {
            "Total_users" : len(USERS),
            "Total_students" : len(STUDENTS),
            "Total_teachers" : len(TEACHERS),
            "Total_parents" : len(PARENTS),
            "Total_assignments" : len(ASSIGNMENTS),
            "Total_grades" : len(GRADES)
        }
        for k, v in report.items():
            print(f"{k.replace("_", " ")}: {v}")
        return report

class Grade():
    def __init__(self, id: int, student_id: int, subject: str, value: Literal[1, 2, 3, 4, 5], date: str, teacher_id: int):
        self.id = id
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = date
        self.teacher_id = teacher_id

    def update_grade(self, value: Literal[1, 2, 3, 4, 5]):
        self.value = value

    def get_grade_info(self):
        info = {
            "Student_ID" : self.student_id,
            "Subject" : self.subject,
            "Value" : self.value,
            "Date" : self.date,
            "Teacher_ID" : self.teacher_id
        }
        for k, v in info.items():
            print(f"{k.replace("_", " ")}: {v}")
        return info

class Schedule:
    def __init__(self, id: int, class_id: str, day: str):
        self.id = id
        self.class_id = class_id
        self.day = day
        self.lessons : dict[str, dict[str, int]] = {} # lessons to be added later in form {time: {subject : teacher_id}}

    def add_lesson(self, time: str, subject: str, teacher_id: int):
        if time not in self.lessons:
            self.lessons[time] = {subject : teacher_id}
        else:
            raise ValueError("Bu vaqtda allaqachon dars bor.")

    def view_schedule(self):
        schedule = {
            "Schedule_ID" : self.id,
            "Class_ID" : self.class_id,
            "Day" : self.day,
            "Lessons": self.lessons
        }
        for k, v in schedule.items():
            print(f"{k.replace("_", " ")} : {v}")
        return schedule

    def remove_lesson(self, time):
        if time in self.lessons:
            lesson = self.lessons.pop(time)
            subject = list(lesson)[0]
            print(f"Dars jadvalidan {subject} darsi o'chirildi.")
        else:
            print(f"Dars jadvalida {time} vaqt oralig'ida dars mavjud emas.")

class Notification():
    def __init__(self, id: int, message: str, receipent_id: int, created_at=None):
        self.id = id
        


USERS: dict[int, User] = {}
ADMINS: dict[int, Admin] = {}
STUDENTS: dict[int, Student] = {}
TEACHERS: dict[int, Teacher] = {}
PARENTS: dict[int, Parent] = {}
ASSIGNMENTS: dict[int, Assignment] = {}
GRADES: dict[int, Grade] = {}
SCHEDULES: dict[int, Schedule] = {}
NOTIFICATIONS: dict[int, Notification] = {}