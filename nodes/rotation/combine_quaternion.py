import bpy
from ... base_types.node import AnimationNode

class CombineQuaternionNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_CombineQuaternionNode"
    bl_label = "Combine Quaternion"

    def create(self):
        self.newInput("Float", "W", "w").value = 1
        self.newInput("Float", "X", "x")
        self.newInput("Float", "Y", "y")
        self.newInput("Float", "Z", "z")
        self.newOutput("Quaternion", "Quaternion", "quaternion")

    def getExecutionCode(self):
        return "quaternion = mathutils.Quaternion((w, x, y, z))"

    def getUsedModules(self):
        return ["mathutils"]
