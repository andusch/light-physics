from manim import *
import numpy as np

class PhotonicModel(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        
        title = Text("Modelul Fotonic al Luminii", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.play(Write(title))
        
        energy_formula = MathTex(
            r"E = h\nu = \frac{hc}{\lambda}",
            font_size=32
        ).next_to(title, DOWN, buff=0.3)
        self.play(Write(energy_formula))
        
        # Constante
        h = 6.626e-34  # Constanta lui Planck (J·s)
        c = 3e8         # Viteza luminii (m/s)
        
        colors_data = [
            ("Roșu", 650e-9, RED, -2),
            ("Verde", 550e-9, GREEN, 0),
            ("Albastru", 450e-9, BLUE, 2)
        ]
        
        source = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8)
        source.shift(LEFT * 5)
        source_label = Text("Sursă", font_size=18).next_to(source, DOWN)
        
        self.play(Create(source), Write(source_label))
        
        info_group = VGroup()
        for color_name, wavelength, color, y_offset in colors_data:
            energy = (h * c) / wavelength  # Energie foton (J)
            energy_eV = energy / 1.602e-19  # Convertire în eV
            
            info_text = VGroup(
                Text(f"{color_name}:", font_size=20, color=color),
                MathTex(f"\\lambda = {wavelength*1e9:.0f} \, \\text{{nm}}", font_size=18),
                MathTex(f"E = {energy_eV:.2f} \, \\text{{eV}}", font_size=18)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            
            info_group.add(info_text)
            
        info_group.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        info_box = SurroundingRectangle(info_group, color=WHITE, buff=0.3)
        info_with_box = VGroup(info_box, info_group).to_corner(UR)
        
        self.play(Create(info_box), Write(info_group))
        self.wait(2)
        
        for color_name, wavelength, color, y_offset in colors_data:
            photons = VGroup()
            
            for i in range(8):
                photon = Circle(radius = 0.08, color=color, fill_opacity=0.9)
                photon.shift(LEFT * 5 + UP * y_offset)
                photons.add(photon)
                
            self.play(
                *[photon.animate.shift(RIGHT * 11).set_opacity(0) 
                  for photon in photons],
                lag_ratio=0.15,
                run_time=2
            )
        self.wait(2)
