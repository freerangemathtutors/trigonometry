from manim import *
import math
import copy

# Please excuse the mess and try not to trip on the spaghetti ;)
# It gets better in more-trig.py

# config.renderer = "opengl"

class Intro(Scene):
    def construct(self):
        # Setup geometry
        dots = Group(
            Dot([-1.5, -2.0, 0]).set_opacity(0),
            Dot([1.5, 2.0, 0]).set_opacity(0),
            Dot([1.5, -2.0, 0]).set_opacity(0)
        )
        get_a = lambda: dots[0].get_center()
        get_b = lambda: dots[1].get_center()
        get_c = lambda: dots[2].get_center()

        line_a = Line(get_b(), get_c()).set_opacity(0)
        line_b = Line(get_a(), get_c()).set_opacity(0)
        line_c = Line(get_a(), get_b()).set_opacity(0)
        line_a.add_updater(lambda mob: mob.put_start_and_end_on(get_b(), get_c()))
        line_b.add_updater(lambda mob: mob.put_start_and_end_on(get_a(), get_c()))
        line_c.add_updater(lambda mob: mob.put_start_and_end_on(get_a(), get_b()))

        big_tri = Polygon(get_a(), get_b(), get_c(), color=WHITE, stroke_width=4).set_fill(BLUE, 0.3, False)

        def update_triangle(mob):
            mob.set_points_as_corners([get_a(), get_b(), get_c(), get_a()])

        big_tri.add_updater(update_triangle)

        angle_a = Angle(line_b, line_c, radius=0.7, color=BLUE).set_opacity(0).set_stroke(BLUE, 0.3)
        angle_b = Angle(Line(get_b(), get_a()), line_a, radius=0.7, color=RED).set_opacity(0)
        angle_c = RightAngle(Line(get_c(), get_b()), Line(get_c(), get_a()), length=0.4, color=WHITE)

        angle_a.add_updater(lambda mob: mob.become(
            Angle(line_b, line_c, radius=0.7, color=BLUE)
        ))
        angle_b.add_updater(lambda mob: mob.become(
            Angle(Line(get_b(), get_a()), line_a, radius=0.7, color=RED)
        ))
        angle_c.add_updater(lambda mob: mob.become(
            RightAngle(Line(get_c(), get_b()), Line(get_c(), get_a()), length=0.4, color=WHITE)
        ))


        with register_font("Teachers-Medium.ttf"):
            Text.set_default(font="Teachers")
            label_a = MathTex(r"a", color=BLUE).set_opacity(0)
            label_b = MathTex(r"b", color=RED).set_opacity(0)
            label_c = MathTex(r"90^\circ", color=WHITE)
            label_d = Tex(r"Opposite", color=TEAL_B).set_opacity(0)
            label_e = Tex(r"Adjacent", color=GREEN).set_opacity(0)
            label_f = Tex(r"Hypotenuse", color=GOLD)
            label_same = Text("Similar", color=YELLOW)
            label_prop = Text("Proportions", color=YELLOW)
            detour_box = Rectangle(WHITE, 5.5, 9.6)
            detour_label = Text("Naming the sides")

        label_a.next_to(angle_a, RIGHT, buff=0.1)
        label_b.next_to(angle_b, DOWN, buff=0.1)
        label_c.next_to(angle_c, UP + LEFT, buff=0.1)
        label_d.next_to(line_a, RIGHT, buff=0.3)
        label_e.next_to(line_b, DOWN, buff=0.3)
        label_f.next_to(line_c, LEFT, buff=0.1)
        label_f.shift([0.5, 0, 0])
        label_same.shift([0, -3, 0])
        label_prop.shift([0, -3, 0])
        detour_box.shift([0, -0.2, 0])
        detour_label.move_to([0, 3, 0])

        label_a.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))
        label_b.add_updater(lambda mob: mob.next_to(angle_b, DOWN, buff=0.1))
        label_c.add_updater(lambda mob: mob.next_to(angle_c, UP + LEFT, buff=0.1))

        # Setup 2nd triangle
        tri_copy = copy.deepcopy(big_tri)
        tri_copy.clear_updaters()
        copy_vertices = tri_copy.get_vertices()
        angle_f = RightAngle(
            Line(copy_vertices[2], copy_vertices[1]), 
            Line(copy_vertices[2], copy_vertices[0]), 
            length=0.4, color=WHITE
        )
        
        copy_group = VGroup(tri_copy, angle_f)
        self.add(line_a, line_b, line_c)

        # Animations begin
        self.play(
            Create(big_tri),
            Create(angle_c),
            Write(label_c)
        )
        self.wait(1)

        self.play(
            Unwrite(label_c)
        )
        self.wait(0.5)

        self.add(copy_group)
        self.play(
            copy_group.animate.move_to([3.0, 0, 0]),
            dots.animate.shift([-3.0, 0, 0])
        )
        self.wait()

        # self.play(
        #     dots[1].animate.move_to([-0.5, 3.0, 0]),
        #     run_time=3,
        #     rate_func=there_and_back
        # )
        # self.wait()

        self.play(
            copy_group.animate.scale(1.6),
            run_time=2
        )
        self.wait(0.1)
        self.play(
            copy_group.animate.scale(0.625),
            Write(label_same),
            run_time=2
        )
        self.wait(0.1)

        self.play(
            copy_group.animate.scale(0.625),
            run_time=2
        )
        self.wait()
        # self.play(
        #     copy_group.animate.scale(1.6)
        # )
        # self.wait()

        copy_vertices = tri_copy.get_vertices()
        angle_d = Angle(
            Line(copy_vertices[0], copy_vertices[2]), 
            Line(copy_vertices[0], copy_vertices[1]), 
            radius=0.4, color=BLUE
        ).set_opacity(0).set_fill(0)
        angle_e = Angle(
            Line(copy_vertices[1], copy_vertices[0]), 
            Line(copy_vertices[1], copy_vertices[2]), 
            radius=0.4, color=RED
        ).set_opacity(0).set_fill(0)
        line_d = Line(copy_vertices[2], copy_vertices[1])
        line_e = Line(copy_vertices[0], copy_vertices[2])
        line_f = Line(copy_vertices[0], copy_vertices[1])

        self.add(angle_a, angle_b, angle_d, angle_e, line_d, line_e, line_f)
        self.play(
            angle_a.animate.set_opacity(1).set_fill(0),
            angle_b.animate.set_opacity(1).set_fill(0),
            angle_d.animate.set_opacity(1).set_fill(0),
            angle_e.animate.set_opacity(1).set_fill(0),
            run_time = 0.5
        )
        angle_a.suspend_updating()
        angle_b.suspend_updating()
        angle_c.suspend_updating()
        angle_d.suspend_updating()
        angle_e.suspend_updating()
        angle_f.suspend_updating()
        self.play(
            Indicate(angle_a),
            Indicate(angle_d),
        )
        self.play(
            Indicate(angle_b),
            Indicate(angle_e),
        )
        self.play(
            Indicate(angle_c),
            Indicate(angle_f),
        )
        angle_a.resume_updating()
        angle_b.resume_updating()
        angle_c.resume_updating()
        angle_d.resume_updating()
        angle_e.resume_updating()
        angle_f.resume_updating()

        line_a.suspend_updating()
        line_b.suspend_updating()
        line_c.suspend_updating()

        self.play(Transform(label_same, label_prop))
        line_a.set_opacity(1).set_z_index(1.0)
        line_b.set_opacity(1).set_z_index(1.0)
        line_c.set_opacity(1).set_z_index(1.0)
        self.wait()
        self.play(
            Indicate(line_b),
            Indicate(line_e)
        )
        self.play(
            Indicate(line_c),
            Indicate(line_f)
        )
        self.play(
            Indicate(line_a),
            Indicate(line_d)
        )
        self.wait()

        line_a.resume_updating()
        line_b.resume_updating()
        line_c.resume_updating()
        self.remove(line_d, line_e, line_f)
        
        self.play(
            angle_d.animate.set_opacity(0),
            angle_e.animate.set_opacity(0),
            Uncreate(copy_group),
            Unwrite(label_same),
            dots.animate.shift([3.0, 0, 0])
        )
        self.wait()

        self.play(
            Create(detour_box),
            Write(detour_label)
        )

        self.play(Write(label_f))
        self.wait(2)

        self.play(
            label_a.animate.set_opacity(1),
            label_b.animate.set_opacity(1),
            label_c.animate.set_opacity(1),
        )
        self.wait()

        self.play(
            Succession(
                AnimationGroup(Indicate(angle_a), Indicate(label_a), run_time=0.2),
                AnimationGroup(Indicate(angle_b), Indicate(label_b), run_time=0.2),
                AnimationGroup(Indicate(angle_a), Indicate(label_a), run_time=0.2),
                AnimationGroup(Indicate(angle_b), Indicate(label_b), run_time=0.2),
                AnimationGroup(Indicate(angle_a), Indicate(label_a), run_time=0.2),
                AnimationGroup(Indicate(angle_b), Indicate(label_b), run_time=0.2),
            ),
        )
        self.wait()
        self.play(
            Indicate(angle_a),
            Indicate(label_a),
            Unwrite(angle_b),
            Unwrite(label_b),
            run_time=2.5
        )
        self.play(Transform(label_a, MathTex(r"\theta", color=BLUE).move_to(label_a)))
        self.play(Indicate(label_a))

        label_d.set_opacity(1)
        label_e.set_opacity(1)

        self.play(Write(label_d))
        self.wait()

        self.play(Write(label_e))
        self.wait(1.5)

        label_a.clear_updaters()
        angle_a.clear_updaters()
        angle_b.clear_updaters()
        angle_b.become(Angle(Line(get_b(), get_a()), line_a, radius=0.7, color=BLUE).set_opacity(1))
        self.play(
            label_a.animate.next_to(angle_b, DOWN, buff=0.1),
            label_d.animate.next_to(line_b, DOWN, buff=0.3),
            label_e.animate.next_to(line_a, RIGHT, buff=0.3),
            Create(angle_b),
            angle_a.animate.set_opacity(0)
        )
        self.wait(1.5)
        self.play(
            label_a.animate.next_to(angle_a, RIGHT, buff=0.1),
            label_d.animate.next_to(line_a, RIGHT, buff=0.3),
            label_e.animate.next_to(line_b, DOWN, buff=0.3),
            Uncreate(angle_b),
            angle_a.animate.set_opacity(1).set_fill(opacity=0)
        )
        label_a.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))
        angle_a.add_updater(lambda mob: mob.become(
            Angle(line_b, line_c, radius=0.7, color=BLUE)
        ))

        self.play(
            AnimationGroup(
                AnimationGroup(
                    Unwrite(label_d),
                    Unwrite(label_e),
                    Unwrite(label_f),
                    Uncreate(detour_box),
                    Unwrite(detour_label),
                    lag_ratio=0
                ),
                AnimationGroup(
                    *(pos.animate.shift([-4.0, 0, 0]) for pos in dots), 
                    lag_ratio=0
                ),
                lag_ratio=0.5
            )
        )
        self.wait()


