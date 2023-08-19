import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate("servicesAccountKey.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': "registro-7bd66.appspot.com"
})

# Importamos las imagenes de los estudiantes
folderPath = 'Images'
PathList = os.listdir(folderPath)
print(PathList)
imgList = []
studentsId = []

for path in PathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentsId.append(os.path.splitext(path)[0])

    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
print(studentsId)

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)

    return encodeList

encodeListKnow = findEncodings(imgList)
encodeListKnowWithIds = [encodeListKnow, studentsId]
print("Completado...")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnowWithIds, file)
file.close()
print("File Saved")