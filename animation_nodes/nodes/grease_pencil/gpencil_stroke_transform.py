import bpy
from ... base_types import AnimationNode, VectorizedSocket

class GPencilStrokeTransformNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_GPencilStrokeTransformNode"
    bl_label = "GPencil Stroke Transform"
    bl_width_default = 165

    useStrokeList: VectorizedSocket.newProperty()
    useMatrixList: VectorizedSocket.newProperty()

    def create(self):
        self.newInput(VectorizedSocket("Stroke", "useStrokeList",
            ("Stroke", "stroke"), ("Strokes", "strokes")), dataIsModified = True)
        self.newInput(VectorizedSocket("Matrix", "useMatrixList",
            ("Matrix", "matrix"), ("Matices", "matrices")))
        self.newOutput(VectorizedSocket("Stroke", "useStrokeList",
            ("Stroke", "outStroke"), ("Strokes", "outStrokes")))

    def getExecutionFunctionName(self):
        if self.useStrokeList and self.useMatrixList:
            return "executeListList"
        elif self.useStrokeList:
            return "executeList"
        else:
            return "executeSingle"

    def executeSingle(self, stroke, matrix):
        if stroke is None: return None
        if matrix is not None:
            self.strokeTransfom(stroke, matrix)
        return stroke

    def executeList(self, strokes, matrix):
        if len(strokes) == 0: return strokes
        for stroke in strokes:
            if stroke is not None:
                if matrix is not None:
                    self.strokeTransfom(stroke, matrix)
        return strokes

    def executeListList(self, strokes, matrices):
        if len(strokes) == 0 or len(matrices) == 0 or len(strokes) != len(matrices): return strokes
        for i, stroke in enumerate(strokes):
            if stroke is not None:
                if matrices[i] is not None:
                    self.strokeTransfom(stroke, matrices[i])
        return strokes

    def strokeTransfom(self, outStroke, matrix):
        return outStroke.vertices.transform(matrix)
