# Genera consulta.js (formulario "¿Tienes una consulta?" compartido) a partir de index.html.
# Uso: python3 fuentes/consulta/build.py   — luego subir el ?v= de consulta.js en servicios, equipo, blog y fuentes/serv/tpl.html.
import json
import re,sys
import os
ROOT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..')
idx=open(os.path.join(ROOT,'index.html'),encoding='utf-8').read()
css=re.search(r'<style>(.*?)</style>',idx,re.S).group(1)
css=re.sub(r'/\*.*?\*/','',css,flags=re.S)
STRONG={'consulta','cgrid','cl','qstat','qact','qhrs','ccard','qsec','qtopics','oth','segc','qrow','ff','cnt2','tick','chk','fld','qdone','demo','prog','viewport','track','pane','lnk','e','ta','ti','lb','nav','seg'}
KF={'qp','dr'}
def blocks(s):
    i=0;out=[]
    while i<len(s):
        j=s.find('{',i)
        if j<0:break
        head=s[i:j].strip();d=1;k=j+1
        while d:
            if s[k]=='{':d+=1
            elif s[k]=='}':d-=1
            k+=1
        out.append((head,s[j+1:k-1]));i=k
    return out
REN=[('bar','qpb'),('lead','qlead'),('prog','qprog'),('seg','qseg')]
def ren(sel):
    for a,b in REN: sel=re.sub(r'\.'+a+r'(?![\w-])','.'+b,sel)
    return sel
def scope(sel):
    sel=sel.strip()
    if sel.startswith('.consulta'): return '#consulta'+sel[len('.consulta'):]
    if sel.startswith('#qform'): return '#consulta '+sel
    return '#consulta '+sel
def keep(sel):
    toks=set(re.findall(r'\.([\w-]+)',sel))|set(re.findall(r'#([\w-]+)',sel))
    if 'qform' in toks: return True
    # .cl .lead and .qsec.seg handled since cl/qsec are strong
    return bool(toks & STRONG)
def rule(head,body):
    sels=[s for s in head.split(',') if keep(s)]
    if not sels: return ''
    return ','.join(scope(ren(s)) for s in sels)+'{'+body.strip()+'}'
out=[]
for head,body in blocks(css):
    if head.startswith('@keyframes'):
        if head.split()[1] in KF: out.append(head+'{'+body+'}')
    elif head.startswith('@media'):
        inner=[rule(h,b) for h,b in blocks(body)]
        inner=[x for x in inner if x]
        if inner: out.append(head+'{'+''.join(inner)+'}')
    elif not head.startswith('@'):
        r=rule(head,body)
        if r: out.append(r)
CSSOUT='\n'.join(out)

css=CSSOUT.split('\n')
css=[l for l in css if 'url(data:' not in l and ' .tk ' not in l and '#cvform' not in l and ' .done ' not in l]
css='\n'.join(css)+'\n#consulta{scroll-margin-top:0}\n#consulta h2{margin:.7rem 0 1rem}\n'
a=idx.index('<section class="consulta" id="consulta">');sec=idx[a:idx.index('<nav class="qbar"',a)]
REN={'bar':'qpb','lead':'qlead','prog':'qprog','seg':'qseg'}
def fixcls(m):
    t=[REN.get(c,c) for c in m.group(1).split() if c!='rv']
    return 'class="'+' '.join(t)+'"'
