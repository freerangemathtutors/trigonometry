# Started getting good enough at manim, swapped to object oriented!

from manim import *
import math

def setup(scene):
    scene.dots = VGroup(
        Dot([-1.5, -2.0, 0]).set_opacity(0),
        Dot([1.5, 2.0, 0]).set_opacity(0),
        Dot([1.5, -2.0, 0]).set_opacity(0)
    )
    scene.get_a = lambda: scene.dots[0].get_center()
    scene.get_b = lambda: scene.dots[1].get_center()
    scene.get_c = lambda: scene.dots[2].get_center()

    scene.line_a = Line(scene.get_b(), scene.get_c())
    scene.line_b = Line(scene.get_a(), scene.get_c())
    scene.line_c = Line(scene.get_a(), scene.get_b())
    scene.line_a.add_updater(lambda mob: mob.put_start_and_end_on(scene.get_b(), scene.get_c()))
    scene.line_b.add_updater(lambda mob: mob.put_start_and_end_on(scene.get_a(), scene.get_c()))
    scene.line_c.add_updater(lambda mob: mob.put_start_and_end_on(scene.get_a(), scene.get_b()))

    scene.big_tri = Polygon(scene.get_a(), scene.get_b(), scene.get_c(), color=WHITE, stroke_width=4).set_fill(BLUE, 0.3, False)

    def update_triangle(mob):
        mob.set_points_as_corners([scene.get_a(), scene.get_b(), scene.get_c(), scene.get_a()])
    scene.big_tri.add_updater(update_triangle)

    scene.angle_a = Angle(scene.line_b, scene.line_c, radius=0.7, color=BLUE)
    scene.angle_b = Angle(Line(scene.get_b(), scene.get_a()), scene.line_a, radius=0.7, color=RED).set_opacity(0)
    scene.angle_c = RightAngle(Line(scene.get_c(), scene.get_b()), Line(scene.get_c(), scene.get_a()), length=0.4, color=WHITE)

    scene.angle_a.add_updater(lambda mob: mob.become(
        Angle(scene.line_b, scene.line_c, radius=0.7, color=BLUE)
    ))
    scene.angle_b.add_updater(lambda mob: mob.become(
        Angle(Line(scene.get_b(), scene.get_a()), scene.line_a, radius=0.7, color=RED)
    ))
    scene.angle_c.add_updater(lambda mob: mob.become(
        RightAngle(Line(scene.get_c(), scene.get_b()), Line(scene.get_c(), scene.get_a()), length=0.4, color=WHITE)
    ))

    # ":" cannot be used in Text()
    with register_font("Teachers-Medium.ttf"):
        Text.set_default(font="Teachers")
        scene.label_a = MathTex(r"\theta", color=BLUE).next_to(scene.angle_a, RIGHT, buff=0.1)
        scene.label_b = MathTex(r"\phi", color=RED).next_to(scene.angle_b, DOWN, buff=0.1)
        scene.label_c = MathTex(r"90^\circ", color=WHITE).next_to(scene.angle_c, UP + LEFT, buff=0.1)
        scene.label_d = Tex(r"Opposite", color=WHITE).next_to(scene.line_a, RIGHT, buff=0.3).set_opacity(0)
        scene.label_e = Tex(r"Adjacent", color=WHITE).next_to(scene.line_b, DOWN, buff=0.3).set_opacity(0)
        scene.label_f = Tex(r"Hypotenuse", color=WHITE).next_to(scene.line_c, LEFT, buff=0.1)

class Unitcircle(Scene):
    def construct(self):
        setup(self)
        self.add()