import bpy
from bpy.types import Node
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged
from mn_utils import *

class SubProgramNode(Node, AnimationNode):
	bl_idname = "SubProgramNode"
	bl_label = "Sub-Program"
	
	def getSubProgramNames(self, context):
		nodeTree = self.id_data
		subProgramNames = []
		for node in nodeTree.nodes:
			if node.bl_idname == "SubProgramStartNode": subProgramNames.append((node.subProgramName, node.subProgramName, ""))
		return subProgramNames
	def getStartNode(self):
		subProgramName = self.subProgramsEnum
		for node in self.id_data.nodes:
			if node.bl_idname == "SubProgramStartNode":
				if node.subProgramName == subProgramName:
					return node
		return None
	
	subProgramsEnum = bpy.props.EnumProperty(items = getSubProgramNames, name = "Sub-Programs")
	
	def init(self, context):
		self.inputs.new("IntegerSocket", "Amount")
		
	def draw_buttons(self, context, layout):
		layout.prop(self, "subProgramsEnum")
		rebuild = layout.operator("mn.rebuild_sub_program_sockets", "Rebuild Sockets")
		rebuild.nodeTreeName = self.id_data.name
		rebuild.nodeName = self.name
						
	def rebuildSubProgramSockets(self):
		self.removeDynamicSockets()
		startNode = self.getStartNode()
		if startNode is not None:
			for socket in startNode.sockets:
				self.inputs.new(socket.socketType, socket.socketName)
				self.outputs.new(socket.socketType, socket.socketName)
	def removeDynamicSockets(self):
		self.outputs.clear()
		for i, socket in enumerate(self.inputs):
			if i > 0: self.inputs.remove(socket)		
					

		
# register
################################
		
def register():
	bpy.utils.register_module(__name__)

def unregister():
	bpy.utils.unregister_module(__name__)