from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from channels.db import database_sync_to_async
from users.models import User
import logging

logger = logging.getLogger(__name__)

class JWTAuthMiddleware:

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token = self.get_token_from_scope(scope)
        logger.debug(f"Extracted token: {token}")
        scope["user"] = await self.get_user(token)
        return await self.inner(scope, receive, send)

    def get_token_from_scope(self, scope):

        query_string = scope.get("query_string", b"").decode("utf-8")
        for param in query_string.split("&"):
            if param.startswith("token="):
                return param.split("=")[1]


        headers = dict(scope.get("headers", []))
        auth_header = headers.get(b'authorization')

        if auth_header:
            try:
                prefix, token = auth_header.decode().split()
                if prefix.lower() == "bearer":
                    return token
            except Exception as e:
                logger.warning(f"Invalid authorization header format: {e}")

        return None

    @database_sync_to_async
    def get_user(self, token):
        if not token:
            logger.warning("No token provided")
            return AnonymousUser()
        try:
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            user = User.objects.get(id=user_id)
            logger.debug(f"Authenticated user: {user.email} (ID: {user.id})")
            return user
        except Exception as e:
            logger.warning(f"Token authentication failed: {e}")
            return AnonymousUser()
