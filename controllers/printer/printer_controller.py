from flask import Flask, request, Blueprint, abort, current_app
from jinja2 import TemplateNotFound
import types
import werkzeug
from setting import OS_WIN32, WEIGHT_ON_BARCODE, AUTO_PRINT, DOLLAR_PRICE
from . import tag_generator as generator
from . import mute_print as printer

printer_routes = Blueprint('printer_routes', __name__, template_folder='controllers/printer')

@printer_routes.route('/print-tag', methods=['POST'])
def print_tag():
    try:
        req_data = request.get_json()
        body_tag={}
        body_tag['barcode'] = req_data.get('barcode', False)
        body_tag['weight'] = req_data.get('weight',False)
        body_tag['name'] = req_data.get('name',False)
        body_tag['price'] = req_data.get('price',False)
        body_tag['dollarPrice'] = req_data.get('dollarPrice',False)
        body_tag['date'] = req_data.get('date',False)

        if any((isinstance(body_tag[key], bool) and bool(body_tag[key]) == False) for key in body_tag):
            current_app.logger.warning('null values')
            abort(500, 'se han enviado valores nulos')

        else:
            if(body_tag['weight'] < 100):
                if(WEIGHT_ON_BARCODE):
                    weight_barcode= generate_barcode_EAN13(body_tag['weight'], body_tag['barcode'])
                    body_tag['barcode']= weight_barcode

                body_tag['printer_price']= body_tag['dollarPrice'] if(DOLLAR_PRICE) else body_tag['price']

                generator.generate_tag(body_tag)
                if(OS_WIN32 and AUTO_PRINT):
                    printer.auto_print()
                    current_app.logger.info('auto print')
                else:
                    current_app.logger.info('no print')
            else:
                current_app.logger.warning('to much weight: %s', str(body_tag['weight']))
                abort(500, 'to much weight: ' +str(body_tag['weight']) )
                
        return ({ 'status': 'ok'})
    except Exception as e:
        current_app.logger.error(e)
        abort(500)


def generate_barcode_EAN13(weight, barcode):
    w =weight * 1000
    str_w= str(int(w)).zfill(5)
    return barcode[0:7]+str_w
    