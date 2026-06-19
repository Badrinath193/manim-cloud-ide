"""Example Manim scene for the cloud IDE."""
from manim import *


class CircleToSquare(Scene):
    """A beautiful animation transforming a circle to a square."""

    def construct(self):
        # Create a circle
        circle = Circle(fill_opacity=0.5, color=BLUE)
        circle.shift(LEFT * 2)

        # Create a square
        square = Square(fill_opacity=0.5, color=ORANGE)
        square.shift(RIGHT * 2)

        # Create labels
        circle_label = Text("Circle", font_size=36).next_to(circle, DOWN)
        square_label = Text("Square", font_size=36).next_to(square, DOWN)

        # Animation sequence
        self.play(Write(circle), Write(circle_label))
        self.wait(0.5)

        # Transform circle to square
        self.play(
            Transform(circle.copy().set_color(ORANGE), square),
            circle.animate.set_opacity(0),
            circle_label.animate.next_to(square, DOWN),
            Write(square_label),
            run_time=2
        )

        # Add some flair with a rotation
        self.play(Rotate(square, angle=TAU), run_time=2)

        # Final message
        message = Text("Manim in the Cloud! 🎬", font_size=48, color=GOLD)
        message.to_edge(UP, buff=0.5)
        self.play(Write(message), run_time=1.5)

        self.wait(2)


class MathematicalFunction(Scene):
    """Plot a mathematical function with beautiful styling."""

    def construct(self):
        # Axes configuration
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-2, 2, 1],
            x_length=6,
            y_length=4,
            axis_config={"include_tip": True},
        )

        # Labels
        labels = axes.get_axis_labels(
            x_label="x",
            y_label="f(x)"
        )

        # Graph the function
        graph = axes.plot(
            lambda x: x**2 - 1,
            x_range=[-2.5, 2.5],
            color=BLUE,
        )

        # Graph area
        area = axes.get_area(graph, x_range=[-2, 2], color=BLUE, opacity=0.3)

        # Create the scene
        self.play(Create(axes), Write(labels))
        self.play(Create(graph))
        self.play(FadeIn(area))

        # Add a moving point
        dot = Dot(color=RED)
        dot.move_to(graph.point_from_proportion(0))

        def update_dot(mob, alpha):
            x = -2 + alpha * 4
            y = x**2 - 1
            mob.move_to(axes.c2p(x, y))

        self.play(
            UpdateFromAlphaFunc(dot, update_dot),
            run_time=3,
            rate_func=linear
        )

        self.wait(2)