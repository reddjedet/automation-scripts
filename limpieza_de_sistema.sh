#!/bin/bash
echo "Iniciando limpieza segura del sistema..."

# 1. Limpiar runtimes y dependencias viejas de Flatpak
echo "-> 1/4: Limpiando Flatpaks en desuso..."
flatpak uninstall --unused -y

# 2. Reducir registros de logs de systemd a los últimos 2 días
echo "-> 2/4: Purgando registros antiguos de journalctl..."
sudo journalctl --vacuum-time=2d

# 3. Limpiar paquetes descargados temporales de DNF
if command -v dnf &>/dev/null; then
    echo "-> 3/4: Limpiando caché de paquetes DNF..."
    sudo dnf clean packages
fi

# 4. Borrar miniaturas de imágenes y videos viejos en caché
echo "-> 4/4: Vaciando caché de miniaturas..."
rm -rf ~/.cache/thumbnails/*

# 5. Notificación nativa al finalizar
if command -v notify-send &>/dev/null; then
    notify-send -i "trash-empty" "Mantenimiento" "Limpieza segura del sistema completada"
fi

echo "Listo. Sistema optimizado."