sec=re.sub(r'class="([^"]*)"',fixcls,sec)
js=r'''/* Formulario de consulta compartido (servicios, equipo, blog). Generado a partir de index.html. */
(function(){
if(window.__consulta)return;window.__consulta=1;
var CSS=%s,HTML=%s;
function mount(){
var slot=document.getElementById('consulta-slot');if(!slot||document.getElementById('consulta'))return;
var st=document.createElement('style');st.textContent=CSS;document.head.appendChild(st);
slot.insertAdjacentHTML('afterend',HTML);slot.parentNode.removeChild(slot);
init();}
function init(){const f=document.getElementById('qform');if(!f)return;
const q=s=>f.querySelector(s),tel=q('#q-tel'),msg=q('#q-msg');
const panes=[...f.querySelectorAll('.pane')],track=q('.track'),vp=q('.viewport'),steps=[...f.querySelectorAll('.qprog li')],bar=q('.qpb i'),back=q('.back'),next=q('.next'),send=q('.send');let cur=0;
const fit=()=>{const h=panes[cur].offsetHeight;if(h)vp.style.height=h+'px'};
const viaTel=()=>f.via.value==='telefono';
function show(i,foc){cur=i;track.style.transform='translateX(-'+(i*100/3)+'%%)';panes.forEach((p,k)=>{p.inert=k!==i});steps.forEach((s,k)=>{s.classList.toggle('on',k===i);s.classList.toggle('ok',k<i)});bar.style.width=(i/2*100)+'%%';back.hidden=i===0;next.hidden=i===2;send.hidden=i!==2;fit();
if(foc){const el=panes[i].querySelector('input:not([type=radio]):not([type=checkbox]),textarea');if(el)el.focus({preventScroll:true})}}
const V={name:v=>v.trim().split(/\s+/).filter(Boolean).length>=2||'Escribe tu nombre y apellidos.',email:v=>/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim())||'Introduce un correo electrónico válido.',tel:v=>{const s=v.trim();if(!s)return viaTel()?'Indícanos un teléfono para llamarte.':true;return /^[+\d][\d\s().-]{6,}$/.test(s)||'Revisa el número de teléfono.'},priv:c=>c||'Debes aceptar la política de privacidad.'};
const res=el=>V[el.dataset.q](el.type==='checkbox'?el.checked:el.value);
function mark(el,showErr){const r=res(el),box=el.closest('.ff,.fld'),e=f.querySelector('#e-'+el.id),filled=el.type==='checkbox'?el.checked:el.value.trim()!=='';
box.classList.toggle('ok',r===true&&filled&&el.type!=='checkbox');if(showErr||box.classList.contains('bad')){e.textContent=r===true?'':r;box.classList.toggle('bad',r!==true);el.setAttribute('aria-invalid',r!==true)}return r===true}
function check(i){let ok=true,first=null;
if(i===0){const e=q('#e-q-tema');if(!f.tema.value){e.textContent='Elige el servicio sobre el que quieres consultar.';ok=false}else e.textContent=''}
panes[i].querySelectorAll('[data-q]').forEach(el=>{if(!mark(el,true)){ok=false;if(!first)first=el}});if(first)first.focus({preventScroll:true});fit();return ok}
next.addEventListener('click',()=>{if(check(cur))show(cur+1,true)});
back.addEventListener('click',()=>show(cur-1,true));
f.addEventListener('keydown',e=>{if(e.key==='Enter'&&e.target.tagName==='INPUT'&&e.target.type!=='checkbox'&&e.target.type!=='radio'&&cur<2){e.preventDefault();next.click()}});
f.addEventListener('input',e=>{const el=e.target;if(el.dataset&&el.dataset.q)mark(el,false);
if(el===msg){msg.dataset.auto='0';q('#qc').textContent=msg.value.length;msg.style.height='auto';msg.style.height=Math.max(120,msg.scrollHeight)+'px';fit()}});
function setTema(v,advance){q('#e-q-tema').textContent='';if(!msg.value.trim()||msg.dataset.auto==='1'){msg.value='Quisiera información sobre: '+v+'. ';msg.dataset.auto='1';q('#qc').textContent=msg.value.length}
clearTimeout(f._t);if(advance)f._t=setTimeout(()=>{if(cur===0)show(1,false)},450)}
f.addEventListener('change',e=>{if(e.target.name==='via'){q('#q-telreq').hidden=!viaTel();if(!viaTel()){tel.closest('.ff').classList.remove('bad');q('#e-q-tel').textContent=''}else mark(tel,false);fit()}
if(e.target.name==='tema')setTema(e.target.value,true)});
f.addEventListener('submit',e=>{e.preventDefault();if(!check(2))return;
q('#qn').textContent=q('#q-name').value.trim().split(/\s+/)[0];const tm=f.tema.value;q('#qt').textContent=tm&&tm!=='Otra consulta'?' sobre '+tm.toLowerCase():'';q('#qv').textContent=viaTel()?'por teléfono':'por email';f.classList.add('sent');const d=q('.qdone');d.hidden=false;d.focus({preventScroll:true})});
show(0,false);addEventListener('resize',fit);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);
if('ResizeObserver' in window)new ResizeObserver(fit).observe(f);
addEventListener('hashchange',()=>setTimeout(fit,60));
/* Preseleccionar el servicio cuando se llega desde su ficha */
window.consultaTema=function(name){if(!name||f.classList.contains('sent'))return;const r=[...f.querySelectorAll('input[name=tema]')].find(x=>x.value===name);if(!r||r.checked)return;if(cur!==0)return;r.checked=true;setTema(name,false)};
/* Estado de apertura (Europe/Madrid) */
const st=document.getElementById('qstat');
function upd(){let w,h,m;try{const p=new Intl.DateTimeFormat('es-ES',{timeZone:'Europe/Madrid',weekday:'short',hour:'numeric',minute:'numeric',hour12:false}).formatToParts(new Date());const g=k=>p.find(x=>x.type===k).value;w=g('weekday').toLowerCase().slice(0,2);h=+g('hour')%%24;m=+g('minute')}catch(_){st.querySelector('span').textContent='Lun–Jue 9–19 h · Vie 9–14 h';return}
const map={lu:1,ma:2,mi:3,ju:4,vi:5,'sá':6,do:0,sa:6};const d=map[w];const close=d>=1&&d<=4?19:d===5?14:null;const now=h+m/60;
if(close&&now>=9&&now<close){st.className='qstat open';st.querySelector('span').textContent='Abierto ahora · hasta las '+close+' h'}
else{st.className='qstat';let nd=d,txt;if(close&&now<9)txt='hoy a las 9 h';else{nd=(d+1)%%7;while(nd===6||nd===0)nd=(nd+1)%%7;txt=(nd===(d+1)%%7?'mañana':'el lunes')+' a las 9 h'}st.querySelector('span').textContent='Cerrado ahora · abrimos '+txt}}
upd();setInterval(upd,60000);}
/* Cualquier enlace a "#consulta" baja al formulario de esta misma página si está visible */
document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a[href]');if(!a)return;var h=a.getAttribute('href')||'';if(!/(^|index\.html)#consulta$/.test(h))return;
var c=document.getElementById('consulta');if(!c||!c.offsetParent)return;e.preventDefault();
var t=document.querySelector('#hero h1');if(t&&window.consultaTema)window.consultaTema(t.textContent.trim());
c.scrollIntoView({behavior:'smooth',block:'start'})});
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',mount);else mount();
})();
''' % (json.dumps(css,ensure_ascii=False), json.dumps(sec,ensure_ascii=False))
open(os.path.join(ROOT,'consulta.js'),'w',encoding='utf-8').write(js)
print(len(js))
