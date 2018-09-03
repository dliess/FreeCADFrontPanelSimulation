import json
from FPWidgetFunction import FPWidgetFunction

class WidgetCodeGenerator:
    def __init__(self, filename):
        with open(filename) as f:
            self.topology = json.load(f)

    def createCppHeader(self, fileName):
        with open(fileName, "w") as outFile:
            outFile.write(self.createCppHeaderCode())

    def createCppHeaderCode(self):
        ret = ""
        ret += "#ifndef WIDGET_TOPOLOGY_H\n"
        ret += "#define WIDGET_TOPOLOGY_H\n\n"
        ret += "#include \"WidgetTypes.h\"\n"
        ret += "#include \"Vector2D.h\"\n\n"
        ret += "template<class WidgetType>\n"
        ret += "class WidgetTopology\n"
        ret += "{};\n\n"
        for fpFunction in FPWidgetFunction.all:
            ret += "template<>\n"
            ret += "class WidgetTopology<WidgetTypes::" + FPWidgetFunction.toString(fpFunction) + ">\n{\n"
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
            ret += "   static const Vec2D& getDim(WidgetId widgetId)\n"
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
                ret += "      static const Vec2D dim[WidgetId::Last + 1] = { " + dimStr + "} ;\n"
                ret += "      return dim[widgetId];\n"
            else:
                ret += "      static const Vec2D dim = {0,0};\n"
                ret += "      return dim;\n"
            ret += "   }\n"
            ret += "};\n\n"
        ret += "#endif"
        return ret

if __name__ == "__main__":
    import sys
    import os.path
    if len(sys.argv) < 2:
        print("Filename needed as argument\n")
        exit(1)
    jsonName = sys.argv[1]
    topology = WidgetCodeGenerator(str(jsonName))
    baseName = os.path.basename(jsonName)
    woExt = os.path.splitext(baseName)[0]
    topology.createCppHeader(str(woExt) + ".h")
