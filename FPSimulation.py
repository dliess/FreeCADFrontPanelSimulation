import FreeCADGui
import FPEventDispatcher
import FPSimServer

simulationRunning = False

def startSimulation():
    global simulationRunning
    FPEventDispatcher.eventDispatcher.activate()
    FPSimServer.server.start()
    simulationRunning = True

def stopSimulation():
    global simulationRunning
    if simulationRunning:
        FPEventDispatcher.eventDispatcher.deactivate()
        FPSimServer.server.stop()
        simulationRunning = False
