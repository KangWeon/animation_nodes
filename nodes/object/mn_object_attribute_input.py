import bpy
from bpy.types import Node
from mn_node_base import AnimationNode
from mn_execution import nodePropertyChanged, allowCompiling, forbidCompiling

class mn_ObjectAttributeInputNode(Node, AnimationNode):
	bl_idname = "mn_ObjectAttributeInputNode"
	bl_label = "Object Attribute Input"
	
	def init(self, context):
		forbidCompiling()
		self.inputs.new("mn_ObjectSocket", "Object").showName = False
		self.inputs.new("mn_StringSocket", "Attribute").string = ""
		self.outputs.new("mn_GenericSocket", "Value")
		allowCompiling()
		
	def getInputSocketNames(self):
		return {"Object" : "object",
				"Attribute" : "attribute"}
	def getOutputSocketNames(self):
		return {"Value" : "value"}
		
	def execute(self, object, attribute):
		try:
			return eval("object." + attribute)
		except:
			return None