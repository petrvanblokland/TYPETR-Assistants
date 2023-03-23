import vanilla
import merz

class MerzInteractingView(merz.MerzView):
    pass
    
class MerzDemo:

    def __init__(self):
        self.w = vanilla.Window((530, 150))
        self.merzView = MerzInteractingView(
            "auto",
            backgroundColor=(1, 1, 1, 1)
        )
        self.button = vanilla.Button(
            "auto",
            "Animate",
            callback=self.buttonCallback
        )
        self.w.stack = vanilla.VerticalStackView(
            (0, 0, 0, 0),
            views=[
                dict(
                    view=self.merzView,
                    height=200
                ),
                dict(
                    view=self.button,
                    height=30
                )
            ],
            spacing=10,
            edgeInsets=(15, 15, 15, 15)
        )

        container = self.merzView.getMerzContainer()
        container.appendBaseSublayer(
            position=(50, 50),
            size=(400, 100),
            backgroundColor=(1, 1, 0, 1)
        )
        self.layer = container.appendBaseSublayer(
            position=(0, 0),
            size=(400, 100),
            backgroundColor=(1, 0, 0, 0.75),
            borderColor=(0, 0, 1, 1),
            borderWidth=10
        )

        self.w.open()

    def buttonCallback(self, sender):
        with self.layer.propertyGroup(
                duration=4
            ):
            self.layer.setPosition((100, 100))
            self.layer.setBackgroundColor((0, 0, 1, 0.75))
            self.layer.setBorderColor((0, 0, 1, 1))
            self.layer.setBorderWidth(30)


MerzDemo()