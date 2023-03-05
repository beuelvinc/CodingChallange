from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken


@database_sync_to_async
def get_user(token_key):
    """
    Async function that gets a user object from a JWT access token.

    Args:
        token_key (str): The access token.

    Returns:
        A User object if the token is valid and belongs to a user, otherwise None.
    """
    try:
        access_token_obj = AccessToken(token_key)
        user_id = access_token_obj['user_id']
        if not user_id:
            return None
        else:
            return user_id

    except Exception:
        return None


class TokenAuthMiddleware:
    """
    Middleware class that authenticates users based on a JWT access token.

    If a valid access token is provided in the Authorization header, the user object associated with the token is added to the scope as `scope['user']`.
    If an invalid or missing token is provided, an AnonymousUser object is added to the scope as `scope['user']`.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        headers = dict(scope['headers'])

        if b'authorization' in headers:
            token_key = headers[b'authorization'].decode().split(' ')[-1]
            user = await get_user(token_key)
            scope['user'] = user if user else None
        else:
            scope['user'] = None

        return await self.inner(scope, receive, send)
