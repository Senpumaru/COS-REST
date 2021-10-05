from celery import shared_task
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
import numpy as np
from time import sleep
import io
from ST1010.PDF import Reporter
from rest_framework.response import Response


@shared_task
def celery_send_report(email_editor, email_recipient, case_data, consultant_data):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    Reporter.Report(
        buffer=buffer,
        # Registration Data
        date_of_dispatch=str(case_data["date_of_dispatch"]),
        case_code=case_data["case_code"],
        block_codes=case_data["block_codes"],
        diagnosis=case_data["diagnosis"],
        case_sender=case_data["case_sender"],
        # Report Data
        date_of_report=str(case_data["date_of_report"]),
        case_editor_first_name=case_data["case_editor"]["first_name"],
        case_editor_middle_name=case_data["case_editor"]["middle_name"],
        case_editor_last_name=case_data["case_editor"]["last_name"],
        case_editor_title=case_data["case_editor"]["title"],
        case_editor_signature=case_data["case_editor"]["signature"],
        head_consultant_first_name=consultant_data["first_name"],
        head_consultant_middle_name=consultant_data["middle_name"],
        head_consultant_last_name=consultant_data["last_name"],
        head_consultant_title=consultant_data["title"],
        head_consultant_signature=consultant_data["signature"],
        microscopic_description=case_data["microscopic_description"],
        histological_description=case_data["histological_description"],
        staining_pattern=case_data["staining_pattern"],
        clinical_interpretation=case_data["clinical_interpretation"],
    )
    buffer.seek(0)
    pdf = buffer.getvalue()

    ## Email sending (Celery) ##
    email_message = EmailMessage(
        "Report",
        f"Report sent with Celery by {email_editor}",
        "cos@omr.by",
        [email_recipient],
    )
    email_message.attach(
        # PDF Name
        case_data["case_code"],
        content=pdf,
        mimetype="application/pdf",
    )
    sleep(5)
    email_message.send()

    return None
