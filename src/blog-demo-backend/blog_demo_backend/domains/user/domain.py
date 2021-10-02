from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import (
    IPermissionService,
    IReader,
    ByUserId,
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

    def __init__(
            self,
            connection_fn: DBConnectionFn,
            permission_service: IPermissionService,
            user_role_repository: IReader[str, ByUserId],
    ) -> None:

        user_repository = UserRepository(
            connection_fn=connection_fn,
        )
        session_repository = UserSessionRepository(
            connection_fn=connection_fn,
        )

        self.user_service = UserService(
            user_repository=user_repository,
            permission_service=permission_service,
            user_role_repository=user_role_repository,
        )

        self.session_service = UserSessionService(
            user_repository=user_repository,
            session_repository=session_repository,
        )
