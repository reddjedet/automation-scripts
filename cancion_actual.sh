#!/bin/bash

# ==============================================================================
# CONFIGURACIÓN DEL REPRODUCTOR
# ==============================================================================
# Si se pasa un reproductor como argumento (ej: ./cancion_actual.sh spotify o brave), lo usa.
# Si no se pasa nada, playerctl detecta automáticamente cualquier reproductor activo.
REPRODUCTOR="${1:-%any}"

if ! command -v playerctl &>/dev/null; then
    echo "Error: playerctl no esta instalado en el sistema."
    exit 1
fi

# ==============================================================================
# CONSULTA Y NOTIFICACIÓN
# ==============================================================================
ESTADO=$(playerctl -p "$REPRODUCTOR" status 2>/dev/null)

if [ "$ESTADO" = "Playing" ]; then
    INFO=$(playerctl -p "$REPRODUCTOR" metadata --format '{{artist}} - {{title}}' 2>/dev/null)
    
    # Fallback si no hay artista separado (ej: videos directos de YouTube)
    if [ "$INFO" = " - " ] || [ -z "$INFO" ]; then
        INFO=$(playerctl -p "$REPRODUCTOR" metadata --format '{{title}}' 2>/dev/null)
    fi
    
    NOMBRE_PLAYER=$(playerctl -p "$REPRODUCTOR" metadata --format '{{playerName}}' 2>/dev/null)
    NOMBRE_PLAYER="${NOMBRE_PLAYER:-Reproductor}"
    
    echo "Reproduciendo en $NOMBRE_PLAYER: $INFO"
    
    if command -v notify-send &>/dev/null; then
        notify-send -t 5000 -i "audio-headphones" "Reproduciendo en $NOMBRE_PLAYER" "$INFO"
    fi

elif [ "$ESTADO" = "Paused" ]; then
    INFO=$(playerctl -p "$REPRODUCTOR" metadata --format '{{title}}' 2>/dev/null)
    NOMBRE_PLAYER=$(playerctl -p "$REPRODUCTOR" metadata --format '{{playerName}}' 2>/dev/null)
    NOMBRE_PLAYER="${NOMBRE_PLAYER:-Reproductor}"
    
    echo "Pausado en $NOMBRE_PLAYER: $INFO"
    
    if command -v notify-send &>/dev/null; then
        notify-send -t 4000 -i "media-playback-pause" "$NOMBRE_PLAYER (Pausado)" "$INFO"
    fi

else
    echo "No hay ningun reproductor activo en este momento."
    if command -v notify-send &>/dev/null; then
        notify-send -t 3000 -i "dialog-information" "Control Multimedia" "No hay musica reproduciendose"
    fi
fi
