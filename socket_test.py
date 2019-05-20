# pip install eventlet
from app import app
from flask_socketio import SocketIO, emit
    
socketio = SocketIO(app)



# ----------
# Server
# socketio.on('receiving an order/image uppload')
# emit something back to the client (send the images back to the client)

# client side:
# .on('receiving images from the server')
# do something (display the images)