def Report(
        buffer,
        date_of_registration,
        personal_number,
        block_number,
        full_name,
        date_of_birth,
        institution,
        diagnosis,
        doctor_sender,
        date_of_response,
        doctor_reporter,
        cancer_cell_percentage,
        immune_cell_percentage,
        clin_interpretation):

    from datetime import date, datetime
    from pathlib import Path
    import os

    from textwrap import wrap

    from reportlab.pdfgen import canvas
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import Table, TableStyle

    BASE_DIR = Path(__file__).resolve().parent.parent

    #####################
    # Load Fonts
    pdfmetrics.registerFont(
        TTFont("Verdana", os.path.join(BASE_DIR, "PDF/verdana.ttf"))
    )

    pdfmetrics.registerFont(
        TTFont("Verdana-Bold", os.path.join(BASE_DIR, "PDF/Verdana Bold.ttf"))
    )

    #####################
    # Help
    def drawMyRuler(pdf):
        pdf.drawString(100, 810, "x100")
        pdf.drawString(200, 810, "x200")
        pdf.drawString(300, 810, "x300")
        pdf.drawString(400, 810, "x400")
        pdf.drawString(500, 810, "x500")

        pdf.drawString(10, 100, "y100")
        pdf.drawString(10, 200, "y200")
        pdf.drawString(10, 300, "y300")
        pdf.drawString(10, 400, "y400")
        pdf.drawString(10, 500, "y500")
        pdf.drawString(10, 600, "y600")
        pdf.drawString(10, 700, "y700")
        pdf.drawString(10, 800, "y800")

    LEFT_LINE = 35
    RIGHT_LINE = 500

    ###################
    # Content
    ICON = os.path.join(BASE_DIR, "PDF/ICON 3.png")
    DOCUMENT_TITLE = "PDL1 Report"
    HEADER = [
        "Министерство здравоохранения Республики Беларусь",
        "РНПЦ онкологии и медицинской радиологии им. Н.Н.Александрова",
        "Республиканская молекулярно-генетическая лаборатория канцерогенеза",
    ]
    TITLE = "Определение PD-L1-статуса образца опухолевой ткани иммуногистохимическим методом"
    SUMMARY = [
        ["Ф.И.О. пациента:", full_name],
        ["Личный номер:", personal_number],
        ["Дата рождения:", date_of_birth],
        ["Дата получения материала:", date_of_registration],
        ["Диагноз (направительный):", diagnosis],
        ["№ гистологического исследования:", ",".join(block_number)],
        ["Направившая организация:", institution],
        ["Врач, направивший на исследование:", doctor_sender],
    ]
    print(SUMMARY)

    RESEARCH = [
        "Иммуногистохимическое исследование с моноклональным антителом к PD-L1 (клон SP142)",
        """Иммуногистохимическое окрашивание с антителом к PD-L1 (SP142) выполнено с использованием
        набора реагентов производства Ventana Medical Systems (США), включающим в себя систему детекции
        OptiView DAB IHC Detection Kit и комплект реагентов для усиления сигнала OptiView Amplification Kit.
        Исследование выполнено на автоматической станции окраски срезов 
        Benchmark GX (Ventana Medical Systems, США)."""
    ]

    STAINING = [
        "Критерии отнесения опухоли к категории PD-L1-позитивных",
        [["НМРЛ*: опухолевые клетки ≥50% или иммунные клетки ≥10%",
          "\n".join(wrap("VENTANA PD-L1 (SP142) Assay Interpretation Guide for Non-Small Cell Lung" +
                         " Cancer ≥ 50% TC or ≥ 10% IC Stepwise Scoring Algorithm", 60))],

         ["Уротелиальная карцинома**: иммунные клетки ≥5%",
          "\n".join(wrap("VENTANA PD-L1 (SP142) Assay Interpretation" +
                         " Guide for Urothelial Carcinoma", 60))],
         ["ТНРМЖ***: иммунные клетки ≥1%",
          "\n".join(wrap("VENTANA PD-L1 (SP142) Assay Interpretation Guide" +
                         " for Triple-Negative Breast Carcinoma (TNBC)", 60))]]
    ]

    if cancer_cell_percentage < 1:
        cancer_cell_percentage = "<1"
    else:
        pass
    EXPRESSION = [
        "Показатели экспресии",
        "Показатель экспрессии PD-L1 опухолевыми клетками (ОК) составляет " + str(cancer_cell_percentage) + "%",
        "Показатель экспрессии PD-L1 иммунными клетками (ИК) составляет " + str(immune_cell_percentage) + "%"

    ]
    INTERPRETATION = ["Клиническая интерпретация:", clin_interpretation]

    FOOTER = [
        [
            "Заведующий онкологическим",
            "отделением (иммуноморфологии и",
            "протеомики), к.м.н.",
        ],
        doctor_reporter,
    ]

    ###################
    # Canvas
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Verdana", 10)
    pdf.setTitle(DOCUMENT_TITLE)

    # Icon
    pdf.drawInlineImage(ICON, 30, 770)

    # Header
    text = pdf.beginText(120, 800)
    text.setFont("Verdana", 10)
    for line in HEADER:
        text.textLine(line)
    pdf.drawText(text)

    # Separation Line
    pdf.line(15, 765, 580, 765)

    # Title
    text = pdf.beginText(LEFT_LINE, 750)
    text.setFont("Verdana-Bold", 10)
    text.textLine(TITLE)
    pdf.drawText(text)

    # Summary
    table = Table(data=SUMMARY)
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Verdana", 8),
                ("FONT", (0, 0), (0, -1), "Verdana-Bold", 10),
                ("LINEBEFORE", (1, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    
    table.wrapOn(pdf, 100, 300)
    table.drawOn(pdf, LEFT_LINE, 600)

    # Separation Line
    pdf.line(15, 590, 580, 590)

    # Research Characteristic
    text = pdf.beginText(LEFT_LINE, 570)
    text.setFont("Verdana-Bold", 10)
    text.textLines(RESEARCH[0])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 555)
    text.setFont("Verdana", 10)
    text.textLines(RESEARCH[1], )
    pdf.drawText(text)

    # Staining
    text = pdf.beginText(LEFT_LINE, 490)
    text.setFont("Verdana-Bold", 10)
    text.textLines(STAINING[0], )
    pdf.drawText(text)

    table = Table(data=STAINING[1], colWidths=[275,275], rowHeights=len(STAINING[1] * 12))
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (-1, -1), "Verdana", 8),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                # ("RIGHTPADDING", (1, 1), (1, -1), 80),
                # ("SPAN", (1, 0), (0, 0)),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table.wrapOn(pdf, 100, 300)
    table.drawOn(pdf, LEFT_LINE, 375)

    # Expression
    text = pdf.beginText(LEFT_LINE, 360)
    text.setFont("Verdana-Bold", 10)
    text.textLine(EXPRESSION[0])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 350)
    text.setFont("Verdana", 10)
    text.textLine(EXPRESSION[1])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 340)
    text.setFont("Verdana", 10)
    text.textLine(EXPRESSION[2])
    pdf.drawText(text)


    # Interpretation
    text = pdf.beginText(LEFT_LINE, 320)
    text.setFont("Verdana-Bold", 10)
    text.textLine(INTERPRETATION[0])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 310)
    text.setFont("Verdana", 10)
    text.textLine(INTERPRETATION[1])
    pdf.drawText(text)

    # Footer
    FOOTER_HEIGHT = 140
    text = pdf.beginText(LEFT_LINE, FOOTER_HEIGHT)
    text.setFont("Verdana", 10)
    text.textLine(str(date_of_response))
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, FOOTER_HEIGHT - 15)
    text.setFont("Verdana", 10)
    for line in FOOTER[0]:
        text.textLine(line)
    pdf.drawText(text)

    text = pdf.beginText(RIGHT_LINE, FOOTER_HEIGHT - 15)
    text.setFont("Verdana", 10)
    text.textLine(FOOTER[1])
    pdf.drawText(text)
    pdf.showPage()
    pdf.save()