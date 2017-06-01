# -*- coding: utf-8 -*-
from get_exo import get_exo_2
import os
f = open('start.tex','r')
exo=f.read()+get_exo_2(150)+"\\end{document}"
f.close()
with open('a.tex', 'w') as f:
    f.write(exo)
f.close()
os.system("pdflatex a.tex")