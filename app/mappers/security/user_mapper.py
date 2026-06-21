from app.dto.security import UserResponse
from app.models.security.user import User


def user_to_user_response(
    user: User,
    role_code: str,
    status_code: str,
) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role_code=role_code,
        status_code=status_code,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def users_to_user_response(
    users: list[tuple[User, str, str]],
) -> list[UserResponse]:
    return [
        user_to_user_response(user, role_code, status_code)
        for user, role_code, status_code in users
    ]
