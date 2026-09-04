#!/usr/bin/env python3
import json
import urllib.request
import subprocess
import time
import sys

def obtener_dolares():
    try:
        url = "https://dolarapi.com/v1/dolares"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            precios = {}
            for item in data:
                if item['casa'] in ['oficial', 'blue', 'bolsa']:
                    nombre = "MEP" if item['casa'] == 'bolsa' else item['nombre']
                    precios[nombre] = f"${item['venta']:.0f}"
            return f"💵 Oficial: {precios.get('Oficial', 'N/D')}  |  Blue: {precios.get('Blue', 'N/D')}  |  MEP: {precios.get('MEP', 'N/D')}"
    except Exception:
        return "💵 Dólar: No disponible"

def obtener_clima():
    try:
        # Consulta wttr.in en formato JSON (detecta automáticamente tu ubicación por IP)
        url = "https://wttr.in/?format=j1&lang=es"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            
            ciudad = data['nearest_area'][0]['areaName'][0]['value']
            temp_actual = data['current_condition'][0]['temp_C']
            sensacion = data['current_condition'][0]['FeelsLikeC']
            
            # Descripción en español si está disponible
            desc = data['current_condition'][0].get('lang_es', [{'value': ''}])[0]['value']
            if not desc:
                desc = data['current_condition'][0]['weatherDesc'][0]['value']
            
            # Mínima y Máxima del día
            min_temp = data['weather'][0]['mintempC']
            max_temp = data['weather'][0]['maxtempC']
            
            return f"🌤️ {ciudad}: {temp_actual}°C ({desc})  |  Min: {min_temp}°C - Max: {max_temp}°C (ST: {sensacion}°C)"
    except Exception:
        # Fallback si falla el JSON
        try:
            url = "https://wttr.in/?format=%c+%t+%C&m&lang=es"
            req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.read().decode('utf-8').strip()
        except Exception:
            return "🌤️ Clima: No disponible"

def ejecutar(modo="todo"):
    clima = obtener_clima()
    dolares = obtener_dolares()
    
    if modo == "clima":
        mensaje = clima
        titulo = "Reporte del Clima"
        icono = "weather-clouds"
    elif modo == "dolar":
        mensaje = dolares
        titulo = "Cotizaciones del Dólar"
        icono = "help-donate"
    else:
        mensaje = f"{clima}\n{dolares}"
        titulo = "Resumen Matutino"
        icono = "appointment-soon"
    
    print("\n" + mensaje + "\n")
    
    subprocess.run([
        "notify-send",
        "-t", "12000",
        "-i", icono,
        titulo,
        mensaje
    ])

if __name__ == "__main__":
    param = sys.argv[1] if len(sys.argv) > 1 else "todo"
    ejecutar(param)
