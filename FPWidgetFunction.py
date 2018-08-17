class FPWidgetFunction:
    POTENTIOMETER       = 0
    BUTTON              = 1
    ENCODER             = 2
    TOUCH               = 3
    DISPLAY             = 4
    LED                 = 5
    POT_MOVE            = 6

    all = [ POTENTIOMETER, \
            BUTTON,        \
            ENCODER,       \
            TOUCH,         \
            DISPLAY,       \
            LED,           \
            POT_MOVE ]


    @staticmethod
    def toString(widgetCat):
        if widgetCat == FPWidgetFunction.POTENTIOMETER:
            return "Potentiometer"
        elif widgetCat == FPWidgetFunction.BUTTON:
            return "Button"
        elif widgetCat == FPWidgetFunction.ENCODER:
            return "Encoder"
        elif widgetCat == FPWidgetFunction.TOUCH:
            return "TouchSurface"
        elif widgetCat == FPWidgetFunction.DISPLAY:
            return "Display"
        elif widgetCat == FPWidgetFunction.LED:
            return "Led"
        elif widgetCat == FPWidgetFunction.POT_MOVE:
            return "PotentiometerMove"

