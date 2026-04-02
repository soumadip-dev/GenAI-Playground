from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

student_records = {
    "S001": {"name": "Arijit", "marks": 92, "grade": "A+"},
    "S002": {"name": "Soumadip", "marks": 88, "grade": "A"},
}


class MarksSubmissionRequest(BaseModel):
    student_id: str
    marks: int
    subject: str


# Retrieve details of a student by their ID.
@app.get("/students/{student_id}")
def get_student_details(student_id: str):
    if student_id not in student_records:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {student_id} not found",
        )

    return student_records[student_id]


# Submit marks for a student with input validation and custom error handling.
@app.post("/submit_marks")
def submit_student_marks(submission_data: MarksSubmissionRequest):
    # Validate that the student exists.
    if submission_data.student_id not in student_records:
        raise HTTPException(
            status_code=404,
            detail=f"Student with ID {submission_data.student_id} not found",
        )

    # Validate that marks are within the allowed range.
    if submission_data.marks < 0 or submission_data.marks > 100:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Marks should be between 0 and 100",
                "marks_received": submission_data.marks,
                "fix": "Provide a value between 0 and 100",
            },
        )

    # Validate that the subject name is not empty.
    if submission_data.subject.strip() == "":
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Subject name cannot be empty",
                "fix": "Provide a valid subject name",
            },
        )

    try:
        student_records[submission_data.student_id]["marks"] = submission_data.marks
        return {
            "message": "Marks submitted successfully",
            "student": student_records[submission_data.student_id]["name"],
            "subject": submission_data.subject,
            "grade": student_records[submission_data.student_id]["grade"],
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Something went wrong on server: {str(e)}"
        )
