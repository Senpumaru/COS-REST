from django.core.management import BaseCommand
from ST1011.models import Case
from datetime import datetime
import numpy as np
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        df = pd.read_excel("./ST1011/Supplementary/ST1011 (Rework).xlsx")
        df = df[df["Result"] != "In-work"]
        df = df.replace(np.nan, None, regex=True)

        for row, index in df.iterrows():
            if isinstance(index["Block codes"], str):
                block_codes = [str(index["Block codes"])]
            else:
                block_codes = str(index["Block codes"]).split(",")

            if isinstance(index["Slide codes"], str):
                slide_codes = [str(index["Slide codes"])]
            else:
                slide_codes = str(index["Slide codes"]).split(",")

            Case.objects.create(
                institution=index["Orginization"],
                personal_number=index["ID"],
                diagnosis=index["Diagnosis"],
                last_name=index["Last name"],
                first_name=index["First name"],
                middle_name=index["Middle name"],
                decline_reason=index["Decline (Reason)"],
                date_of_acquisition=index["Date of acquisition"],
                date_of_report=index["Date of report"],
                immune_cell_percentage=index["PD-L1 (IC) Expression %"],
                cancer_cell_percentage=index["PD-L1 (CC) Expression %"],
                # Block Codes
                block_codes=block_codes,
                block_count=index["Block count"],
                # Slide Codes
                slide_codes=slide_codes,
                slide_count=index["Slide count"],
                clinical_interpretation=index["Result"],
                version_state=index["Version"])
