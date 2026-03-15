from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from telegram_integration.models import TelegramLinkToken


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def generate_link_token(request):
    request.user.telegram_tokens.filter(is_used=False).delete()
    token = TelegramLinkToken.issue_for_user(request.user)
    return Response(
        {
            "token": token.token,
            "instructions": f"/start {token.token}",
            "expires_at": token.expires_at,
        }
    )
