from pydantic import BaseModel
from typing import Optional,List

class Investments(BaseModel):
    investment_types : str
    total_amount : int
    

class BudgetPlan(BaseModel):
    monthly_income : int
    eb_bill : int
    rent :  int
    groceries : int
    travel : int
    internet : int 
    EMIs : int
    existing_investments : bool
    investments : Optional[List[Investments]] = None

class FinancialGoals(BaseModel):
    goal : str
    goal_amount : int
    target_timeline_in_months : int
    priority : str
    
class RegisterCredentials(BaseModel):
    username : str
    email : str
    password : str
    
# class LoginCredentials(BaseModel):
#     email : str
#     password : str

