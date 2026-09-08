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

def obtener_grafico_blue_30d(altura=6, ancho=42):
    try:
        url = "https://api.bluelytics.com.ar/v2/evolution.json"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            datos = json.loads(response.read().decode('utf-8'))
        
        # Filtrar solo 'Blue', tomar los ultimos 30 dias y ordenarlos cronologicamente (de pasado a presente)
        registros_blue = [d for d in datos if d.get('source') == 'Blue'][:30]
        registros_blue.reverse()

        if len(registros_blue) < 2:
            return ""

        precios = [float(d['value_sell']) for d in registros_blue]
        fechas = [d['date'] for d in registros_blue]

        paso = (len(precios) - 1) / (ancho - 1) if ancho > 1 else 1
        muestras = [precios[int(round(i * paso))] for i in range(ancho)]

        min_p = min(muestras)
        max_p = max(muestras)
        rango = max_p - min_p if max_p != min_p else 1.0

        filas_puntos = [int(round((p - min_p) / rango * (altura - 1))) for p in muestras]

        lienzo = [[" " for _ in range(ancho)] for _ in range(altura)]
        for col in range(ancho - 1):
            y1 = (altura - 1) - filas_puntos[col]
            y2 = (altura - 1) - filas_puntos[col + 1]

            if y1 == y2:
                lienzo[y1][col] = "─"
            elif y1 < y2:
                lienzo[y1][col] = "╮"
                for y in range(y1 + 1, y2):
                    lienzo[y][col] = "│"
            else:
                lienzo[y1][col] = "╯"
                for y in range(y2 + 1, y1):
                    lienzo[y][col + 1] = "│"

        ultimo_y = (altura - 1) - filas_puntos[-1]
        lienzo[ultimo_y][-1] = "─"

        lineas_grafico = []
        for r in range(altura):
            val_eje = max_p - (r / (altura - 1)) * rango
            etiqueta_eje = f"${val_eje:5.0f} ┤"
            lineas_grafico.append(etiqueta_eje + "".join(lienzo[r]))

        eje_x = "       └" + "─" * (ancho) + "┘"
        
        # Fechas con formato DD/MM
        f_ini_partes = fechas[0].split("-")
        f_fin_partes = fechas[-1].split("-")
        fecha_ini = f"{f_ini_partes[2]}/{f_ini_partes[1]}"
        fecha_fin = f"{f_fin_partes[2]}/{f_fin_partes[1]}"

        espacio = " " * (ancho - len(fecha_ini) - len(fecha_fin) + 1)
        fechas_pie = f"        {fecha_ini}{espacio}{fecha_fin} (Últimos 30 días)"

        encabezado = f"\nEvolución Dólar Blue (Mín: ${min_p:.0f} | Máx: ${max_p:.0f}):\n"
        return encabezado + "\n".join(lineas_grafico) + "\n" + eje_x + "\n" + fechas_pie
    except Exception:
        return ""

def obtener_clima():
    try:
        url = "https://wttr.in/?format=j1&lang=es"
        req = urllib.request.Request(url, headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req, timeout=8) as response:
            data = json.loads(response.read().decode())
            
            ciudad = data['nearest_area'][0]['areaName'][0]['value']
            temp_actual = data['current_condition'][0]['temp_C']
            sensacion = data['current_condition'][0]['FeelsLikeC']
            
            desc = data['current_condition'][0].get('lang_es', [{'value': ''}])[0]['value']
            if not desc:
                desc = data['current_condition'][0]['weatherDesc'][0]['value']
            
            min_temp = data['weather'][0]['mintempC']
            max_temp = data['weather'][0]['maxtempC']
            
            return f"🌤️ {ciudad}: {temp_actual}°C ({desc})  |  Min: {min_temp}°C - Max: {max_temp}°C (ST: {sensacion}°C)"
    except Exception:
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
    grafico = ""
    
    if modo == "dolar" or modo == "todo":
        grafico = obtener_grafico_blue_30d()

    if modo == "clima":
        mensaje_notif = clima
        mensaje_consola = clima
        titulo = "Reporte del Clima"
        icono = "weather-clouds"
    elif modo == "dolar":
        mensaje_notif = dolares
        mensaje_consola = dolares + (grafico if grafico else "")
        titulo = "Cotizaciones del Dólar"
        icono = "help-donate"
    else:
        mensaje_notif = f"{clima}\n{dolares}"
        mensaje_consola = f"{clima}\n{dolares}" + (grafico if grafico else "")
        titulo = "Resumen Matutino"
        icono = "appointment-soon"
    
    print("\n" + mensaje_consola + "\n")
    
    subprocess.run([
        "notify-send",
        "-t", "12000",
        "-i", icono,
        titulo,
        mensaje_notif
    ])

if __name__ == "__main__":
    param = sys.argv[1] if len(sys.argv) > 1 else "todo"
    ejecutar(param)
