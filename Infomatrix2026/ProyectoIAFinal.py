from ultralytics import YOLO
import cv2
import serial
import time

# ===== SERIAL =====
PORT = "COM3"
BAUD = 9600
arduino = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)

def enviar_estado(semaforo_id: int, estado: str):
    # estado: "ROJO" o "VERDE"
    arduino.write(f"S{semaforo_id}:{estado}\n".encode("utf-8"))

def estado_para_arduino(estado_texto: str) -> str:
    if "VERDE" in estado_texto:
        return "VERDE"
    return "ROJO"

# ===== MODELO =====
model = YOLO("yolov8n.pt")

# ===== CAMARAS =====
cap1 = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)

if not cap1.isOpened() or not cap2.isOpened():
    print("No se pudieron abrir las cámaras")
    exit()

ultimo_s1 = ""
ultimo_s2 = ""

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not ret1 or not ret2:
        break

    # ================= CAMARA 1 =================
    results1 = model(frame1, stream=True)
    for r in results1:
        annotated1 = r.plot()
        boxes = r.boxes

        if boxes is not None:
            classes = boxes.cls.cpu().numpy().astype(int)
            carros1 = (classes == 2).sum()
            motos1 = (classes == 3).sum()
            buses1 = (classes == 5).sum()
            camiones1 = (classes == 7).sum()
            personas1 = (classes == 0).sum()
        else:
            carros1 = motos1 = buses1 = camiones1 = personas1 = 0

    vehiculos1 = carros1 + motos1 + buses1 + camiones1

    if vehiculos1 >= 5:
        estado1, color1 = "MUCHO TRAFICO - VERDE", (0, 255, 0)
    else:
        estado1, color1 = "POCO TRAFICO - ROJO", (0, 0, 255)

    cv2.putText(annotated1, f"Peatones: {personas1}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(annotated1, f"Vehiculos: {vehiculos1}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(annotated1, estado1, (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color1, 2)

    s1 = estado_para_arduino(estado1)
    if s1 != ultimo_s1:
        enviar_estado(1, s1)
        ultimo_s1 = s1

    # ================= CAMARA 2 =================
    results2 = model(frame2, stream=True)
    for r in results2:
        annotated2 = r.plot()
        boxes = r.boxes

        if boxes is not None:
            classes = boxes.cls.cpu().numpy().astype(int)
            carros2 = (classes == 2).sum()
            motos2 = (classes == 3).sum()
            buses2 = (classes == 5).sum()
            camiones2 = (classes == 7).sum()
            personas2 = (classes == 0).sum()
        else:
            carros2 = motos2 = buses2 = camiones2 = personas2 = 0

    vehiculos2 = carros2 + motos2 + buses2 + camiones2

    if vehiculos2 >= 5:
        estado2, color2 = "MUCHO TRAFICO - VERDE", (0, 255, 0)
    else:
        estado2, color2 = "POCO TRAFICO - ROJO", (0, 0, 255)

    cv2.putText(annotated2, f"Peatones: {personas2}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(annotated2, f"Vehiculos: {vehiculos2}", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(annotated2, estado2, (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, color2, 2)

    s2 = estado_para_arduino(estado2)
    if s2 != ultimo_s2:
        enviar_estado(2, s2)
        ultimo_s2 = s2

    cv2.imshow("Camara 1", annotated1)
    cv2.imshow("Camara 2", annotated2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap1.release()
cap2.release()
cv2.destroyAllWindows()
arduino.close()
