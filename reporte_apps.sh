#!/bin/bash

# ==============================================================================
# CONFIGURACIÓN (Personalizable mediante argumentos o variables de entorno)
# ==============================================================================
OUTPUT="${1:-${OBSIDIAN_VAULT:-$HOME/Documents}/reporte-apps.md}"
mkdir -p "$(dirname "$OUTPUT")"

SEARCH_DIR="${APPIMAGE_DIR:-$HOME}"

# ==============================================================================
# GENERACIÓN DEL REPORTE
# ==============================================================================
echo "---" > "$OUTPUT"
echo "fecha: $(date +'%Y-%m-%d %H:%M')" >> "$OUTPUT"
echo "sistema: $(grep PRETTY_NAME /etc/os-release 2>/dev/null | cut -d= -f2 | tr -d '\"' || echo 'Linux')" >> "$OUTPUT"
echo "tags: [reporte, software, linux]" >> "$OUTPUT"
echo -e "---\n" >> "$OUTPUT"

echo "# Control de Software y Paquetes - $(date +'%Y-%m-%d %H:%M')" >> "$OUTPUT"

# 1. Paquetes instalados explícitamente por el usuario
echo -e "\n## Paquetes instalados por el usuario" >> "$OUTPUT"
if command -v dnf &>/dev/null; then
    dnf repoquery --userinstalled --queryformat '* %{name} (%{version})' 2>/dev/null | sort | uniq >> "$OUTPUT"
elif command -v pacman &>/dev/null; then
    pacman -Qe 2>/dev/null | awk '{print "* **" $1 "** - " $2}' >> "$OUTPUT"
elif command -v apt &>/dev/null; then
    apt-mark showmanual 2>/dev/null | awk '{print "* " $1}' >> "$OUTPUT"
fi

# 2. Aplicaciones Flatpak
if command -v flatpak &>/dev/null; then
    echo -e "\n## Aplicaciones Flatpak" >> "$OUTPUT"
    flatpak list --app --columns=name,version,application 2>/dev/null | awk '{print "* **" $1 "** - " $2 " (`" $3 "`)"}' >> "$OUTPUT"
fi

# 3. Escaneo de AppImages
echo -e "\n## AppImages encontradas" >> "$OUTPUT"
find "$SEARCH_DIR" -maxdepth 3 -iname "*appimage*" -printf "* %f (\`%p\`)\n" 2>/dev/null >> "$OUTPUT"

echo "Reporte generado con éxito en: $OUTPUT"

if command -v notify-send &>/dev/null; then
    notify-send -i "text-x-markdown" "Reporte de Software" "Inventario generado exitosamente en $OUTPUT"
fi
