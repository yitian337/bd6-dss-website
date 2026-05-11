import re
import sqlite3

# -----------------------------
# Initiate setup
# -----------------------------

def clear_data():
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM PATIENTS")
    cursor.execute("DELETE FROM MOVEMENTS")
    connection.commit()
    connection.close()

def init_data():
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()

    patients_table = '''CREATE TABLE IF NOT EXISTS PATIENTS(
    PATIENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT,
    GENDER TEXT,
    DOB TEXT
    )'''
    cursor.execute(patients_table)
    
    movements_table = '''CREATE TABLE IF NOT EXISTS MOVEMENTS(
    MOVEMENT_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PATIENT_ID INTEGER,
    DATETIME TEXT,
    MOVEMENT_TYPE TEXT,
    RISK_LEVEL TEXT,
    FOREIGN KEY(PATIENT_ID) REFERENCES PATIENTS(PATIENT_ID)
    )'''
    cursor.execute(movements_table)

    notes_table = '''CREATE TABLE IF NOT EXISTS NOTES(
    NOTE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    PATIENT_ID INTEGER,
    DATETIME TEXT,
    NOTE_TEXT TEXT,
    FOREIGN KEY(PATIENT_ID) REFERENCES PATIENTS(PATIENT_ID)
    )'''
    cursor.execute(notes_table)

    connection.commit()
    connection.close()

# -----------------------------
# Patient functions
# -----------------------------

def add_patient(name, gender, dob):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()

    patient = '''INSERT INTO PATIENTS(NAME, GENDER, DOB) 
        VALUES(?, ?, ?)'''
    cursor.execute(patient, (name, gender, dob))
    connection.commit()
    connection.close()

def all_patients():
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()

    read = '''SELECT * FROM PATIENTS'''
    cursor.execute(read)
    output = cursor.fetchall()
    connection.close()
    return output

# -----------------------------
# Notes functions
# -----------------------------

def add_note(patient_id, datetime_str, note_text):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    
    # Insert note record
    insert = '''INSERT INTO NOTES(PATIENT_ID, DATETIME, NOTE_TEXT)
        VALUES(?, ?, ?)'''
    cursor.execute(insert, (patient_id, datetime_str, note_text))
    connection.commit()
    connection.close()

def get_patient_notes(patient_id):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()

    read = '''SELECT NOTE_ID, DATETIME, NOTE_TEXT FROM NOTES 
              WHERE PATIENT_ID = ? ORDER BY DATETIME DESC'''
    cursor.execute(read, (patient_id,))
    output = cursor.fetchall()
    connection.close()
    return output   

# -----------------------------
# Patient data functions
# -----------------------------

def add_movement(patient_id, datetime_str, movement_type, risk_level):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()
    
    # Insert movement record
    insert = '''INSERT INTO MOVEMENTS(PATIENT_ID, DATETIME, MOVEMENT_TYPE, RISK_LEVEL)
        VALUES(?, ?, ?, ?)'''
    cursor.execute(insert, (patient_id, datetime_str, movement_type, risk_level))
    connection.commit()
    connection.close()

def get_patient_movements(patient_id):
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()

    read = '''SELECT MOVEMENT_ID, DATETIME, MOVEMENT_TYPE, RISK_LEVEL FROM MOVEMENTS 
              WHERE PATIENT_ID = ? ORDER BY DATETIME DESC'''
    cursor.execute(read, (patient_id,))
    output = cursor.fetchall()
    connection.close()
    return output

def get_all_movements():
    connection = sqlite3.connect('clinic.db')
    cursor = connection.cursor()

    read = '''SELECT MOVEMENT_ID, PATIENT_ID, DATETIME, MOVEMENT_TYPE, RISK_LEVEL FROM MOVEMENTS 
              ORDER BY DATETIME DESC'''
    cursor.execute(read)
    output = cursor.fetchall()
    connection.close()
    return output



















# patients = [
#     {"id": "P001", "name": "Patient A", "gender": "Unknown", "initials": "PA"},
#     {"id": "P002", "name": "Patient B", "gender": "Unknown", "initials": "PB"},
#     {"id": "P003", "name": "Patient C", "gender": "Unknown", "initials": "PC"},
#     {"id": "P004", "name": "Patient D", "gender": "Unknown", "initials": "PD"},
# ]

# # -----------------------------
# # Fake exercise report data
# # later can be replaced by SQL
# # -----------------------------
# fake_reports = {
#     "Patient A": {
#         "score": 84,
#         "rom": "72%",
#         "stability": "80%",
#         "coordination": "78%",
#         "feedback": "goodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgood",
#         "clinician_note": "I hate the start of school.",
#         "image": "images/reach.png"
#     },
#     "Patient B": {
#         "score": 88,
#         "rom": "85%",
#         "stability": "82%",
#         "coordination": "86%",
#         "feedback": "Arm lifting performance was generally good. Minor asymmetry appeared near the end of the movement.",
#         "clinician_note": "hi",
#         "image": "images/lift_arm.png"
#     },
#     "Patient C": {
#         "score": 76,
#         "rom": "68%",
#         "stability": "74%",
#         "coordination": "71%",
#         "feedback": "Rotation task showed limited range and reduced smoothness. Compensation at the shoulder was detected.",
#         "clinician_note": "wish we can get good marks.",
#         "image": "images/rotate_arm.png"
#     },
#     "Patient D": {
#         "score": 69,
#         "rom": "61%",
#         "stability": "65%",
#         "coordination": "63%",
#         "feedback": "no feedback",
#         "clinician_note": "🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱",
#         "image": "images/unknown.png"
#     }
# }

# fake_exercise = {
#     "Reach and Retrieve": {
#         "image": "images/reach.png",
#         "feedback": "Reach task performance...",
#         "clinician_note": "Keep arm straight."
#     },
#     "Lift Arm": {
#         "image": "images/lift_arm.png",
#         "feedback": "Arm lifting is stable...",
#         "clinician_note": "Reduce shoulder elevation."
#     },
#     "Rotate Arm": {
#         "image": "images/rotate_arm.png",
#         "feedback": "Rotation limited...",
#         "clinician_note": "Focus on smooth motion."
#     },
#     "Unknown": {
#         "image": "images/unknown.png",
#         "feedback": "Unknown exercise...",
#         "clinician_note": "Check classification."
#     }
# }