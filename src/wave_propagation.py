from manim import *
import numpy as np

class WavePropagation1D(Scene):
    # Constructia scenei
    def construct(self):
        self.camera.background_color = '#0a0a0a'
        title = Text("Propagare Luminii 1D", 
                    font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Formula undei electromagnetice
        wave_formula = MathTex(
            r"E(x,t) = E_0 \sin\left[2\pi\left(\frac{t}{T} - \frac{x}{\lambda}\right)\right]",
            font_size=32
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(wave_formula))
        self.wait(2)
        
        # Parametri undă
        E0 = 1.0
        wavelength = 2.0
        T = 2.0
        nu = 1.0 / T
        c = wavelength / T
        
        # Parametri afișați
        params_group = VGroup(
            MathTex(rf"E_0 = {E0:.1f}", font_size=24, color=BLUE),
            MathTex(rf"\lambda = {wavelength:.1f} \, \text{{m}}", font_size=24, color=GREEN),
            MathTex(rf"T = {T:.1f} \, \text{{s}}", font_size=24, color=ORANGE),
            MathTex(rf"\nu = \frac{{1}}{{T}} = {nu:.1f} \, \text{{Hz}}", font_size=24, color=PURPLE),
            MathTex(rf"c = \lambda \nu = {c:.1f} \, \text{{m/s}}", font_size=24, color=RED)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        params_box = SurroundingRectangle(params_group, color=WHITE, buff=0.2)
        params_with_box = VGroup(params_box, params_group)
        params_with_box.to_corner(UL).shift(DOWN * 1.5)

        self.play(Create(params_box), Write(params_group))
        self.wait(2)
        
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=8,
            y_length=4,
            axis_config={"color": GREY, "stroke_width": 2},
            tips=False
        ).shift(DOWN * 0.5)
        
        x_label = MathTex("x (m)}", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("E(x,t)", font_size=24).next_to(axes.y_axis, UP)
        
        self.play(Create(axes), Write(x_label), Write(y_label))
        self.wait(2)

        t_tracker = ValueTracker(0)
        time_display = always_redraw(
            lambda: MathTex(
                f"t = {t_tracker.get_value():.2f} \, \\text{{s}}",
                font_size=28,
                color=YELLOW
            ).next_to(axes, DOWN, buff=0.3)
        )
        self.add(time_display)
        
        def wave_function(x, t):
            return E0 * np.sin(2 * np.pi * (t / T - x / wavelength))
        
        wave_graph = always_redraw(
            lambda: axes.plot(
                lambda x: wave_function(x, t_tracker.get_value()),
                color=BLUE,
                stroke_width=4
            )
        )
        
        self.play(Create(wave_graph))
        
        speed_vector = always_redraw(
            lambda: Arrow(
                start=axes.c2p(2, 1.2),
                end=axes.c2p(3, 1.2),
                color=RED,
                buff=0,
                stroke_width=3
            )
        )
        
        speed_label = always_redraw(
            lambda: MathTex(
                f"v = {c:.1f} \, \\text{{m/s}}",
                font_size=20,
                color=RED
            ).next_to(speed_vector, UP, buff=0.1)
        )

        self.play(Create(speed_vector), Write(speed_label))
        
        self.play(
            t_tracker.animate.set_value(3 * T),
            rate_func = linear,
            run_time = 7
        )
        
        self.wait(2)
        
