import camera
import os

# Configurar la cámara
def init_camera():
    camera.init(0, format=camera.JPEG)
    camera.framesize(camera.FRAME_VGA)  # Tamaño de la imagen: QVGA, VGA, SVGA, etc.
    camera.flip(0)
    camera.mirror(0)
    camera.saturation(0)  # Ajuste de saturación (0 para sin ajuste)
    camera.contrast(0)    # Ajuste de contraste (0 para sin ajuste)
    camera.brightness(0)  # Ajuste de brillo (0 para sin ajuste)
    camera.quality(10)    # Ajuste de calidad de imagen (10 es estándar)
    print("Cámara inicializada")

# Función para capturar la imagen y guardarla en la memoria
def capture_image(filename='captura.jpg'):
    buf = camera.capture()
    if buf:
        # Guardar la imagen capturada en la memoria con el nombre especificado
        with open(filename, 'wb') as f:
            f.write(buf)
        print(f"Imagen guardada como {filename}")
    else:
        print("Error al capturar la imagen")

# Inicializar la cámara
init_camera()

# Capturar y guardar la imagen
capture_image("imagen_esp32.jpg")

# Liberar los recursos de la cámara al terminar
camera.deinit()