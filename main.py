from kivymd.app import MDApp
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image

class ZoomLayout(FloatLayout):
    zoom_factor = NumericProperty(1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_canvas)
        self.bind(pos=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            scale = self.zoom_factor
            Window.transform = self.matrix(scale, scale, scale, scale, 0, 0)

    def on_touch_down(self, touch):
        if len(self.touches) >= 2:
            distance = self.distance(*self.touches)
            self.initial_distance = distance
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if len(self.touches) >= 2:
            distance = self.distance(*self.touches)
            self.zoom_factor *= distance / self.initial_distance
            self.initial_distance = distance
        return super().on_touch_move(touch)

    @staticmethod
    def distance(touch1, touch2):
        return ((touch1.x - touch2.x) ** 2 + (touch1.y - touch2.y) ** 2) ** 0.5

    @staticmethod
    def matrix(xx, xy, yx, yy, x, y):
        return [xx, xy, 0, 0,
                yx, yy, 0, 0,
                0,  0,  1, 0,
                x,  y,  0, 1]


class MyApp(MDApp):
    def build(self):
        layout = ZoomLayout()
        image = Image(source="icon/weather.png", size_hint=(None, None), size=(300, 300))
        layout.add_widget(image)

        return layout


if __name__ == "__main__":
    MyApp().run()
