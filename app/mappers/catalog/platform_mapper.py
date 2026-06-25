from app.dto.catalog import PlatformResponse
from app.models.catalog.platform import Platform


def platform_to_platform_response(platform: Platform) -> PlatformResponse:
    return PlatformResponse(
        id=platform.id,
        code=platform.code,
        name=platform.name,
        is_active=platform.is_active,
    )

def platforms_to_platform_response(platforms: list[Platform]) -> list[PlatformResponse]:
    return [platform_to_platform_response(platform) for platform in platforms]
