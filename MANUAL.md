# Dossier CH — Manual de uso

Herramienta de tracking de ofertas de trabajo en Suiza. Arquitectura en tres capas
que **nunca mezclan responsabilidades**:

```
job_capture.html          pipeline.py + parse.py         review.html
   (capturar)         →       (analizar)             →   (verificar y corregir)
   solo texto              catálogos CSV                 pills visuales,
   + Job ID                 → dossier.json                perfil, match %,
                                                            estado de postulación
```

Regla que sostiene todo el sistema: **la detección (regex, catálogos) vive solo en
`parse.py` y los `.csv`. Ningún HTML vuelve a analizar texto.** `review.html` solo
muestra lo que Python ya decidió y te deja corregirlo o completarlo a mano.

---

## 1. Los archivos, uno por uno

| Archivo | Qué hace | ¿Lo tocas tú? |
|---|---|---|
| `job_capture.html` | Pegas la oferta, le pone un Job ID permanente (`JOB-2026-000001`...), exporta JSON | Sí, a diario |
| `catalogs/skills.csv` | Lista de skills técnicas a detectar (id, nombre, regex) | Sí, cuando quieras enseñarle una skill nueva |
| `catalogs/languages.csv` | Idiomas a detectar | Raramente |
| `catalogs/soft_skills.csv` | Soft skills a detectar | Raramente |
| `catalogs/cities.csv` | Ciudades suizas → cantón | Si te postulas en una ciudad que falte |
| `catalogs/aliases.csv` | Sinónimos que apuntan a un `skill_id` ya existente (ej. "PBI" → `powerbi`) | Cuando una skill no se detecta por usar un sinónimo raro |
| `parse.py` | El cerebro: convierte texto crudo en campos estructurados | No, salvo que quieras cambiar la lógica de detección en sí |
| `pipeline.py` | Orquesta todo: junta captura + parseo, sin pisar tus correcciones | No |
| `profile.json` | Tus skills/idiomas/soft skills reales, con nivel CEFR | Mejor editarlo desde `review.html`, no a mano |
| `review.html` | Verificación visual, correcciones, perfil, match %, estado de postulación | Sí, a diario |
| `dossier.json` | El resultado final — cada oferta con todo lo detectado + tus correcciones | Se genera solo, tú lo importas/exportas |
| `coverage.py` | Reporte de qué % de campos se detectan bien sobre un lote de ofertas en `data/raw/*.txt` | Opcional, para auditar el sistema |

---

## 2. Preparar el entorno Python (una sola vez)

Hoy el proyecto no usa ninguna librería externa (solo librería estándar de Python),
así que técnicamente un entorno virtual no es imprescindible. Aun así, conviene
crear uno para no mezclar nada con el Python del sistema — sobre todo porque en
algún momento vas a retomar `adzuna_collector.py`, que sí necesita `requests`.

```bash
# Desde la carpeta del proyecto
python3 -m venv venv

# Activar (macOS/Linux)
source venv/bin/activate

# Activar (Windows)
venv\Scripts\activate

# Instalar dependencias (hoy no hay ninguna, pero deja el hábito)
pip install -r requirements.txt
```

Cada vez que abras una terminal nueva para trabajar en el proyecto, actívalo primero
con `source venv/bin/activate`. Sabrás que está activo porque el prompt de la terminal
empieza con `(venv)`. Para salir: `deactivate`.

---

## 3. El flujo de trabajo día a día

### Paso 1 — Capturar (`job_capture.html`)
1. Abre el archivo en el navegador (doble clic).
2. Al abrir, si ya habías capturado ofertas antes, haz clic en **"Import JSON ←"**
   y carga tu último `dossier_ch_capture.json`. El navegador **no es memoria fiable** —
   la exportación JSON es tu backup real.
3. Pega el texto completo de la oferta, revisa el nombre de empresa que se autodetecta
   (corrígelo si hace falta), elige la fuente (LinkedIn, JobUp...), clic en **"Save capture →"**.
4. Cuando termines la sesión, clic en **"Export JSON →"**. Ese archivo (`dossier_ch_capture.json`)
   es la entrada del siguiente paso.

