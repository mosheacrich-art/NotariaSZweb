# Genera videofirma.html a partir de tpl.html, reutilizando cabecera, pie, menú móvil
# y estilos base de blog.html.
# Uso: python3 fuentes/videofirma/build.py
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..', '..')
rd = lambda p: open(os.path.join(ROOT, p), encoding='utf-8').read()

blog = rd('blog.html')
tpl = open(os.path.join(HERE, 'tpl.html'), encoding='utf-8').read()

css = re.search(r'<style>\n?(.*?)</style>', blog, re.S).group(1)
lines = css.split('\n')
a = next(i for i, l in enumerate(lines) if l.startswith('/* cabecera de periódico'))
f = next(i for i, l in enumerate(lines) if l.startswith('/* footer'))
m = next(i for i, l in enumerate(lines) if '@media(min-width:901px){#mm{display:none}}' in l)
base = '\n'.join(lines[:a]) + '\n[hidden]{display:none!important}\n'
foot = '\n'.join(lines[f:m + 1])

header = re.search(r'<header id="hd">.*?</header>', blog, re.S).group(0)
header = re.sub(r'<nav>.*?</nav>', '<nav><a href="servicios.html">Servicios</a><a class="on" href="videofirma.html" aria-current="page">Videofirma</a><a href="index.html#proceso">Cómo trabajamos</a><a href="equipo.html">Equipo</a><a href="blog.html">Blog</a><a href="index.html#consulta">Contacto</a></nav>', header, flags=re.S)
footer = re.search(r'<footer class="ft">.*?</footer>', blog, re.S).group(0)
menujs = re.search(r"<script>\(function\(\)\{var h=document.getElementById\('hd'\).*?</script>", blog, re.S).group(0)

out = (tpl.replace('%%BASECSS%%', base).replace('%%FOOTCSS%%', foot)
          .replace('%%HEADER%%', header).replace('%%FOOTER%%', footer)
          .replace('%%MENUJS%%', menujs))
assert '%%' not in out
open(os.path.join(ROOT, 'videofirma.html'), 'w', encoding='utf-8').write(out)
print(len(out) // 1024, 'KB')
