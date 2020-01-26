import bpy
from ... base_types import AnimationNode, VectorizedSocket

class GPencilLayerOpacityNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_GPencilLayerOpacityNode"
    bl_label = "GPencil Layer Opacity"

    useLayerList: VectorizedSocket.newProperty()

    def create(self):
        self.newInput(VectorizedSocket("Layer", "useLayerList",
            ("Layer", "layer"), ("Layers", "layers")), dataIsModified = True)
        self.newInput(VectorizedSocket("Float", "useLayerList",
            ("Opacity", "opacity"), ("Opacities", "opacities")))
        self.newOutput(VectorizedSocket("Layer", "useLayerList",
            ("Layer", "layer"), ("Layers", "layers")))

    def getExecutionFunctionName(self):
        if self.useLayerList:
            return "execute_LayerList"
        else:
            return "execute_Layer"

    def execute_Layer(self, layer, opacity):
        layer.opacity = opacity
        return layer

    def execute_LayerList(self, layers, opacities):
        if len(opacities) < len(layers): return layers
        for i, layer in enumerate(layers):
            layer.opacity = opacities[i]
        return layers
