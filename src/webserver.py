import network
import esp
import time
import socket
import camera

# Desactivar mensajes de debug
esp.osdebug(False)

# Configuración de tus credenciales Wi-Fi
WIFI_SSID = 'iPhone'
WIFI_PASS = 'jorgerivera'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASS)
    while not wlan.isconnected():
        print('Conectando a Wi-Fi...')
        time.sleep(1)
    print('Conectado a Wi-Fi')
    print('Dirección IP:', wlan.ifconfig()[0])

def init_camera():
    try:
        camera.deinit()  # Asegurarse de reiniciar la cámara
        camera.init(0)  # Inicializar la cámara con valores predeterminados

        # Configurar los parámetros de la cámara utilizando las funciones disponibles
        camera.framesize(camera.FRAME_UXGA)  # 1600x1200
        camera.quality(40)  # Calidad JPEG (10-63), menor es mejor calidad
        camera.brightness(1)  # Brillo: -2 a 2
        camera.contrast(1)  # Contraste: -2 a 2
        camera.saturation(0)  # Saturación: -2 a 2
        camera.flip(0)  # Volteo vertical (0: no voltear)
        camera.mirror(0)  # Espejo horizontal (0: no espejar)
        camera.whitebalance(camera.WB_NONE)  # Balance de blancos automático
        camera.speffect(camera.EFFECT_NONE)  # Sin efecto especial

        print('Cámara inicializada')
    except Exception as e:
        print('Error al inicializar la cámara:', e)

def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Servidor iniciado en:', addr)
    return s

def serve_stream(s):
    boundary = '123456789000000000000987654321'
    while True:
        cl, addr = s.accept()
        print('Cliente conectado desde:', addr)
        cl.settimeout(5.0)
        try:
            request = cl.recv(1024)
            if b'GET / HTTP/1.1' in request:
                cl.send('HTTP/1.1 200 OK\r\n')
                cl.send('Content-Type: multipart/x-mixed-replace; boundary={}\r\n\r\n'.format(boundary))
                while True:
                    buf = camera.capture()
                    if buf:
                        cl.send('--{}\r\n'.format(boundary))
                        cl.send('Content-Type: image/jpeg\r\n')
                        cl.send('Content-Length: {}\r\n\r\n'.format(len(buf)))
                        cl.send(buf)
                        cl.send('\r\n')
                        time.sleep(0.1)
                    else:
                        print('Error al capturar la imagen')
                        break
            else:
                cl.send('HTTP/1.1 404 NOT FOUND\r\n\r\n')
            cl.close()
        except Exception as e:
            print('Error al atender al cliente:', e)
            cl.close()

def main():
    connect_wifi()
 #   init_camera()
 #   s = start_server()
 #   serve_stream(s)
print('primera parte lista')
if __name__ == '__main__':
    main()