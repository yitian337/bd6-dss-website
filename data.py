import re
import sqlite3
from pathlib import Path

# Database path - absolute path to ensure single database location
DB_PATH = str(Path(__file__).parent / 'clinic.db')

# -----------------------------
# Initiate setup
# -----------------------------

def clear_data():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM PATIENTS")
    cursor.execute("DELETE FROM MOVEMENTS")
    cursor.execute("DELETE FROM NOTES")
    connection.commit()
    connection.close()

def init_data():
    connection = sqlite3.connect(DB_PATH)
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
    ROM_VALUE REAL,      
    JERK_VALUE REAL,     
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
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    patient = '''INSERT INTO PATIENTS(NAME, GENDER, DOB) 
        VALUES(?, ?, ?)'''
    cursor.execute(patient, (name, gender, dob))
    connection.commit()
    connection.close()

def all_patients():
    connection = sqlite3.connect(DB_PATH)
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
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    # Insert note record
    insert = '''INSERT INTO NOTES(PATIENT_ID, DATETIME, NOTE_TEXT)
        VALUES(?, ?, ?)'''
    cursor.execute(insert, (patient_id, datetime_str, note_text))
    connection.commit()
    connection.close()

def get_patient_notes(patient_id):
    connection = sqlite3.connect(DB_PATH)
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

def add_movement(patient_id, datetime_str, movement_type, rom_value, jerk_value, risk_level):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    insert = '''INSERT INTO MOVEMENTS(PATIENT_ID, DATETIME, MOVEMENT_TYPE, ROM_VALUE, JERK_VALUE, RISK_LEVEL)
                VALUES(?, ?, ?, ?, ?, ?)'''
    
    cursor.execute(insert, (patient_id, datetime_str, movement_type, rom_value, jerk_value, risk_level))
    
    connection.commit()
    
    last_id = cursor.lastrowid
    connection.close()
    
    return last_id

def get_patient_movements(patient_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    read = '''SELECT MOVEMENT_ID, DATETIME, MOVEMENT_TYPE, ROM_VALUE, JERK_VALUE, RISK_LEVEL FROM MOVEMENTS 
              WHERE PATIENT_ID = ? ORDER BY DATETIME DESC'''
    cursor.execute(read, (patient_id,))
    output = cursor.fetchall()
    connection.close()
    return output

def get_all_movements():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    read = '''SELECT MOVEMENT_ID, PATIENT_ID, DATETIME, MOVEMENT_TYPE, ROM_VALUE, JERK_VALUE, RISK_LEVEL FROM MOVEMENTS 
              ORDER BY DATETIME DESC'''
    cursor.execute(read)
    output = cursor.fetchall()
    connection.close()
    return output