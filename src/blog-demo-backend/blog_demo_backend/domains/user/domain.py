from blog_demo_backend.shared import DBConnectionFn
from blog_demo_backend.domains.shared import (
    IPermissionService,
    CacheFactoryFn,
    UserRoleRepository,
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

    class EntityTypes:
        USER = 'user'
        SESSION = 'session'
        USER_ROLE = 'user-role'

    def __init__(
            self,
            cache_factory_fn: CacheFactoryFn,
            connection_fn: DBConnectionFn,
            permission_service: IPermissionService,
    ) -> None:

        self.user_cache = cache_factory_fn(self.EntityTypes.USER)
        self.session_cache = cache_factory_fn(self.EntityTypes.SESSION)
        self.user_role_cache = cache_factory_fn(self.EntityTypes.USER_ROLE)

        user_repository = UserRepository(
            connection_fn=connection_fn,
            cache=self.user_cache,
        )
        session_repository = UserSessionRepository(
            connection_fn=connection_fn,
            cache=self.session_cache,
        )

        self.user_role_repository = UserRoleRepository(
            connection_fn=connection_fn,
            cache=self.user_role_cache,
        )

        self.user_service = UserService(
            user_repository=user_repository,
            session_repository=session_repository,
            permission_service=permission_service,
            user_role_repository=self.user_role_repository,
        )

        self.session_service = UserSessionService(
            session_repository=session_repository,
            user_repository=user_repository,
        )

    async def on_cache_changed(self, entity_type: str) -> None:
        if entity_type == self.EntityTypes.USER:
            await self.user_cache.reset_cache()

        elif entity_type == self.EntityTypes.SESSION:
            await self.session_cache.reset_cache()

        elif entity_type == self.EntityTypes.USER_ROLE:
            await self.user_role_cache.reset_cache()
