from app.dto.auth import AuthenticatedUserResponse, LoginResponse
from app.models.security.user import User


def user_to_authenticated_user_response(
    user: User,
    role_code: str,
    permission_codes: list[str],
) -> AuthenticatedUserResponse:
    # Convierte el usuario autenticado al DTO publico de sesion.
    return AuthenticatedUserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=role_code,
        permissions=permission_codes,
    )


def user_to_login_response(
    user: User,
    role_code: str,
    permission_codes: list[str],
) -> LoginResponse:
    return LoginResponse(
        user=user_to_authenticated_user_response(
            user=user,
            role_code=role_code,
            permission_codes=permission_codes,
        )
    )
