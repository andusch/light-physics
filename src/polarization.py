from manim import *
import numpy as np

class Polarization(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        
        title = Text("Polarizarea Luminii", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Legea lui Malus
        malus_law = MathTex(
            r"I = I_0 \cos^2(\theta)",
            font_size=32
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(malus_law))
        
        # Lumină nepolarizată
        unpolarized_source = Circle(radius=0.2, color=YELLOW, fill_opacity=0.8)
        unpolarized_source.shift(LEFT * 5)
        
        # Săgeți în toate direcțiile pentru lumină nepolarizată
        arrows_unpolarized = VGroup()
        for angle in np.linspace(0, 2*np.pi, 8, endpoint=False):
            arrow = Arrow(
                start=unpolarized_source.get_center(),
                end=unpolarized_source.get_center() + 0.6 * np.array([np.cos(angle), np.sin(angle), 0]),
                color=YELLOW,
                stroke_width=2,
                buff=0.2,
                max_tip_length_to_length_ratio=0.2
            )
            arrows_unpolarized.add(arrow)
        
        unpolarized_label = Text("Nepolarizată", font_size=16).next_to(unpolarized_source, DOWN)
        
        self.play(
            Create(unpolarized_source),
            *[GrowArrow(arrow) for arrow in arrows_unpolarized],
            Write(unpolarized_label)
        )
        self.wait(1)
        
        # Polarizator 1 (vertical)
        polarizer1 = Rectangle(
            height=2, width=0.15,
            color=BLUE,
            fill_opacity=0.5
        ).shift(LEFT * 2.5)
        
        polarizer1_lines = VGroup(*[
            Line(UP * 0.9, DOWN * 0.9, stroke_width=1, color=BLUE)
            .shift(LEFT * 2.5 + RIGHT * 0.05 * i)
            for i in range(-2, 3)
        ])
        
        polarizer1_label = Text("Polarizator\n(0°)", font_size=14, color=BLUE).next_to(polarizer1, DOWN, buff=0.3)
        
        self.play(
            Create(polarizer1),
            Create(polarizer1_lines),
            Write(polarizer1_label)
        )
        self.wait(0.5)
        
        # Lumină polarizată vertical
        polarized_arrow = Arrow(
            start=LEFT * 2.5,
            end=LEFT * 2.5 + UP * 0.8,
            color=GREEN,
            stroke_width=4,
            buff=0.1
        )
        polarized_arrow2 = Arrow(
            start=LEFT * 2.5,
            end=LEFT * 2.5 + DOWN * 0.8,
            color=GREEN,
            stroke_width=4,
            buff=0.1
        )
        
        self.play(GrowArrow(polarized_arrow), GrowArrow(polarized_arrow2))
        self.wait(0.5)
        
        # Propagare către polarizator 2
        moving_arrows = VGroup(polarized_arrow.copy(), polarized_arrow2.copy())
        self.play(moving_arrows.animate.shift(RIGHT * 2.5), run_time=1)
        self.remove(moving_arrows)
        
        # Polarizator 2 (la unghi θ)
        theta_tracker = ValueTracker(0)
        
        polarizer2 = always_redraw(
            lambda: Rectangle(
                height=2, width=0.15,
                color=ORANGE,
                fill_opacity=0.5
            ).rotate(theta_tracker.get_value() * DEGREES).shift(RIGHT * 0.5)
        )
        
        polarizer2_lines = always_redraw(
            lambda: VGroup(*[
                Line(UP * 0.9, DOWN * 0.9, stroke_width=1, color=ORANGE)
                .rotate(theta_tracker.get_value() * DEGREES)
                .shift(RIGHT * 0.5 + 0.05 * i * np.array([
                    np.cos(theta_tracker.get_value() * DEGREES + PI/2),
                    np.sin(theta_tracker.get_value() * DEGREES + PI/2),
                    0
                ]))
                for i in range(-2, 3)
            ])
        )
        
        angle_display = always_redraw(
            lambda: MathTex(
                f"\\theta = {theta_tracker.get_value():.0f}°",
                font_size=24,
                color=ORANGE
            ).next_to(polarizer2, DOWN, buff=0.5)
        )
        
        self.play(
            Create(polarizer2),
            Create(polarizer2_lines),
            Write(angle_display)
        )
        
        # Intensitate ieșire
        intensity_display = always_redraw(
            lambda: MathTex(
                f"I = I_0 \\cos^2({theta_tracker.get_value():.0f}°) = {np.cos(theta_tracker.get_value() * DEGREES)**2:.2f} I_0",
                font_size=20,
                color=GREEN
            ).to_corner(DR)
        )
        self.play(Write(intensity_display))
        
        # Lumină ieșită (proporțională cu intensitatea)
        output_arrows = always_redraw(
            lambda: VGroup(
                Arrow(
                    start=RIGHT * 0.5,
                    end=RIGHT * 0.5 + UP * 0.8 * np.cos(theta_tracker.get_value() * DEGREES)**2,
                    color=GREEN,
                    stroke_width=4,
                    buff=0.1
                ) if np.cos(theta_tracker.get_value() * DEGREES)**2 > 0.05 else VMobject(),
                Arrow(
                    start=RIGHT * 0.5,
                    end=RIGHT * 0.5 + DOWN * 0.8 * np.cos(theta_tracker.get_value() * DEGREES)**2,
                    color=GREEN,
                    stroke_width=4,
                    buff=0.1
                ) if np.cos(theta_tracker.get_value() * DEGREES)**2 > 0.05 else VMobject()
            )
        )
        self.add(output_arrows)
        
        # Rotație polarizator
        self.play(
            theta_tracker.animate.set_value(90),
            run_time=4,
            rate_func=linear
        )
        self.wait(1)
        
        self.play(
            theta_tracker.animate.set_value(0),
            run_time=2,
            rate_func=linear
        )
        
        self.wait(2)

