from fastapi import APIRouter, Depends
from backend.core.dependencies import role_required

router = APIRouter(prefix="/test", tags=["Role Test"])


@router.get("/admin")
def admin_only(user=Depends(role_required(["admin"]))):
    return {"message": f"Welcome Admin {user['email']}"}


@router.get("/security")
def security_only(user=Depends(role_required(["admin", "security"]))):
    return {"message": f"Welcome Security {user['email']}"}


@router.get("/user")
def user_only(user=Depends(role_required(["admin", "security", "user"]))):
    return {"message": f"Welcome User {user['email']}"}
