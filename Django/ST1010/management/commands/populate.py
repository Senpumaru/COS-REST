from django.core.management import BaseCommand
from faker import Faker
from ST1010.models import Case
from datetime import datetime
import numpy as np
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        df = pd.read_excel("/media/zen/Data Science/IHC/Projects/ACS/Database ALK.xlsx")
        df = df.replace(np.nan, None, regex=True)
        
        for row, index in df.iterrows():
            print(index["Date of registration"].to_pydatetime())
            
            Case.objects.create(
                personal_number = index["ID"],
                date_of_registration = index["Date of registration"].to_pydatetime(),
                region=index["Region"],
                block_number=str(index["Block number"]).split(", "),
                block_amount=index["Block Amount"],
                slide_number=str(index["Slide number"]).split(", "),
                slide_amount=index["Slide Amount"],
                # date_of_response=index["Date of Response"],
                # date_of_delivery=index["Date of Delivery"],
            )
