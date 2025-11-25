from manim import *
import numpy as np

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
        
      