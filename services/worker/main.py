"""Worker service for scheduling and dispatching reminders.

This worker runs a periodic job that checks for pending reminders and
sends them via SMS (Twilio) or logs them to the console in
development.  The worker uses APScheduler to schedule the check task
every minute.  Reminder delivery status is updated in the database
upon success.
"""

import os
from datetime import datetime, timezone
import logging
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from twilio.rest import Client

from ..api.database import SessionLocal
from ..api.repositories.reminder import ReminderRepository
from ..api.settings import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


settings = get_settings()

def send_sms(to: str, body: str) -> None:
    if not (settings.twilio_account_sid and settings.twilio_auth_token and settings.twilio_from_number):
        # No Twilio configured; log to console instead
        logger.info(f"SMS to {to}: {body}")
        return
    client = Client(settings.twilio_account_sid, settings.twilio_auth_token)
    message = client.messages.create(body=body, from_=settings.twilio_from_number, to=to)
    logger.info(f"Sent SMS to {to}: {message.sid}")


def process_reminders():
    now = datetime.now(timezone.utc)
    db = SessionLocal()
    repo = ReminderRepository(db)
    pending = repo.list_pending(now)
    for rem in pending:
        payload = rem.payload_json or {}
        message = payload.get("message", "Reminder")
        if rem.channel == "sms":
            send_sms(rem.target, message)
        else:
            logger.info(f"Email to {rem.target}: {message}")
        repo.mark_sent(rem)
    db.close()


def main():
    scheduler = BlockingScheduler(timezone=timezone.utc)
    scheduler.add_job(process_reminders, 'interval', minutes=1, next_run_time=datetime.now(timezone.utc))
    try:
        logger.info("Reminder worker started")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()


if __name__ == "__main__":
    main()