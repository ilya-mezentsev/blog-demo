from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import IPermissionService
from blog_demo_backend.domains.user import (
    UserService,
    UserRepository,
)


__all__ = [
    'UserDomain',
]


class UserDomain:

    def __init__(
            self,
            connection_fn: DBConnectionFn,
            permission_service: IPermissionService,
    ) -> None:

        self.user_service = UserService(
            repository=UserRepository(
                connection_fn=connection_fn,
            ),
            permission_service=permission_service,
        )
