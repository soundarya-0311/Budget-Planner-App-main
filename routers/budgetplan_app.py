import traceback
from fastapi import APIRouter,HTTPException,status
from fastapi.responses import JSONResponse
from schemas.schemas import BudgetPlan,FinancialGoals
from prompts.llm_prompts import BUDGET_PLANNER_PROMPT, SAVINGS_STRATEGIST_PROMPT
from main import llm


router = APIRouter()

@router.post("/budget_planner")
def budget_planner(payload : BudgetPlan):
    """This API sets a rough plan for savings and expenses and record data in DB for future purposes."""
    try:
        if payload.existing_investments:
            investment_details = "\n".join([f"{inv.investment_types}: {inv.total_amount}" for inv in payload.investments])
        else:
            investment_details = "No existing investments"
            
        prompt = BUDGET_PLANNER_PROMPT.format(
            monthly_income = payload.monthly_income,
            eb_bill = payload.eb_bill,
            rent = payload.rent,
            groceries = payload.groceries,
            travel = payload.travel,
            internet = payload.internet,
            EMIs = payload.EMIs,
            existing_investments = payload.existing_investments,
            investment_details = investment_details
        )
        
        llm_response = llm.invoke([{"role":"system","content":prompt}])
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content = llm_response.content
        )

    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = "Something Went Wrong"
        )
        
@router.post("/set_financial_goal")
def set_financial_goals(goal : FinancialGoals):
    try:
        if goal.target_timeline_in_months < 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "timeline need to contain something greater than zero")
                
        """This API will be helpful to set very clear, specific idea and saving strategy according to the user need."""
        
        prompt = SAVINGS_STRATEGIST_PROMPT.format(
            goal = goal.goal,
            goal_amount = goal.goal_amount,
            target_timeline = goal.target_timeline_in_months,
            priority = goal.priority
        )
        
        response = llm.invoke([{"role":"system", "content": prompt}])
        savings_strategy = response.content
        
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = savings_strategy
        )
    
    except HTTPException as e:
        traceback.print_exc()
        return JSONResponse(
            status_code = e.status_code,
            content = e.detail
        )
        
    except Exception:
        traceback.print_exc()
        return JSONResponse(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = "Something Went Wrong"
        )