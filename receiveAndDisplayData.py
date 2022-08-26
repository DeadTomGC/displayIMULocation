from importlib.abc import Loader
from direct.task import Task
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, TextNode
from direct.gui.DirectGui import *
import sys
import zmq

class TestClass(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.title = OnscreenText(  # Create the title
            text="DeltaT: 0.01",
            parent=base.a2dBottomRight, align=TextNode.A_right,
            style=1, fg=(1, 1, 1, 1), pos=(-0.1, 0.1), scale=.07)
        self.board = loader.loadModel("models/imu.gltf")
        self.board.reparentTo(render)
        self.board.setScale(1)
        self.board.setP(self.board,-90)
        self.board.setPos(0,0,0)
        self.disableMouse()
        camera.setPos(0, 0, 1000)  # Set the camera position (X, Y, Z)
        camera.setHpr(0, -90, 180)  # Set the camera orientation
        self.addTask(self.updatePosition,'update position')
        self.context = zmq.Context()
        self.sock = self.context.socket(zmq.SUB)
        self.sock.connect ("tcp://localhost:1337")
        self.sock.setsockopt(zmq.SUBSCRIBE, b"") 

    def updatePosition(self,argument):
        message = ''
        try:
            while not self.sock.poll(timeout=0)==0: 
                message = self.sock.recv_string(flags=zmq.NOBLOCK)
        except:
            message = message
            #pass
        pos = self.board.getPos()
        hpr = self.board.getHpr()
        msgSplit = message.split()
        if len(msgSplit)==7:
            pos[0] = -float(msgSplit[1])*1000
            pos[1] = float(msgSplit[0])*1000
            pos[2] = float(msgSplit[2])*1000
            hpr[0] = float(msgSplit[3])
            hpr[1] = -float(msgSplit[4])
            hpr[2] = float(msgSplit[5])
            self.title.text = "DeltaT: " + msgSplit[6] + "s"
        self.board.setPos(pos)
        self.board.setHpr(hpr)
        return Task.cont

game = TestClass()
game.run()