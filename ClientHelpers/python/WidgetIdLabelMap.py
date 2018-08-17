import json

class WidgetIdLabelMap:
    def __init__(self, filename):
        self._labelToId = dict()
        self._idToLabel = dict()
        with open(filename) as f:
            topology = json.load(f)
            for widget in topology:
                self._labelToId[widget['Label']] = widget['Id']
                self._idToLabel[widget['Id']] = widget['Label']

    def widgetLabelToId(widgetLabel):
        match = re.match("(.*)\[(\d+)\]\[(\d+)\]", widgetLabel)
        label = widgetLabel
        widgetCoord = None
        if match:
            label = match.group(1)
            widgetCoord = (int(match.group(2)), int(match.group(3)))
        else: 
            match = re.match("(.*)\[(\d+)\]", widgetLabel)
            if match:
                label = match.group(1)
                widgetCoord = (int(match.group(2)))
        return (self._labelToId[label], widgetCoord)

    def widgetIdToLabel(widgetId):
        label = self._idToLabel(widgetId[0])
        if widget[1]:
            coord = widget[1]
            for i in range(len(coord)):
                label = label + "[" + str(coord[i]) + "]"
        return label
