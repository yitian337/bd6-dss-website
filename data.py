# -----------------------------
# Data & Setup
# later can be replaced by SQL
# -----------------------------
patients = [
    {"id": "P001", "name": "Patient A", "gender": "Unknown", "initials": "PA"},
    {"id": "P002", "name": "Patient B", "gender": "Unknown", "initials": "PB"},
    {"id": "P003", "name": "Patient C", "gender": "Unknown", "initials": "PC"},
    {"id": "P004", "name": "Patient D", "gender": "Unknown", "initials": "PD"},
]

# -----------------------------
# Fake exercise report data
# later can be replaced by SQL
# -----------------------------
fake_reports = {
    "Patient A": {
        "score": 84,
        "rom": "72%",
        "stability": "80%",
        "coordination": "78%",
        "feedback": "goodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgoodgood",
        "clinician_note": "I hate the start of school.",
        "image": "images/reach.png"
    },
    "Patient B": {
        "score": 88,
        "rom": "85%",
        "stability": "82%",
        "coordination": "86%",
        "feedback": "Arm lifting performance was generally good. Minor asymmetry appeared near the end of the movement.",
        "clinician_note": "hi",
        "image": "images/lift_arm.png"
    },
    "Patient C": {
        "score": 76,
        "rom": "68%",
        "stability": "74%",
        "coordination": "71%",
        "feedback": "Rotation task showed limited range and reduced smoothness. Compensation at the shoulder was detected.",
        "clinician_note": "wish we can get good marks.",
        "image": "images/rotate_arm.png"
    },
    "Patient D": {
        "score": 69,
        "rom": "61%",
        "stability": "65%",
        "coordination": "63%",
        "feedback": "no feedback",
        "clinician_note": "🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱🥱",
        "image": "images/unknown.png"
    }
}

fake_exercise = {
    "Reach and Retrieve": {
        "image": "images/reach.png",
        "feedback": "Reach task performance...",
        "clinician_note": "Keep arm straight."
    },
    "Lift Arm": {
        "image": "images/lift_arm.png",
        "feedback": "Arm lifting is stable...",
        "clinician_note": "Reduce shoulder elevation."
    },
    "Rotate Arm": {
        "image": "images/rotate_arm.png",
        "feedback": "Rotation limited...",
        "clinician_note": "Focus on smooth motion."
    },
    "Unknown": {
        "image": "images/unknown.png",
        "feedback": "Unknown exercise...",
        "clinician_note": "Check classification."
    }
}