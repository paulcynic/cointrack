import httpx
from app.core.config import settings


# To check bot_chatId click the url:
# https://api.telegram.org/bot{bot_token}/getUpdates

def send_message(bot_message: str) -> dict:
    bot_token = settings.TELEGRAM_BOT_TOKEN
    bot_chatId = settings.BOT_CHAT_ID
    params = {'chat_id': bot_chatId, 'parse_mode': 'MarkdownV2', 'text': bot_message}
    headers = {"User-agent": "cointrack bot 0.1"}

    response = httpx.get(f'https://api.telegram.org/bot{bot_token}/sendMessage', params=params, headers=headers)
    return response.json()


