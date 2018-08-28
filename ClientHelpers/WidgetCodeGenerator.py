import json
from FPWidgetFunction import FPWidgetFunction

class WidgetCodeGenerator:
    def __init__(self, filename):
        with open(filename) as f:
            self.topology = json.load(f)

    def createPythonHeader(self, fileName):
        with open(fileName, "w") as outFile:
            outFile.write(self.createPythonCode())

    def createCppHeader(self, fileName):
        with open(fileName, "w") as outFile:
            outFile.write(self.createCppHeaderCode())


    def createPythonCode(self):
        ret = "class FpWidgets:\n"
        return ret

    def createCppHeaderCode(self):
        ret = ""
        ret += "#ifndef FP_WIDGETS_H\n"
        ret += "#define FP_WIDGETS_H\n\n"
        ret += "#include <cstdint> // uint8_t\n\n"
        ret += "namespace FPWidgets\n{\n\n"
        ret += "struct TopologyDim{uint8_t x; uint8_t y;};\n\n"
        for fpFunction in FPWidgetFunction.all:
            ret += "class " + FPWidgetFunction.toString(fpFunction) + "\n{\n"
            ret += "public:\n"
            ret += "   enum WidgetId\n"
            ret += "   {\n"
            widgetId = 0
            lastLabel = None
            for widget in self.topology:
                if fpFunction in widget['WidgetFunction']:
                    ret += "      " + widget['Label'] + " = " + str(widgetId) + ",\n"
                    widgetId += 1
                    lastLabel = widget['Label']
            if lastLabel:
                ret += "      Last = " + lastLabel + "\n"
            else:
                ret += "      Last = -1\n"
            ret += "   };\n"
            ret += "   static const TopologyDim& getDim(WidgetId widgetId)\n"
            ret += "   {\n"
            dimStr = ""
            for widget in self.topology:
                if fpFunction in widget['WidgetFunction']:
                    if not widget['Dimension']:
                        dimX, dimY = (1, 1)
                    elif len(widget['Dimension']) == 1:
                        dimX, dimY = (widget['Dimension'][0], 1)
                    elif len(widget['Dimension']) == 2:
                        dimX, dimY = (widget['Dimension'][0], widget['Dimension'][1])
                    if dimX == 0:
                        dimX = 1
                    if dimY == 0:
                        dimY = 1
                    if dimStr:
                        dimStr += ", "
                    dimStr += "{" + str(dimX) + ", " + str(dimY) + "}"
            if dimStr:
                ret += "      static const TopologyDim dim[WidgetId::Last + 1] = { " + dimStr + "} ;\n"
                ret += "      return dim[widgetId];\n"
            else:
                ret += "      static const TopologyDim dim = {0,0};\n"
                ret += "      return dim;\n"
            ret += "   }\n"
            ret += "};\n\n"
        ret += "} // namespace\n\n"
        ret += "#endif"
        return ret

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Filename needed as argument\n")
        exit(1)
    topology = WidgetCodeGenerator(sys.argv[1])
    topology.createPythonHeader("FpWidgets.py")
    topology.createCppHeader("FpWidgets.h")