### Paso 2 — Analizar (`pipeline.py`)
Desde la terminal, en la carpeta del proyecto:

```bash
python3 pipeline.py dossier_ch_capture.json
```

Esto:
- Lee cada oferta capturada.
- Para las que sean **nuevas** (Job ID que no existía antes), corre `parse.py` sobre el
  texto y las añade al `dossier.json`.
- Para las que **ya existían**, las deja intactas — así nunca pierdes una corrección
  manual o un cambio de estado de postulación solo por volver a capturar.
- Recalcula el `match_percent` de **todas** las ofertas contra `profile.json`, así que
  si actualizas tu perfil, todas las ofertas reflejan el nuevo match aunque no captures nada nuevo.

Verás algo así:
```
Ofertas en captura: 12
Nuevas analizadas: 3
Total en el dossier: 12
Guardado en: dossier.json
```

**Si editaste un catálogo CSV** (añadiste una skill nueva, corregiste una regex) y quieres
que se vuelva a analizar TODO desde cero con la regla nueva:
```bash
python3 pipeline.py dossier_ch_capture.json --reparse
```
Ojo: esto no borra tus correcciones manuales tampoco — solo actualiza lo que dice `parsed`
(lo que Python detectó), no `corrections` (lo que tú corregiste a mano).

### Paso 3 — Revisar y corregir (`review.html`)
1. Abre `review.html` en el navegador.
2. Clic en **"Importar dossier.json ←"** y carga el archivo que acabas de generar.
3. La primera vez, importa también tu **"profile.json ←"** (el que viene precargado en
   este paquete, con lo que ya sé de tu CV — ajústalo, es solo un punto de partida).
4. Verás la tabla de ofertas con Job ID, empresa, ciudad, **match %** y un desplegable
   de **estado de postulación** (Not applied / Applied / Interview / Offer / Rejected / Withdrawn).
5. Clic en una fila para ver el detalle: pills de colores.

**Cómo leer los colores:**
- 🔴 Rojo = la oferta lo pide como **requerido**
- 🟠 Ámbar = la oferta lo menciona como **nice-to-have**
- 🟢 Verde = detectado (soft skills) o, en la sección de idiomas, el nivel CEFR exigido
- Gris = no detectado en el texto
- Un lápiz (✎) junto a una pill significa que la **corregiste tú a mano** — el color
  que ves ya no es lo que dijo `parse.py`, es tu corrección.

**Corregir una detección:** clic en la pill. Primer clic = invierte el resultado
(la marca como encontrada/no encontrada) y le pone el ✎. Segundo clic sobre la misma
pill = borra tu corrección y vuelve a confiar en lo que dijo `parse.py`.

**Añadir una skill que el catálogo no conoce (vía rápida):** en el campo de texto bajo
las pills de skills, escribe el nombre (ej. "Looker Studio") y clic en
**"Añadir (vía rápida)"**. Esto:
- La cuenta como detectada **ya mismo**, solo para esta oferta (afecta al match % al instante).
- Te da una línea lista para copiar-pegar al final de `catalogs/skills.csv`, con este formato:
  ```
  lookerstudio,Looker Studio,\bLooker\s?Studio\b
  ```
  Cuando la pegues en el CSV y corras `pipeline.py --reparse`, esa skill se detectará
  sola en **todas** las ofertas de ahí en adelante, no solo en esta.

**Tu perfil (sección "01 Mi perfil"):** clic en el encabezado para desplegarla. Ahí
activas/desactivas skills y soft skills con un clic, y eliges el nivel CEFR real de
cada idioma. Clic en **"Guardar perfil →"** recalcula el match % de todas las ofertas
al instante. No olvides exportar `profile.json` para que sobreviva si cierras el navegador.

Si aún no has capturado ninguna oferta, esta sección aparece vacía — necesita saber
qué skills/idiomas existen para poder mostrarte pills. En vez de esperar a capturar algo,
clic en **"Import catalogs (CSV) ←"** y selecciona (puedes elegir varios a la vez)
`catalogs/skills.csv`, `catalogs/languages.csv` y `catalogs/soft_skills.csv` — así montas
tu perfil desde el primer minuto, sin depender del dossier.

