import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
import pygame
import prueba

def rep_alerta(ruta_sonido):
    pygame.mixer.init()
    sonido = pygame.mixer.Sound(ruta_sonido)
    sonido.play()


cred = credentials.Certificate("servicesAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "registro-7bd66.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgBackground = cv2.imread('Resources/background.png')

# Importamos las imagenes de modelo en una lista
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))

print(len(imgModeList))

# Cargar EncodeFile
file = open('EncodeFile.p', 'rb')
encodeListKnowWithsIds = pickle.load(file)
file.close()
encodeListKnow, studentsId = encodeListKnowWithsIds
print(studentsId)

modeType = 0
counter = 0
id = -1
usuario = ""
imgStudent = []
edad = 0
while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnow, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnow, encodeFace)
            print("matches", matches)
            print("faceDis", faceDis)
            matchIndex = np.argmin(faceDis)
            # print("Match Index", matchIndex)
            if matches[matchIndex]:
                if faceDis[matchIndex] < 0.35:
                    # print("Rostro Detectado")
                    # print(studentsId[matchIndex])
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentsId[matchIndex]
                    aux = id.split("_")[0]
                    id = aux
                    print(id)
                    if counter == 0:
                        cvzone.putTextRect(imgBackground, 'Loading', (275, 275))
                        cv2.imshow("Control de Ingreso", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1
                        usuario = id
            else:
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                cvzone.putTextRect(imgBackground, 'Failed', (275, 275))
                cv2.imshow("Control de Ingreso", imgBackground)
                cv2.waitKey(1)
                counter = 0
                modeType = 0
                imgStudent = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[4]
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[5]
                rep_alerta('alerta.wav')

        if counter != 0:
            # noinspection PyBroadException
            try:

                if counter == 1:
                    blob = bucket.get_blob(f'Images/{usuario}.png')
                    array = np.frombuffer(blob.download_as_string(), np.uint8)
                    imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                    ultimo_registro = prueba.obtener_ultimo_registro(usuario)
                    print(ultimo_registro)
                    datetimeObject = datetime.strptime(ultimo_registro, "%Y-%m-%d %H:%M:%S")
                    print(datetimeObject)
                    secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                    print(secondsElapsed)

                    if secondsElapsed > 30:
                        prueba.insertar_registro(usuario)
                    else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                if modeType != 3:
                    if 8 < counter < 15:
                        modeType = 2

                    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

                    if counter <= 8:
                        # noinspection PyUnboundLocalVariable

                        cv2.putText(imgBackground, str(prueba.obtener_datos(usuario).typo), (862, 120), cv2.FONT_HERSHEY_TRIPLEX, 0.7,
                                    (255, 255, 255),
                                    1)
                        cv2.putText(imgBackground, str(usuario), (1006, 493), cv2.FONT_HERSHEY_TRIPLEX, 0.6,
                                    (255, 255, 255),
                                    1)
                        cv2.putText(imgBackground, str(prueba.obtener_datos(usuario).cedula), (1006, 550), cv2.FONT_HERSHEY_TRIPLEX,
                                    0.6, (255, 255, 255),
                                    1)
                        cv2.putText(imgBackground, str(prueba.obtener_ultimo_registro(usuario)), (900, 650), cv2.FONT_HERSHEY_TRIPLEX,
                                    0.6,
                                    (50, 50, 50),
                                    1)

                        (w, h), _ = cv2.getTextSize(str(prueba.obtener_datos(usuario).nombre), cv2.FONT_HERSHEY_TRIPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(prueba.obtener_datos(usuario).nombre), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_TRIPLEX, 1, (50, 50, 50),
                                    1)
                        dim = 216
                        imgStudent_modificada = cv2.resize(imgStudent, (dim, dim))
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent_modificada

                    counter += 1

                    if counter >= 15:
                        counter = 0
                        modeType = 0
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
            except Exception as e:
                print(e)
                counter = 0
                modeType = 0
                imgStudent = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[5]
                rep_alerta('alerta.wav')

    else:
        modeType = 0
        counter = 0
    cv2.imshow("Control de Ingreso", imgBackground)

    cv2.waitKey(1)
