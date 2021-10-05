from django.core.management import BaseCommand
from ST0001.models import Patient
from datetime import datetime
import numpy as np
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        df = pd.read_excel("./ST0001/Supplementary/ST0001 (Rework).xlsx")
        df = df.replace(np.nan, None, regex=True)
        df = df.dropna()

        for row, index in df.iterrows():
            print(index["номер а/к"])
            
            Patient.objects.create(
                id_ambulatory=index["номер а/к"],
                last_name=index["last_name"],
                middle_name=index["middle_name"],
                first_name=index["first_name"],
                department=index["Учр. здравоохр."]
                )