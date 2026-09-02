"""
models.py
SQLAlchemy model for the Assignment Design Assistant.
Mirrors schema.sql exactly - one row per student submission.
"""
from datetime import datetime
from extensions import db


class AssignmentResponse(db.Model):
    __tablename__ = "assignment_responses"

    id = db.Column(db.Integer, primary_key=True)

    # Student / cover sheet details
    student_usn = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(150), nullable=False)
    tutor_name = db.Column(db.String(150))
    unit_code = db.Column(db.String(50), default="H6S9 46")
    unit_title = db.Column(db.String(200), default="Computing: Applications Development")
    date_due = db.Column(db.Date)
    date_submitted = db.Column(db.Date)

    # Application basics
    app_name = db.Column(db.String(200))
    app_type = db.Column(db.String(100))
    dev_environment = db.Column(db.String(150))

    # Task A - Outcome 1: Design Document
    task_1_1_proposal = db.Column(db.Text)
    task_1_2_resources = db.Column(db.Text)
    task_1_3_action_plan = db.Column(db.Text)
    task_1_4_design_diagrams = db.Column(db.Text)

    # Task B - Outcome 2: Application Development
    task_2_1_build_summary = db.Column(db.Text)
    task_2_2_project_log = db.Column(db.Text)

    # Task C - Outcome 3: Testing
    task_3_1_testing_evidence = db.Column(db.Text)
    task_3_2_error_log = db.Column(db.Text)
    task_3_3_demo_notes = db.Column(db.Text)

    # Task D - Outcome 4: Evaluation Report
    task_4_1_eval_design = db.Column(db.Text)
    task_4_2_eval_process = db.Column(db.Text)
    task_4_3_eval_application = db.Column(db.Text)
    task_4_4_future_actions = db.Column(db.Text)
    task_4_5_self_evaluation = db.Column(db.Text)

    status = db.Column(db.String(20), default="draft")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Field groups used to render the form and the export sheet in one place,
    # so the on-screen form always matches the assignment brief's structure.
    FIELD_GROUPS = [
        {
            "task": "Task A - Outcome 1: Design Document (25 Marks)",
            "fields": [
                ("task_1_1_proposal", "1.1 Application Proposal (min. 300 words)",
                 "Describe the application name, type, purpose, and target audience.", 5),
                ("task_1_2_resources", "1.2 Resources & Justification",
                 "List hardware, software and electronic media needed; justify your chosen "
                 "development environment (confirm it supports variables, selection, loops, functions).", 5),
                ("task_1_3_action_plan", "1.3 Action Plan",
                 "Key tasks, milestones and realistic timescales within the 40-hour unit.", 5),
                ("task_1_4_design_diagrams", "1.4 Design Diagrams & Written Designs",
                 "Describe at least two annotated diagrams (wireframes, flowcharts, storyboards, etc.) "
                 "you have produced separately. Paste descriptions/links here.", 10),
            ],
        },
        {
            "task": "Task B - Outcome 2: Application Development (35 Marks)",
            "fields": [
                ("task_2_1_build_summary", "2.1 Build Summary",
                 "Summarise what you built and which constructs (variables, selection, loops, "
                 "functions) you evidenced. Attach the actual application/PDF separately.", 25),
                ("task_2_2_project_log", "2.2 Project Log",
                 "Key decisions made, problems encountered, and solutions implemented.", 10),
            ],
        },
        {
            "task": "Task C - Outcome 3: Testing (20 Marks)",
            "fields": [
                ("task_3_1_testing_evidence", "3.1 Testing Evidence Summary",
                 "Summarise your test scenarios, expected/actual results and pass/fail status. "
                 "Full test cases belong in your Excel testing sheet.", 10),
                ("task_3_2_error_log", "3.2 Error Rectification Log",
                 "Errors identified during testing and the changes made to fix them.", 5),
                ("task_3_3_demo_notes", "3.3 Application Demonstration Notes",
                 "Notes on your 2-3 minute demo video: what it shows and where it is stored.", 5),
            ],
        },
        {
            "task": "Task D - Outcome 4: Evaluation Report (20 Marks)",
            "fields": [
                ("task_4_1_eval_design", "4.1 Evaluation of the Design Document",
                 "Strengths and areas for improvement.", 4),
                ("task_4_2_eval_process", "4.2 Evaluation of the Development Process",
                 "Strengths/improvements; comment on time management and the action plan.", 4),
                ("task_4_3_eval_application", "4.3 Evaluation of the Application",
                 "Strengths/improvements; compare the final app against your design document.", 4),
                ("task_4_4_future_actions", "4.4 Action Points for Future Development",
                 "Specific action points to improve future projects.", 4),
                ("task_4_5_self_evaluation", "4.5 Self-Evaluation of Personal Performance",
                 "Critical reflection on your own performance throughout the project.", 4),
            ],
        },
    ]

    def to_export_row(self):
        """Flat dict used for the Excel export - column order matches the brief."""
        row = {
            "Student USN": self.student_usn,
            "Student Name": self.student_name,
            "Tutor": self.tutor_name,
            "Unit Code": self.unit_code,
            "Unit Title": self.unit_title,
            "Date Due": self.date_due.isoformat() if self.date_due else "",
            "Date Submitted": self.date_submitted.isoformat() if self.date_submitted else "",
            "Application Name": self.app_name,
            "Application Type": self.app_type,
            "Development Environment": self.dev_environment,
        }
        for group in self.FIELD_GROUPS:
            for field_name, label, _hint, _marks in group["fields"]:
                row[label] = getattr(self, field_name) or ""
        row["Status"] = self.status
        row["Submitted At (UTC)"] = self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else ""
        return row