class Proportions(Scene):
    def construct(self):
        # Setup geometry
        dots = VGroup(
            Dot([-1.5, -2.0, 0]).set_opacity(0),
            Dot([1.5, 2.0, 0]).set_opacity(0),
            Dot([1.5, -2.0, 0]).set_opacity(0)
        )
        get_a = lambda: dots[0].get_center()
        get_b = lambda: dots[1].get_center()
        get_c = lambda: dots[2].get_center()

        line_a = Line(get_b(), get_c())
        line_b = Line(get_a(), get_c())
        line_c = Line(get_a(), get_b())
        line_a.add_updater(lambda mob: mob.put_start_and_end_on(get_b(), get_c()))
        line_b.add_updater(lambda mob: mob.put_start_and_end_on(get_a(), get_c()))
        line_c.add_updater(lambda mob: mob.put_start_and_end_on(get_a(), get_b()))

        big_tri = Polygon(get_a(), get_b(), get_c(), color=WHITE, stroke_width=4).set_fill(BLUE, 0.3, False)

        def update_triangle(mob):
            mob.set_points_as_corners([get_a(), get_b(), get_c(), get_a()])
        big_tri.add_updater(update_triangle)

        angle_a = Angle(line_b, line_c, radius=0.7, color=BLUE)
        angle_b = Angle(Line(get_b(), get_a()), line_a, radius=0.7, color=GREEN).set_opacity(0)
        angle_c = RightAngle(Line(get_c(), get_b()), Line(get_c(), get_a()), length=0.4, color=WHITE)

        angle_a.add_updater(lambda mob: mob.become(
            Angle(line_b, line_c, radius=0.7, color=BLUE)
        ))
        angle_b.add_updater(lambda mob: mob.become(
            Angle(Line(get_b(), get_a()), line_a, radius=0.7, color=GREEN)
        ))
        angle_c.add_updater(lambda mob: mob.become(
            RightAngle(Line(get_c(), get_b()), Line(get_c(), get_a()), length=0.4, color=WHITE)
        ))

        # ":" cannot be used in Text()
        with register_font("Teachers-Medium.ttf"):
            Text.set_default(font="Teachers")
            label_a = MathTex(r"\theta", color=BLUE)
            label_b = MathTex(r"\phi", color=GREEN)
            label_c = MathTex(r"90^\circ", color=WHITE)
            label_d = Tex(r"Opposite", color=TEAL_B)
            label_e = Tex(r"Adjacent", color=GREEN)
            label_f = Tex(r"Hypotenuse", color=GOLD)
            label_opp = Tex(r"Opp.", color=WHITE)
            label_adj = Tex(r"Adj.", color=WHITE)
            label_hyp = Tex(r"Hyp.", color=WHITE)
            label_sub = Tex(r"Similar!", color=YELLOW)
            label_angle = MathTex(r"53.1^\circ", color=BLUE)
            tex_ratio = Tex(r"4 : 3", color=WHITE)
            tex_frac = MathTex(r"\frac{4}{3}", color=WHITE)
            box = Rectangle(WHITE, 3, 6)
            title = Text("Proportions")
            sine_ratio = MathTex(
                r"\frac{Opp.}{Hyp.}=", 
                tex_to_color_map={"Opp.": TEAL_B, "Adj.": GREEN, "Hyp.": GOLD},
                font_size=50
            )
            cosine_ratio = MathTex(
                r"\frac{Adj.}{Hyp.}=", 
                tex_to_color_map={"Opp.": TEAL_B, "Adj.": GREEN, "Hyp.": GOLD},
                font_size=50
            )
            tangent_ratio = MathTex(
                r"\frac{Opp.}{Adj.}=", 
                tex_to_color_map={"Opp.": TEAL_B, "Adj.": GREEN, "Hyp.": GOLD},
                font_size=50
            )
            sine_frac = MathTex(
                r"\frac{0.00}{0.00}=",
                tex_to_color_map={"0.00": BLACK},
                font_size=50
            ).set_z_index(-1)
            cosine_frac = MathTex(
                r"\frac{0.00}{0.00}=",
                tex_to_color_map={"0.00": BLACK},
                font_size=50
            ).set_z_index(-1)
            tangent_frac = MathTex(
                r"\frac{0.00}{0.00}=",
                tex_to_color_map={"0.00": BLACK},
                font_size=50
            ).set_z_index(-1)
            sine_result = MathTex(r"0.8", color=BLUE_A)
            cosine_result = MathTex(r"0.6", color=BLUE_B)
            tangent_result = MathTex(r"1.\overline{3}", color=BLUE_C)

        label_a.next_to(angle_a, RIGHT, buff=0.1)
        label_b.next_to(angle_b, DOWN, buff=0.1)
        label_c.next_to(angle_c, UP + LEFT, buff=0.1)
        label_d.next_to(line_a, RIGHT, buff=0.3)
        label_e.next_to(line_b, DOWN, buff=0.3)
        label_f.next_to(line_c, [0, 0, 0], buff=0.1)
        label_opp.next_to(line_a, RIGHT, buff=0.3)
        label_adj.next_to(line_b, DOWN, buff=0.3)
        label_hyp.next_to(line_c, [0, 0, 0], buff=0.1)
        label_angle.next_to(angle_a, RIGHT, buff=0.1)
        label_f.shift([0.5, 0, 0])
        label_sub.shift([0, -3, 0])
        box.shift([2, -0.5, 0])
        title.move_to([2, 2, 0])
        tex_ratio.next_to(box, LEFT, -2.5)
        tex_frac.next_to(box, RIGHT, -1.9)
        sine_ratio.move_to([1, 2, 0])
        cosine_ratio.move_to([1, 0, 0])
        tangent_ratio.move_to([1, -2, 0])
        sine_frac.move_to([3, 2.05, 0])
        cosine_frac.move_to([3, 0.05, 0])
        tangent_frac.move_to([3, -1.95, 0])
        sine_result.move_to([4.35, 2, 0])
        cosine_result.move_to([4.35, 0, 0])
        tangent_result.move_to([4.35, -1.95, 0])

        label_a.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))
        label_b.add_updater(lambda mob: mob.next_to(angle_b, DOWN, buff=0.1))
        label_c.add_updater(lambda mob: mob.next_to(angle_c, UP + LEFT, buff=0.1))
        label_opp.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))
        label_adj.add_updater(lambda mob: mob.next_to(angle_b, DOWN, buff=0.1))
        label_hyp.add_updater(lambda mob: mob.next_to(angle_c, UP + LEFT, buff=0.1))

        def length_label(label, line, location, buff, colour=WHITE, static=False):
            label.become(Tex(f"{line.get_length():.2f}", color=colour))
            if not static:
                label.rotate(line.get_angle())
                label.next_to(*location, buff=buff)
            else:
                label.move_to(location)

        def text_label(label, line, location, buff, text, colour=WHITE, static=False):
            label.become(Tex(text, color=colour))
            if not static:
                label.rotate(line.get_angle())
                label.next_to(*location, buff=buff)
            else:
                label.move_to(label.get_center())

        def current_angle():
            return angle_between_vectors(
                line_b.get_vector(),
                line_c.get_vector()
            )

        label_d.add_updater(
            lambda mob: length_label(mob, line_a, (line_a, RIGHT), 0.3, TEAL_B)
        )
        label_e.add_updater(
            lambda mob: length_label(mob, line_b, (line_b, DOWN), 0.3, GREEN)
        )
        label_f.add_updater(
            lambda mob: length_label(mob, line_c, (line_c, [0, 0, 0]), -0.3, GOLD)
        )
        label_f.add_updater(lambda mob: mob.shift([-0.5, 0, 0]))

        label_opp.add_updater(
            lambda mob: text_label(mob, line_a, (line_a, RIGHT), 0.3, "Opp.")
        )
        label_adj.add_updater(
            lambda mob: text_label(mob, line_b, (line_b, DOWN), 0.3, "Adj.")
        )
        label_hyp.add_updater(
            lambda mob: text_label(mob, line_c, (line_c, [0, 0, 0]), -0.3, "Hyp.")
        )
        label_hyp.add_updater(lambda mob: mob.shift([-0.5, 0, 0]))
        label_angle.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))
        
        self.add(dots, big_tri, line_a, line_b, line_c, angle_a, label_a, angle_c)
        dots.shift([-4, 0, 0])
        self.update_mobjects(0)
        self.wait()

        self.play(
            Create(box),
            Write(title)
        )
        self.wait()
        self.play(
            Succession(
                GrowFromCenter(tex_ratio),
                GrowFromCenter(tex_frac)
            )
        )
        self.wait(0.5)
        self.play(
            Succession(
                Circumscribe(tex_ratio),
                Circumscribe(tex_frac)
            )
        )
        self.wait()
        self.play(
            Uncreate(box),
            Unwrite(title),
            Unwrite(tex_frac),
            Unwrite(tex_ratio)
        )
        self.play(
            dots[1].animate.move_to([
                get_c()[0], 
                get_c()[1] + 5 * math.sin(53.1/360*2*math.pi), 
                0
            ]),
            Transform(label_a, label_angle.move_to(label_a))
        )
        tex_frac.become(
            MathTex(r"\frac{side}{side}", color=WHITE, font_size=69).move_to([3, 0, 0])
        )
        self.play(
            Succession(
                Write(label_d),
                Write(label_e),
                Write(label_f),
            ),
            run_time=1.5
        )
        self.wait(0.5)
        self.play(Write(tex_frac))
        self.wait()
        self.play(
            Succession(
                tex_frac.animate.shift([1, 0, 0]),
                Write(sine_ratio),
                Write(cosine_ratio),
                Write(tangent_ratio),
                Unwrite(tex_frac)
            )
        )
        self.wait()

        copy_d = label_d.copy().clear_updaters()
        copy_e = label_e.copy().clear_updaters()
        copy_f = label_f.copy().clear_updaters()
        kopi_d = label_d.copy().clear_updaters()
        kopi_e = label_e.copy().clear_updaters()
        kopi_f = label_f.copy().clear_updaters()
        self.add(copy_d, copy_e, copy_f, kopi_d, kopi_e, kopi_f)

        self.play(
            Write(sine_frac),
            copy_d.animate.move_to(sine_frac.get_center()+[-0.3, 0.35, 0]).rotate(PI/2),
            copy_f.animate.move_to(sine_frac.get_center()+[-0.3, -0.4, 0]).rotate(-float(line_c.get_angle())),
        )
        self.play(Write(sine_result))
        self.wait()
        self.play(
            Write(cosine_frac),
            copy_e.animate.move_to(cosine_frac.get_center()+[-0.3, 0.35, 0]),
            kopi_f.animate.move_to(cosine_frac.get_center()+[-0.3, -0.4, 0]).rotate(-float(line_c.get_angle())),
        )
        self.play(Write(cosine_result))
        self.wait()
        self.play(
            Write(tangent_frac),
            kopi_d.animate.move_to(tangent_frac.get_center()+[-0.3, 0.35, 0]).rotate(PI/2),
            kopi_e.animate.move_to(tangent_frac.get_center()+[-0.3, -0.4, 0]),
        )
        self.play(Write(tangent_result))
        self.wait()

        copy_d.add_updater(
            lambda mob: length_label(mob, line_a, (sine_frac.get_center()+[-0.3, 0.35, 0]), 0, TEAL_B, True)
        )
        kopi_d.add_updater(
            lambda mob: length_label(mob, line_a, (tangent_frac.get_center()+[-0.3, 0.35, 0]), 0, TEAL_B, True)
        )
        copy_e.add_updater(
            lambda mob: length_label(mob, line_b, (cosine_frac.get_center()+[-0.3, 0.35, 0]), 0, GREEN, True)
        )
        kopi_e.add_updater(
            lambda mob: length_label(mob, line_b, (tangent_frac.get_center()+[-0.3, -0.4, 0]), 0, GREEN, True)
        )
        copy_f.add_updater(
            lambda mob: length_label(mob, line_c, (sine_frac.get_center()+[-0.3, -0.4, 0]), 0, GOLD, True)
        )
        kopi_f.add_updater(
            lambda mob: length_label(mob, line_c, (cosine_frac.get_center()+[-0.3, -0.4, 0]), 0, GOLD, True)
        )

        self.play(
            dots.animate.scale(1.6),
            run_time=2
        )
        self.wait()
        self.play(
            dots.animate.scale(0.625),
            run_time=2
        )
        self.wait()
        self.play(
            Indicate(sine_result),
            Indicate(cosine_result),
            Indicate(tangent_result)
        )
        self.wait()

        label_a.add_updater(lambda mob: mob.become(
            MathTex(
                rf"{current_angle() / DEGREES:.1f}^\circ",
                color=BLUE
            ).next_to(angle_a, RIGHT, buff=0.1)
        ))
        sine_result.add_updater(lambda mob: mob.become(
            MathTex(
                rf"{math.sin(current_angle()):.2f}\ldots",
                color=BLUE_A
            ).move_to([4.65, 2, 0])
        ))
        cosine_result.add_updater(lambda mob: mob.become(
            MathTex(
                rf"{math.cos(current_angle()):.2f}\ldots",
                color=BLUE_B
            ).move_to([4.65, 0, 0])
        ))
        tangent_result.add_updater(lambda mob: mob.become(
            MathTex(
                rf"{math.tan(current_angle()):.2f}\ldots",
                color=BLUE_C
            ).move_to([4.65, -2, 0])
        ))
        results = Group(sine_result, cosine_result, tangent_result)

        self.update_mobjects(0)
        self.play(
            dots[1].animate.move_to([
                get_c()[0], 
                get_c()[1] + 3 * math.tan(45/360*2*math.pi), 
                0
            ]),
            run_time=0.5
        )
        self.play(
            dots.animate.move_to([-4, 0, 0]),
            run_time=0.5
        )
        self.play(Indicate(label_a)),

        self.play(
            dots.animate.scale(1.6),
            run_time=1.5
        )
        results.suspend_updating()
        self.play(Indicate(results))
        results.resume_updating()
        self.play(
            dots.animate.scale(0.5),
            run_time=1.5
        )
        results.suspend_updating()
        self.play(Indicate(results))
        results.resume_updating()
        self.wait(2)

        self.play(
            dots[1].animate.move_to([
                get_c()[0], 
                get_c()[1] + line_b.get_length() * math.tan(67/360*2*math.pi), 
                0
            ]),
            run_time=0.5
        )
        self.play(
            dots.animate.move_to([-4, 0, 0]),
            run_time=0.5
        )
        results.suspend_updating()
        self.play(Indicate(results))
        results.resume_updating()
        self.play(
            dots.animate.scale(1.6),
            run_time=1
        )
        results.suspend_updating()
        self.play(Indicate(results))
        results.resume_updating()
        self.play(
            dots.animate.scale(0.7),
            run_time=1
        )
        self.wait(2)

        self.play(
            dots[1].animate.move_to([
                get_c()[0], 
                get_c()[1] + line_b.get_length() * math.tan(36/360*2*math.pi), 
                0
            ]),
            run_time=0.5
        )
        self.play(
            dots.animate.move_to([-4, 0, 0]),
            run_time=0.5
        )
        results.suspend_updating()
        self.play(Indicate(results))
        results.resume_updating()
        self.play(
            dots.animate.scale(1.6),
            run_time=1
        )
        results.suspend_updating()
        self.play(Indicate(results))
        results.resume_updating()
        self.play(
            dots.animate.scale(0.7),
            run_time=1
        )
        self.wait()

        results.suspend_updating()
        self.play(Indicate(results))
        angle_a.suspend_updating()
        label_a.suspend_updating()
        self.wait()
        self.play(
            Indicate(angle_a),
            Indicate(label_a)
        )
        self.wait()

        self.play(
            dots[1].animate.move_to([
                get_c()[0], 
                get_c()[1] + line_b.get_length() * math.tan(56/360*2*math.pi), 
                0
            ]),
            run_time=0.5
        )
        self.play(
            dots.animate.move_to([-4, 0, 0]),
            run_time=0.5
        )

        self.play(
            Transform(sine_ratio, MathTex(r"\sin(56^\circ) =").move_to(sine_ratio))
        )
        self.play(
            Transform(cosine_ratio, MathTex(r"\cos(56^\circ) =").move_to(cosine_ratio))
        )
        self.play(
            Transform(tangent_ratio, MathTex(r"\tan(56^\circ) =").move_to(tangent_ratio))
        )

        new_theta = MathTex(r"\theta", color=BLUE).next_to(angle_a, RIGHT, buff=0.1)
        self.play(
            FadeOut(label_a),
            FadeIn(new_theta)
        )
        self.play(
            Indicate(new_theta)
        ) 
        new_theta.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))

        self.play(
            Transform(sine_ratio, MathTex(r"\sin \theta =").move_to(sine_ratio)),
            Transform(cosine_ratio, MathTex(r"\cos \theta =").move_to(cosine_ratio)),
            Transform(tangent_ratio, MathTex(r"\tan \theta =").move_to(tangent_ratio))
        )
        self.wait()

        label_d.clear_updaters()
        label_e.clear_updaters()
        label_f.clear_updaters()
        copy_d.clear_updaters()
        copy_e.clear_updaters()
        copy_f.clear_updaters()
        kopi_d.clear_updaters()
        kopi_e.clear_updaters()
        kopi_f.clear_updaters()
        self.play(
            Transform(label_d, Tex("Opp.", color=TEAL_B).move_to(label_d).rotate(-PI/2)),
            Transform(label_e, Tex("Adj.", color=GREEN).move_to(label_e)),
            Transform(label_f, Tex("Hyp.", color=GOLD).move_to(label_f).rotate(float(line_c.get_angle())))
        )

        self.play(
            Transform(
                sine_frac, 
                MathTex(
                    r"\frac{Opp.}{Hyp.}", 
                    tex_to_color_map={"Opp.": TEAL_B, "Adj.": GREEN, "Hyp.": GOLD},
                    font_size=50
                ).move_to(sine_frac).shift([-0.2, -0.05, 0])
            ),
            Transform(
                cosine_frac, 
                MathTex(
                    r"\frac{Adj.}{Hyp.}", 
                    tex_to_color_map={"Opp.": TEAL_B, "Adj.": GREEN, "Hyp.": GOLD},
                    font_size=50
                ).move_to(cosine_frac).shift([-0.2, -0.05, 0])
            ),
            Transform(
                tangent_frac, 
                MathTex(
                    r"\frac{Opp.}{Adj.}", 
                    tex_to_color_map={"Opp.": TEAL_B, "Adj.": GREEN, "Hyp.": GOLD},
                    font_size=50
                ).move_to(tangent_frac).shift([-0.2, -0.05, 0])
            ),
            Unwrite(sine_result),
            Unwrite(cosine_result),
            Unwrite(tangent_result),
            FadeOut(copy_d),
            FadeOut(kopi_d),
            FadeOut(copy_e),
            FadeOut(kopi_e),
            FadeOut(copy_f),
            FadeOut(kopi_f)
        )
        self.wait(3)

        self.play(
            Unwrite(sine_ratio),
            Unwrite(cosine_ratio),
            Unwrite(tangent_ratio),
            Unwrite(sine_frac),
            Unwrite(cosine_frac),
            Unwrite(tangent_frac)
        )
        self.wait()

        label_d.add_updater(
            lambda mob: text_label(mob, line_a, (line_a, RIGHT), 0.3, "Opp.", TEAL_B)
        )
        label_e.add_updater(
            lambda mob: text_label(mob, line_b, (line_b, DOWN), 0.3, "Adj.", GREEN)
        )
        label_f.add_updater(
            lambda mob: text_label(mob, line_c, (line_c, [0, 0, 0]), -0.3, "Hyp.", GOLD)
        )
        label_f.add_updater(lambda mob: mob.shift([-0.5, 0, 0]))

        box = Rectangle(WHITE, 3, 9).shift([2, -0.5, 0])
        title = Tex(r"Find $\sin(50^\circ)$").move_to(title)
        self.play(
            Create(box),
            Write(title),
            dots.animate.shift([-1, 0, 0])
        )
        self.wait()

        self.play(
            dots[1].animate.move_to([
                get_c()[0], 
                get_c()[1] + line_b.get_length() * math.tan(50/360*2*math.pi), 
                0
            ]),
            Transform(new_theta, MathTex(r"50^\circ", color=BLUE).next_to(angle_a, RIGHT, buff=0.1)),
            run_time=0.5
        )
        self.play(
            Indicate(new_theta)
        )
        self.wait()

        tex_ratio = MathTex(
            r"\sin(50^\circ)=\frac{Opp.}{Hyp.}=",
            tex_to_color_map={"Opp.": TEAL_B, "Adj.": GREEN, "Hyp.": GOLD},
            font_size=50
        ).next_to(box, LEFT, -4.9)
        tex_frac = MathTex(
            rf"\frac{{0.00}}{{0.00}} = {math.sin(math.radians(50)):.5f}",
            color=BLUE_C,
            tex_to_color_map={"0.00": BLACK}
        ).next_to(box, RIGHT, -3.8).shift([0, 0.05, 0]).set_z_index(-1)

        self.play(
            Write(tex_ratio)
        )

        label_d.clear_updaters()
        label_e.clear_updaters()
        label_f.clear_updaters()
        self.play(
            Transform(
                label_d,
                MathTex(f"{line_a.get_length():.2f}", color=TEAL_B)
                .move_to(label_d)
                .rotate(-PI/2)
            ),
            Transform(
                label_e,
                MathTex(f"{line_b.get_length():.2f}", color=GREEN)
                .move_to(label_e)
            ),
            Transform(
                label_f,
                MathTex(f"{line_c.get_length():.2f}", color=GOLD)
                .move_to(label_f)
                .rotate(float(line_c.get_angle()))
            )
        )

        copy_d = label_d.copy().clear_updaters()
        copy_f = label_f.copy().clear_updaters()

        self.add(copy_d, copy_f)

        self.play(
            Write(tex_frac),
            copy_d.animate.move_to(tex_frac.get_center() + [-1.2, 0.35, 0]).rotate(PI/2),
            copy_f.animate.move_to(tex_frac.get_center() + [-1.2, -0.4, 0]).rotate(-float(line_c.get_angle()))
        )

        label_d.add_updater(
            lambda mob: length_label(mob, line_a, (line_a, RIGHT), 0.3, TEAL_B)
        )
        label_e.add_updater(
            lambda mob: length_label(mob, line_b, (line_b, DOWN), 0.3, GREEN)
        )
        label_f.add_updater(
            lambda mob: length_label(mob, line_c, (line_c, [0, 0, 0]), -0.3, GOLD)
        )
        label_f.add_updater(lambda mob: mob.shift([-0.5, 0, 0]))

        copy_d.add_updater(
            lambda mob: mob.become(
                Tex(f"{line_a.get_length():.2f}", color=TEAL_B).move_to(
                    tex_frac.get_center() + [-1.2, 0.35, 0]
                )
            )
        )
        copy_f.add_updater(
            lambda mob: mob.become(
                Tex(f"{line_c.get_length():.2f}", color=GOLD).move_to(
                    tex_frac.get_center() + [-1.2, -0.4, 0]
                )
            )
        )
        new_theta.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))

        self.play(
            dots.animate.scale(1.6),
            rate_func=there_and_back,
            run_time=2
        )
        self.wait()

        self.play(
            Unwrite(new_theta),
            Unwrite(label_d),
            Unwrite(label_e),
            Unwrite(label_f),
            Unwrite(title),
            Unwrite(tex_frac),
            Unwrite(tex_ratio),
            Uncreate(box),
            Unwrite(copy_d),
            Unwrite(copy_f)
        )
        self.play(
            dots[0].animate.move_to([-5.5, -2.0, 0]),
            dots[1].animate.move_to([-2.5, 2.0, 0]),
            dots[2].animate.move_to([-2.5, -2.0, 0])
        )
        self.wait()