#!/usr/bin/env python3
import os
import platform
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.barcode.eanbc import Ean13BarcodeWidget
from reportlab.graphics import renderPDF
from reportlab.pdfgen.canvas import Canvas

from flask import Flask, request, Blueprint, abort, current_app


from setting import TEMP_DIR, NAME_PDF, PRINTER_CONF, DOLLAR_PRICE

"""
Adjust pagesize, number of labels, barcode size and
positions of barcode and description to your needs.
"""

PAGESIZE = (PRINTER_CONF['PAGESIZE_WIDHT'] *mm, PRINTER_CONF['PAGESIZE_HEIGHT']*mm)
NUM_LABELS_X = 1
NUM_LABELS_Y = 1

BAR_WIDTH = PRINTER_CONF['BAR_WIDTH']
BAR_HEIGHT = PRINTER_CONF['BAR_HEIGHT']
TEXT_NAME_Y = PRINTER_CONF['TEXT_NAME_Y']
TEXT_NAME2_Y = PRINTER_CONF['TEXT_NAME2_Y']
TEXT_DATE_Y = PRINTER_CONF['TEXT_DATE_Y']
BARCODE_Y = PRINTER_CONF['BARCODE_Y']
TEXT_WEIGHT_Y = PRINTER_CONF['TEXT_WEIGHT_Y']
TEXT_PRICE_Y = PRINTER_CONF['TEXT_PRICE_Y']

LABEL_WIDTH = PAGESIZE[0] / NUM_LABELS_X
LABEL_HEIGHT = PAGESIZE[1] / NUM_LABELS_Y
SHEET_TOP = PAGESIZE[1]

def label(ean13: str, description: str, date:str, price: float, weight: float) -> Drawing:
    """
    Generate a drawing with EAN-13 barcode and descriptive text.
    :param ean13: The EAN-13 Code.
    :type ean13: str
    :param description: Short product description.
    :type description: str
    :return: Drawing with barcode and description
    :rtype: Drawing
    """
    currency = "${:,.2f}".format(price) if(DOLLAR_PRICE) else "{:,.3f} Bs".format(price)

    main_currency, fractional_currency = currency.split(".")[0], currency.split(".")[1]
    new_main_currency = main_currency.replace(",", ".")
    currency = new_main_currency + ',' + fractional_currency

    text_price = String(0, TEXT_PRICE_Y, currency, fontName="Helvetica",fontSize=12, textAnchor="middle")
    text_price.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)
    
    str_weight= "{:,.3f}".format(weight)

    main_weight, fractional_weight = str_weight.split(".")[0], str_weight.split(".")[1]
    new_main_weight = main_weight.replace(",", ".")
    str_weight = new_main_weight
    if(not int(fractional_weight) == 0):
        str_weight += ','+ fractional_weight
    str_weight += " Kg"

    text_weight = String(0, TEXT_WEIGHT_Y, str_weight, fontName="Helvetica",fontSize=10, textAnchor="middle")
    text_weight.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)

    name1 = description[:25]
    name2= ''
    if(len(description) > 25):
        name2 = (description[25:50] + '..') if len(description) > 50 else description[25:]

    text_name1 = String(0, TEXT_NAME_Y, name1, fontName="Helvetica",fontSize=10, textAnchor="middle")
    text_name1.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)

    text_name2 = String(0, TEXT_NAME2_Y, name2, fontName="Helvetica",fontSize=10, textAnchor="middle")
    text_name2.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)

    text_date = String(0, TEXT_DATE_Y, date, fontName="Helvetica",fontSize=6, textAnchor="middle")
    text_date.x = LABEL_WIDTH / 2  # center text (anchor is in the middle)


    barcode = Ean13BarcodeWidget(ean13)
    barcode.barWidth = BAR_WIDTH
    barcode.barHeight = BAR_HEIGHT
    x0, y0, bw, bh = barcode.getBounds()
    barcode.x = (LABEL_WIDTH - bw) / 2  # center barcode
    barcode.y = BARCODE_Y  # spacing from label bottom (pt)

    label_drawing = Drawing(LABEL_WIDTH, LABEL_HEIGHT)
    label_drawing.add(text_name1)
    label_drawing.add(text_name2)
    label_drawing.add(text_date)
    label_drawing.add(barcode)
    label_drawing.add(text_weight)
    label_drawing.add(text_price)
    return label_drawing

def fill_sheet(canvas: Canvas, label_drawing: Drawing):
    """
    Simply fill the given ReportLab canvas with label drawings.
    :param canvas: The ReportLab canvas
    :type canvas: Canvas
    :param label_drawing: Contains Drawing of configured size
    :type label_drawing: Drawing
    """
    """ for u in range(0, NUM_LABELS_Y):
        for i in range(0, NUM_LABELS_X):
            x = i * LABEL_WIDTH
            y = SHEET_TOP - LABEL_HEIGHT - u * LABEL_HEIGHT
            renderPDF.draw(label_drawing, canvas, x, y) """
    
    renderPDF.draw(label_drawing, canvas, 0,0)

def generate_tag(body):
    try:
        canvas = Canvas(TEMP_DIR+NAME_PDF, pagesize=PAGESIZE)
        sticker = label(body['barcode'], body['name'], body['date'], body['printer_price'], body['weight'])
        fill_sheet(canvas, sticker)
        canvas.save()
    except Exception as e:
        print(e)
        abort(500, e)
        # current_app.logger.error(e)
        