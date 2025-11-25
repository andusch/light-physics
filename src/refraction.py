from manim import *
import numpy as np

class Refraction(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        
        title = Text("Refracția Luminii - Legea lui Snell", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        snell_law = MathTex(
            r"n_1 \sin\theta_1 = n_2 \sin\theta_2",
            font_size=32
        )
        snell_law.next_to(title, DOWN, buff=0.3)
        self.play(Write(snell_law))
        
        # Interfața
        interface = Line(LEFT * 6, RIGHT * 6, color=WHITE, stroke_width=3)
        
        # Medii
        medium1 = Rectangle(
            height=3, width=12, 
            fill_color=BLUE, fill_opacity=0.2,
            stroke_color=BLUE, stroke_width=2
        ).shift(UP * 1.5)
        
        medium2 = Rectangle(
            height=3, width=12,
            fill_color=GREEN, fill_opacity=0.3,
            stroke_color=GREEN, stroke_width=2
        ).shift(DOWN * 1.5)
        
        medium1_label = Text("Aer (n₁ = 1.0)", font_size=18, color=BLUE).move_to(UP * 2.3 + LEFT * 4)
        medium2_label = Text("Sticlă (n₂ = 1.5)", font_size=18, color=GREEN).move_to(DOWN * 2.3 + LEFT * 4)
        
        self.play(
            Create(medium1), Create(medium2),
            Write(medium1_label), Write(medium2_label),
            Create(interface)
        )
        
        self.wait(1)
        
        # Normala
        normal = DashedLine(UP * 2.2, DOWN * 2.2, color=GRAY, stroke_width=2)
        self.play(Create(normal))
        
        # Parametri
        n1, n2 = 1.0, 1.5
        theta1_deg = 45
        theta1 = theta1_deg * DEGREES
        theta2 = np.arcsin((n1 / n2) * np.sin(theta1))
        
        # Punct de refracție
        refraction_point = Dot(ORIGIN, color=RED, radius=0.08)
        
        # Rază incidentă
        incident_length = 2.5
        incident_start = LEFT * incident_length * np.sin(theta1) + UP * incident_length * np.cos(theta1)
        
        incident_ray = Arrow(
            start=incident_start,
            end=ORIGIN,
            color=YELLOW,
            stroke_width=4,
            buff=0
        )
        
        # Rază refractată
        refracted_length = 2.5
        refracted_end = RIGHT * refracted_length * np.sin(theta2) + DOWN * refracted_length * np.cos(theta2)
        
        refracted_ray = Arrow(
            start=ORIGIN,
            end=refracted_end,
            color=ORANGE,
            stroke_width=4,
            buff=0
        )
        
        self.play(Create(refraction_point))
        self.play(GrowArrow(incident_ray))
        self.wait(0.5)
        self.play(GrowArrow(refracted_ray))
        
        # Unghiuri - folosim from_three_points pentru control precis
        angle1 = Angle.from_three_points(
            incident_start,  # punct pe raza incidentă
            ORIGIN,          # punct de refracție (vârful unghiului)
            ORIGIN + UP * 2.5, # vârful normalei
            radius=0.8,
            color=YELLOW,
            other_angle = True
        )
        
        angle2 = Angle.from_three_points(
            ORIGIN + DOWN * 2.5, # baza normalei
            ORIGIN,              # punct de refracție (vârful unghiului)
            refracted_end,       # punct pe raza refractată
            radius=0.8,
            color=ORANGE
        )
        
        angle1_label = MathTex(r"\theta_1 = 45°", font_size=20, color=YELLOW).next_to(angle1, LEFT, buff=0.3)
        angle2_label = MathTex(f"\\theta_2 = {np.degrees(theta2):.1f}°", font_size=20, color=ORANGE).next_to(angle2, RIGHT, buff=0.3)
        
        self.play(Create(angle1), Create(angle2))
        self.play(Write(angle1_label), Write(angle2_label))
        
        # Info
        n_text = VGroup(
            MathTex(f"n_1 = {n1}", font_size=24, color=BLUE),
            MathTex(f"n_2 = {n2}", font_size=24, color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        
        self.play(Write(n_text))
        