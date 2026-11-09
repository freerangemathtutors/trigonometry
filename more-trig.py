# Started getting good enough at manim, swapped to object oriented!

import sys
from manim import *
import math

# sys.setrecursionlimit(30000) 

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

    scene.big_tri.add_updater(lambda mob: update_triangle(scene, mob))

    scene.angle_a = Angle(scene.line_b, scene.line_c, radius=0.7, color=scene.colours["angle_a"])
    scene.angle_b = Angle(Line(scene.get_b(), scene.get_a()), scene.line_a, radius=0.7, color=scene.colours["angle_b"]).set_opacity(0)

    scene.angle_c = RightAngle(scene.line_a, scene.line_b, length=0.4, quadrant=[-1, 1], color=scene.colours["angle_c"])

    scene.angle_a.add_updater(lambda mob: 
        nice_angle(scene, mob, "a", scene.line_b, scene.line_c)
    )
    scene.angle_b.add_updater(lambda mob:
        nice_angle(scene, mob, "b", Line(scene.get_b(), scene.get_a()), scene.line_a)    
    )
    scene.angle_c.add_updater(lambda mob: mob.become(
        RightAngle(scene.line_a, scene.line_b, length=0.4, quadrant=[-1, 1], color=scene.colours["angle_c"])
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
    scene.label_f.add_updater(lambda mob: normal_pos(mob, scene.line_c, 0.3)) # mob.next_to(scene.line_c, LEFT, buff=0.1).shift([0.6, 0, 0])

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
            [-6, 6, 1],
            [-6, 6, 1],
            12, 12, faded_line_ratio=2
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
        self.angle_c.clear_updaters()
        self.angle_c.add_updater(
            lambda mob: right_angle(
                mob,
                self.get_c(),
                self.line_a,
                self.line_b,
                length=angle_radius(self) * (4/7),
                quadrant=(1, 1)
            )
        )
        self.cover = Rectangle(BLACK, 10, 10).set_fill(BLACK, 1).set_opacity(0.5)
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
        print(self.theta.get_value())

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
                ).move_to(self.sine_ratio[3]).shift([0, -0.1, 0])
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
            # self.dot_d.animate.set_opacity(0)
            self.dot_d.animate.shift([0, 3*math.tan(self.theta.get_value()), 0])
        )

        # Redefine everything to theta
        for mob in self.mobjects:
            mob.clear_updaters()
        print("Theta is", self.theta.get_value())
        print("Radius is", self.circle.radius)
        
        self.dots[1].add_updater(lambda dot: 
            theta_dot(dot, [-3, 0, 0], self.theta.get_value(), 3)
        )
        self.dots[2].add_updater(lambda dot: 
            perpendicular_dot(dot, self.dots[1], [0, 0, 0])
        )
        # self.dot_d.add_updater(
        #     lambda dot: tan_dot(dot, self.dots[1], self.theta.get_value(), [-3, 0, 0], 3)
        # )

        self.line_a.add_updater(lambda mob: mob.put_start_and_end_on(self.get_b(), self.get_c()))
        self.line_b.add_updater(lambda mob: mob.put_start_and_end_on(self.get_a(), self.get_c()))
        self.line_c.add_updater(lambda mob: mob.put_start_and_end_on(self.get_a(), self.get_b()))
        self.line_cc.add_updater(
            lambda line: hyp_ext(line, self.dots[1], self.theta.get_value(), [-3, 0, 0])
        )

        self.angle_a.add_updater(lambda mob: 
            nice_angle(self, mob, "a", self.line_b, self.line_c)
        )
        self.angle_b.add_updater(lambda mob:
            nice_angle(self, mob, "b", Line(self.get_b(), self.get_a()), self.line_a)    
        )
        self.angle_c.clear_updaters()
        self.angle_c.add_updater(
            lambda mob: right_angle(
                mob,
                self.get_c(),
                self.line_a,
                self.line_b,
                length=angle_radius(self) * (4/7),
                quadrant=(1, 1)
            )
        )
        # self.angle_c.add_updater(lambda mob: right_angle(self, mob, "c", Line(self.get_c(), self.get_b()), Line(self.get_c(), self.get_a())))

        self.label_a.add_updater(lambda mob: mob.next_to(self.angle_a, RIGHT, buff=0.1))
        self.label_b.add_updater(lambda mob: mob.next_to(self.angle_b, DOWN, buff=0.1))
        self.label_c.add_updater(lambda mob: mob.next_to(self.angle_c, UP + LEFT, buff=0.1))
        self.label_d.add_updater(lambda mob: mob.next_to(self.line_a, RIGHT, buff=0.3))
        self.label_e.add_updater(lambda mob: mob.next_to(self.line_b, DOWN, buff=0.3))
        self.label_f.add_updater(lambda mob: normal_pos(mob, self.line_c, 0.3))
        self.dot_d.set_z_index(10)

        self.play(
            Create(self.line_cc),
            Unwrite(question),
            self.tangent_segment.animate.put_start_and_end_on([0, 0, 0], self.dot_d.get_center()),
            run_time=2
        )

        self.tangent_segment.add_updater(
            lambda mob: mob.put_start_and_end_on([0, 0, 0], self.dot_d.get_center())
        )

        print("DOT d 2: ", self.dot_d.get_center())
        self.wait(2)
        self.play(
            FadeOut(self.dot_d)
        )


