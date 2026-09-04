# 🛠️ Linux Automation Scripts

Colección de scripts y herramientas ligeras en **Python** y **Bash** diseñadas para la automatización de tareas diarias, reportes, mantenimiento del sistema y notificaciones de escritorio en Linux.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Bash](https://img.shields.io/badge/Shell-Bash%20%2F%20Fish-4EAA25?style=flat&logo=gnubash&logoColor=white)
![Platform](https://img.shields.io/badge/Plataforma-Linux-FCC624?style=flat&logo=linux&logoColor=black)
![License](https://img.shields.io/badge/Licencia-MIT-green.svg)

---

## Contenido del Repositorio

| Script | Lenguaje | Descripción |
| :--- | :--- | :--- |
| **`notificacion_matutina.py`** | Python 3 | Clima local por geolocalización IP y cotización del Dólar (Oficial, Blue, MEP). |
| **`cancion_actual.sh`** | Bash | Consulta bajo demanda qué canción está sonando en cualquier reproductor (Brave, Spotify, Firefox, VLC). |
| **`limpieza_de_sistema.sh`** | Bash | Mantenimiento seguro: limpia Flatpaks huérfanos, logs viejos de systemd, caché DNF y miniaturas. |
| **`reporte_apps.sh`** | Bash | Genera un inventario en Markdown para Obsidian con paquetes del sistema, Flatpaks y AppImages. |

---

## 1. Notificación Matutina (Clima y Dólar)

Script modular sin dependencias externas que obtiene información en tiempo real y la muestra tanto en consola como en una notificación nativa de escritorio (`notify-send`).

### Uso
```bash
# Reporte completo (Clima y Dólares):
./notificacion_matutina.py

# Consultar únicamente el clima:
./notificacion_matutina.py clima

# Consultar únicamente las cotizaciones:
./notificacion_matutina.py dolar
```

---

## 2. Consulta de Canción Actual (`cancion_actual.sh`)

Script bajo demanda para consultar instantáneamente el título y artista de la música que se está reproduciendo en el sistema.

### Características
* **Detección automática de reproductor:** Detecta automáticamente Brave, Spotify, Firefox, VLC o cualquier reproductor compatible con MPRIS.
* **Soporte para reproductor específico:** Permite especificar un reproductor por argumento.
* **Notificación de escritorio:** Muestra una tarjeta emergente y se cierra inmediatamente sin consumir recursos en segundo plano.

### Uso
```bash
# Detectar cualquier reproductor activo:
./cancion_actual.sh

# Consultar un reproductor específico (ejemplo Brave o Spotify):
./cancion_actual.sh brave
./cancion_actual.sh spotify
```

### Alias y Atajo de Teclado
* **Atajo en KDE / GNOME:** Asignar una combinación de teclas (ejemplo: `Meta + M`) a la orden `/ruta/al/script/cancion_actual.sh` para ver la canción actual desde cualquier ventana o juego.
* **Alias en Fish (`~/.config/fish/config.fish`):**
  ```fish
  alias tema "/ruta/al/script/cancion_actual.sh"
  ```

---

## 3. Limpieza Segura del Sistema (`limpieza_de_sistema.sh`)

Script de mantenimiento diseñado para liberar espacio en disco de forma segura sin desinstalar dependencias del sistema.

### Uso
```bash
./limpieza_de_sistema.sh
```

---

## 4. Reporte de Software para Obsidian (`reporte_apps.sh`)

Genera un documento Markdown (`.md`) estructurado con frontmatter YAML que lista el software instalado por el usuario en el sistema.

### Uso
```bash
# Generar reporte en la ruta por defecto:
./reporte_apps.sh

# Especificar una ruta de destino personalizada:
./reporte_apps.sh "/ruta/personalizada/reporte.md"
```

---

## Instalación y Configuración General

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/reddjedet/automation-scripts.git
   cd automation-scripts
   ```

2. **Otorgar permisos de ejecución:**
   ```bash
   chmod +x *.sh *.py
   ```

3. **Requisitos:**
   * Python 3
   * `libnotify` (`notify-send`)
   * `playerctl` (para el control de música)

---

## Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE).
