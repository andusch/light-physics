# LightPhysics — Proiect "Lumina"

Scurtă descriere
- Proiect educațional pentru notițe și calcule legate de optică (reflexie, refracție, difracție, interferență) și modelul undulator/corpuscular al luminii.
- Conținut principal: notebook Jupyter cu teorie și formule fundamentale.

Structură proiect
- lumina.ipynb — notebook Jupyter cu teoria (legea lui Snell, ecuația undei, formule foton)  
  Link: [lumina.ipynb](lumina.ipynb)
- README.md — acest fișier (sumar și instrucțiuni)
  Link: [README.md](README.md)

Cerinte / Dependențe recomandate
- Python 3.8+ (în notebook metadata este Python 3.11.11)
- Jupyter Notebook / JupyterLab
- Opțional pentru calcule și vizualizări: numpy, matplotlib

Instalare și rulare (macOS)
1. Creează un mediu virtual:
   - python3 -m venv .venv
   - source .venv/bin/activate
2. Instalează pachete minimale:
   - python -m pip install --upgrade pip
   - python -m pip install jupyter numpy matplotlib
3. Deschide proiectul în VS Code:
   - code .
4. Rulează notebook-ul:
   - jupyter notebook lumina.ipynb
   sau
   - jupyter lab

Cum contribui
- Editează sau extinde `lumina.ipynb` cu texte, derivări sau exemple numerice.
- Pentru cod Python adițional, adaugă fișiere .py și teste corespunzătoare.

Note
- Notebook-ul folosește formule TeX în celule Markdown; pentru calcule, adaugă celule de cod Python.
- Păstrează versiunea Python compatibilă cu mediul de lucru (vezi metadata din `lumina.ipynb`).

Licență
- Adaugă o licență în repo dacă intenționezi să protejezi / publici conținutul.

Contact
- Modificări și întrebări: editează fișierele din proiect sau deschide un issue în sistemul de versiune folosit.