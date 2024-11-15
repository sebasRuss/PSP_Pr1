import psutil
import os
import subprocess
import time
import subprocess
import pywin32clipboard

#obtenemos la lista de procesos
def listar_procesos(nombre_proceso):
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        if nombre_proceso.lower() in proc.info['name'].lower():
            print(f"Proceso: {proc.info['name']}, PID: {proc.info['pid']}, Uso de memoria: {proc.info['memory_percent']}%")
        else:
            print(f"El proceso {nombre_proceso} no está en ejecución.")

#finalizar un proceso especifico
def finalizar_proceso(nombre_proceso):
    for proc in psutil.process_iter(['pid', 'name']):
        if nombre_proceso.lower() in proc.info['name'].lower():
            try:
                proc.terminate()
                print(f"Proceso {nombre_proceso} finalizado correctamente.")
            except psutil.NoSuchProcess:
                print(f"No se pudo finalizar el proceso {nombre_proceso}.")
            return
    print(f"Proceso {nombre_proceso} no encontrado.")

#comunicacion interprocesos pipes
def comunicacion_con_pipes():
    pid = os.fork()
    if pid == 0:  # Hijo
        mensaje = input("Hijo: Ingresa un mensaje: ")
        mensaje = mensaje.upper()
        os.write(os.pipe()[1], mensaje.encode())
    else:  # Padre
        mensaje, _ = os.pipe()
        mensaje_hijo = os.read(mensaje[0], 1024).decode()
        print(f"Padre: El hijo envió: {mensaje_hijo}")

def ejecutar_programa(modo, programa):
    if modo == 'sincrono':
        start = time.time()
        subprocess.call(programa)
        end = time.time()
        print(f"Tiempo de ejecución síncrona: {end - start} segundos")
    else:
        start = time.time()
        subprocess.Popen(programa)
        end = time.time()
        print(f"Tiempo de ejecución asíncrona (inicio): {end - start} segundos")

#transferencia de datos
def verificar_portapapeles():
    while True:
        try:
            pywin32clipboard.OpenClipboard()
            data = pywin32clipboard.GetClipboardData()
            pywin32clipboard.CloseClipboard()
            # ... (Procesar el contenido del portapapeles)
        except pywin32clipboard.pywintypes.error:
            pass  # No hay datos en el portapapeles