from manim import *


class TwoPlusTwo(Scene):
    def construct(self):
        title = Text("Basic Addition", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))

        equation = MathTex("2", "+", "2", "=", "4", font_size=96)
        two_left, plus, two_right, equals, four = equation
        equation.move_to(UP * 0.5)

        self.play(Write(two_left), Write(plus), Write(two_right))
        self.wait(0.3)

        left_dots = VGroup(*[Dot(radius=0.15, color=BLUE) for _ in range(2)])
        left_dots.arrange(RIGHT, buff=0.3)
        right_dots = VGroup(*[Dot(radius=0.15, color=BLUE) for _ in range(2)])
        right_dots.arrange(RIGHT, buff=0.3)

        left_dots.next_to(two_left, DOWN, buff=1.2)
        right_dots.next_to(two_right, DOWN, buff=1.2)

        self.play(FadeIn(left_dots), FadeIn(right_dots))
        self.wait(0.5)

        self.play(Write(equals))

        all_dots = VGroup(*left_dots, *right_dots)
        target_row = VGroup(*[d.copy() for d in all_dots])
        target_row.arrange(RIGHT, buff=0.3)
        target_row.next_to(four, DOWN, buff=1.2)

        self.play(
            *[
                dot.animate.move_to(target.get_center())
                for dot, target in zip(all_dots, target_row)
            ]
        )
        self.play(Write(four))

        result_box = SurroundingRectangle(four, color=YELLOW)
        self.play(Create(result_box))
        self.wait(1)

        self.play(FadeOut(VGroup(title, equation, result_box, all_dots)))
        self.wait(0.5)
