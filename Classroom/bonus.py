"""
1. Create users and subjects data from files

get_subjects_from_json(subjects_json)

get_users_with_grades(users_json, subjects_json, grades_json)

2. Simulate working with the application

method User.create_user(username, password, role) creates user

method user.add_score_for_subject(subject:Subject, score: Score) adds score for subject

function add_user(user, users) adds user to users (in case of uniqueness username)

function add_subject(subject, subjects) adds subject to subjects (in case of uniqueness title)

function get_grades_for_user(username:str, user:User, users:list) returns all grades for the user
 with username (only own grades or for mentor)

3. Rewrite the old json-files with new ones

users_to_json(users, json_file)

subjects_to_json(subjects, json_file)

grades_to_json(users, subjects, json_file)
"""
import re
from enum import Enum
import json
import uuid


class Role(Enum):
    Mentor = 1
    Trainee = 0


class Subject:
    def __init__(self, title, id=None):
        self.title = title
        self.id = id
        if self.id is None:
            self.id = uuid.uuid4()


class Score(Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'


class User:
    def __init__(self, username, password, role, grades=[], id=None):
        self.username = username
        self.password = password
        self.role = role
        self.grades = grades
        self.id = id
        self._validate_password()


    @classmethod
    def create_user(cls, username, password, role):
        return cls(username, password, role, id=uuid.uuid4())


    def add_score_for_subject(self, subjects, score):
        subject_score = {subjects.title: score.value}
        return self.grades.append(subject_score)


    def _validate_password(self):
        if not re.compile(
            '^(?=\S{6,}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])').search(
            self.password):
            raise PasswordValidationException


    def __repr__(self):
        return f"{self.username} with role {self.role}: {self.grades}"


def get_subjects_from_json(subjects_json):
    with open(subjects_json) as s:
        return [Subject(**i) for i in json.load(s)]


def get_users_with_grades(users_json, subjects_json, grades_json):
    with open(users_json) as u, open(subjects_json) as s, open(grades_json) as g:
        u1, s2, g3 = json.load(u), json.load(s), json.load(g)
        subject_grade = []
        for i in g3:
            for j in s2:
                if i['subject_id'] == j['id']:
                    subject_grade.append({j['title']: i['score']})
        u1[0].setdefault('grades', subject_grade)
        return [User(**u1[0])]


def add_user(user, users):
    for i in users:
        if user.username == i.username:
            raise NonUniqueException(f'User with name {user.username} already exists')
    users.append(user)
    return users


def check_if_user_present(name, password, data):
    for i in data:
        if name == i.username and password == i.password:
            return True
    return False


def get_grades_for_user(username, user, users):
    if username == user.username or user.role == Role.Mentor:
        for i in users:
            if i.username == username:
                return i.grades
    raise ForbiddenException


# def get_grades_for_user(username, user, users):
#     if username == user.username or user.role == Role.Mentor:
#         grade = []
#         for i in users:
#             if i.username == username:
#                     grade.extend(i.grades)
#                     break
#         grade_unique = []
#         for i in grade:
#             if i not in grade_unique:
#                 grade_unique.append(i)
#         return grade_unique
#     raise ForbiddenException


def users_to_json(users, json_file):
    with open(json_file, 'w') as f:
        users_json = [i.__dict__ for i in users]
        out = []

        for i in users_json:
            user = {}
            for j in i.keys():
                if isinstance(i[j], uuid.UUID):
                    i[j] = uuid_to_str(i[j])
                if isinstance(i[j], Enum):
                    i[j] = i[j].value
                if j != 'grades':
                    user.setdefault(j, i[j])
            out.append(user)
        return json.dump(out, f, indent=4)


def uuid_to_str(id):
    return str(id).replace('-', '')


def file_contains(json_file, id, num):  #####Exception user must have id
    with open(json_file) as f:
        data = json.load(f)
        for i in data:
            if num > len(i[id]):
                return False
        return True


def subjects_to_json(subjects, json_file):
    with open(json_file, 'w') as f:
        subjects_json = [i.__dict__ for i in subjects]
        for i in subjects_json:
            if isinstance(i['id'], uuid.UUID):
                i['id'] = uuid_to_str(i['id'])
        return json.dump(subjects_json, f, indent=4)


def grades_to_json(users, subjects, json_file):
    subjects_json = [i.__dict__ for i in subjects]
    users_json = [i.__dict__ for i in users]
    grades_json = []
    for user in users_json:

        for grade in user['grades']:
            key, value = list(grade.items())[0]

            for subject in subjects_json:
                grades = {}

                if key == subject['title']:
                    grades.setdefault('user_id', uuid_to_str(user['id']))
                    grades.setdefault('subject_id', uuid_to_str(subject['id']))
                    grades.setdefault('score', value)

                    grades_json.append(grades)
                    break

    with open(json_file, 'w') as f:
        return json.dump(grades_json, f, indent=4)


def add_subject(subject, subjects):
    return subjects.append(subject)


class NonUniqueException(Exception):
    def __init__(self, msg):
        self.msgs = msg


class PasswordValidationException(Exception):
    pass


class ForbiddenException(Exception):
    pass


users = get_users_with_grades("users.json", "subject.json", "grades.json")
print(len(users))

subjects = get_subjects_from_json("subject.json")
print(len(subjects))
mentor = User.create_user("Mentor", "!1qQ456", Role.Mentor)
add_user(mentor, users)
print(mentor)
student = User.create_user("Mentor", "!1qQ456", Role.Trainee)
try:
    add_user(student, users)
except NonUniqueException as e:
    print(str(e))

print(check_if_user_present("Mentor", "aaaaaa", users))
print(check_if_user_present("Mentor", "!1qQ456", users))
print(get_grades_for_user("Trainee1", users[1], users))
print(get_grades_for_user("Mentor", users[1], users))
user2 = User.create_user("Second", "Password_0", Role.Trainee)
add_user(user2, users)
user2.add_score_for_subject(subjects[1], Score.B)
print(len(users))
print(user2)
subject = Subject("New Subject")
add_subject(subject, subjects)
users[0].add_score_for_subject(subject, Score.D)

print(get_grades_for_user("Trainee1", users[1], users))
users_to_json(users, "345.json")
print(file_contains("345.json", "id", 20))

subjects_to_json(subjects, "578.json")
print(file_contains("578.json", "id", 20))
grades_to_json(users, subjects, "987.json")
print(file_contains("987.json", "user_id", 20))
print(file_contains("987.json", "subject_id", 20))

try:
    user = User.create_user("Name", "InvalidPassword", Role.Trainee)
except PasswordValidationException:
    print("Invalid password")

try:
    print(get_grades_for_user("Second", users[0], users))
except ForbiddenException:
    print("Forbidden")
print(get_grades_for_user("Second", users[2], users))
