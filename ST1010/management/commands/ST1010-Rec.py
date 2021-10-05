from django.core.management import BaseCommand
from ST1010.models import Case
from datetime import datetime
import numpy as np
import pandas as pd


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        df = pd.read_excel("./ST1010/Supplementary/ST1010 (Rework).xlsx")
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
                institution_code=int(index["Institution"]),
                order_number=int(index["Order number"]),
                date_of_acquisition=index["Date of acquisition"],
                # Block Codes
                block_codes=block_codes,
                block_count=index["Block count"],
                # Slide Codes
                slide_codes=slide_codes,
                slide_count=index["Slide count"],
                clinical_interpretation=index["Result"],
                version=1.0,
                version_state="Verified")
