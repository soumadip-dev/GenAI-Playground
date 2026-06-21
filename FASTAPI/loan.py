from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class LoanRequest(BaseModel):
    age: int
    annual_income: float
    requested_loan_amount: float
    years_of_employment: int


@app.post("/predict")
def predict_loan_approval(loan_request: LoanRequest):
    if loan_request.annual_income > 50_000 and loan_request.years_of_employment > 2:
        loan_status = "Approved"
        response_message = "Loan application approved."
    else:
        loan_status = "Rejected"
        response_message = "Loan application rejected."

    return {
        "message": response_message,
        "data": {
            "age": loan_request.age,
            "annual_income": loan_request.annual_income,
            "requested_loan_amount": loan_request.requested_loan_amount,
            "loan_status": loan_status,
        },
    }


@app.get("/customer/{customer_id}")
def get_customer_loan_status(customer_id: int):
    return {
        "customer_id": customer_id,
        "status": f"Customer record of {customer_id} fetched successfully.",
    }
