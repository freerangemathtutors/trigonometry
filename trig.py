from manim import *
import copy

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
        line_a.add_updater(lambda mob: mob.become(Line(get_b(), get_c())))
        line_b.add_updater(lambda mob: mob.become(Line(get_a(), get_c())))
        line_c.add_updater(lambda mob: mob.become(Line(get_a(), get_b())))

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

        label_a = MathTex(r"a", color=BLUE).set_opacity(0)
        label_b = MathTex(r"b", color=RED).set_opacity(0)
        label_c = MathTex(r"90^\circ", color=WHITE)
        label_d = Tex(r"Opposite", color=WHITE).set_opacity(0)
        label_e = Tex(r"Adjacent", color=WHITE).set_opacity(0)
        label_f = Tex(r"Hypotenuse", color=WHITE)
        label_same = Tex(r"Similar!", color=YELLOW)
        label_prop = Tex(r"Proportions!", color=YELLOW)
        detour_box = Rectangle(WHITE, 6, 10)
        detour_label = Tex(r"Naming the sides:")

        label_a.next_to(angle_a, RIGHT, buff=0.1)
        label_b.next_to(angle_b, DOWN, buff=0.1)
        label_c.next_to(angle_c, UP + LEFT, buff=0.1)
        label_d.next_to(line_a, RIGHT, buff=0.3)
        label_e.next_to(line_b, DOWN, buff=0.3)
        label_f.next_to(line_c, LEFT, buff=0.1)
        label_f.shift([0.5, 0, 0])
        label_same.shift([0, -3, 0])
        label_prop.shift([0, -3, 0])
        detour_box.shift([0, -0.67, 0])
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
            angle_a.animate.set_opacity(1),
            angle_b.animate.set_opacity(1),
            angle_d.animate.set_opacity(1),
            angle_e.animate.set_opacity(1),
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

        self.play(TransformMatchingShapes(label_same, label_prop))
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
            Unwrite(label_prop),
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

        label_d.set_opacity(1)
        label_e.set_opacity(1)

        self.play(Write(label_d))
        self.wait()

        self.play(Write(label_e))
        self.wait(1.5)

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
                    *(pos.animate.shift([-3.5, 0, 0]) for pos in dots), 
                    lag_ratio=0
                ),
                lag_ratio=0.5
            )
        )
        self.wait()


