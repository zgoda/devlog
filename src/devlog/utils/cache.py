from flask import current_app

from typing import Optional

from flask_caching import Cache


class DevlogCache(Cache):

    def delete_prefixed(self, prefix: str) -> Optional[int]:
        """Delete cache keys with prefix. This works only for Redis cache
        and is no-op for any other cache type.

        :param prefix: key prefix
        :type prefix: str
        :return: number of keys deleted or None
        :rtype: Optional[int]
        """
        if 'redis' in current_app.config.get('CACHE_TYPE', 'simple').lower():
            redis = self.cache._write_client
            app_prefix = current_app.config.get("CACHE_KEY_PREFIX", "")
            key_prefix = f'{app_prefix}{prefix}*'
            deleted = 0
            for key in redis.scan_iter(match=key_prefix):
                deleted = deleted + redis.delete(key)
            return deleted
