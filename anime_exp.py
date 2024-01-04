from manim import *

class FunctionTransform(Scene):
    def construct(self):
        # Create axes
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-1, 5],
            axis_config={"color": BLUE},
        )

        # Create a function curve
        func_curve = axes.plot(lambda x: x**2, color=WHITE)

        # Add axes and curve to the scene
        self.play(Create(axes), Create(func_curve))

        # Define the transformation
        def transform(x):
            return x**3 - x**2 + x + 1

        # Apply the transformation to the curve
        transformed_curve = axes.plot(transform, color=YELLOW)

        # Animate the transformation
        self.play(Transform(func_curve, transformed_curve))
        self.wait(2)
