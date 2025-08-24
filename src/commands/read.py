from parser import command
from functions import get_messages_from_channel
from logger import logger
import dateutil
import context
import tzlocal


@command(name="read", description="")
def read():
    if not context.channel_id:
        logger.error("select a channel first.")
    messages = get_messages_from_channel(context.token, context.channel_id)
    user_timezone = tzlocal.get_localzone()  # Dynamically fetch system timezone
    for message in reversed(messages):
        timestamp_str = message["timestamp"]
        timestamp = dateutil.parser.isoparse(timestamp_str)
        timestamp_user_timezone = timestamp.astimezone(user_timezone)
        readable_timestamp = timestamp_user_timezone.strftime("%d/%m/%Y %H:%M:%S")
        print(
            f"[{readable_timestamp}] {message['author']['username']}: {message['content']}"
        )
