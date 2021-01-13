from flask import Flask, url_for, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
import threading
import time
from logs import logger_conf 
from controllers.balance import get_weight as balance
from controllers.printer.printer_controller import printer_routes

# set to flask
app = Flask(__name__)

# set to config on project
app.config.from_pyfile('setting.py')

# set logger
logger_conf.configure_logging(app)

# set to routes witch  blueprint
app.register_blueprint(printer_routes, url_prefix='/printer')

# set cors
CORS(app)

#main endponit
@app.route('/')
def welcome():
    return 'welcome to the balance app!'

# set socketIo 
socketio = SocketIO(app, cors_allowed_origins="*")

# Socket
@socketio.on('connect')
def handler_connect():
    app.logger.info('user connect')
    send('connection success')

@socketio.on('disconnect')
def handler_disconnect():
    app.logger.info('user disconect')
    send('user disconnect')

# create background process for balance
def background():
    data= 0
    try:
        while True:
            data, status= balance.get_weight()
            if (status):
                app.logger.info('emit data from balance: %s', data)
                socketio.emit('weight from balance', {'weight': data})
            else:
                # app.logger.warning('no data to send from balance')
                # socketio.emit('weight from balance', {'weight': data})
                time.sleep(10)
    except Exception as e:
        app.logger.error('%s', e)
        
# set threading for background process
tr = threading.Thread(name='background', target=background)
tr.start()

# show routes
with app.test_request_context(): 
    print(url_for('printer_routes.print_tag')) 

if __name__ == '__main__':
    app.run()
    # socketio.run(app)