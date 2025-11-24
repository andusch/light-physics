from manim import *
import numpy as np

# Propagare luminii 1D
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
        
# Reflexie
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
      
# Refracție  
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
        

class Interference(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        
        title = Text("Interferența Luminii în 3D", font_size=36, color=YELLOW)
        title.to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # Setup camerei 3D
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        
        # Axe 3D
        axes = ThreeDAxes(
            x_range=[-4, 4, 1],
            y_range=[-4, 4, 1],
            z_range=[-2, 2, 0.5],
            x_length=8,
            y_length=8,
            z_length=4,
            axis_config={"color": GREY}
        )
        
        # Etichete axe
        x_label = MathTex("x", font_size=24).next_to(axes.x_axis, RIGHT)
        y_label = MathTex("y", font_size=24).next_to(axes.y_axis, UP)
        z_label = MathTex("z", font_size=24).next_to(axes.z_axis, OUT)
        
        self.play(Create(axes), Write(x_label), Write(y_label), Write(z_label))
        
        # Poziții surse
        source1_pos = np.array([-1.5, 0, 0])
        source2_pos = np.array([1.5, 0, 0])
        
        # Surse ca sfere
        source1 = Sphere(radius=0.15, color=YELLOW).move_to(source1_pos)
        source2 = Sphere(radius=0.15, color=YELLOW).move_to(source2_pos)
        
        source1.set_fill(YELLOW, opacity=0.8)
        source2.set_fill(YELLOW, opacity=0.8)
        
        self.play(Create(source1), Create(source2))
        
        # Parametri undă
        wavelength = 1.5
        k = 2 * np.pi / wavelength
        omega = 1.0
        amplitude = 0.3  # Factor de amplitudine redus
        
        # Funcție pentru calculul interferenței
        def interference_wave(u, v, time):
            x = u
            y = v
            
            # Distanțe de la surse
            r1 = np.sqrt((x - source1_pos[0])**2 + (y - source1_pos[1])**2)
            r2 = np.sqrt((x - source2_pos[0])**2 + (y - source2_pos[1])**2)
            
            # Unde de la fiecare sursă (cu atenuare și amplitudine redusă)
            wave1 = amplitude * np.cos(k * r1 - omega * time) / (1 + r1 * 0.3)
            wave2 = amplitude * np.cos(k * r2 - omega * time) / (1 + r2 * 0.3)
            
            # Suprapunere
            return wave1 + wave2
        
        # Time tracker
        time_tracker = ValueTracker(0)
        
        # Suprafață parametrică pentru interferență
        surface = always_redraw(
            lambda: Surface(
                lambda u, v: axes.c2p(u, v, interference_wave(u, v, time_tracker.get_value())),
                u_range=[-3.5, 3.5],
                v_range=[-3.5, 3.5],
                resolution=(40, 40),
                fill_opacity=0.8,
                checkerboard_colors=[BLUE_D, BLUE_E],
                stroke_color=BLUE,
                stroke_width=0.5
            )
        )
        
        self.play(Create(surface), run_time=2)
        
        # Rotație camerei în timp ce unda se propagă
        self.begin_ambient_camera_rotation(rate=0.15)
        
        # Animație propagare undă
        self.play(
            time_tracker.animate.set_value(8),
            rate_func=linear,
            run_time=10
        )
        
        self.stop_ambient_camera_rotation()
        
        self.wait(2)
        
        # Explicație finală
        explanation = VGroup(
            Text("Pattern de interferență:", font_size=18, color=YELLOW),
            Text("Zonele înalte = interferență constructivă", font_size=14, color=WHITE),
            Text("Zonele joase = interferență destructivă", font_size=14, color=WHITE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        explanation.to_corner(DL)
        self.add_fixed_in_frame_mobjects(explanation)
        self.play(Write(explanation))
        
        self.wait(2)
        
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


# 4. Experimentul Double Slit (Young)
class DoubleSlit(Scene):
    def construct(self):
        self.camera.background_color = "#0a0a0a"
        
        # Titlu
        title = Text("Experimentul Double Slit - Mecanică Cuantică", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=0.2)
        self.play(Write(title), run_time=1)
        
        # Formula principală - ecuația lui Schrödinger
        formula = MathTex(
            r"\Psi(x,y,t) = \Psi_1(x,y,t) + \Psi_2(x,y,t)",
            font_size=24
        ).next_to(title, DOWN, buff=0.15)
        self.play(Write(formula), run_time=1)
        
        # Parametri fizici
        wavelength = 0.5  # lungime de undă (unități arbitrare)
        k = 2 * np.pi / wavelength  # număr de undă
        omega = k  # frecvență angulară
        slit_separation = 1.5
        slit_width = 0.2
        
        # Poziții
        source_x = -5
        barrier_x = -2
        screen_x = 3
        
        # === PARTEA 1: Setup experimental ===
        
        # Sursă cuantică
        source = Circle(radius=0.15, color=YELLOW, fill_opacity=0.9)
        source.shift(LEFT * 5 + UP * 0.5)
        source_glow = Circle(radius=0.25, color=YELLOW, fill_opacity=0.3, stroke_width=0)
        source_glow.move_to(source.get_center())
        source_label = Text("Sursă\nfoton", font_size=11).next_to(source, DOWN, buff=0.15)
        
        self.play(
            FadeIn(source_glow),
            Create(source),
            Write(source_label),
            run_time=1
        )
        
        # Bariera cu fante
        barrier_height = 4
        
        # Partea de sus a barierei
        barrier_top = Rectangle(
            height=1.25,
            width=0.15,
            color=WHITE,
            fill_opacity=0.95
        ).shift(LEFT * 2 + UP * 2.1)
        
        # Partea de jos a barierei
        barrier_bottom = Rectangle(
            height=1.25,
            width=0.15,
            color=WHITE,
            fill_opacity=0.95
        ).shift(LEFT * 2 + DOWN * 2.1)
        
        # Mijlocul barierei
        barrier_middle = Rectangle(
            height=0.7,
            width=0.15,
            color=WHITE,
            fill_opacity=0.95
        ).shift(LEFT * 2)
        
        # Fantele
        slit1_y = slit_separation / 2
        slit2_y = -slit_separation / 2
        
        slit1 = Line(
            LEFT * 2 + UP * (slit1_y + slit_width/2),
            LEFT * 2 + UP * (slit1_y - slit_width/2),
            color=BLUE,
            stroke_width=4
        )
        slit2 = Line(
            LEFT * 2 + UP * (slit2_y + slit_width/2),
            LEFT * 2 + UP * (slit2_y - slit_width/2),
            color=BLUE,
            stroke_width=4
        )
        
        barrier_label = Text("Barieră", font_size=11).next_to(barrier_middle, DOWN, buff=0.5)
        
        self.play(
            Create(barrier_top),
            Create(barrier_middle),
            Create(barrier_bottom),
            Create(slit1),
            Create(slit2),
            Write(barrier_label),
            run_time=1
        )
        
        # Ecran
        screen = Rectangle(
            height=barrier_height,
            width=0.1,
            color=GRAY,
            fill_opacity=0.4,
            stroke_color=WHITE
        ).shift(RIGHT * screen_x)
        screen_label = Text("Ecran", font_size=11).next_to(screen, DOWN, buff=0.2)
        
        self.play(Create(screen), Write(screen_label), run_time=0.8)
        
        # === PARTEA 2: Animație undă cuantică propagându-se ===
        
        # Creăm o grilă 2D pentru funcția de undă
        x_range = np.linspace(-6, 4, 100)
        y_range = np.linspace(-2.5, 2.5, 50)
        X, Y = np.meshgrid(x_range, y_range)
        
        def quantum_wave_function(X, Y, t, phase_offset=0):
            """Funcție de undă cuantică în spațiu 2D"""
            # Distanța de la sursă
            r = np.sqrt((X - source_x)**2 + (Y - 0.5)**2)
            
            # Funcția de undă sferică
            psi = np.exp(1j * (k * r - omega * t + phase_offset)) / np.sqrt(r + 1)
            
            # Mascare pentru barieră
            mask = np.ones_like(X)
            barrier_region = (X > barrier_x - 0.1) & (X < barrier_x + 0.1)
            
            # Blocăm unde în afara fantelor
            slit1_region = (Y > slit1_y - slit_width/2) & (Y < slit1_y + slit_width/2)
            slit2_region = (Y > slit2_y - slit_width/2) & (Y < slit2_y + slit_width/2)
            
            mask[barrier_region & ~(slit1_region | slit2_region)] = 0
            
            return psi * mask
        
        # Animație undă
        wave_points = VGroup()
        n_particles = 15
        
        for i in range(n_particles):
            angle = (i / n_particles) * 0.4 - 0.2
            particle = Dot(radius=0.04, color=YELLOW, fill_opacity=0.8)
            particle.move_to(source.get_center())
            wave_points.add(particle)
        
        def update_particles(mob, dt):
            for i, particle in enumerate(mob):
                pos = particle.get_center()
                if pos[0] < screen_x - 0.2:
                    # Propagare înainte de barieră
                    if pos[0] < barrier_x - 0.2:
                        particle.shift(RIGHT * dt * 1.5)
                    # Trecere prin fante
                    elif abs(pos[0] - barrier_x) < 0.3:
                        # Determină prin ce fantă trece
                        if abs(pos[1] - slit1_y) < slit_width/2:
                            particle.shift(RIGHT * dt * 1.5)
                        elif abs(pos[1] - slit2_y) < slit_width/2:
                            particle.shift(RIGHT * dt * 1.5)
                    # După barieră - interferență
                    else:
                        particle.shift(RIGHT * dt * 1.2)
                        # Adăugăm deviație bazată pe interferență
                        r1 = np.sqrt((pos[0] - barrier_x)**2 + (pos[1] - slit1_y)**2)
                        r2 = np.sqrt((pos[0] - barrier_x)**2 + (pos[1] - slit2_y)**2)
                        phase_diff = k * (r1 - r2)
                        deviation = 0.3 * np.sin(phase_diff) * dt
                        particle.shift(UP * deviation)
                else:
                    # Reset particula
                    angle = (i / n_particles) * 0.4 - 0.2
                    particle.move_to(source.get_center() + UP * angle * 0.5)
        
        wave_points.add_updater(update_particles)
        self.add(wave_points)
        self.wait(3)
        wave_points.clear_updaters()
        self.play(FadeOut(wave_points), run_time=0.5)
        
        # === PARTEA 3: Pattern de interferență cuantică ===
        
        # Calcul probabilitate cuantică |Ψ|²
        y_screen = np.linspace(-2.5, 2.5, 80)
        intensities = []
        
        for y in y_screen:
            # Distanțe de la fante la punct
            r1 = np.sqrt((screen_x - barrier_x)**2 + (y - slit1_y)**2)
            r2 = np.sqrt((screen_x - barrier_x)**2 + (y - slit2_y)**2)
            
            # Funcții de undă de la fiecare fantă
            psi1 = np.exp(1j * k * r1) / np.sqrt(r1)
            psi2 = np.exp(1j * k * r2) / np.sqrt(r2)
            
            # Superpoziție cuantică
            psi_total = psi1 + psi2
            
            # Densitate de probabilitate
            intensity = np.abs(psi_total)**2
            intensities.append(intensity)
        
        # Normalizare
        intensities = np.array(intensities)
        intensities = intensities / np.max(intensities)
        
        # Creăm pattern-ul vizual
        dots = VGroup()
        bars = VGroup()
        
        for i, (y, intensity) in enumerate(zip(y_screen, intensities)):
            # Punct pe ecran
            dot = Dot(
                point=RIGHT * screen_x + UP * y,
                radius=0.04,
                color=YELLOW,
                fill_opacity=intensity
            )
            dots.add(dot)
            
            # Bare de intensitate
            if i % 3 == 0:
                bar = Rectangle(
                    height=0.08,
                    width=intensity * 0.8,
                    color=YELLOW,
                    fill_opacity=0.7,
                    stroke_width=0
                ).next_to(RIGHT * screen_x + UP * y, RIGHT, buff=0)
                bars.add(bar)
        
        self.play(
            *[FadeIn(dot) for dot in dots],
            lag_ratio=0.01,
            run_time=2
        )
        self.play(
            *[Create(bar) for bar in bars],
            lag_ratio=0.01,
            run_time=1.5
        )
        
        # === PARTEA 4: Etichetare și explicații ===
        
        # Maxime și minime
        max_indices = []
        for i in range(1, len(intensities) - 1):
            if intensities[i] > 0.7 and intensities[i] > intensities[i-1] and intensities[i] > intensities[i+1]:
                max_indices.append(i)
        
        if len(max_indices) > 2:
            mid_max = max_indices[len(max_indices)//2]
            max_arrow = Arrow(
                RIGHT * (screen_x + 1.2) + UP * y_screen[mid_max],
                RIGHT * (screen_x + 0.2) + UP * y_screen[mid_max],
                color=GREEN,
                buff=0,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.2
            )
            max_label = Text("Maxim\nconstructiv", font_size=10, color=GREEN)
            max_label.next_to(max_arrow, RIGHT, buff=0.05)
            
            self.play(GrowArrow(max_arrow), Write(max_label), run_time=0.8)
        
        # Parametri cuantici
        params = VGroup(
            MathTex(r"|\Psi|^2 = \text{Probabilitate}", font_size=16, color=YELLOW),
            MathTex(f"\\lambda = {wavelength}", font_size=16, color=BLUE),
            MathTex(f"d = {slit_separation}", font_size=16, color=GREEN),
            MathTex(r"\Delta\phi = kd\sin\theta", font_size=16, color=ORANGE)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        params.to_corner(DL, buff=0.3)
        
        self.play(Write(params), run_time=1.5)
        
        # Explicație finală
        explanation = Text(
            "Fiecare foton trece prin AMBELE fante\nsimultan (superpoziție cuantică)",
            font_size=13,
            color=BLUE_B
        ).to_corner(DR, buff=0.3)
        
        self.play(Write(explanation), run_time=2)
        
        self.wait(3)
            
            
            