**Notas:** cada oferta tiene un campo de texto libre — usa esto para lo que no encaje
en ningún otro campo (ej. "Recruiter contactó por LinkedIn el 3/8, seguimiento previsto").

**Exportar:**
- **"Exportar dossier.json →"** — guarda tus correcciones/estados/notas. Este archivo
  es el que vuelves a poner en la carpeta del proyecto para la próxima corrida de `pipeline.py`.
- **"Exportar profile.json →"** — igual, para tu perfil.
- **"Exportar CSV (para Google Sheet) →"** — una tabla plana con todas las ofertas y
  columnas por skill/idioma, lista para pegar en tu Google Sheet de tracking.

---

## 4. Cómo ampliar los catálogos

### Añadir una skill técnica nueva
Abre `catalogs/skills.csv` y añade una línea:
```
skill_id,Nombre visible,patrón_regex
```
- `skill_id`: minúsculas, sin espacios, único (ej. `looker`, `dbt`).
- El patrón usa regex de Python, insensible a mayúsculas por defecto. Ejemplo simple:
  `\bLooker\b` detecta la palabra "Looker" como palabra completa.

### Añadir un sinónimo de una skill que ya existe
En `catalogs/aliases.csv`:
```
alias,canonical_skill_id
pbi,powerbi
```
Esto hace que "PBI" en una oferta cuente como una mención de Power BI, sin tocar el
patrón principal de `powerbi` en `skills.csv`.

### Añadir una ciudad
En `catalogs/cities.csv`: `Ciudad,CANTÓN` (usa el código de dos letras del cantón, ej. `ZH`, `GE`, `VD`).

Después de tocar cualquier catálogo, corre `pipeline.py --reparse` para que el cambio
se aplique a las ofertas que ya tenías capturadas.

---

## 5. Auditar la calidad de la detección (`coverage.py`)

Si quieres saber qué tan bien está funcionando el sistema en general (no oferta por
oferta, sino en conjunto):
1. Guarda varios textos de ofertas como archivos `.txt` sueltos en `data/raw/`
   (uno por oferta).
2. Corre:
   ```bash
   python3 coverage.py
   ```
3. Verás algo así:
   ```
   Coverage report — 20 offers parsed

     company                             19/20 (95%)
     city                                17/20 (85%)
     canton                              17/20 (85%)
     workload                            12/20 (60%)
     workmode                            14/20 (70%)
     at_least_one_skill_detected         20/20 (100%)
     at_least_one_language_detected      18/20 (90%)
     at_least_one_soft_skill_detected    16/20 (80%)
   ```
   Los campos con % bajo son candidatos a mejorar el regex correspondiente en `parse.py`
   o los catálogos.

---

## 6. Qué NO hace este sistema (a propósito)

- **No scrapea LinkedIn ni Indeed.** Va contra sus términos de servicio. Todo es copiar/pegar
  manual, o vía APIs oficiales como Adzuna si más adelante retomas ese script.
- **No llama a la API de Anthropic desde el HTML descargado** — eso solo funciona dentro
  del sandbox de Claude.ai en vivo, nunca en un archivo abierto localmente.
- **`review.html` no vuelve a interpretar el texto de la oferta.** Si algo se detectó
  mal, la corrección se hace con clics (queda registrada), no editando regex desde el navegador.
  Si el error se repite en muchas ofertas, el arreglo real es mejorar el patrón en el `.csv`
  correspondiente y volver a correr `--reparse`.

---

## 7. Primeros pasos con este paquete

1. Descomprime la carpeta en tu máquina.
2. Instala Python si no lo tienes (`python3 --version` en terminal), crea el entorno
   virtual y actívalo (ver sección 2).
3. Abre `job_capture.html` y captura un par de ofertas de prueba.
4. Exporta el JSON de captura.
5. Con el `venv` activado, corre `python3 pipeline.py dossier_ch_capture.json`.
6. Abre `review.html`, importa el `dossier.json` generado y el `profile.json` incluido,
   ajusta tu perfil real, y revisa las pills.
7. Repite el ciclo captura → pipeline → review con cada oferta nueva.
