class FPWidgetTypes:
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
        if widgetCat == FPWidgetTypes.POTENTIOMETER:
            return "Potentiometer"
        elif widgetCat == FPWidgetTypes.BUTTON:
            return "Button"
        elif widgetCat == FPWidgetTypes.ENCODER:
            return "Encoder"
        elif widgetCat == FPWidgetTypes.TOUCH:
            return "TouchSurface"
        elif widgetCat == FPWidgetTypes.DISPLAY:
            return "Display"
        elif widgetCat == FPWidgetTypes.LED:
            return "Led"
        elif widgetCat == FPWidgetTypes.POT_MOVE:
            return "PotentiometerMove"

