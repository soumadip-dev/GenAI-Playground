from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class VoterDetails(BaseModel):
    name: str
    email: str
    phone: str
    age: int
    voter_id: int


@app.post("/voter")
def check_voter_eligibility(voter: VoterDetails):
    # Optional: check for empty strings
    if not all([voter.name, voter.email, voter.phone]):
        return {"message": "Name, email, and phone are required."}

    if voter.age < 18:
        return {
            "message": f"{voter.name} is not eligible to vote.",
            "voter_details": voter,
        }

    return {"message": "Voter is eligible to vote.", "voter_details": voter}
