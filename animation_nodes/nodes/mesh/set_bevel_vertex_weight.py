import bpy
from ... data_structures import VirtualDoubleList
from ... base_types import AnimationNode, VectorizedSocket

class BevelVertexWeights(bpy.types.Node, AnimationNode):
    bl_idname = "an_SetBevelVertexWeight"
    bl_label = "Set Bevel Vertex Weight"
    errorHandlingType = "EXCEPTION"

    useWeightList: VectorizedSocket.newProperty()

    def create(self):
        self.newInput("Object", "Object", "object", defaultDrawType = "PROPERTY_ONLY")
        self.newInput(VectorizedSocket("Float", "useWeightList",
            ("Weight", "weight"), ("Weights", "weights")))

        self.newOutput("Object", "Object", "object")

    def execute(self, object, weights):
        if object is None: return None

        if object.type != "MESH":
            self.raiseErrorMessage("Object is not a mesh object.")

        if object.mode != "OBJECT":
            self.raiseErrorMessage("Object is not in object mode.")

        if not object.data.use_customdata_vertex_bevel:
            object.data.use_customdata_vertex_bevel = True

        weights = VirtualDoubleList.create(weights, 0).materialize(len(object.data.vertices))
        object.data.vertices.foreach_set('bevel_weight', weights)
        object.data.update()
        return object
