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

    scene.big_tri = Polygon(scene.get_a(), scene.get_b(), scene.get_c(), color=scene.colours["tri_out"], stroke_width=4).set_fill(BLUE, scene.colours["tri_in_op"], False)

    def update_triangle(mob):
        mob.set_points_as_corners([scene.get_a(), scene.get_b(), scene.get_c(), scene.get_a()])
    scene.big_tri.add_updater(update_triangle)

    scene.angle_a = Angle(scene.line_b, scene.line_c, radius=0.7, color=scene.colours["angle_a"])
    scene.angle_b = Angle(Line(scene.get_b(), scene.get_a()), scene.line_a, radius=0.7, color=scene.colours["angle_b"]).set_opacity(0)
    scene.angle_c = RightAngle(Line(scene.get_c(), scene.get_b()), Line(scene.get_c(), scene.get_a()), length=0.4, color=scene.colours["angle_c"])

    scene.angle_a.add_updater(lambda mob: mob.become(
        Angle(scene.line_b, scene.line_c, radius=angle_radius(scene), color=scene.colours["angle_a"])
    ))
    scene.angle_b.add_updater(lambda mob: mob.become(
        Angle(Line(scene.get_b(), scene.get_a()), scene.line_a, radius=angle_radius(scene), color=scene.colours["angle_b"])
    ))
    scene.angle_c.add_updater(lambda mob: mob.become(
        RightAngle(Line(scene.get_c(), scene.get_b()), Line(scene.get_c(), scene.get_a()), length=angle_radius(scene)*(4/7), color=scene.colours["angle_c"])
    ))

    # ":" cannot be used in Text()
    with register_font("Teachers-Medium.ttf"):
        Text.set_default(font="Teachers")
        scene.label_a = MathTex(r"\theta", color=scene.colours["angle_a"]).next_to(scene.angle_a, RIGHT, buff=0.1)
        scene.label_b = MathTex(r"\phi", color=scene.colours["angle_b"]).next_to(scene.angle_b, DOWN, buff=0.1)
        scene.label_c = MathTex(r"90^\circ", color=scene.colours["angle_c"]).next_to(scene.angle_c, UP + LEFT, buff=0.1)
        scene.label_d = Tex(r"Opp", color=WHITE).next_to(scene.line_a, RIGHT, buff=0.3).set_opacity(0)
        scene.label_e = Tex(r"Adj", color=WHITE).next_to(scene.line_b, DOWN, buff=0.3).set_opacity(0)
        scene.label_f = Tex(r"1", color=WHITE).next_to(scene.line_c, LEFT, buff=0.1).set_opacity(0)

class Unitcircle(Scene):
    colours = {
        "hyp": GOLD,
        "opp": TEAL,
        "adj": GREEN,
        "tri_out": WHITE,
        "tri_in": BLUE,
        "tri_in_op": 0.3,
        "angle_a": BLUE,
        "angle_b": RED, 
        "angle_c": WHITE
    }

    def construct(self):
        self.init_scale = 5
        setup(self)
        self.dots.shift([-4.0, 0, 0])
        self.grid_cir = NumberPlane(
            [-1.5, 1.5, 1], 
            [-1.5, 1.5, 1],
            6, 6, faded_line_ratio=2
        ).move_to([3, 0, 0])
        self.grid_big = NumberPlane(
            [-3, 3, 1],
            [-3, 3, 1],
            6, 6, faded_line_ratio=2
        )
        self.grid_coords = VGroup(
            Tex("1").move_to([3.2, 0, 0]),
            Tex("1").move_to([0, 3.3, 0]),
            Tex("-1").move_to([-3.3, 0, 0]),
            Tex("-1").move_to([0, -3.3, 0])
        )
        self.circle = Circle(3).rotate(math.radians(53.13))
        
        self.add(
            self.dots, 
            self.big_tri, 
            self.line_a, 
            self.line_b, 
            self.line_c, 
            self.angle_a, 
            self.angle_c,
            self.label_f
        )
        self.update_mobjects(0)
        self.init_scale = self.line_c.get_length()
        self.wait()

        self.play(Create(self.grid_cir))
        self.play(
            self.dots.animate.scale(3/self.line_c.get_length())
        )

        self.onebrace = BraceLabel(self.line_c, "1", rotate_vector(self.line_c.get_unit_vector(), PI / 2))

        self.play(
            Create(self.onebrace)
        )
        self.wait()
        self.play(
            self.onebrace.animate.set_opacity(0),
            self.grid_cir.animate.move_to([0, 0, 0])
        )
        self.play(
            self.grid_cir.animate.scale(3/2),
            self.dots.animate.shift(-self.get_a())
        )
        self.play(
            Transform(self.grid_cir, self.grid_big.scale(3)),
            Write(self.grid_coords)
        )
        self.wait()

        #completely rebuild dot updaters
        #dot b gets colour
        self.play(
            Create(self.circle),
            run_time=2
        )



def angle_radius(scene):
    return 0.7 * scene.line_c.get_length() / scene.init_scale