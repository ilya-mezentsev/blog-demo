from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import (
    IPermissionService,
    IReader,
    ByUserId,
    MemoryCache,
)
from blog_demo_backend.domains.user import (
    UserService,
    UserSessionService,
    UserRepository,
    UserSessionRepository,
)


__all__ = [
    'UserDomain',
]


class UserDomain:

    user_role_cache = MemoryCache()

    def __init__(
            self,
            connection_fn: DBConnectionFn,
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        self.user_cache = MemoryCache()
        self.session_cache = MemoryCache()

        user_repository = UserRepository(
            connection_fn=connection_fn,
            cache=self.user_cache,
        )
        session_repository = UserSessionRepository(
            connection_fn=connection_fn,
            cache=self.session_cache,
        )

        self.user_service = UserService(
            user_repository=user_repository,
            session_repository=session_repository,
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self.session_service = UserSessionService(
            session_repository=session_repository,
            user_repository=user_repository,
        )
