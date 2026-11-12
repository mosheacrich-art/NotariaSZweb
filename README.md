# Notaría Sultán-Zulueta · web

Sitio estático (HTML/CSS/JS sin build). Páginas: `index.html` (landing), `servicios.html`, `equipo.html`, `blog.html`.
Vídeo del hero: `hero.mp4` (escritorio) y `hero_m.mp4` (móvil), ya enlazados en `index.html`.
Tipografías: Libre Caslon Text + Source Sans 3 (Google Fonts). Las imágenes van incrustadas en los HTML.

## Desplegar en Vercel
Importar el repositorio con el preset **Other**, sin comando de build y con el directorio raíz como salida.

## Editar servicios
`servicios.html` se genera desde `fuentes/serv/` (`tpl.html` + `data.js`): `python3 build.py` dentro de esa carpeta.

## Pendiente
- Enlace de política de privacidad y LinkedIn.
- Los formularios (consulta, trabajo, presupuesto) todavía no envían datos: falta conectar un backend.
