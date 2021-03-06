def Report(
    buffer,
    case_code,
    date_of_dispatch,
    diagnosis,
    block_codes,
    case_sender,
    # Case Data
    date_of_report,
    case_editor_first_name,
    case_editor_last_name,
    case_editor_middle_name,
    case_editor_title,
    case_editor_signature,
    head_consultant_first_name,
    head_consultant_last_name,
    head_consultant_middle_name,
    head_consultant_title,
    head_consultant_signature,
    microscopic_description,
    histological_description,
    staining_pattern,
    clinical_interpretation,
):

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
    pdfmetrics.registerFont(TTFont("Verdana", os.path.join(BASE_DIR, "PDF/verdana.ttf")))

    pdfmetrics.registerFont(TTFont("Verdana-Bold", os.path.join(BASE_DIR, "PDF/Verdana Bold.ttf")))

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

    DOCUMENT_TITLE = "ALK Report"
    HEADER = [
        "Министерство здравоохранения Республики Беларусь",
        "РНПЦ онкологии и медицинской радиологии им. Н.Н.Александрова",
        "Республиканская молекулярно-генетическая лаборатория канцерогенеза",
    ]
    TITLE = "Определение ALK-статуса образца опухолевой ткани иммуногистохимическим методом"
    SUMMARY = [
        ["Номер протокола:", "BO 40336"],
        ["Идентификатор:", case_code],
        ["Дата получения материала:", date_of_dispatch],
        ["Диагноз (направительный):", diagnosis],
        ["№ гистологического исследования:", " ".join(block_codes)],
        ["Врач, направивший на исследование:", case_sender],
    ]

    MICRO_CHAR = ["Микроскопическое описание:", "\n".join(wrap(microscopic_description, 98))]

    CONCLUSION = ["Заключение:", "\n".join(wrap(histological_description, 95))]
    RESEARCH = [
        "Иммуногистохимическое исследование с моноклональным антителом к ALK (клон D5F3):",
        [
            "Иммуногистохимическое окрашивание с антителом к ALK (D5F3) выполнено с использованием комплекта реагентов",
            "производства Ventana Medical Systems (США), включающим в себя систему детекции OptiView DAB IHC Detection Kit и",
            "комплект реагентов для усиления сигнала OptiView Amplification Kit.",
            "Исследование выполнено на автоматической станции окраски срезов Benchmark GX (Ventana Medical Systems, США).",
        ],
    ]
    STAINING = [
        ["Характеристика окрашивания", ""],
        [
            "Позитивный и негативный контрольные образцы",
            "Паттерн окрашивания приемлем для дальнейшей\nоценки исследуемого образца.",
        ],
        ["Исследуемый образец", "\n".join(wrap(staining_pattern, 50))],
    ]

    if clinical_interpretation == "ALK-Positive":
        clinical_interpretation = "Исследуемый образец опухолевой ткани является ALK-позитивным"
    elif clinical_interpretation == "ALK-Negative":
        clinical_interpretation = "Исследуемый образец опухолевой ткани является ALK-негативным"

    INTERPRETATION = ["Клиническая интерпретация:", clinical_interpretation]

    FOOTER = [
        "\n".join(wrap(case_editor_title, 30)),
        case_editor_last_name + " " + case_editor_first_name[0] + "." + case_editor_middle_name[0] + ".",
        "\n".join(wrap(head_consultant_title, 30)),
        head_consultant_last_name + " " + head_consultant_first_name[0] + "." + head_consultant_middle_name[0] + ".",
    ]
    SIGNATURE = case_editor_signature
    HEAD_SIGNATURE = head_consultant_signature

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
                ("FONT", (0, 0), (-1, -1), "Verdana"),
                ("FONT", (0, 0), (0, -1), "Verdana-Bold"),
                ("LINEBEFORE", (1, 0), (-1, -1), 0.25, colors.black),
            ]
        )
    )
    table.wrapOn(pdf, 100, 300)
    table.drawOn(pdf, LEFT_LINE, 630)

    # Microscopic Characteristic
    text = pdf.beginText(LEFT_LINE, 615)
    text.setFont("Verdana-Bold", 10)
    text.textLine(MICRO_CHAR[0])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 600)
    text.setFont("Verdana", 10)
    text.textLines(MICRO_CHAR[1])
    pdf.drawText(text)

    # Microscopic Characteristic
    text = pdf.beginText(LEFT_LINE, 585)
    text.setFont("Verdana-Bold", 10)
    text.textLine(CONCLUSION[0])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 570)
    text.setFont("Verdana", 10)
    text.textLines(CONCLUSION[1])
    pdf.drawText(text)

    # Research Characteristic
    text = pdf.beginText(LEFT_LINE, 535)
    text.setFont("Verdana-Bold", 10)
    text.textLine(RESEARCH[0])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 525)
    text.setFont("Verdana", 8)
    for line in RESEARCH[1]:
        text.textLine(line)
    pdf.drawText(text)

    # Staining
    table = Table(data=STAINING)
    table.setStyle(
        TableStyle(
            [
                ("FONT", (0, 0), (0, 0), "Verdana-Bold", 10),
                ("FONT", (0, 1), (0, -1), "Verdana-Bold", 8),
                ("FONT", (1, 1), (1, -1), "Verdana", 8),
                ("ALIGN", (0, 0), (0, 0), "CENTER"),
                ("VALIGN", (0, 1), (0, -1), "MIDDLE"),
                ("RIGHTPADDING", (1, 1), (1, -1), 30),
                ("SPAN", (1, 0), (0, 0)),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )
    table.wrapOn(pdf, 100, 400)
    table.drawOn(pdf, LEFT_LINE, 410)

    # Interpretation
    text = pdf.beginText(LEFT_LINE, 390)
    text.setFont("Verdana-Bold", 10)
    text.textLine(INTERPRETATION[0])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 375)
    text.setFont("Verdana", 10)
    text.textLine(INTERPRETATION[1])
    pdf.drawText(text)

    # Footer
    text = pdf.beginText(LEFT_LINE, 355)
    text.setFont("Verdana", 10)
    text.textLine(date_of_report)
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 335)
    text.setFont("Verdana", 10)
    text.textLines(FOOTER[0])
    pdf.drawImage(SIGNATURE, RIGHT_LINE-100, 80, width=80, preserveAspectRatio=True, mask="auto")
    pdf.drawText(text)

    text = pdf.beginText(RIGHT_LINE, 330)
    text.setFont("Verdana", 10)
    text.textLine(FOOTER[1])
    pdf.drawText(text)

    text = pdf.beginText(LEFT_LINE, 260)
    text.setFont("Verdana", 10)
    text.textLines(FOOTER[2])
    pdf.drawImage(HEAD_SIGNATURE, RIGHT_LINE-100, 10, width=80, preserveAspectRatio=True, mask="auto")
    pdf.drawText(text)

    text = pdf.beginText(RIGHT_LINE, 255)
    text.setFont("Verdana", 10)
    text.textLine(FOOTER[3])
    pdf.drawText(text)
    pdf.showPage()
    pdf.save()
