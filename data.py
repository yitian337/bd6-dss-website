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
    "Reach and Retrieve": {
        "score": 84,
        "rom": "72%",
        "stability": "80%",
        "coordination": "78%",
        "feedback": "The patient completed the reach task with moderate control. Slight trunk compensation was observed during forward reach.",
        "clinician_note": "Encourage slower reaching speed and reduce shoulder elevation during retrieval.",
        "image": "images/reach.png"
    },
    "Lift Arm": {
        "score": 88,
        "rom": "85%",
        "stability": "82%",
        "coordination": "86%",
        "feedback": "Arm lifting performance was generally good. Minor asymmetry appeared near the end of the movement.",
        "clinician_note": "Continue with guided repetition and monitor fatigue in the final phase.",
        "image": "images/lift_arm.png"
    },
    "Rotate Arm": {
        "score": 76,
        "rom": "68%",
        "stability": "74%",
        "coordination": "71%",
        "feedback": "Rotation task showed limited range and reduced smoothness. Compensation at the shoulder was detected.",
        "clinician_note": "Focus on controlled rotation and reduce excessive upper body movement.",
        "image": "images/rotate_arm.png"
    },
    "Unknown": {
        "score": 69,
        "rom": "61%",
        "stability": "65%",
        "coordination": "63%",
        "feedback": "Unknown exercise category. Motion quality appears inconsistent and requires manual review.",
        "clinician_note": "Please verify exercise type and confirm whether the uploaded sample is correctly labeled.",
        "image": "images/unknown.png"
    }
}