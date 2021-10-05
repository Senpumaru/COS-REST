from celery import shared_task
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
import numpy as np
from time import sleep
import io
from ST1011.PDF import Reporter
from rest_framework.response import Response


@shared_task
def celery_send_report(email_editor, email_recipient, case_data, consultant_data):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    Reporter.Report(
        buffer=buffer,
        # Registration Data
        date_of_dispatch=str(case_data["date_of_dispatch"]),
        personal_number=case_data["personal_number"],
        block_codes=case_data["block_codes"],
        date_of_birth=case_data["date_of_birth"],
        full_name=case_data["full_name"],
        institution=case_data["institution"],
        diagnosis=case_data["diagnosis"],
        case_sender=case_data["case_sender"],
        # Report Data
        date_of_report=str(case_data["date_of_report"]),
        case_editor_first_name=case_data["case_editor"].first_name,
        case_editor_middle_name=case_data["case_editor"].middle_name,
        case_editor_last_name=case_data["case_editor"].last_name,
        case_editor_title=case_data["case_editor"].title,
        case_editor_signature=case_data["case_editor"].signature.url,
        head_consultant_first_name=consultant_data["first_name"],
        head_consultant_middle_name=consultant_data["middle_name"],
        head_consultant_last_name=consultant_data["last_name"],
        head_consultant_title=consultant_data["title"],
        head_consultant_signature=consultant_data["signature"].url,
        decline_reason=case_data["decline_reason"],
        cancer_cell_percentage=case_data["cancer_cell_percentage"],
        immune_cell_percentage=case_data["immune_cell_percentage"],
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
        case_data["personal_number"],
        content=pdf,
        mimetype="application/pdf",
    )
    sleep(5)
    email_message.send()

    return None
