import os
import platform
import configparser

config = configparser.ConfigParser()


## Directory config
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMP_DIR= BASE_DIR+'/temp/'
LOG_DIR= BASE_DIR+'/logs/'
NAME_PDF = 'weight_tag.pdf'
OS_WIN32= False

## Windows
if(platform.system() in ['Windows', 'win32']):
    config.read("config\\config.ini")
    OS_WIN32= True
    TEMP_DIR= BASE_DIR+'\\temp\\'
    LOG_DIR= BASE_DIR+'\\logs\\'

else:
    config.read("config/config.ini")

# Only Windows
ACROBAT_READER = config['PRINTER']['ADOBE_PATH']

## Printer Config
PRINTER_CONF = {}
PRINTER_CONF['PAGESIZE_WIDHT'] = float(config['PRINTER']['PAGESIZE_WIDHT'])
PRINTER_CONF['PAGESIZE_HEIGHT'] = float(config['PRINTER']['PAGESIZE_HEIGHT'])
PRINTER_CONF['BAR_WIDTH'] = float(config['PRINTER']['BAR_WIDTH'])
PRINTER_CONF['BAR_HEIGHT'] = float(config['PRINTER']['BAR_HEIGHT'])
PRINTER_CONF['TEXT_NAME_Y'] = float(config['PRINTER']['TEXT_NAME_Y'])
PRINTER_CONF['TEXT_NAME2_Y'] = float(config['PRINTER']['TEXT_NAME2_Y'])
PRINTER_CONF['TEXT_DATE_Y'] = float(config['PRINTER']['TEXT_DATE_Y'])
PRINTER_CONF['BARCODE_Y'] = float(config['PRINTER']['BARCODE_Y'])
PRINTER_CONF['TEXT_WEIGHT_Y'] = float(config['PRINTER']['TEXT_WEIGHT_Y'])
PRINTER_CONF['TEXT_PRICE_Y'] = float(config['PRINTER']['TEXT_PRICE_Y'])
WEIGHT_ON_BARCODE = True if (config['PRINTER']['WEIGHT_ON_BARCODE']== 'True') else False
AUTO_PRINT= True if (config['PRINTER']['AUTO_PRINT']== 'True') else False
DOLLAR_PRICE= True if (config['PRINTER']['DOLLAR_PRICE']== 'True') else False

## Balance Config
BALANCE_CONF = {}
BALANCE_CONF['PORT'] = config['BALANCE']['PORT']

# App
SECRET_KEY = os.environ.get('SECRET_KEY')
API_KEY = os.environ.get('API_KEY')