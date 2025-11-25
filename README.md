# Lumina în modelare digitală
Proiect interdisciplinar – animaţii Manim, grafice Python şi învăţare automată
pentru demonstraţia fenomenelor ondulatorii şi cuantice ale luminii.

## 🎯 Obiectiv
Ilustrarea propagării, reflexiei, refracţiei, interferenţei, polarizării
şi comportamentului fotonic al luminii într-o formă vizual interactivă.

## 🧪 Conţinut
| Fenomen               | Fişier / Clasă Manim              | Bonus ML / Plot |
|-----------------------|-----------------------------------|-----------------|
| Propagare 1D          | `WavePropagation1D`               | –               |
| Reflexie              | `Reflection`                      | `reflection.png`|
| Refracţie (Snell)     | `Refraction`                      | `snell_ml.png`, `snell_physics_informed.png` |
| Interferenţă 3D       | `Interference`                    | `pi_gan.png`    |
| Model fotonic         | `PhotonicModel`                   | `photon_energy.png` |
| Polarizare            | `Polarization`                    | –               |
| Double-slit cuantic   | `DoubleSlit`                      | –               |

## 🚀 Rulare animaţii Manim
```bash
# creează mediu izolat (opţional)
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# instalează Manim (comunitate)
pip install manim

# rulează o scenă (exemplu)
manim -pqh nume_fisier.py WavePropagation1D
```

Opţiuni calitate: -ql (low), -qm (medium), -qh (high), -qk (4K).

## 📊 Generare grafice ML
```bash
pip install numpy pandas matplotlib scikit-learn torch sympy
python grafice.py               # generează toate plot-urile în folderul `plots/`

```

## 📁 Structură repo
```
lumina-modelare-digitala/
├── README.md
├── src/                    # scene Manim (câte un fişier per fenomen)
│   ├── wave_propagation.py
│   ├── reflection.py
│   ├── refraction.py
│   ├── interference.py
│   ├── photonic_model.py
│   ├── polarization.py
│   └── double_slit.py
├── plots.ipynb             # cod matplotlib + ML
├── plots/                  # figuri exportate
└── media_output/videos/                  # clipuri Manim (generate automat)

```