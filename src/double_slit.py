from manim import *
import numpy as np

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
            
            