class Similarity(Scene):
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
        line_a.add_updater(lambda mob: mob.become(Line(get_b(), get_c())))
        line_b.add_updater(lambda mob: mob.become(Line(get_a(), get_c())))
        line_c.add_updater(lambda mob: mob.become(Line(get_a(), get_b())))

        big_tri = Polygon(get_a(), get_b(), get_c(), color=WHITE, stroke_width=4)

        def update_triangle(mob):
            mob.set_points_as_corners([get_a(), get_b(), get_c(), get_a()])

        big_tri.add_updater(update_triangle)

        angle_a = Angle(line_b, line_c, radius=0.7, color=BLUE).set_opacity(0)
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

        label_a = MathTex(r"a", color=BLUE)
        label_b = MathTex(r"\phi", color=RED)
        label_c = MathTex(r"90^\circ", color=WHITE)
        label_d = Tex(r"Opposite", color=WHITE)
        label_e = Tex(r"Adjacent", color=WHITE)
        label_f = Tex(r"Hypotenuse", color=WHITE)
        label_opp = Tex(r"Opp.", color=WHITE)
        label_adj = Tex(r"Adj.", color=WHITE)
        label_hyp = Tex(r"Hyp.", color=WHITE)
        label_same = Tex(r"Similar!", color=YELLOW)
        label_angle = MathTex(r"0^\circ", color=BLUE)

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
        label_same.shift([0, -3, 0])

        label_a.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))
        label_b.add_updater(lambda mob: mob.next_to(angle_b, DOWN, buff=0.1))
        label_c.add_updater(lambda mob: mob.next_to(angle_c, UP + LEFT, buff=0.1))
        label_opp.add_updater(lambda mob: mob.next_to(angle_a, RIGHT, buff=0.1))
        label_adj.add_updater(lambda mob: mob.next_to(angle_b, DOWN, buff=0.1))
        label_hyp.add_updater(lambda mob: mob.next_to(angle_c, UP + LEFT, buff=0.1))

        def length_label(label, line, location, buff):
            label.become(MathTex(f"{line.get_length():.2f}"))
            label.rotate(line.get_angle())
            label.next_to(*location, buff=buff)

        def text_label(label, line, location, buff, text):
            label.become(MathTex(text))
            label.rotate(line.get_angle())
            label.next_to(*location, buff=buff)

        label_d.add_updater(
            lambda mob: length_label(mob, line_a, (line_a, RIGHT), 0.3)
        )
        label_e.add_updater(
            lambda mob: length_label(mob, line_b, (line_b, DOWN), 0.3)
        )
        label_f.add_updater(
            lambda mob: length_label(mob, line_c, (line_c, [0, 0, 0]), -0.3)
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

        tri_copy = big_tri.copy()
        tri_copy.clear_updaters()
        
        self.add(big_tri, line_a, line_b, line_c, angle_a, label_a, angle_c)
        for pos in dots:
            pos.shift([-3.0, 0, 0])
        tri_copy.shift([-3.0, 0, 0])

        self.play(
            tri_copy.animate.shift([6.0, 0, 0]),
            FadeOut(angle_a),
            FadeOut(angle_c),
            FadeOut(label_a),
            run_time=0.5
        )
        self.wait(0.1)
        self.play(
            dots.animate.scale(1.25),
            tri_copy.animate.scale(0.8)
        )
        self.wait()
        self.play(
            dots.animate.scale(0.8),
            tri_copy.animate.scale(1.25)
        )
        self.play(
            tri_copy.animate.shift([-6.5, 0, 0]),
            dots.animate.shift([-0.5, 0, 0]),
            # dots[1].animate.shift([0, -0.0068, 0])
        )
        label_angle.become(MathTex(r"53^\circ", color=BLUE))
        self.remove(tri_copy)
        self.wait()

        label_a.clear_updaters()
        self.play(
            FadeIn(angle_a),
            FadeIn(angle_c),
            FadeIn(label_angle),
            Write(label_d),
            Write(label_e),
            Write(label_f)
        )
        self.wait()

        self.play(dots.animate.scale(1.25), run_time=2)
        self.play(dots.animate.scale(0.8), run_time=2)
        self.play(dots.animate.scale(0.8), run_time=2)
        self.play(dots.animate.scale(1.25), run_time=2)

        copy_d = label_d.copy().clear_updaters()
        copy_e = label_e.copy().clear_updaters()
        copy_f = label_f.copy().clear_updaters()
        label_d.clear_updaters()
        label_e.clear_updaters()
        label_f.clear_updaters()
        
        self.play(
            label_d.animate.move_to([1.0, 2.0, 0]).rotate(PI / 2),
            copy_d.animate.move_to([1.0, 1.0, 0]).rotate(PI / 2),
            label_e.animate.move_to([2.0, 2.0, 0]),
            copy_e.animate.move_to([2.0, 1.0, 0]),
            label_f.animate.move_to([3.0, 2.0, 0]).rotate(-float(line_c.get_angle())),
            copy_f.animate.move_to([3.0, 1.0, 0]).rotate(-float(line_c.get_angle())),
        )

        label_d.add_updater(lambda mob: mob.become(MathTex(f"{line_a.get_length():.2f}")))
        label_d.add_updater(lambda mob: mob.become(MathTex(f"{line_b.get_length():.2f}")))
        label_d.add_updater(lambda mob: mob.become(MathTex(f"{line_c.get_length():.2f}")))
        copy_d.add_updater(lambda mob: mob.become(MathTex(f"{line_a.get_length():.2f}")))
        copy_e.add_updater(lambda mob: mob.become(MathTex(f"{line_b.get_length():.2f}")))
        copy_f.add_updater(lambda mob: mob.become(MathTex(f"{line_c.get_length():.2f}")))


