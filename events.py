import bpy
from . import event_handler
from bpy.app.handlers import persistent
from . import tree_info

class EventState:
    def __init__(self):
        self.reset()
        self.isRendering = False

    def reset(self):
        self.treeChanged = False
        self.fileChanged = False
        self.sceneChanged = False
        self.frameChanged = False
        self.addonChanged = False
        self.propertyChanged = False

    def getActives(self):
        events = set()
        if self.treeChanged: events.add("Tree")
        if self.fileChanged: events.add("File")
        if self.addonChanged: events.add("Addon")
        if self.sceneChanged: events.add("Scene")
        if self.frameChanged: events.add("Frame")
        if self.isRendering: events.add("Render")
        if self.propertyChanged: events.add("Property")
        return events

event = EventState()

@persistent
def sceneUpdated(scene):
    event.sceneChanged = True
    event_handler.update(event.getActives())
    event.reset()

@persistent
def frameChanged(scene):
    event.frameChanged = True

@persistent
def fileLoaded(scene):
    event.fileChanged = True
    treeChanged()

def addonChanged():
    event.addonChanged = True
    treeChanged()

def propertyChanged(self = None, context = None):
    event.propertyChanged = True

def executionCodeChanged(self = None, context = None):
    treeChanged()

def networkChanged(self = None, context = None):
    treeChanged()

def treeChanged(self = None, context = None):
    event.treeChanged = True
    tree_info.treeChanged()

@persistent
def renderIsStarting(scene):
    event.isRendering = True

@persistent
def renderIsEnding(scene):
    event.isRendering = False

def isRendering():
    return event.isRendering



# Register
##################################

def registerHandlers():
    bpy.app.handlers.scene_update_post.append(sceneUpdated)
    bpy.app.handlers.frame_change_post.append(frameChanged)
    bpy.app.handlers.load_post.append(fileLoaded)

    bpy.app.handlers.render_pre.append(renderIsStarting)
    bpy.app.handlers.render_init.append(renderIsStarting)
    bpy.app.handlers.render_post.append(renderIsEnding)
    bpy.app.handlers.render_cancel.append(renderIsEnding)
    bpy.app.handlers.render_complete.append(renderIsEnding)

    addonChanged()

def unregisterHandlers():
    bpy.app.handlers.frame_change_post.remove(frameChanged)
    bpy.app.handlers.scene_update_post.remove(sceneUpdated)
    bpy.app.handlers.load_post.remove(fileLoaded)

    bpy.app.handlers.render_pre.remove(renderIsStarting)
    bpy.app.handlers.render_init.remove(renderIsStarting)
    bpy.app.handlers.render_post.remove(renderIsEnding)
    bpy.app.handlers.render_cancel.remove(renderIsEnding)
    bpy.app.handlers.render_complete.remove(renderIsEnding)
