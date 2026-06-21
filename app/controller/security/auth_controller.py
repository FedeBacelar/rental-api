from fastapi import APIRouter, Depends, Response, Security, status
from sqlalchemy.orm import Session

from app.core.auth import refresh_token_cookie
from app.db.session import get_db
from app.dto.auth import LoginRequest, LoginResponse
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
) -> LoginResponse:
    service = AuthService(db)

    return service.login(request, response)


@router.post("/refresh", response_model=LoginResponse)
def refresh(
    response: Response,
    refresh_token: str | None = Security(refresh_token_cookie),
    db: Session = Depends(get_db),
) -> LoginResponse:
    service = AuthService(db)

    return service.refresh(refresh_token, response)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    response: Response,
    refresh_token: str | None = Security(refresh_token_cookie),
    db: Session = Depends(get_db),
) -> None:
    service = AuthService(db)

    service.logout(refresh_token, response)
