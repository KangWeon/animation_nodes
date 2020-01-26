import bpy
from bpy.props import *
from ... events import propertyChanged
from ... data_structures import Stroke
from ... base_types import AnimationNode, VectorizedSocket

strokeTypeItems = [
    ("ALL", "All Strokes", "Get all strokes", "NONE", 0),
    ("INDEX", "Index Stroke ", "Get a specific stroke", "NONE", 1)
]

class GPencilFrameInputNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_GPencilFrameInputNode"
    bl_label = "GPencil Frame Input"
    errorHandlingType = "EXCEPTION"

    strokeType: EnumProperty(name = "Stroke Type", default = "ALL",
        items = strokeTypeItems, update = AnimationNode.refresh)

    useIntegerList: VectorizedSocket.newProperty()

    def create(self):
        self.newInput("Frame", "Frame", "frame", dataIsModified = True)

        if self.strokeType == "ALL":
            self.newOutput("Stroke List", "Strokes", "strokes")
        elif self.strokeType == "INDEX":
            self.newInput(VectorizedSocket("Integer", "useIntegerList",
            ("Stroke Index", "strokeIndex"), ("Stroke Indices", "strokeIndices")))

            self.newOutput(VectorizedSocket("Stroke", "useIntegerList",
            ("Stroke", "stroke"), ("Strokes", "strokes")))

    def draw(self, layout):
        layout.prop(self, "strokeType", text = "")

    def getExecutionFunctionName(self):
        if self.strokeType == "ALL":
            return "execute_AllStrokes"
        elif self.strokeType == "INDEX":
            if self.useIntegerList:
                return "execute_StrokeIndices"
            else:
                return "execute_StrokeIndex"

    def execute_AllStrokes(self, frame):
        return frame.strokes

    def execute_StrokeIndex(self, frame, strokeIndex):
        strokes = frame.strokes
        if len(frame.strokes) == 0:
            return Stroke()
        return self.getStroke(strokes, strokeIndex)

    def execute_StrokeIndices(self, frame, strokeIndices):
        strokes = frame.strokes
        outStrokes = []
        if len(frame.strokes) == 0:
            return outStrokes

        for index in strokeIndices:
            outStrokes.append(self.getStroke(strokes, index))
        return outStrokes

    def getStroke(self, strokes, strokeIndex):
        try: return strokes[strokeIndex]
        except: self.raiseErrorMessage(f"There is no stroke for index '{strokeIndex}'.")
