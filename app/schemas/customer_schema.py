"""
Issue #10 -- FastAPI Scaffold -- app/schemas/customer_schema.py

STATUS: repaired by Theresia. CustomerPredictionRequest below is
untouched -- it was correct, including the SeniorCitizen: int typing,
which correctly matches the real dataset's 0/1 encoding.

One thing changed in CustomerPredictionResponse: `risk_level` was
removed.

Why: the issue and spec both require this response to contain EXACTLY
`churn_probability: float` and `churn_prediction: bool` -- because
Latifah's predict() (Issue #11) is contracted to return exactly that
shape, and Issue #14 is only supposed to swap the mock for the real
model without the response schema changing. Tested directly: with
risk_level present as a required field, validating Latifah's exact
contracted output shape against this schema fails with
"risk_level: Field required." That's a guaranteed break the day #14
happens, not a hypothetical one.

risk_level is a genuinely reasonable idea for the dashboard -- it just
can't live on this locked contract without being discussed first (it'd
need to be Optional with a default, and computed somewhere that isn't
this schema -- e.g. in routes.py, from churn_probability). Raise it
with the team if you want it back in; don't silently re-add it here.
"""

from pydantic import BaseModel, Field


class CustomerPredictionRequest(BaseModel):
    """
    Pydantic schema representing input parameters of the IBM Telco Churn Dataset.
    Enforces types and validation properties, ensuring incoming API requests match.
    """
    gender: str = Field(..., description="Gender of the customer (Male, Female)", example="Female")
    SeniorCitizen: int = Field(..., description="Whether the customer is a senior citizen (1, 0)", example=0, ge=0, le=1)
    Partner: str = Field(..., description="Whether the customer has a partner (Yes, No)", example="Yes")
    Dependents: str = Field(..., description="Whether the customer has dependents (Yes, No)", example="No")
    tenure: int = Field(..., description="Number of months the customer has stayed with the company", example=12, ge=0)
    PhoneService: str = Field(..., description="Whether the customer has phone service (Yes, No)", example="Yes")
    MultipleLines: str = Field(..., description="Whether customer has multiple lines (Yes, No, No phone service)", example="No")
    InternetService: str = Field(..., description="Customer's internet service provider (DSL, Fiber optic, No)", example="Fiber optic")
    OnlineSecurity: str = Field(..., description="Whether online security is enabled (Yes, No, No internet)", example="No")
    OnlineBackup: str = Field(..., description="Whether online backup is enabled (Yes, No, No internet)", example="Yes")
    DeviceProtection: str = Field(..., description="Whether device protection is enabled (Yes, No, No internet)", example="No")
    TechSupport: str = Field(..., description="Whether technical support is enabled (Yes, No, No internet)", example="No")
    StreamingTV: str = Field(..., description="Whether streaming TV is enabled (Yes, No, No internet)", example="Yes")
    StreamingMovies: str = Field(..., description="Whether streaming movies is enabled (Yes, No, No internet)", example="No")
    Contract: str = Field(..., description="The contract term of the customer (Month-to-month, One year, Two year)", example="Month-to-month")
    PaperlessBilling: str = Field(..., description="Whether the customer has paperless billing (Yes, No)", example="Yes")
    PaymentMethod: str = Field(..., description="The customer's payment method", example="Electronic check")
    MonthlyCharges: float = Field(..., description="The amount charged to the customer monthly", example=70.05, ge=0.0)
    TotalCharges: float = Field(..., description="The total amount charged to the customer", example=840.60, ge=0.0)


class CustomerPredictionResponse(BaseModel):
    """
    Pydantic schema returning prediction risk scoring output.
    Shape is locked: churn_probability and churn_prediction only,
    matching Latifah's predict() contract (Issue #11) exactly, so
    Issue #14 can swap the mock for the real model without this
    schema needing to change.
    """
    churn_probability: float = Field(..., description="Predicted churn probability value (between 0.0 and 1.0)", example=0.65, ge=0.0, le=1.0)
    churn_prediction: bool = Field(..., description="Binary determination of churn threshold", example=True)