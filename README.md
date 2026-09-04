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
| **`limpieza_de_sistema.sh`** | Bash | Mantenimiento seguro: limpia Flatpaks huérfanos, logs viejos de systemd, caché DNF y miniaturas. |
| **`reporte_apps.sh`** | Bash | Genera un inventario en Markdown para Obsidian con paquetes RPM, Flatpaks y AppImages. |

---

## 1. Notificación Matutina (Clima y Dólar)

Script modular sin dependencias externas que obtiene información en tiempo real y la muestra tanto en consola como en una notificación nativa de escritorio (`notify-send`).

### Características
* **Detección automática de ubicación:** Identifica la ciudad por IP mediante `wttr.in`.
* **Datos meteorológicos:** Temperatura actual, sensación térmica (ST), mínima/máxima del día y condición del cielo.
* **Cotizaciones en vivo:** Dólar Oficial, Blue y MEP vía `dolarapi.com`.
* **Sin dependencias externas:** No requiere `pip install`, utiliza la biblioteca estándar de Python.

### Uso
```bash
# Reporte completo (Clima y Dólares):
./notificacion_matutina.py

# Consultar únicamente el clima:
./notificacion_matutina.py clima

# Consultar únicamente las cotizaciones:
./notificacion_matutina.py dolar
```

### Alias recomendados en Shell
* **Fish (`~/.config/fish/config.fish`):**
  ```fish
  alias clima "/ruta/al/script/notificacion_matutina.py clima"
  alias dolar "/ruta/al/script/notificacion_matutina.py dolar"
  ```
* **Bash / Zsh (`~/.bashrc` o `~/.zshrc`):**
  ```bash
  alias clima="/ruta/al/script/notificacion_matutina.py clima"
  alias dolar="/ruta/al/script/notificacion_matutina.py dolar"
  ```

---

## 2. Limpieza Segura del Sistema (`limpieza_de_sistema.sh`)

Script de mantenimiento diseñado para liberar espacio en disco de forma segura sin desinstalar dependencias del sistema.

### Acciones que realiza:
1. Elimina runtimes y dependencias en desuso de Flatpak (`flatpak uninstall --unused`).
2. Purga registros antiguos del sistema reduciendo `journalctl` a los últimos 2 días.
3. Limpia paquetes descargados temporales de DNF (`dnf clean packages`).
4. Vacía la caché de miniaturas de imágenes y videos (`~/.cache/thumbnails/`).
5. Emite una notificación de escritorio al finalizar.

### Uso
```bash
./limpieza_de_sistema.sh
```

---

## 3. Reporte de Software para Obsidian (`reporte_apps.sh`)

Genera un documento Markdown (`.md`) estructurado con frontmatter YAML que lista el software instalado por el usuario en el sistema.

### Secciones generadas:
* Paquetes de sistema instalados explícitamente (`dnf`, `pacman` o `apt`).
* Aplicaciones Flatpak con nombre, versión e identificador.
* Escaneo de archivos AppImage en directorios locales.

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

---

## Licencia

Este proyecto está bajo la Licencia [MIT](LICENSE).
