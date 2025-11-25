from manim import *
import numpy as np

class Reflection(Scene):
    def construct(self):
        self.camera.background_color = '#0a0a0a'
        
        title = Text("Reflexia Luminii", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        law = MathTex(
            r"\theta_i = \theta_r",
            font_size=32
        )
        law.next_to(title, DOWN, buff=0.3)
        self.play(Write(law))
        
        # Suprafață și normală
        surface = Line(LEFT * 5, RIGHT * 5, color=WHITE, stroke_width=3).shift(DOWN * 1)
        normal = DashedLine(
            start=ORIGIN + DOWN * 1,
            end=ORIGIN + UP * 2,
            color=GRAY,
            stroke_width=2
        )
        
        self.play(Create(surface), Create(normal))
        
        # Punctul de incidență
        incident_point = Dot(ORIGIN + DOWN * 1, color=RED, radius=0.08)
        
        # Raze - cu direcții corecte
        incident_start = LEFT * 2.5 + UP * 1.5
        incident_end = ORIGIN + DOWN * 1
        
        reflected_end = RIGHT * 2.5 + UP * 1.5
        
        incident_ray = Arrow(
            start=incident_start,
            end=incident_end,
            color=YELLOW,
            stroke_width=4,
            buff=0
        )
        
        reflected_ray = Arrow(
            start=incident_end,
            end=reflected_end,
            color=ORANGE,
            stroke_width=4,
            buff=0
        )
        
        self.play(Create(incident_point))
        self.play(GrowArrow(incident_ray))
        self.wait(0.5)
        self.play(GrowArrow(reflected_ray))
        
        # Unghiuri - folosim metoda from_three_points pentru control precis
        # Pentru unghiul incident: de la start incident_ray, prin punctul de incidență, la vârful normalei
        angle_incident = Angle.from_three_points(
            incident_start,  # punct pe raza incidentă
            incident_end,    # punct de incidență (vârful unghiului)
            ORIGIN + UP * 2, # vârful normalei
            radius=0.7,
            color=YELLOW,
            other_angle=True
        )
        
        # Pentru unghiul reflectat: de la vârful normalei, prin punctul de incidență, la end reflected_ray
        angle_reflected = Angle.from_three_points(
            ORIGIN + UP * 2, # vârful normalei
            incident_end,    # punct de incidență (vârful unghiului)
            reflected_end,   # punct pe raza reflectată
            radius=0.7,
            color=ORANGE,
            other_angle=True
        )
        
        self.play(Create(angle_incident), Create(angle_reflected))
        
        angle_i_label = MathTex(r"\theta_i", font_size=24, color=YELLOW).next_to(angle_incident, LEFT, buff=0.2)
        angle_r_label = MathTex(r"\theta_r", font_size=24, color=ORANGE).next_to(angle_reflected, RIGHT, buff=0.2)
        
        self.play(Write(angle_i_label), Write(angle_r_label))
        self.wait(2)

