import os
import subprocess

quanta_testes = [1, 2, 3, 4, 5, 6, 8, 10, 15, 20]

for q in quanta_testes:
    with open("programas/quantum.txt", "w") as f:
        f.write(str(q))
    subprocess.run(["python", "Escalonador.py"])
    print(f"Log gerado: log{q:02d}.txt")