class Tangent(Scene):
    colours = {
        "hyp": GOLD,
        "opp": TEAL_B,
        "adj": GREEN,
        "tan": PURPLE,
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
        self.theta = ValueTracker(
            math.atan(self.line_c.get_height()/self.line_c.get_width())
        )
        self.dots.scale(3/self.line_c.get_length())
        self.grid = NumberPlane(
            [-6, 6, 1],
            [-6, 6, 1],
            36, 36, faded_line_ratio=2
        ).shift([-3, 0, 0])
        self.grid_cir = NumberPlane(
            [-1.5, 1.5, 1], 
            [-1.5, 1.5, 1],
            4.5, 4.5, faded_line_ratio=2
        ).move_to([-3, 0, 0]).set_z_index(-1)
        self.grid_coords = VGroup(
            Tex("1").move_to([3.3, 0.3, 0]),
            Tex("1").move_to([0.3, 3.3, 0]),
            Tex("-1").move_to([-3.3, 0.3, 0]),
            Tex("-1").move_to([0.3, -3.3, 0])
        ).shift([-3, 0, 0])
        self.circle = Circle(3).move_to([-3, 0, 0])
        self.o_arm = Line(ORIGIN, 3*RIGHT)
        self.cover = Rectangle(BLACK, 10, 10).set_fill(BLACK, 1).move_to([6, 0, 0]).set_opacity(0.5)
        self.line_cc = DashedLine(dash_length=0.2)
        self.dot_d = Dot([0, 3*math.tan(self.theta.get_value()), 0])
        self.tangent_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["tan"], stroke_width=10)

        self.dots[0].move_to([-3, 0, 0])
        print("Theta is", self.theta.get_value(), math.degrees(self.theta.get_value()), "degrees")
        print("Radius is", self.circle.radius)
        self.angle_a.clear_updaters()
        self.angle_a.add_updater(lambda mob: mob.become(
            Angle(
                self.o_arm, self.line_c, 
                radius=angle_radius(self), 
                color=self.colours["angle_a"]
            )
        ))
        self.angle_c.clear_updaters()
        self.angle_c.add_updater(
            lambda mob: right_angle(
                mob,
                self.get_c(),
                self.line_a,
                self.line_b,
                length=angle_radius(self) * (4/7),
                quadrant=(1, 1)
            )
        )
        
        self.dots[1].add_updater(lambda dot: 
            theta_dot(dot, [-3, 0, 0], self.theta.get_value(), 3)
        )
        self.dots[2].add_updater(lambda dot: 
            perpendicular_dot(dot, self.dots[1], [-3, 0, 0])
        )
        self.dot_d.add_updater(
            lambda dot: tan_dot(dot, self.dots[1], self.theta.get_value(), [-3, 0, 0], 3)
        )
        self.dot_d.set_z_index(10)
        self.line_cc.add_updater(
            lambda line: hyp_ext(line, self.dots[1], self.theta.get_value(), [-3, 0, 0])
        )
        self.tangent_segment.add_updater(
            lambda mob: mob.put_start_and_end_on([0, 0, 0], self.dot_d.get_center())
        )
        
        self.add(
            self.dots, 
            self.dot_d,
            self.big_tri, 
            self.line_a, 
            self.line_b, 
            self.line_c,
            self.line_cc,
            self.angle_a, 
            self.angle_c,
            self.label_f,
            self.grid,
            self.grid_coords,
            self.cover,
            self.circle,
            self.tangent_segment
        )
        self.label_f.set_opacity(1)
        self.dots[1].set_opacity(1).set_z_index(10)
        self.line_c.set_color(GOLD)
        print(self.init_scale)

        self.update_mobjects(0)
        self.wait()
        self.play(
            self.theta.animate.set_value(PI/4)
        )
        self.wait()

        self.play(self.theta.animate.set_value(2.2*PI), run_time=2)
        self.wait()

        self.smol_tri = Polygon(
            self.get_a(), self.get_b(), self.get_c(), 
            color=GOLD, stroke_width=7
        )
        self.tan_tri = Polygon(
            self.get_a(), self.dot_d.get_center(), [0, 0, 0], 
            color=PURPLE, stroke_width=7
        )
        self.tan_formula = MathTex(
            r"\frac{",
            r"\mathrm{Opp.}",
            r"}{",
            r"\mathrm{Adj.}",
            r"}",
            r"=",
            r"\frac{",
            r"\mathrm{????}",
            r"}{",
            r"1",
            r"}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([3.5, 1.5, 0])
        self.tan_formula[9].set_color(self.colours["adj"])

        self.play(FadeIn(self.smol_tri))
        self.play(Indicate(self.smol_tri))
        self.play(self.smol_tri.animate.move_to([2, -1, 0]))
        self.play(FadeIn(self.tan_tri))
        self.play(Indicate(self.tan_tri))
        self.play(self.tan_tri.animate.move_to([5, -1+0.208, 0]))

        self.angle_a_smol = self.angle_a.copy().shift(
            self.smol_tri.get_center()-self.big_tri.get_center()
        ).clear_updaters()
        self.angle_a_tan = self.angle_a.copy().shift(
            self.tan_tri.get_center()-self.big_tri.get_center()
        ).clear_updaters()
        self.angle_c_smol = self.angle_c.copy().shift(
            self.smol_tri.get_center()-self.big_tri.get_center()
        ).clear_updaters()
        self.angle_c_tan = self.angle_c.copy().shift(
            self.tan_tri.get_center()-self.big_tri.get_center()
        ).clear_updaters()
        self.tan_tri_angles = Group(self.angle_a_tan, self.angle_c_tan)
        self.tan_tri_angles.scale(1/math.cos(self.theta.get_value())).shift([0, -0.208, 0])

        self.label_theta_a = self.label_a.copy().next_to(self.angle_a_smol, RIGHT, buff=0.1).clear_updaters()
        self.label_theta_b = self.label_a.copy().next_to(self.angle_a_tan, RIGHT, buff=0.1).clear_updaters()
        self.label_adj_a = MathTex(r"Adj.", color=self.colours["adj"], font_size=40).next_to(self.smol_tri, DOWN, buff=0.2)
        self.label_adj_b = MathTex(r"1", color=self.colours["adj"], font_size=40).next_to(self.tan_tri, DOWN, buff=0.2)
        self.label_opp_a = MathTex(r"Opp.", color=self.colours["opp"], font_size=40).next_to(self.smol_tri, RIGHT, buff=0.1).shift([-1.1, -0.2, 0])
        self.label_opp_b = MathTex(r"\tan \theta", color=self.colours["opp"], font_size=40).next_to(self.tan_tri, RIGHT, buff=0.1).shift([-1.2, -0.2, 0])

        self.play(
            Create(self.angle_a_smol),
            Create(self.angle_a_tan),
            Create(self.angle_c_smol),
            Create(self.angle_c_tan),
            Write(self.label_a),
            Write(self.label_theta_a),
            Write(self.label_theta_b)
        )
        self.play(
            Indicate(self.angle_a_smol),
            Indicate(self.angle_a_tan),
            Indicate(self.angle_c_smol),
            Indicate(self.angle_c_tan)
        )
        self.wait()

        self.play(
            Write(self.label_adj_a),
            Write(self.label_adj_b),
            Write(self.label_opp_a)
        )

        self.play(
            Write(self.tan_formula)
        )
        self.play(
            Transform(self.tan_formula[7], MathTex(r"\tan \theta", color=PURPLE).move_to(self.tan_formula[7]))
        )
        self.wait()
        self.play(
            Write(self.label_opp_b)
        )

        self.sin_label = MathTex(r"\sin \theta", color=self.colours["opp"]).rotate(PI/2)
        self.sin_label.add_updater(
            lambda mob: mob.next_to(self.line_a, LEFT, buff=0.3)
        )
        self.cos_label = MathTex(r"\cos \theta", color=self.colours["adj"])
        self.cos_label.add_updater(
            lambda mob: mob.next_to(self.line_b, DOWN, buff=0.3)
        )
        self.tan_label = MathTex(r"\tan \theta", color=self.colours["tan"]).rotate(PI/2)
        self.tan_label.add_updater(
            lambda mob: mob.next_to(self.tangent_segment, RIGHT, buff=0.3)
        )

        self.play(Write(self.tan_label))
        self.play(Indicate(self.tan_label))
        self.wait()

        self.play(
            Unwrite(self.tan_formula),
            Uncreate(self.smol_tri),
            Uncreate(self.tan_tri),
            Uncreate(self.angle_a_smol),
            Uncreate(self.angle_c_smol),
            Uncreate(self.angle_a_tan),
            Uncreate(self.angle_c_tan),
            Unwrite(self.label_opp_a),
            Unwrite(self.label_opp_b),
            Unwrite(self.label_adj_a),
            Unwrite(self.label_adj_b),
            Unwrite(self.label_theta_a),
            Unwrite(self.label_theta_b)
        )
        self.wait()

        self.play(
            self.line_a.animate.set_color(self.colours["opp"]).set_stroke_width(10).set_z_index(1),
            self.line_b.animate.set_color(self.colours["adj"]).set_stroke_width(10).set_z_index(1),
            self.line_c.animate.set_z_index(1),
            Write(self.sin_label),
            Write(self.cos_label)
        )

        self.play(self.theta.animate.set_value(6.2*PI), run_time=8, rate_func=smoothstep)
        self.wait()

        self.sin_label.clear_updaters()
        self.cos_label.clear_updaters()
        self.tan_label.clear_updaters()
        for dot in self.dots:
            dot.clear_updaters()
        self.dot_d.clear_updaters()
        self.tangent_segment.clear_updaters()
        self.line_cc.clear_updaters()
        self.label_c.clear_updaters()
        self.label_a.clear_updaters()

        toutlemonde = Group(
            self.line_cc,
            self.angle_a,
            self.angle_c,
            self.circle,
            self.tangent_segment,
            self.dots,
            self.dot_d,
            self.sin_label,
            self.cos_label,
            self.tan_label,
            self.label_a,
        ).set_z_index(10)
        self.line_a.set_z_index(5)
        self.line_b.set_z_index(5)

        self.play(
            Unwrite(self.label_f),
            Unwrite(self.sin_label),
            Unwrite(self.cos_label),
            Unwrite(self.tan_label),
            self.line_a.animate.set_stroke_width(5),
            self.line_b.animate.set_stroke_width(5),
            self.tangent_segment.animate.set_stroke_width(5),
        )

        self.play(
            Transform(self.grid, self.grid_cir.set_z_index(-10)),
            toutlemonde.animate.scale(0.5, about_point=[-3, 0, 0]),
            ScaleInPlace(self.grid_coords, 0.5)
        )
        self.play(
            self.grid.animate.shift([-1, 0, 0]),
            toutlemonde.animate.shift([-1, 0, 0]),
            self.grid_coords.animate.shift([-1, 0, 0])
        )
        self.wait()

        # self.play(
        #     Transform(
        #         self.tan_tri,
        #         Polygon(
        #             self.get_a(), self.dot_d.get_center(), [0, 0, 0], 
        #             color=self.colours["tri_out"], stroke_width=4
        #         )
        #     ),
        #     run_time=2
        # )


class Graphing(Scene):
    colours = {
        "hyp": GOLD,
        "opp": TEAL_B,
        "adj": GREEN,
        "tan": PURPLE,
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
        self.theta = ValueTracker(
            math.atan(self.line_c.get_height()/self.line_c.get_width())
        )
        self.dots.scale(3/self.line_c.get_length())
        self.grid_cir = NumberPlane(
            [-1.5, 1.5, 1], 
            [-1.5, 1.5, 1],
            4.5, 4.5, faded_line_ratio=2
        ).move_to([-4, 0, 0])
        self.grid = NumberPlane(
            [-6, 6, 1],
            [-6, 6, 1],
            36, 36, faded_line_ratio=2
        )
        self.axises = Axes(
            [0, 10, PI/2], [-1, 1, 1], 
            7.5, 3
        ).shift([3, 0, 0])
        self.axis_coords = VGroup()
        for i in range(1, 7):
            label = MathTex(str(i*90), r"^\circ").move_to(self.axises.coords_to_point(i * PI/2, -0.2)).scale(0.5)
            self.axis_coords.add(label)
        self.grid_coords = VGroup(
            Tex("1").move_to([3.3, 0.3, 0]),
            Tex("1").move_to([0.3, 3.3, 0]),
            Tex("-1").move_to([-3.3, 0.3, 0]),
            Tex("-1").move_to([0.3, -3.3, 0])
        ).shift([-4, 0, 0]).scale(0.5)
        self.circle = Circle(1.5).move_to([-4, 0, 0])
        self.o_arm = Line(ORIGIN, 3*RIGHT)
        self.line_cc = DashedLine(dash_length=0.2)
        self.dot_d = Dot([0, 3*math.tan(self.theta.get_value()), 0])
        self.tangent_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["tan"], stroke_width=5)
        self.func_display = MathTex(r"\sin \theta", color=self.colours["opp"]).move_to(self.axises.get_center()+[0, 3, 0])
        self.deg_display = MathTex(r"\theta =", str(round(math.degrees(self.theta.get_value()))), r"^\circ", color=BLUE)

        self.deg_display.add_updater(
            lambda mob: mob.become(
                MathTex(r"\theta =", str(round(math.degrees(self.theta.get_value()))), r"^\circ", color=BLUE)
            ).move_to([-4, 3, 0])
        )
        self.sin_label = MathTex(r"\sin \theta", color=self.colours["opp"]).rotate(PI/2)
        self.sin_label.add_updater(
            lambda mob: mob.next_to(self.line_a, LEFT, buff=0.3)
        )
        self.cos_label = MathTex(r"\cos \theta", color=self.colours["adj"])
        self.cos_label.add_updater(
            lambda mob: mob.next_to(self.line_b, DOWN, buff=0.3)
        )
        self.tan_label = MathTex(r"\tan \theta", color=self.colours["tan"]).rotate(PI/2)
        self.tan_label.add_updater(
            lambda mob: mob.next_to(self.tangent_segment, RIGHT, buff=0.3)
        )

        self.dots[0].move_to([-4, 0, 0])
        print("Theta is", self.theta.get_value(), math.degrees(self.theta.get_value()), "degrees")
        print("Radius is", self.circle.radius)
        self.angle_a.clear_updaters()
        self.angle_a.add_updater(lambda mob: mob.become(
            Angle(
                self.o_arm, self.line_c, 
                radius=angle_radius(self), 
                color=self.colours["angle_a"]
            )
        ))
        self.angle_c.clear_updaters()
        self.angle_c.add_updater(
            lambda mob: right_angle(
                mob,
                self.get_c(),
                self.line_a,
                self.line_b,
                length=angle_radius(self) * (4/7),
                quadrant=(1, 1)
            )
        )
        
        self.dots[1].add_updater(lambda dot: 
            theta_dot(dot, [-4, 0, 0], self.theta.get_value(), 1.5)
        ).scale(0.5)
        self.dots[2].add_updater(lambda dot: 
            perpendicular_dot(dot, self.dots[1], [-4, 0, 0])
        )
        self.dot_d.add_updater(
            lambda dot: tan_dot(dot, self.dots[1], self.theta.get_value(), [-4, 0, 0], 1.5)
        )
        self.dot_d.set_z_index(10).scale(0.5)
        self.line_cc.add_updater(
            lambda line: hyp_ext(line, self.dots[1], self.theta.get_value(), [-4, 0, 0], dashness=0.1)
        )
        self.tangent_segment.add_updater(
            lambda mob: mob.put_start_and_end_on([-2.5, 0, 0], self.dot_d.get_center())
        )
        
        self.add(
            self.dots, 
            self.dot_d,
            self.big_tri, 
            self.line_a, 
            self.line_b, 
            self.line_c,
            self.line_cc,
            self.angle_a, 
            self.angle_c,
            self.label_a,
            self.grid_cir,
            self.grid_coords,
            self.circle,
            self.tangent_segment,
        )
        self.label_a.scale(0.5)
        self.dots[1].set_opacity(1).set_z_index(10)
        self.line_a.set_z_index(2)
        self.line_b.set_z_index(2)
        self.line_c.set_color(GOLD)
        self.line_a.set_color(self.colours["opp"]).set_stroke_width(5),
        self.line_b.set_color(self.colours["adj"]).set_stroke_width(5),
        self.theta.set_value(0.2*PI)

        self.update_mobjects(0)
        self.wait()

        self.play(
            Create(self.axises),
            Write(self.axis_coords)
        )
        self.line_cc.clear_updaters()
        self.play(
            Write(self.deg_display),
            self.dot_d.animate.set_opacity(0),
            self.tangent_segment.animate.set_opacity(0),
            self.line_cc.animate.set_opacity(0)
        )
        self.play(
            self.line_a.animate.set_stroke_width(10)
        )
        self.play(Indicate(self.line_a))
        self.wait()

        self.play(
            self.theta.animate.set_value(0.0001)
        )

        start = self.axises.coords_to_point(0, 0)
        self.end = Dot(start, 0.1)
        self.connector = Line(self.dots[1].get_center(), start)
        self.connector.add_updater(
            lambda mob: mob.put_start_and_end_on(self.dots[1].get_center(), self.end.get_center())
        )
        self.end.add_updater(
            lambda mob: mob.move_to(self.axises.coords_to_point(
                self.theta.get_value(), math.sin(self.theta.get_value())
            ))
        )
        
        self.sine = self.axises.plot(lambda x: math.sin(x), color=self.colours["opp"], x_range=[0, 10])
        self.cosine = self.axises.plot(lambda x: math.cos(x), color=self.colours["adj"], x_range=[0, 10])

        self.play(
            Create(self.end),
            Create(self.connector),
            Write(self.func_display)
        )

        self.play(
            self.theta.animate.set_value(10),
            Create(self.sine),
            run_time=12
        )
        self.wait()
        self.play(
            self.theta.animate.set_value(0.0001),
            Uncreate(self.sine),
            run_time=5
        )

        self.end.clear_updaters()
        self.play(
            self.connector.animate.set_opacity(0),
            self.end.animate.move_to(self.axises.coords_to_point(0, 1))
        )
        self.play(
            self.line_b.animate.set_stroke_width(10),
            self.line_a.animate.set_stroke_width(5),
            Transform(
                self.func_display, 
                MathTex(r"\cos \theta", color=self.colours["adj"]).move_to(self.axises.get_center()+[0, 3, 0])
            )
        )
        self.play(Indicate(self.line_b))
        self.wait()
        self.end.add_updater(
            lambda mob: mob.move_to(self.axises.coords_to_point(
                self.theta.get_value(), math.cos(self.theta.get_value())
            ))
        )
        self.play(
            self.theta.animate.set_value(10),
            Create(self.cosine),
            run_time=12
        )
        self.wait()
        self.play(
            self.theta.animate.set_value(0.0001),
            Uncreate(self.cosine),
            run_time=5
        )
        self.wait()

        # Thanks Adenosie for the inspo!
        self.tangent = VGroup(color=self.colours["tan"])
        self.tangent.set_points_as_corners(
            (self.axises.coords_to_point(0, 0), self.axises.coords_to_point(-0.0001, 0))
        )
        def update_tangent(func):
            next_point = self.axises.coords_to_point([
                self.theta.get_value(),
                np.tan(self.theta.get_value())
            ])
            if next_point[1] < func.get_last_point()[1]:
                func.start_new_path(next_point)
            else:
                func.add_line_to(next_point)
        self.va = VGroup(
            DashedLine(self.axises.coords_to_point((n+0.5)*PI, 10), self.axises.coords_to_point((n+0.5)*PI, -10))
            for n in range(3)
        )

        self.end.clear_updaters()
        self.play(
            self.dot_d.animate.set_opacity(1),
            self.tangent_segment.animate.set_opacity(1).set_stroke_width(10),
            self.line_b.animate.set_stroke_width(5),
            self.line_b.animate.set_stroke_width(5),
            self.end.animate.move_to(self.axises.coords_to_point(0, 0)),
            Transform(
                self.func_display, 
                MathTex(r"\tan \theta", color=self.colours["tan"]).move_to(self.axises.get_center()+[0, 3, 0])
            )
        )
        self.line_cc.add_updater(
            lambda line: hyp_ext(line, self.dots[1], self.theta.get_value(), [-4, 0, 0], dashness=0.1)
        )
        self.connector.clear_updaters()
        self.connector.add_updater(
            lambda mob: mob.put_start_and_end_on(self.dot_d.get_center(), self.end.get_center())
        )
        self.play(self.line_cc.animate.set_opacity(1))
        self.play(self.theta.animate.set_value(PI/4))
        self.play(Indicate(self.tangent_segment))
        self.play(self.theta.animate.set_value(0.0001))
        self.wait()
        self.play(self.connector.animate.set_opacity(1))
        self.end.add_updater(
            lambda mob: mob.move_to([
                self.axises.coords_to_point(self.theta.get_value())[0], 
                self.dot_d.get_center()[1], 0
        ]))
        self.tangent.add_updater(lambda mob: update_tangent(mob))
        self.add(self.tangent)
        self.play(
            self.theta.animate.set_value(10),
            run_time=12
        )
        self.tangent.clear_updaters()
        self.wait()
        self.play(
            FadeOut(self.tangent),
            self.theta.animate.set_value(0.0001),
            run_time=2
        )
        self.tangent.reset_points()
        self.tangent.set_points_as_corners(
            (self.axises.coords_to_point(0, 0), self.axises.coords_to_point(-0.0001, 0))
        )
        self.tangent.add_updater(lambda mob: update_tangent(mob))
        self.add(self.tangent)
        self.play(
            self.theta.animate.set_value(PI/2-0.0001),
            run_time=2
        )
        self.wait()
        self.line_cc.suspend_updating()
        self.play(
            Indicate(self.line_cc),
            Indicate(self.tangent_segment),
            run_time=2
        )
        self.line_cc.resume_updating()
        self.wait()
        self.play(
            self.theta.animate.set_value(PI-0.0001),
            run_time=2
        )
        self.wait()
        self.play(
            self.theta.animate.set_value(10),
            Create(self.va),
            run_time=4
        )
        self.play(
            Indicate(self.va[0]),
            Indicate(self.va[1]),
            Indicate(self.va[2])
        )
        self.wait()

        self.play(
            Uncreate(self.tangent),
            Uncreate(self.axises),
            Uncreate(self.connector),
            Uncreate(self.end),
            Unwrite(self.axis_coords),
            Uncreate(self.deg_display),
            Uncreate(self.func_display),
            Uncreate(self.va)
        )
        self.play(
            self.theta.animate.set_value(PI*1/5),
            run_time=3
        )
        self.line_cc.clear_updaters()
        self.dot_d.clear_updaters()
        self.tangent_segment.clear_updaters()
        self.dots[1].clear_updaters()
        self.dots[2].clear_updaters()
        self.wait()

        self.play(
            self.dots.animate.shift([4, 0, 0]),
            self.grid_cir.animate.shift([4, 0, 0]),
            self.circle.animate.shift([4, 0, 0]),
            self.grid_coords.animate.shift([4, 0, 0]),
            self.dot_d.animate.shift([4, 0, 0]),
            self.line_cc.animate.shift([4, 0, 0]),
            self.tangent_segment.animate.shift([4, 0, 0])
        )
        toutlemonde = Group(
            self.line_cc,
            self.angle_a,
            self.angle_c,
            self.circle,
            self.tangent_segment,
            self.dots,
            self.dot_d,
            self.label_a,
        ).set_z_index(10)
        self.line_a.set_z_index(5)
        self.line_b.set_z_index(5)
        self.play(
            Transform(self.grid_cir, self.grid.set_z_index(-10)),
            toutlemonde.animate.scale(2, about_point=[0, 0, 0]),
            ScaleInPlace(self.grid_coords, 2)
        )
        self.play(
            Write(self.sin_label),
            Write(self.cos_label),
            Write(self.tan_label),
            Write(self.label_f),
            self.line_a.animate.set_stroke_width(10),
            self.line_b.animate.set_stroke_width(10),
            self.tangent_segment.animate.set_stroke_width(10)
        )
        self.wait()

        self.line_b.clear_updaters()
        self.tan_label.clear_updaters()
        self.cos_label.clear_updaters()
        self.big_tri.clear_updaters()
        temp_d_spot = [1/math.cos(self.theta.get_value())*3, 0, 0]
        self.play(
            self.big_tri.animate.set_points_as_corners((
                [0, 0, 0], 
                [0, 3/math.sin(self.theta.get_value()), 0],
                [3/math.cos(self.theta.get_value()), 0, 0],
                [0, 0, 0]
            )).set_stroke(width=0),
            self.tan_label.animate.rotate(-PI/2).move_to([3.9879, 1.1462, 0]),
            self.cos_label.animate.move_to([1.2135, 2.2417, 0]),
            FadeOut(self.line_cc),
            Uncreate(self.angle_c),
            self.dot_d.animate.move_to(temp_d_spot),
            self.tangent_segment.animate.put_start_and_end_on(temp_d_spot, self.dots[1].get_center()),
            self.line_b.animate.put_start_and_end_on([0, math.sin(self.theta.get_value())*3, 0], self.dots[1].get_center()),
            run_time=3
        )
        self.dots[1].add_updater(lambda dot: 
            theta_dot(dot, [0, 0, 0], self.theta.get_value(), 3)
        )
        self.dots[2].add_updater(lambda dot: 
            perpendicular_dot(dot, self.dots[1], [0, 0, 0])
        )
        self.big_tri.add_updater(lambda mob: mob.set_points_as_corners((
            [0, 0, 0], 
            [0, 3/math.sin(self.theta.get_value()), 0],
            [3/math.cos(self.theta.get_value()), 0, 0],
            [0, 0, 0]
        )))
        self.dot_d.add_updater(lambda mob: tan_dot(
            mob, self.dots[1], self.theta.get_value(), radius=3, axis="x"
        ))
        self.tan_label.add_updater(lambda mob: mob.move_to(self.tangent_segment.get_center()).shift(
            mob.get_center() * 0.3
        ))
        self.cos_label.add_updater(lambda mob: mob.next_to(self.line_b, UP, buff=0.3))
        self.tangent_segment.add_updater(lambda mob: tan_ext(mob, self.dots[1], self.theta.get_value()))
        self.line_b.add_updater(lambda mob: mob.put_start_and_end_on(
            [0, math.sin(self.theta.get_value())*3, 0], 
            self.dots[1].get_center()
        ))
        self.wait()
        print(self.tan_label.get_center())
        print(self.cos_label.get_center())
        self.play(
            self.theta.animate.set_value(PI*17/4),
            run_time=25,
            # rate_func=smoothstep breaks dot_d for some reason
        )
        self.wait()


class Reciprocals(Scene):
    colours = {
        "hyp": GOLD,
        "opp": TEAL_B,
        "adj": GREEN,
        "tan": PURPLE,
        "cot": PURPLE_A,
        "sec": MAROON,
        "csc": MAROON_A,
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
            "1": GOLD,
            r"\sin": TEAL_B,
            r"\cos": GREEN,
            r"\tan": PURPLE,
            r"\sec": MAROON,
            r"\csc": MAROON_A,
            r"\cot": PURPLE_A,
            r"\sin \theta": TEAL_B,
            r"\cos \theta": GREEN,
            r"\tan \theta": PURPLE,
            r"\sec \theta": MAROON,
            r"\csc \theta": MAROON_A,
            r"\cot \theta": PURPLE_A
        }
    }

    def construct(self):
        self.init_scale = 5
        setup(self)
        self.theta = ValueTracker(PI/4)
        self.dots.scale(3/self.line_c.get_length())
        self.grid_cir = NumberPlane(
            [-1.5, 1.5, 1], 
            [-1.5, 1.5, 1],
            4.5, 4.5, faded_line_ratio=2
        )
        self.grid = NumberPlane(
            [-6, 6, 1],
            [-6, 6, 1],
            36, 36, faded_line_ratio=2
        )
        self.axises = Axes(
            [0, 10, PI/2], [-1, 1, 1], 
            7.5, 3
        ).shift([3, 0, 0])
        self.axis_coords = VGroup()
        for i in range(1, 7):
            label = MathTex(str(i*90), r"^\circ").move_to(self.axises.coords_to_point(i * PI/2, -0.2)).scale(0.5)
            self.axis_coords.add(label)
        self.grid_coords = VGroup(
            Tex("1").move_to([3.3, 0.3, 0]),
            Tex("1").move_to([0.3, 3.3, 0]),
            Tex("-1").move_to([-3.3, 0.3, 0]),
            Tex("-1").move_to([0.3, -3.3, 0])
        )
        self.circle = Circle(3)
        self.o_arm = Line(ORIGIN, 3*RIGHT)
        self.cover = Rectangle(BLACK, 10, 10).set_fill(BLACK, 1).set_opacity(0.5).move_to([-15, 0, 0])
        self.line_cc = DashedLine(dash_length=0.2)
        self.dot_o = Dot([0, 0, 0])
        self.dot_d = Dot([0, 3*math.tan(self.theta.get_value()), 0])
        self.dot_e = Dot([0, 3/math.tan(self.theta.get_value()), 0])
        self.func_display = MathTex(r"\sin \theta", color=self.colours["opp"]).move_to(self.axises.get_center()+[0, 3, 0])
        self.deg_display = MathTex(r"\theta =", str(round(math.degrees(self.theta.get_value()))), r"^\circ", color=BLUE)
        
        print("Theta is", self.theta.get_value(), math.degrees(self.theta.get_value()), "degrees")
        print("Radius is", self.circle.radius)
        self.angle_a.clear_updaters()
        self.angle_a.add_updater(lambda mob: mob.become(
            Angle(
                self.o_arm, self.line_c, 
                radius=angle_radius(self), 
                color=self.colours["angle_a"]
            )
        ))
        self.angle_c.clear_updaters()

        self.dots[1].add_updater(lambda dot: 
            theta_dot(dot, [0, 0, 0], self.theta.get_value(), 3)
        )
        self.dots[2].add_updater(lambda dot: 
            perpendicular_dot(dot, self.dots[1], [0, 0, 0])
        )
        self.big_tri.clear_updaters()
        self.big_tri.add_updater(lambda mob: mob.set_points_as_corners((
            [0, 0, 0], 
            [0, 3/math.sin(self.theta.get_value()), 0],
            [3/math.cos(self.theta.get_value()), 0, 0],
            [0, 0, 0]
        )))
        self.dot_d.add_updater(lambda mob: tan_dot(
            mob, self.dots[1], self.theta.get_value(), radius=3, axis="x"
        ))
        self.dot_e.add_updater(lambda mob: cot_dot(
            mob, self.theta.get_value(), radius=3
        ))

        self.tangent_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["tan"], stroke_width=5).set_z_index(2)
        self.tangent_segment.add_updater(
            lambda mob: tan_ext(mob, self.dots[1], self.theta.get_value())
        )
        self.cot_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["cot"], stroke_width=5).set_z_index(2)
        self.cot_segment.add_updater(
            lambda mob: cot_ext(mob, self.dots[1], self.theta.get_value())
        )
        self.sec_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["sec"], stroke_width=5).set_z_index(2)
        self.sec_segment.add_updater(
            lambda mob: mob.put_start_and_end_on([0, 0, 0], self.dot_d.get_center())
        )
        self.csc_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["csc"], stroke_width=5).set_z_index(2)
        self.csc_segment.add_updater(
            lambda mob: mob.put_start_and_end_on([0, 0, 0], self.dot_e.get_center())
        )
        self.line_b.clear_updaters()
        self.line_b.add_updater(lambda mob: mob.put_start_and_end_on(
            [0, math.sin(self.theta.get_value())*3, 0], 
            self.dots[1].get_center()
        ))

        self.deg_display.add_updater(
            lambda mob: mob.become(
                MathTex(r"\theta =", str(round(math.degrees(self.theta.get_value()))), r"^\circ", color=BLUE)
            ).move_to([-4, 3, 0])
        )
        self.sin_label = MathTex(r"\sin \theta", color=self.colours["opp"]).rotate(PI/2)
        self.sin_label.add_updater(
            lambda mob: mob.next_to(self.line_a, LEFT, buff=0.3)
        )
        self.cos_label = MathTex(r"\cos \theta", color=self.colours["adj"])
        self.cos_label.add_updater(
            lambda mob: mob.next_to(self.line_b, UP, buff=0.3)
        )
        self.tan_label = MathTex(r"\tan \theta", color=self.colours["tan"])
        self.tan_label.add_updater(lambda mob: mob.move_to(
            self.tangent_segment.get_center()).shift(mob.get_center() * 0.3)
        )
        self.cot_label = MathTex(r"\cot \theta", color=self.colours["cot"])
        self.cot_label.add_updater(lambda mob: mob.move_to(
            self.cot_segment.get_center()).shift(mob.get_center() * np.array([0.7, 0.1, 0]))
        )
        self.sec_label = MathTex(r"\sec \theta", color=self.colours["sec"])
        self.sec_label.add_updater(
            lambda mob: mob.next_to(self.sec_segment, DOWN, buff=0.3)
        )
        self.csc_label = MathTex(r"\csc \theta", color=self.colours["csc"]).rotate(PI/2)
        self.csc_label.add_updater(
            lambda mob: mob.next_to(self.csc_segment, LEFT, buff=0.3)
        )
        self.label_f.add_updater(lambda mob: normal_pos(mob, self.line_c, 0.3))

        self.sin_formula = MathTex(
            r"\frac{",
            r"\mathrm{Opp.}",
            r"}{",
            r"\mathrm{Hyp.}",
            r"}",
            r"=",
            r"\sin \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, 0, 0])
        self.cos_formula = MathTex(
            r"\frac{",
            r"\mathrm{Adj.}",
            r"}{",
            r"\mathrm{Hyp.}",
            r"}",
            r"=",
            r"\cos \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, 2, 0])
        self.tan_formula = MathTex(
            r"\frac{",
            r"\mathrm{Opp.}",
            r"}{",
            r"\mathrm{Adj.}",
            r"}",
            r"=",
            r"\tan \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, -2, 0])
        self.sec_formula = MathTex(
            r"\frac{",
            r"\mathrm{Hyp.}",
            r"}{",
            r"\mathrm{Adj.}",
            r"}",
            r"=",
            r"\sec \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, 2, 0])
        self.csc_formula = MathTex(
            r"\frac{",
            r"\mathrm{Hyp.}",
            r"}{",
            r"\mathrm{Opp.}",
            r"}",
            r"=",
            r"\csc \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, 0, 0])
        self.cot_formula = MathTex(
            r"\frac{",
            r"\mathrm{Adj.}",
            r"}{",
            r"\mathrm{Opp.}",
            r"}",
            r"=",
            r"\cot \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, -2, 0])

        self.add(
            self.dots,
            self.big_tri,
            self.grid,
            self.circle,
            self.grid_coords,
            self.angle_a,
            self.label_a,
            self.sin_label,
            self.cos_label,
            self.tan_label,
            self.line_c,
            self.line_a,
            self.line_b,
            self.tangent_segment,
            self.dot_d,
        )
        self.dots[0].move_to([0, 0, 0])
        self.dots[1].set_opacity(1).set_z_index(10)
        self.dot_o.set_z_index(10)
        self.dot_d.set_z_index(10)
        self.dot_e.set_z_index(10)
        self.big_tri.set_stroke_width(0)
        self.label_f.set_opacity(1)
        self.line_c.set_color(GOLD)
        self.line_a.set_color(self.colours["opp"]).set_stroke_width(10)
        self.line_b.set_color(self.colours["adj"]).set_stroke_width(10)
        self.tangent_segment.set_stroke_width(10)
        self.cot_segment.set_stroke_width(10)
        self.sec_segment.set_stroke_width(10)
        self.csc_segment.set_stroke_width(10)

        self.update_mobjects(0)
        self.play(Create(self.dot_o), self.theta.animate.set_value(PI/4+0.001))

        self.play(self.theta.animate.set_value(9/4*PI), run_time=7)
        self.play(self.cover.animate.move_to([-8, 0, 0]))

        self.play(
            Write(self.cos_formula),
            Write(self.sin_formula),
            Write(self.tan_formula)
        )
        self.wait()

        self.play(
            Create(self.cot_segment),
            Create(self.dot_e),
            Write(self.cot_label),
            run_time=2
        )
        self.play(TransformMatchingTex(self.tan_formula, self.cot_formula))
        self.play(Indicate(self.cot_formula))
        self.wait()
        self.play(
            Create(self.sec_segment),
            Write(self.sec_label),
            run_time=2
        )
        self.play(TransformMatchingTex(self.cos_formula, self.sec_formula))
        self.play(Indicate(self.sec_formula))
        self.wait()
        self.play(
            Create(self.csc_segment),
            Write(self.csc_label),
            run_time=2
        )
        self.play(TransformMatchingTex(self.sin_formula, self.csc_formula))
        self.play(Indicate(self.csc_formula))
        self.wait(2)
        self.play(
            self.cover.animate.move_to([-15, 0, 0]),
            Unwrite(self.sec_formula),
            Unwrite(self.csc_formula),
            Unwrite(self.cot_formula)
        )

        self.play(self.theta.animate.set_value(4.3*PI), run_time=15)

        self.cos_label.clear_updaters().move_to([0.882, 2.905, 0])
        self.play(self.cos_label.animate.shift([0, -0.5-self.cos_label.height, 0]))
        self.cos_label.add_updater(
            lambda mob: mob.next_to(self.line_b, DOWN, buff=0.2)
        )

        self.play(
            self.cover.animate.move_to([-8, 0, 0])
        )

        # wheel = Group()
        # for mob in self.mobjects:
        #     mob.suspend_updating()
        #     wheel.add(mob)
        # toutlemonde = wheel.copy().clear_updaters()
        # for mob in wheel:
        #     self.remove(mob)
        # self.add(toutlemonde)
        # toutlemonde[7].move_to([1.285, 1.214, 0])
        # toutlemonde[8].move_to([0.882, 2.905, 0])
        # self.play(toutlemonde[8].animate.shift(np.array([0, -0.6-toutlemonde[8].height, 0])))


        # self.add(self.cover)
        # self.cover.set_z_index(11)
        # self.play(
        #     self.cover.animate.move_to([8, 0, 0]),
        #     toutlemonde.animate.shift([-3, 0, 0]),
        # )
        self.tan_angle = RightAngle(self.line_c, self.tangent_segment, 0.2, quadrant=(-1, 1))
        self.angle_d = self.angle_a.copy().clear_updaters().rotate(-PI/2, about_point=[0, 0, 0]).shift([0, 3.708, 0])
        self.angle_d_label = MathTex(r"\theta", color=self.colours["angle_a"]).next_to(self.angle_d, DOWN, buff=0.1)
        self.wait()
        self.play(
            Create(self.tan_angle),
            Create(self.angle_d),
            Write(self.angle_d_label),
            Write(self.label_f),
            self.grid_coords[1].animate.shift([-0.6, 0, 0]),
            self.cos_label.animate.set_z_index(5),
            self.sin_label.animate.set_z_index(5)
        )
        #Redefine to fix geometry after uncreate
        self.sec_formula = MathTex(
            r"\frac{", r"\mathrm{Hyp.}", r"}{", r"\mathrm{Adj.}", r"}",
            r"=",
            r"\sec \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, 1, 0])
        self.csc_formula = MathTex(
            r"\frac{", r"\mathrm{Hyp.}", r"}{", r"\mathrm{Opp.}", r"}",
            r"=",
            r"\csc \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, 1, 0])
        self.cot_formula = MathTex(
            r"\frac{", r"\mathrm{Adj.}", r"}{", r"\mathrm{Opp.}", r"}",
            r"=",
            r"\cot \theta",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, 1, 0])
        self.sec_proof = MathTex(
            r"\frac{", r"1", r"}{", r"\cos \theta", r"}",
            r"="
            r"\frac{", r"\sec \theta", r"}{", r"1", r"}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, -1, 0])
        self.csc_proof = MathTex(
            r"\frac{", r"1", r"}{", r"\sin \theta", r"}",
            r"="
            r"\frac{", r"\csc \theta", r"}{", r"1", r"}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, -1, 0])
        self.cot_proof = MathTex(
            r"\frac{", r"1", r"}{", r"\tan \theta", r"}",
            r"="
            r"\frac{", r"\cot \theta", r"}{", r"1", r"}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=50
        ).move_to([-5, -1, 0])

        self.play(
            Write(self.sec_formula)
        )
        self.wait()
        self.play(
            Write(self.sec_proof[2]),
            Write(self.sec_proof[5]),
            Write(self.sec_proof[7]),
        )
        self.wait()
        self.line_c.suspend_updating()
        self.play(
            Write(self.sec_proof[1]),
            Indicate(self.line_c),
            run_time=1.5
        )
        self.wait(0.5)
        self.sin_label.suspend_updating()
        self.line_a.suspend_updating()
        self.play(
            Write(self.sec_proof[3]),
            Indicate(self.cos_label),
            Indicate(self.line_b),
            run_time=1.5
        )
        self.wait(0.5)
        self.sec_label.suspend_updating()
        self.sec_segment.suspend_updating()
        self.play(
            Write(self.sec_proof[6]),
            Indicate(self.sec_label),
            Indicate(self.sec_segment),
            run_time=2
        )
        self.wait(0.5)
        self.line_c.suspend_updating()
        self.play(
            Write(self.sec_proof[8]),
            Indicate(self.line_c),
            run_time=1.5
        )
        self.wait(0.5)

        tri_a = Polygon(
            [0, math.sin(self.theta.get_value())*3, 0], 
            self.dots[1].get_center(),
            [0, 0, 0],
            color=self.colours["adj"], stroke_width=10
        )
        tri_b = Polygon(
            self.dots[1].get_center(),
            self.dot_d.get_center(),
            [0, 0, 0],
            color=self.colours["sec"], stroke_width=10
        )
        self.play(
            Indicate(tri_a),
            Indicate(self.sec_proof[0]),
            Indicate(self.sec_proof[1]),
            Indicate(self.sec_proof[2]),
            Indicate(self.sec_proof[3]),
            run_time=2
        )
        self.play(
            Indicate(tri_b),
            Indicate(self.sec_proof[6]),
            Indicate(self.sec_proof[7]),
            Indicate(self.sec_proof[8]),
            Indicate(self.sec_proof[9]),
            run_time=2
        )
        self.wait()
        self.play(
            tri_a.animate.set_opacity(0),
            tri_b.animate.set_opacity(0),
            Unwrite(self.sec_formula),
            Unwrite(self.sec_proof)
        )
        
        tri_a = Polygon( 
            self.dots[1].get_center(),
            self.dots[2].get_center(),
            [0, 0, 0],
            color=self.colours["opp"], stroke_width=10
        )
        tri_b = Polygon(
            self.dots[1].get_center(),
            self.dot_e.get_center(),
            [0, 0, 0],
            color=self.colours["csc"], stroke_width=10
        )
        self.play(
            Write(self.csc_formula),
            Write(self.csc_proof)
        )
        self.play(
            Indicate(tri_a),
            Indicate(self.csc_proof[0]),
            Indicate(self.csc_proof[1]),
            Indicate(self.csc_proof[2]),
            Indicate(self.csc_proof[3]),
            run_time=2
        )
        self.play(
            Indicate(tri_b),
            Indicate(self.csc_proof[6]),
            Indicate(self.csc_proof[7]),
            Indicate(self.csc_proof[8]),
            Indicate(self.csc_proof[9]),
            run_time=2
        )
        self.wait()
        self.play(
            tri_a.animate.set_opacity(0),
            tri_b.animate.set_opacity(0),
            Unwrite(self.csc_formula),
            Unwrite(self.csc_proof)
        )
        
        tri_a = Polygon( 
            self.dots[1].get_center(),
            self.dot_d.get_center(),
            [0, 0, 0],
            color=self.colours["tan"], stroke_width=10
        )
        tri_b = Polygon(
            self.dots[1].get_center(),
            self.dot_e.get_center(),
            [0, 0, 0],
            color=self.colours["cot"], stroke_width=10
        )
        self.play(
            Write(self.cot_formula),
            Write(self.cot_proof)
        )
        self.play(
            Indicate(tri_a),
            Indicate(self.cot_proof[0]),
            Indicate(self.cot_proof[1]),
            Indicate(self.cot_proof[2]),
            Indicate(self.cot_proof[3]),
            run_time=2
        )
        self.play(
            Indicate(tri_b),
            Indicate(self.cot_proof[6]),
            Indicate(self.cot_proof[7]),
            Indicate(self.cot_proof[8]),
            Indicate(self.cot_proof[9]),
            run_time=2
        )
        self.wait()
        self.play(
            tri_a.animate.set_opacity(0),
            tri_b.animate.set_opacity(0),
            Unwrite(self.cot_formula),
            Unwrite(self.cot_proof)
        )

        for mob in self.mobjects:
            mob.clear_updaters()

        self.play(
            Unwrite(self.grid_coords),
            Unwrite(self.sin_label),
            Unwrite(self.cos_label),
            Unwrite(self.tan_label),
            Unwrite(self.sec_label),
            Unwrite(self.csc_label),
            Unwrite(self.cot_label),
            Unwrite(self.label_f),
            Uncreate(self.tan_angle),
            Uncreate(self.angle_d),
            Uncreate(self.angle_d_label),
            self.cover.animate.move_to([-15, 0, 0])
        )

        toutlemonde = Group(
            self.dots,
            self.big_tri,
            self.circle,
            self.angle_a,
            self.label_a,
            self.sin_label,
            self.cos_label,
            self.tan_label,
            self.line_c,
            self.line_a,
            self.line_b,
            self.tangent_segment,
            self.sec_segment,
            self.csc_segment,
            self.cot_segment,
            self.dot_d,
            self.dot_e,
            self.dot_o
        )
        self.play(
            Transform(self.grid, self.grid_cir),
            toutlemonde.animate.scale(0.5, about_point=[0, 0, 0])
        )
        self.play(
            toutlemonde.animate.shift([-4, 0, 0]),
            self.grid.animate.shift([-4, 0, 0]).set_z_index(0)
        )
        self.play(
            self.line_a.animate.set_stroke_width(5),
            self.line_b.animate.set_stroke_width(5),
            self.tangent_segment.animate.set_stroke_width(5),
            self.cot_segment.animate.set_stroke_width(5),
            self.sec_segment.animate.set_stroke_width(5),
            self.csc_segment.animate.set_stroke_width(5)
        )
        self.wait()


class ReciprocalGraphs(Scene):
    colours = {
        "hyp": GOLD,
        "opp": TEAL_B,
        "adj": GREEN,
        "tan": PURPLE,
        "cot": PURPLE_A,
        "sec": MAROON,
        "csc": MAROON_A,
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
            "1": GOLD,
            r"\sin": TEAL_B,
            r"\cos": GREEN,
            r"\tan": PURPLE,
            r"\sec": MAROON,
            r"\csc": MAROON_A,
            r"\cot": PURPLE_A,
            r"\sin \theta": TEAL_B,
            r"\cos \theta": GREEN,
            r"\tan \theta": PURPLE,
            r"\sec \theta": MAROON,
            r"\csc \theta": MAROON_A,
            r"\cot \theta": PURPLE_A
        }
    }

    def construct(self):
        self.init_scale = 5
        self.o = [-4, 0, 0]
        self.r = 1.5
        setup(self)
        self.theta = ValueTracker(
            math.atan(self.line_c.get_height()/self.line_c.get_width())
        )
        self.dots.scale(1.5/self.line_c.get_length())
        self.grid_cir = NumberPlane(
            [-1.5, 1.5, 1], 
            [-1.5, 1.5, 1],
            4.5, 4.5, faded_line_ratio=2
        ).move_to(self.o)
        self.grid = NumberPlane(
            [-6, 6, 1],
            [-6, 6, 1],
            36, 36, faded_line_ratio=2
        )
        self.axises = Axes(
            [0, 10, PI/2], [-1, 1, 1], 
            7.5, 3
        ).shift([3, 0, 0])
        self.axis_coords = VGroup()
        for i in range(1, 7):
            label = MathTex(str(i*90), r"^\circ").move_to(self.axises.coords_to_point(i * PI/2, -0.2)).scale(0.5)
            self.axis_coords.add(label)
        self.grid_coords = VGroup(
            Tex("1").move_to([3.3, 0.3, 0]),
            Tex("1").move_to([0.3, 3.3, 0]),
            Tex("-1").move_to([-3.3, 0.3, 0]),
            Tex("-1").move_to([0.3, -3.3, 0])
        ).shift(self.o).scale(0.5)
        self.cast = VGroup(
            Tex("C", color=self.colours["adj"]).move_to([3, -3, 0]),
            Tex("A").move_to([3, 3, 0]),
            Tex("S", color=self.colours["opp"]).move_to([-3, 3, 0]),
            Tex("T", color=self.colours["tan"]).move_to([-3, -3, 0])
        ).shift(self.o).scale(0.75)
        self.frac_cast = VGroup(
            Tex(r"$\frac{1}{\cos \theta}$", tex_to_color_map=self.colours["colour_map"]).move_to([3, -3, 0]),
            Tex("All").move_to([3, 3, 0]),
            Tex(r"$\frac{1}{\sin \theta}$", tex_to_color_map=self.colours["colour_map"]).move_to([-3, 3, 0]),
            Tex(r"$\frac{1}{\tan \theta}$", tex_to_color_map=self.colours["colour_map"]).move_to([-3, -3, 0])
        ).shift(self.o+np.array([0.7, 0, 0])).scale(0.75)
        self.reci_cast = VGroup(
            Tex(r"$= \sec \theta$", tex_to_color_map=self.colours["colour_map"]).move_to([3, -3, 0]),
            #Tex("All").move_to([3, 3, 0]),
            Tex(r"$= \csc \theta$", tex_to_color_map=self.colours["colour_map"]).move_to([-3, 3, 0]),
            Tex(r"$= \cot \theta$", tex_to_color_map=self.colours["colour_map"]).move_to([-3, -3, 0])
        ).shift(self.o+np.array([1.7, 0, 0])).scale(0.75)
        self.circle = Circle(1.5).shift(self.o)
        self.o_arm = Line(self.o, self.r*RIGHT)
        self.cover = Rectangle(BLACK, 10, 10).set_fill(BLACK, 1).set_opacity(0.5).move_to([-15, 0, 0])
        self.mask = Rectangle(BLACK, 10, 10).set_fill(BLACK, 1).move_to([5, 0, 0])
        self.dot_o = Dot(self.o).scale(0.5)
        self.dot_cc = Dot(self.o).scale(0.5)
        self.dot_d = Dot([0, self.r*math.tan(self.theta.get_value()), 0]).scale(0.5)
        self.dot_e = Dot([0, self.r/math.tan(self.theta.get_value()), 0]).scale(0.5)
        self.func_display = MathTex(r"\sec \theta", color=self.colours["sec"]).move_to(self.axises.get_center()+[0, 3, 0])
        self.deg_display = MathTex(r"\theta =", str(round(math.degrees(self.theta.get_value()))), r"^\circ", color=BLUE)

        print("Theta is", self.theta.get_value(), math.degrees(self.theta.get_value()), "degrees")
        print("Radius is", self.circle.radius)
        self.deg_display.add_updater(
            lambda mob: mob.become(
                MathTex(r"\theta =", str(round(math.degrees(self.theta.get_value()))), r"^\circ", color=BLUE)
            ).move_to([-5.5, 3, 0])
        )
        self.angle_a.clear_updaters()
        self.angle_a.add_updater(lambda mob: mob.become(
            Angle(
                self.o_arm, self.line_c, 
                radius=angle_radius(self), 
                color=self.colours["angle_a"]
            )
        ))

        self.dots[0].move_to(self.o)
        self.dots[1].add_updater(lambda dot: 
            theta_dot(dot, self.o, self.theta.get_value(), self.r)
        )
        self.dots[2].add_updater(lambda dot: 
            perpendicular_dot(dot, self.dots[1], self.o)
        )
        self.big_tri.clear_updaters()
        self.big_tri.add_updater(lambda mob: mob.set_points_as_corners((
            [0, 0, 0], 
            [0, self.r/math.sin(self.theta.get_value()), 0],
            [self.r/math.cos(self.theta.get_value()), 0, 0],
            [0, 0, 0]
        )).shift(self.o))
        self.dot_cc.add_updater(lambda mob: tan_dot(
            mob, self.dots[1], self.theta.get_value(), centre=self.o, radius=1.5
        )
        )
        self.dot_d.add_updater(lambda mob: tan_dot(
            mob, self.dots[1], self.theta.get_value(), centre=self.o, radius=1.5, axis="x"
        ))
        self.dot_e.add_updater(lambda mob: cot_dot(
            mob, self.theta.get_value(), centre=self.o, radius=1.5
        ))

        self.line_cc = Line(ORIGIN, RIGHT, color=self.colours["sec"], stroke_width=5)
        self.line_cc.add_updater(
            lambda line: hyp_ext(line, self.dots[1], self.theta.get_value(), self.o, dash=False)
        )
        self.line_ccc = Line(ORIGIN, LEFT, color=self.colours["sec"], stroke_width=5)
        self.line_ccc.add_updater(
            lambda line: ccc_ext(line, self.dots[1], self.o, self.theta.get_value())
        )
        self.tan_segment = DashedLine(
            self.dot_cc.get_center(), 
            [-2.5, 0, 0], 
            dash_length=0.05, color=WHITE, stroke_width=5
        )
        self.tan_segment.add_updater(
            lambda mob: mob.become(DashedLine(
            self.dot_cc.get_center(), 
            [-2.5, 0, 0], 
            dash_length=0.05, color=WHITE, stroke_width=5
        )))

        self.tangent_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["tan"], stroke_width=5)
        self.tangent_segment.add_updater(
            lambda mob: tan_ext(mob, self.dots[1], self.theta.get_value(), self.o)
        )
        self.cot_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["cot"], stroke_width=5)
        self.cot_segment.add_updater(
            lambda mob: cot_ext(mob, self.dots[1], self.theta.get_value(), self.o)
        )
        self.sec_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["sec"], stroke_width=5)
        self.sec_segment.add_updater(
            lambda mob: mob.put_start_and_end_on(self.o, self.dot_d.get_center())
        )
        self.csc_segment = Line([0, 0, 0], self.dot_d.get_center(), color=self.colours["csc"], stroke_width=5)
        self.csc_segment.add_updater(
            lambda mob: mob.put_start_and_end_on(self.o, self.dot_e.get_center())
        )
        self.line_b.clear_updaters()
        self.line_b.add_updater(lambda mob: mob.put_start_and_end_on(
            [-4, math.sin(self.theta.get_value())*self.r, 0], 
            self.dots[1].get_center()
        ))
        self.sec_proof = MathTex(
            r"\frac{",
            r"\sec \theta",
            r"}{",
            r"\tan \theta",
            r"}",
            r"=",
            r"\frac{",
            r"\sec \theta",
            r"}{",
            r"\tan \theta",
            r"}",
            tex_to_color_map=self.colours["colour_map"],
            font_size=30
        ).move_to([-1.3, 2.2, 0])

        with register_font("Teachers-Medium.ttf"):
            self.notice = Text("Actually negative!", font_size=40, font="Teachers")
        
        self.add(
            self.dots, 
            self.dot_o,
            self.dot_d,
            self.dot_e,
            self.big_tri, 
            self.line_a, 
            self.line_b, 
            self.line_c,
            self.angle_a, 
            self.label_a,
            self.grid_cir,
            self.grid_coords,
            self.circle,
            self.tangent_segment,
            self.sec_segment,
            self.csc_segment,
            self.cot_segment
        )
        self.label_a.scale(0.5)
        self.big_tri.set_stroke_width(0)
        self.dots[1].set_opacity(1).set_z_index(3)
        self.dot_o.set_z_index(3)
        self.dot_cc.set_z_index(3)
        self.dot_d.set_z_index(3)
        self.dot_e.set_z_index(3)
        self.line_a.set_z_index(2)
        self.line_b.set_z_index(2)
        self.line_cc.set_z_index(2)
        self.line_ccc.set_z_index(2)
        self.tangent_segment.set_z_index(2)
        self.cot_segment.set_z_index(2)
        self.sec_segment.set_z_index(2)
        self.csc_segment.set_z_index(2)
        self.mask.set_z_index(4)
        self.axises.set_z_index(5)
        self.line_c.set_color(GOLD)
        self.line_a.set_color(self.colours["opp"]).set_stroke_width(5),
        self.line_b.set_color(self.colours["adj"]).set_stroke_width(5),
        self.theta.set_value(0.2*PI)

        self.update_mobjects(0)
        self.wait()
        self.play(
            Create(self.axises),
            Create(self.axis_coords),
            # Create(self.deg_display),
            Create(self.func_display),
        )
        self.play(
            Create(self.dot_cc),
            Create(self.line_cc),
            Create(self.line_ccc)
        )

        self.onebrace = BraceLabel(
            Line(self.o, self.dot_cc), 
            r"\sec \theta", 
            rotate_vector(Line(self.o, self.dot_cc).get_unit_vector(), PI / 2)
        ).set_z_index(5)
        self.play(
            self.line_cc.animate.set_stroke_width(10),
            self.line_ccc.animate.set_stroke_width(10),
            Create(self.tan_segment),
            Write(self.onebrace)
        )
        self.play(
            Indicate(Group(self.line_cc, self.line_ccc)),
            Write(self.sec_proof)
        )
        self.wait(2)
        self.big_tri.clear_updaters()

        self.play(
            self.big_tri.animate.set_points_as_corners((
                self.o,
                [-2.5, 1.5*math.tan(self.theta.get_value()), 0],
                [-2.5, 0, 0],
                self.o
            )),
            Unwrite(self.sec_proof),
            self.sec_segment.animate.set_opacity(0),
            self.tangent_segment.animate.set_opacity(0),
            self.csc_segment.animate.set_opacity(0),
            self.cot_segment.animate.set_opacity(0),
            self.dot_d.animate.set_opacity(0),
            self.dot_e.animate.set_opacity(0),
            Unwrite(self.onebrace)
        )
        self.big_tri.add_updater(lambda mob: mob.set_points_as_corners(((
            self.o,
            [-2.5, 1.5*math.tan(self.theta.get_value()), 0],
            [-2.5, 0, 0],
            self.o
        ))))

        start = self.axises.coords_to_point(0, 0)
        self.end = Dot(start, 0.1)
        self.connector = Line(self.dots[1].get_center(), start)
        self.secant = VGroup(color=self.colours["sec"])
        self.secant.set_points_as_corners(
            (self.axises.coords_to_point(0, 0), self.axises.coords_to_point(-0.0001, 0))
        )
        def secant_graph(func):
            next_point = self.axises.coords_to_point([
                self.theta.get_value(),
                1/np.cos(self.theta.get_value())
            ])
            if abs(next_point)[1] > 8:
                return
            if abs(next_point[1] - func.get_last_point()[1]) > 8:
                func.start_new_path(next_point)
            else:
                func.add_line_to(next_point)

        secant_graph.in_gap = False
        self.va = VGroup(
            DashedLine(self.axises.coords_to_point((n+0.5)*PI, 10), self.axises.coords_to_point((n+0.5)*PI, -10))
            for n in range(3)
        )
        def update_end(mob):
            theta = self.theta.get_value()
            y = 1 / np.cos(theta)
            if abs(y) <= 10:
                mob.move_to(self.axises.coords_to_point(theta, y))
        self.end.add_updater(update_end)
        self.play(
            self.theta.animate.set_value(0.0001), 
            Create(self.end)
        )
        self.wait()
        self.secant.add_updater(lambda mob: secant_graph(mob))
        self.add(self.secant)
        self.play(
            self.theta.animate.set_value(10),
            Create(self.va),
            run_time=12
        )
        self.secant.clear_updaters()
        self.wait()
        self.play(
            self.sec_segment.animate.set_opacity(1).set_stroke_width(10)
        )
        self.notice.move_to([-4, -2.7, 0])
        self.play(Write(self.notice))
        self.play(
            Indicate(self.sec_segment), 
            Indicate(self.end), 
            run_time=2
        )
        self.play(
            Unwrite(self.notice), 
            self.sec_segment.animate.set_opacity(0).set_stroke_width(5)
        )
        self.wait()
        self.secant.clear_updaters()
        self.play(
            self.secant.animate.set_opacity(0),
            Uncreate(self.va),
            self.theta.animate.set_value(0.0001),
            run_time=2
        )
        self.end.clear_updaters()
        self.tan_segment.clear_updaters()
        self.play(self.theta.animate.set_value(0.2*PI))
        self.wait()

        self.big_tri.clear_updaters()
        self.play(
            self.end.animate.move_to(self.axises.coords_to_point(0, 1/math.sin(0.2*PI))),
            self.line_cc.animate.set_opacity(0).set_stroke_width(5),
            self.line_ccc.animate.set_opacity(0).set_stroke_width(5),
            self.dot_cc.animate.set_opacity(0),
            self.dot_e.animate.set_opacity(1),
            self.tan_segment.animate.set_opacity(0),
            self.cot_segment.animate.set_opacity(1),
            self.csc_segment.animate.set_opacity(1).set_stroke_width(10),
            self.big_tri.animate.set_points_as_corners((
                [-4, 0, 0], 
                self.dots[1].get_center(),
                [-4, 1.5/math.sin(self.theta.get_value()), 0],
                [-4, 0, 0]
            )),
            Transform(
                self.func_display, 
                MathTex(r"\csc \theta", color=self.colours["csc"]).move_to(self.axises.get_center()+[0, 3, 0])
            )
        )
        self.big_tri.add_updater(lambda mob: mob.set_points_as_corners((
            self.dot_o.get_center(), 
            self.dots[1].get_center(),
            [-4, 1.5/math.sin(self.theta.get_value()), 0],
            self.dot_o.get_center()
        )))

        self.cosecant = VGroup(color=self.colours["csc"])
        self.cosecant.set_points_as_corners(
            (self.axises.coords_to_point(0, 100), self.axises.coords_to_point(-0.0001, 100))
        )
        def cosecant_graph(func):
            next_point = self.axises.coords_to_point([
                self.theta.get_value(),
                1/np.sin(self.theta.get_value())
            ])
            if abs(next_point)[1] > 8:
                return
            if abs(next_point[1] - func.get_last_point()[1]) > 8:
                func.start_new_path(next_point)
            else:
                func.add_line_to(next_point)
        self.va = VGroup(
            DashedLine(self.axises.coords_to_point(n*PI, 10), self.axises.coords_to_point(n*PI, -10))
            for n in range(4)
        )
        self.connector = Line(self.dot_e.get_center(), start)
        def connector_manager(mob, start, end):
            if abs(start[1]) > 6 or abs(end[1]) > 6:
                return
            else:
                mob.put_start_and_end_on(start, end)
        self.connector.add_updater(
            lambda mob: connector_manager(mob, self.dot_e.get_center(), self.end.get_center())
        )
        self.play(
            Indicate(self.csc_segment),
            run_time=2
        )
        self.wait()
        self.play(Create(self.connector))
        self.end.add_updater(lambda mob: mob.move_to(
            self.axises.coords_to_point(0, 1/np.sin(self.theta.get_value()))
        ))
        self.play(
            self.theta.animate.set_value(0.0001)
        )
        self.end.clear_updaters()
        def update_end(mob):
            theta = self.theta.get_value()
            y = 1 / np.sin(theta)
            if abs(y) <= 10:
                mob.move_to(self.axises.coords_to_point(theta, y))
        self.end.add_updater(update_end)
        self.cosecant.add_updater(lambda mob: cosecant_graph(mob))
        self.add(self.cosecant)
        self.play(
            self.theta.animate.set_value(10),
            Create(self.va),
            run_time=12
        )
        self.cosecant.clear_updaters()
        self.wait(3)
        with register_font("Teachers-Medium.ttf"):
            self.notice = Text("Never between -1 and 1", font_size=35, font="Teachers")
            self.notice.move_to([-4, 3, 0])
        self.deg_display.clear_updaters()
        self.play(
            self.secant.animate.set_opacity(1).set_fill(opacity=0),
            self.deg_display.animate.set_opacity(0),
            Uncreate(self.va),
            Uncreate(self.connector),
            Write(self.notice),
            self.sec_segment.animate.set_opacity(1),
            self.tangent_segment.animate.set_opacity(1),
            Transform(
                self.func_display, 
                MathTex(
                    r"\sec \theta \mathrm{ \& } \csc \theta", tex_to_color_map=self.colours["colour_map"]
                ).move_to(self.axises.get_center()+[0, 3, 0])
            )
        )
        self.onezone = Rectangle(BLACK, 3, 10).move_to(self.axises.coords_to_point(0, 0) + np.array([5, 0, 0])).set_stroke_width(0).set_fill(opacity=0)
        self.play(
            self.onezone.animate.set_fill(color=YELLOW, opacity=0.8),
            rate_func=there_and_back,
            run_time=2
        )
        self.play(
            FadeOut(self.onezone),
            Indicate(self.sec_segment),
            Indicate(self.csc_segment),
            FocusOn([-4.75, -0.25, 0]),
            run_time=2
        )
        self.wait()
        self.play(
            self.sec_segment.animate.set_opacity(0),
            self.tangent_segment.animate.set_opacity(0),
            Unwrite(self.notice)
        )

        self.play(
            FadeOut(self.secant),
            FadeOut(self.cosecant),
            self.theta.animate.set_value(0.0001),
            Transform(
                self.func_display, 
                MathTex(
                    r"\cot \theta", tex_to_color_map=self.colours["colour_map"]
                ).move_to(self.axises.get_center()+[0, 3, 0])
            ),
            run_time=2
        ) 
        self.end.clear_updaters()
        self.wait()
        self.play(self.theta.animate.set_value(0.2*PI))
        self.wait()
        self.deg_display.add_updater(
            lambda mob: mob.become(
                MathTex(r"\theta =", str(round(math.degrees(self.theta.get_value()))), r"^\circ", color=BLUE)
            ).move_to([-5.5, 3, 0])
        )
        self.play(
            self.csc_segment.animate.set_stroke_width(5),
            self.cot_segment.animate.set_stroke_width(10),
            self.deg_display.animate.set_opacity(1)
        )
        self.play(Indicate(self.cot_segment), run_time=2)
        self.wait()
        self.play(
            self.theta.animate.set_value(0.001)
        )

        self.cotangent = VGroup(color=self.colours["cot"])
        self.cotangent.set_points_as_corners(
            (self.axises.coords_to_point(0, 100), self.axises.coords_to_point(-0.0001, 100))
        )
        def cotangent_graph(func):
            next_point = self.axises.coords_to_point([
                self.theta.get_value(),
                1/np.tan(self.theta.get_value())
            ])
            if abs(next_point)[1] > 8:
                return
            if abs(next_point[1] - func.get_last_point()[1]) > 8:
                func.start_new_path(next_point)
            else:
                func.add_line_to(next_point)
        self.va = VGroup(
            DashedLine(self.axises.coords_to_point(n*PI, 10), self.axises.coords_to_point(n*PI, -10))
            for n in range(4)
        )
        def update_end(mob):
            theta = self.theta.get_value()
            y = 1 / np.tan(theta)
            if abs(y) <= 10:
                mob.move_to(self.axises.coords_to_point(theta, y))
        self.end.add_updater(update_end)
        self.cotangent.add_updater(lambda mob: cotangent_graph(mob))
        self.add(self.cotangent)
        self.play(
            self.theta.animate.set_value(10),
            Create(self.va),
            run_time=12
        )
        self.cotangent.clear_updaters()
        self.wait(3)

        self.play(
            FadeOut(self.cotangent),
            Uncreate(self.va),
            Uncreate(self.end),
            Unwrite(self.func_display),
            Unwrite(self.axis_coords),
            Uncreate(self.axises),
        )
        self.big_tri.clear_updaters()
        self.play(
            self.sec_segment.animate.set_opacity(1),
            self.tangent_segment.animate.set_opacity(1),
            self.cot_segment.animate.set_stroke_width(5),
            self.big_tri.animate.set_points_as_corners((
                [-4, 0, 0],
                [-4, self.r/math.sin(self.theta.get_value()), 0],
                [self.r/math.cos(self.theta.get_value())-4, 0, 0],
                [-4, 0, 0]
            ))
        )
        self.big_tri.add_updater(lambda mob: mob.set_points_as_corners((
            [0, 0, 0], 
            [0, self.r/math.sin(self.theta.get_value()), 0],
            [self.r/math.cos(self.theta.get_value()), 0, 0],
            [0, 0, 0]
        )).shift(self.o))
        self.theta.set_value(self.theta.get_value()-2*PI)
        self.play(self.theta.animate.increment_value(PI/2))
        with register_font("Teachers-Medium.ttf"):
            self.notice = Text("CAST rule applies!", font_size=40, font="Teachers")
            self.notice.move_to([3, 0, 0])
        self.play(
            Write(self.notice),
            Write(self.cast),
        )
        self.play(Write(self.frac_cast))
        self.play(Write(self.reci_cast))
        self.wait()
        self.play(Unwrite(self.notice))
        self.play(self.theta.animate.increment_value(2*PI), run_time=5)
        with register_font("Teachers-Medium.ttf"):
            self.notice = Text("One last thing... \nco = complementary \ncosine cosecant cotangent", font_size=40, font="Teachers")
            self.notice.move_to([3, 2, 0])
        self.complementaries = VGroup(
            MathTex(r"\cos \theta = \sin(90^{\circ}-\theta)").move_to([-2, 0, 0]),
            MathTex(r"\csc \theta = \sec(90^{\circ}-\theta)").move_to([0, 0, 0]),
            MathTex(r"\cot \theta = \tan(90^{\circ}-\theta)").move_to([2, 0, 0]),
        ).move_to([3, -2, 0])
        self.play(
            Succession(
                Write(self.notice),
                Write(self.complementaries[0]),
                Write(self.complementaries[1]),
                Write(self.complementaries[2])
        ))
        self.wait(3)

# cast, credits scroll, deg display

# ------------------------ utils

def update_triangle(scene, mob):
    mob.set_points_as_corners([scene.get_a(), scene.get_b(), scene.get_c(), scene.get_a()])

def normal_pos(mob, line, buff=0.3):
    start = line.get_start()
    end = line.get_end()
    dir = end - start
    dir /= np.linalg.norm(dir)

    normal = np.array([-dir[1],dir[0],0])
    mob.move_to(line.get_center() + buff * normal)

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

def tan_dot(dot, target, angle, centre=[0, 0, 0], radius=1, maxi=10, axis="y"):
    if axis != "x":
        tan = np.clip(
            radius * math.tan(angle),
            -maxi,
            maxi
        )
        dot.move_to(
            [centre[0]+radius, centre[1]+tan, 0]
        )
    else:
        sec = np.clip(
            radius / math.cos(angle),
            -maxi,
            maxi
        )
        dot.move_to(
            [centre[0]+sec, centre[1], 0]
        )

def cot_dot(dot, angle, centre=[0, 0, 0], radius=1, maxi=10):
    csc = min(
        radius / math.sin(angle),
        maxi
    )
    dot.move_to(
        [centre[0], centre[1]+csc, 0]
    )

def tan_ext(line, dot, theta, centre=[0, 0, 0]):
    dot_pos = dot.get_center()
    dx = dot_pos[0]-centre[0]
    dy = dot_pos[1]-centre[1]
    r = np.linalg.norm(dot_pos-centre)

    if abs(dx) > r * 0.2:
        tan_pos = [centre[0]+r/math.cos(theta), centre[1], 0]
        line.put_start_and_end_on(dot_pos, tan_pos)
    else:
        dir = (dot_pos - centre) / r
        if math.tan(theta) >= 0:
            dir = np.array([dir[1], -dir[0], 0])
        else:
            dir = np.array([-dir[1], dir[0], 0])
        tan_pos = dir * 10 + dot_pos
        line.put_start_and_end_on(dot_pos, tan_pos)

def cot_ext(line, dot, theta, centre=[0, 0, 0]):
    dot_pos = dot.get_center()
    dx = dot_pos[0]-centre[0]
    dy = dot_pos[1]-centre[1]
    r = np.linalg.norm(dot_pos-centre)

    if abs(dy) > r * 0.2:
        tan_pos = [centre[0], centre[1]+r/math.sin(theta), 0]
        line.put_start_and_end_on(dot_pos, tan_pos)
    else:
        dir = (dot_pos - centre) / r
        if math.tan(theta) >= 0:
            dir = np.array([-dir[1], dir[0], 0])
        else:
            dir = np.array([dir[1], -dir[0], 0])
        tan_pos = dir * 10 + dot_pos
        line.put_start_and_end_on(dot_pos, tan_pos)

def hyp_ext(line, dot, theta, centre=[0, 0, 0], dash=True, dashness=0.2):
    dot_pos = dot.get_center()
    dx = dot_pos[0]-centre[0]
    dy = dot_pos[1]-centre[1]
    r = np.linalg.norm(dot_pos-centre)
    dir = (dot_pos - centre) / r
    if math.cos(theta) >= 0:
        if dx > r * 0.2:
            tan_pos = [centre[0]+r, dy/dx*r, 0]
        else:
            tan_pos = dir * 10 + centre
        if dash:
            line.become(DashedLine(dot_pos, tan_pos, dash_length=dashness))
        else:
            line.put_start_and_end_on(dot_pos, tan_pos)
    else:
        if dx < -r * 0.2:
            tan_pos = [centre[0]+r, dy/dx*r, 0]
        else:
            tan_pos = dir * -10 + centre
        if dash:
            line.become(DashedLine(centre, tan_pos, dash_length=dashness))
        else:
            line.put_start_and_end_on(centre, tan_pos)

def ccc_ext(line, dot, centre, angle):
    if math.cos(angle) <= 0:
        line.put_start_and_end_on(centre, np.array(centre)*1.0001)
    else:
        line.put_start_and_end_on(centre, dot.get_center())

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


# Only function made with AI, was too lazy to code a literal right angle
def right_angle(mob, vertex, line_1, line_2, length=0.4, quadrant=(1, 1)):
    # Find the direction from the vertex along each line
    p1 = line_1.get_start() if np.linalg.norm(line_1.get_start() - vertex) > 1e-6 else line_1.get_end()
    p2 = line_2.get_start() if np.linalg.norm(line_2.get_start() - vertex) > 1e-6 else line_2.get_end()

    u1 = p1 - vertex
    u2 = p2 - vertex

    u1 /= np.linalg.norm(u1)
    u2 /= np.linalg.norm(u2)

    u1 *= quadrant[0]
    u2 *= quadrant[1]

    # Three corners of the little square
    a = vertex + u1 * length
    b = vertex + u1 * length + u2 * length
    c = vertex + u2 * length

    mob.set_points_as_corners([a, b, c])

def nice_angle(scene, mob, ref, line_1, line_2):
    mob.become(
        Angle(
            line_1, line_2, 
            radius = angle_radius(scene), 
            color=scene.colours.get("angle_"+str(ref), WHITE)
        )
    )