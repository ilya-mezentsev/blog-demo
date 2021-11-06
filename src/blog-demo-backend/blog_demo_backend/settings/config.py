import json
from typing import Mapping, Any

from blog_demo_backend.db import DBSettings
from blog_demo_backend.domains import (
    PermissionSettings,
    LoadLevel,
)
from blog_demo_backend.entrypoints import WebEntrypointSettings, BasicAuthSettings


class Config:

    _REQUIRED_KEYS = {
        'db',
        'server',
        'permission_service',
    }

    def __init__(self, config_path: str) -> None:
        self._config_dict = self._load_config(config_path)

        missed_keys = self._REQUIRED_KEYS.difference(self._config_dict.keys())
        assert not missed_keys, f'Some of required configs missed: {missed_keys}'

    @staticmethod
    def _load_config(config_path: str) -> Mapping[str, Any]:
        with open(config_path, 'r') as f:
            return json.loads(f.read())

    def db_settings(self) -> DBSettings:
        return DBSettings(
            dialect=self._config_dict['db']['dialect'],
            driver=self._config_dict['db']['driver'],
            user=self._config_dict['db']['user'],
            password=self._config_dict['db']['password'],
            db_name=self._config_dict['db']['db_name'],
            schema_name=self._config_dict['db']['schema_name'],
            host=self._config_dict['db']['host'],
            port=self._config_dict['db']['port'],
            pool_timeout=self._config_dict['db']['pool_timeout'],
            echo=self._config_dict['db']['echo'],
        )

    def permission_settings(self) -> PermissionSettings:
        return PermissionSettings(
            permission_resolver_url=self._config_dict['permission_service']['permission_resolver_url'],
            request_timeout=self._config_dict['permission_service']['request_timeout'],
            load_levels=[
                LoadLevel(
                    version_id=item['version_id'],
                    max_latency=item['max_latency'],
                )
                for item in self._config_dict['permission_service']['load_levels']
            ],
            critical_version_id=self._config_dict['permission_service']['critical_version_id'],
        )

    def web_entrypoint_settings(self) -> WebEntrypointSettings:
        return WebEntrypointSettings(
            host=self._config_dict['server']['host'],
            port=self._config_dict['server']['port'],
            basic_auth=BasicAuthSettings(
                username=self._config_dict['server']['basic_auth']['username'],
                password=self._config_dict['server']['basic_auth']['password'],
            ),
        )
