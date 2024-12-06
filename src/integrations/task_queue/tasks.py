from src.integrations.task_queue.celery_task_queue import CeleryTaskQueue
from src.integrations.email.email import EmailUtils

app = CeleryTaskQueue().celery_app

@app.task(name="send_email")
def send_email(email: str, code: str):
    email_utils = EmailUtils()
    try:
        success = email_utils.send_code_to_email(send_to=email, random_password=code)
        print(f"Sending message {code} to {email}")
    except Exception as e:
        raise e
    return success
