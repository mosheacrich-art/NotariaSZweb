import re,base64,io,json
from PIL import Image
sp='/tmp/claude-0/-home-claude/3c03e3ac-5377-5cba-aeed-00aa36a4213a/scratchpad/'
blog=open(sp+'web/blog.html',encoding='utf8').read()
css=re.search(r'<style>\n(.*?)</style>',blog,re.S).group(1)
lines=css.split('\n')
a=next(i for i,l in enumerate(lines) if l.startswith('/* cabecera'))
b=next(i for i,l in enumerate(lines) if l.startswith('/* footer'))
base='\n'.join(lines[:a])+'\n[hidden]{display:none!important}\n'
foot='\n'.join(lines[b:])
header=re.search(r'<header id="hd">.*?</header>',blog,re.S).group(0)
header=re.sub(r'<nav>.*?</nav>','<nav><a class="on" href="servicios.html" aria-current="page">Servicios</a><a href="videofirma.html">Videofirma</a><a href="index.html#proceso">Cómo trabajamos</a><a href="equipo.html">Equipo</a><a href="blog.html">Blog</a><a href="index.html#consulta">Contacto</a></nav>',header,flags=re.S)
footer=re.search(r'<footer class="ft">.*?</footer>',blog,re.S).group(0)
footer=footer.replace('<a href="index.html#servicios">Servicios notariales</a>','<a href="servicios.html">Servicios notariales</a>').replace('<a href="#">Videoconferencias</a>','<a href="servicios.html#videoconferencias">Videoconferencias</a>')
def b64(im,fmt,**k):
    o=io.BytesIO();im.save(o,fmt,**k);return 'data:image/%s;base64,'%('jpeg' if fmt=='JPEG' else 'png')+base64.b64encode(o.getvalue()).decode()
ic={}
import glob,os
for f in glob.glob(sp+'ic/*.png'):
    if f.endswith('sello.png'): continue
    ic[os.path.basename(f)[:-4]]=b64(Image.open(f).convert('RGBA'),'PNG',optimize=True)
ph={}
for f in glob.glob(sp+'servicios/*.jpg'):
    k=os.path.basename(f)[:-4]
    im=Image.open(f).convert('RGB');im.thumbnail((900,900));ph[k]=b64(im,'JPEG',quality=68,optimize=True)
for k,n in {'mast':'vestibulo','cta':'galeria-vidrieras'}.items():
    im=Image.open(sp+'notaria/%s.jpg'%n).convert('RGB');im.thumbnail((1400 if k=='mast' else 900,)*2);ph[k]=b64(im,'JPEG',quality=70,optimize=True)
t=open('tpl.html',encoding='utf8').read()
t=t.replace('%%BASECSS%%',base).replace('%%FOOTCSS%%',foot).replace('%%HEADER%%',header).replace('%%FOOTER%%',footer)
t=t.replace('%%IMGS%%',json.dumps({'ic':ic,'ph':ph})).replace('%%DATA%%',open('data.js',encoding='utf8').read())
open(sp+'web/servicios.html','w',encoding='utf8').write(t)
print(len(t)//1024,'KB')
