import zmq
import time

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:1337")

loc = [0.0,0.0,0.0]

while True:
    loc[1]+=0.01
    time.sleep(0.01)
    socket.send_string("%f %f %f" % (loc[0], loc[1], loc[2]))