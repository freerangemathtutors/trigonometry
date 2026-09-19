# Started getting good enough at manim, swapped to object oriented!

from manim import *
import math

def setup(scene):
    scene.dots = VGroup(
        Dot([-1.5, -2.0, 0], radius=0.2, color=YELLOW).set_opacity(0),
        Dot([1.5, 2.0, 0], radius=0.2, color=YELLOW).set_opacity(0),
        Dot([1.5, -2.0, 0], radius=0.2, color=YELLOW).set_opacity(0)
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
        scene.label_d = MathTex(r"Opp", color=scene.colours["opp"]).next_to(scene.line_a, RIGHT, buff=0.3).set_opacity(0)
        scene.label_e = MathTex(r"Adj", color=scene.colours["adj"]).next_to(scene.line_b, DOWN, buff=0.3).set_opacity(0)
        scene.label_f = MathTex(r"1", color=scene.colours["hyp"]).next_to(scene.line_c, LEFT, buff=0.1).set_opacity(0)

    scene.label_a.add_updater(lambda mob: mob.next_to(scene.angle_a, RIGHT, buff=0.1))
    scene.label_b.add_updater(lambda mob: mob.next_to(scene.angle_b, DOWN, buff=0.1))
    scene.label_c.add_updater(lambda mob: mob.next_to(scene.angle_c, UP + LEFT, buff=0.1))
    scene.label_d.add_updater(lambda mob: mob.next_to(scene.line_a, RIGHT, buff=0.3))
    scene.label_e.add_updater(lambda mob: mob.next_to(scene.line_b, DOWN, buff=0.3))
    scene.label_f.add_updater(lambda mob: mob.next_to(scene.line_c, LEFT, buff=0.1).shift([0.6, 0, 0]))

class Unitcircle(Scene):
    colours = {
        "hyp": GOLD,
        "opp": TEAL_B,
        "adj": GREEN,
        "tri_out": WHITE,
        "tri_in": BLUE,
        "tri_in_op": 0.3,
        "angle_a": BLUE,
        "angle_b": RED, 
        "angle_c": WHITE,
        "colour_map": {
            "Opp.": TEAL_B, 
            "Adj.": GREEN, 
            "Hyp.": GOLD, 
            "1": GOLD
        }
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
            Tex("1").move_to([3.3, 0.3, 0]),
            Tex("1").move_to([0.3, 3.3, 0]),
            Tex("-1").move_to([-3.3, 0.3, 0]),
            Tex("-1").move_to([0.3, -3.3, 0])
        )
        self.circle = Circle(3).rotate(math.radians(53.13))
        self.o_arm = Line(ORIGIN, 3*RIGHT)
        self.sine_ratio = MathTex(
            r"\sin \theta = \frac{",
            r"\mathrm{Opp.}",
            r"}{",
            r"\mathrm{Hyp.}",
            r"}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([4, 0, 0])
        self.cosine_ratio = MathTex(
            r"\cos \theta = \frac{",
            r"\mathrm{Adj.}",
            r"}{",
            r"\mathrm{Hyp.}",
            r"}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([4, 0, 0])
        self.sine_formula = MathTex(
            r"\sin \theta = \mathrm{Opp.}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        )
        self.cover = Rectangle(BLACK, 10, 10).set_fill(BLACK, 1)
        self.line_cc = DashedLine(dash_length=0.2)
        
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

        self.dots[2].add_updater(lambda dot: perpendicular_dot(dot, self.dots[1], [0, 0, 0]))
        self.angle_a.add_updater(lambda mob: mob.become(
            Angle(
                self.o_arm, self.line_c, 
                radius=angle_radius(self), 
                color=self.colours["angle_a"]
            )
        ))

        self.dots[1].set_color(YELLOW).set_z_index(10)
        self.play(
            self.dots[1].animate.set_opacity(1)
        )

        # Everything now redefined to unit circle
        self.theta = ValueTracker(0)
        self.theta.add_updater(
            lambda mob: mob.set_value(math.atan(
                self.line_c.get_height()/self.line_c.get_width()
            ))
        )
        self.add(self.theta)

        self.play(
            Create(self.circle),
            MoveAlongPath(self.dots[1], self.circle),
            run_time=2,
            rate_func=smooth
        )
        self.play(
            Rotate(self.dots[1], math.radians(-53), OUT, [0, 0, 0])
        )
        self.label_f.set_opacity(1)
        self.add(self.label_f)
        self.play(
            self.line_c.animate.set_color(GOLD), 
            Write(self.label_f)
        )
        self.play(
            Rotate(self.dots[1], math.radians(53), OUT, [0, 0, 0])
        )

        self.cover.move_to([10, 0, 0])
        self.play(
            self.circle.animate.shift([-3, 0, 0]),
            self.grid_coords.animate.shift([-3, 0, 0]),
            self.dots.animate.shift([-3, 0, 0]), # Note that updater does not break because it is based on the centre's y position which is not changed
            self.grid_cir.animate.shift([-3, 0, 0]),
            self.cover.animate.move_to([6, 0, 0])
        )
        self.wait()
        self.label_d.set_opacity(1)
        self.label_e.set_opacity(1)
        self.add(self.label_d, self.label_e, self.label_f)
        self.update_mobjects(0)
        self.play(
            Write(self.label_d),
            Write(self.label_e),
            Write(self.label_a)
        )
        self.play(Write(self.sine_ratio))
        self.wait()
        self.play(
            Transform(
                self.sine_ratio[3],
                MathTex(
                    r"1",
                    color=self.colours["hyp"],
                    font_size=50
                ).move_to(self.sine_ratio[3])
            )
        )
        self.wait()
        self.sine_formula.move_to(self.sine_ratio)
        print(self.sine_ratio.submobjects)
        new_left = MathTex(
            r"\sin \theta =",
            font_size=50
        ).move_to(self.sine_ratio[0])

        new_opp = MathTex(
            r"\mathrm{Opp.}",
            color=self.colours["opp"],
            font_size=50
        ).move_to([self.sine_ratio[1].get_center()[0], 0, 0])

        self.play(
            Unwrite(self.sine_ratio[2]),
            Unwrite(self.sine_ratio[3]),
            Unwrite(self.sine_ratio[4]),
            Transform(self.sine_ratio[1], new_opp)
        )
        self.wait()
        self.play(Transform(
            self.label_d,
            MathTex(r"\sin \theta", color=self.colours["opp"])
            .next_to(self.line_a, RIGHT, buff=0.3)
        ))
        self.play(Indicate(self.label_d))
        self.wait()

        self.play(
            Unwrite(self.sine_ratio[0]),
            Unwrite(self.sine_ratio[1]),
            Unwrite(new_opp)
        )

        new_adj = MathTex(
            r"\mathrm{Adj.}",
            color=self.colours["adj"],
            font_size=50
        ).move_to([self.cosine_ratio[1].get_center()[0], 0, 0])
        self.play(Write(self.cosine_ratio))
        self.wait()
        self.play(
            Transform(
                self.cosine_ratio[3],
                MathTex(
                    r"1",
                    color=self.colours["hyp"],
                    font_size=50
                ).move_to(self.sine_ratio[3])
            )
        )
        self.play(
            Unwrite(self.cosine_ratio[2]),
            Unwrite(self.cosine_ratio[3]),
            Unwrite(self.cosine_ratio[4])
        )
        self.play(Transform(self.cosine_ratio[1], new_adj))
        self.play(Transform(
            self.label_e,
            MathTex(r"\cos \theta", color=self.colours["adj"])
            .next_to(self.line_b, DOWN, buff=0.3)
        ))
        self.play(Indicate(self.label_e))
        self.wait()

        self.play(
            Unwrite(self.cosine_ratio),
            Unwrite(new_adj)
        )

        with register_font("Teachers-Medium.ttf"):
            Text.set_default(font="Teachers")
            question = Text(
                "What is a\ntangent line?",
                t2c = {"tan": PURPLE}
            ).move_to([4, 0, 0])

        self.play(Write(question))
        self.wait()
        self.tangent_segment = Line([-10, 0, 0], [10, 0, 0])
        self.dot_d = Dot(self.dots[1].get_center() * [1, -1, 1], radius=0.2, color=YELLOW)
        self.arc_segment = Arc(3, -math.radians(53), -PI/2, arc_center=[-3, 0, 0]).set_z_index(-1)
        self.tangent_segment.add_updater(
            lambda mob: tangent_line(mob, self.dot_d, [-3, 0, 0], 20)
        )

        self.play(
            Create(self.tangent_segment),
            FadeIn(self.dot_d)
        )
        self.play(FocusOn(self.dot_d))
        self.play(
            MoveAlongPath(self.dot_d, self.arc_segment), 
            rate_func=there_and_back,
            run_time=2
        )
        self.wait()
        self.arc_segment.become(Arc(3, -math.radians(53), math.radians(53), arc_center=[-3, 0, 0]).set_z_index(-1))
        self.play(
            MoveAlongPath(self.dot_d, self.arc_segment),
            run_time=2
        )
        self.tangent_segment.clear_updaters()
        self.play(
            Indicate(self.tangent_segment), 
            self.dot_d.animate.set_opacity(0)
        )
        self.dot_d.add_updater(
            lambda dot: tan_dot(dot, self.dots[1], self.theta.get_value())
        )
        self.line_cc.add_updater(
            lambda line: hyp_ext(line, self.dot_d, [-3, 0, 0])
        )
        self.dots[1].add_updater(
            lambda dot: theta_dot(dot, [-3, 0, 0], self.theta.get_value(), 3)
        )
        self.play(
            Create(self.line_cc),
            Unwrite(question),
            self.tangent_segment.animate.put_start_and_end_on([0, 0, 0], self.dot_d.get_center()),
            run_time=2
        )
        print("DOT d: ", self.dot_d.get_center())


def theta_dot(dot, origin, angle, radius):
    dot.move_to([
        origin[0] + radius * math.cos(angle),
        origin[1] + radius * math.sin(angle),
        0
    ])


def perpendicular_dot(dot, target, centre=[0, 0, 0]):
    target_pos = target.get_center()
    sine = -float(target_pos[1] - centre[1])
    dot.move_to(
        [target_pos[0], target_pos[1]+sine, target_pos[2]]
    )

def tan_dot(dot, target, angle, centre=[0, 0, 0], radius=1, maxi=10):
    target_pos = target.get_center()
    tan = min(
        radius * math.tan(angle),
        maxi
    )
    dot.move_to(
        [target_pos[0], target_pos[1]+tan, target_pos[2]]
    )

def hyp_ext(line, dot, centre=[0, 0, 0]):
    dot_pos = dot.get_center()
    dx = dot_pos[0]-centre[0]
    dy = dot_pos[1]-centre[1]
    ext = np.array([dx, dy, 0])
    t = (1 - centre[0]) / dx
    intersection = np.array(centre) + t * ext
    dir = intersection - dot_pos
    d = np.linalg.norm(dir)
    dir /= d
    end = dot_pos + dir * min(d, 10)
    line.put_start_and_end_on(dot_pos, end)

def tangent_line(line, dot, centre=[0, 0, 0], len=20):
    dot_pos = dot.get_center()
    dx = dot_pos[0]-centre[0]
    dy = dot_pos[1]-centre[1]
    tangent = np.array([-dy, dx, 0])
    tangent = tangent / np.linalg.norm(tangent) # Unit vectorssss MCV unit 7 !!
    line.put_start_and_end_on(
        dot_pos - tangent * len / 2,
        dot_pos + tangent * len / 2
    )

def angle_radius(scene):
    return 0.7 * scene.line_c.get_length() / scene.init_scale