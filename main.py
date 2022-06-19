import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import time
import random


cap = cv2.VideoCapture(0)

 
detector = HandDetector(detectionCon=0.8, maxHands=1)


x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57] #x piksel değerleri
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]  #cm cinsinden değeri

#polyfit fonksiyonunu kullanarak x ve y arasında bir denklem oluşturuyoruz.
coff = np.polyfit(x, y, 2)  
# y = Ax^2 + Bx + C

finishTime =0
cx, cy = 300, 300
circleColor = (255, 0, 0)
counter = 0
score = 0
timeStart = time.time() 
totalTime = 60
level = 1
finish = 0
backgroundColor= (255,0,0)

def textWin():
    cvzone.putTextRect(img, 'KAZANDINIZ!', (450, 250), scale=3, offset=20,colorR=backgroundColor)
    cvzone.putTextRect(
        img, f'Skorunuz: {score}', (450, 350), scale=3, offset=20,colorR=backgroundColor)
    cvzone.putTextRect(img,(str)(finishTime) + ' saniye kala bitirdiniz.',
                       (350, 450), scale=2, offset=10,colorR=backgroundColor)
    
    cvzone.putTextRect(
        img, f' {level}. seviyeyi tamamlayarak oyunu bitirdiniz.', (350, 520), scale=2, offset=10,colorR=backgroundColor)
    cvzone.putTextRect(
        img, 'Yeniden oynamak icin R tusuna basiniz.', (350, 585), scale=2, offset=10,colorR=backgroundColor)
    cvzone.putTextRect(img, 'Q tusuna basarak cikabilirsiniz.',
                       (350, 650), scale=2, offset=10,colorR=backgroundColor)
                       
    

 
def textLose():
    cvzone.putTextRect(img, 'KAYBETTINIZ!', (450, 250), scale=3, offset=20,colorR=backgroundColor)
    cvzone.putTextRect(
        img, f'Skorunuz: {score}', (450, 350), scale=3, offset=20,colorR=backgroundColor)
    cvzone.putTextRect(img,'Sure bitti',
                       (350, 450), scale=2, offset=10,colorR=backgroundColor)
    
    cvzone.putTextRect(
        img, f' {level}. seviye ile oyun bitti.', (350, 520), scale=2, offset=10,colorR=backgroundColor)
    cvzone.putTextRect(
        img, 'Yeniden oynamak icin R tusuna basiniz.', (350, 585), scale=2, offset=10,colorR=backgroundColor)
    cvzone.putTextRect(img, 'Q tusuna basarak cikabilirsiniz.',
                       (350, 650), scale=2, offset=10,colorR=backgroundColor)


def status():
    cvzone.putTextRect(img, f'Zaman: {int((totalTime)-(time.time()-timeStart))}',
                       (1000, 75), scale=3, offset=20,colorR=backgroundColor)
    cvzone.putTextRect(
        img, f'Skor: {str(score).zfill(2)}', (60, 75), scale=3, offset=20,colorR=backgroundColor)
    cvzone.putTextRect(
        img, f'Seviye: {str(level)}', (600, 75), scale=3, offset=20,colorR=backgroundColor)
while True:
    ret, img = cap.read()
    
    img = cv2.flip(img, 1)


   
   
    if time.time()-timeStart < totalTime:

        if finish != 1:
            hands = detector.findHands(img, draw=False)

            if hands:
                lmList = hands[0]['lmList']
                x, y, w, h = hands[0]['bbox']
                # 5 ve 17 arasında ki noktaların mesafesi elimizi kameradan uzaklaştırdıkça piksel olarak azalıcak.cm cinsinden de elimizin kameraya olan mesafesi artacak.
                x1, y1, _ = lmList[5]
                x2, y2, _ = lmList[17]


                #17 ve 5 markları arasında ki mesafeyi ölçüyoruz.pisagor yapıyoruz ki stabiliteyi koruyalım.
                distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
                
                #aralarında ilişki kurduğumuz denklemden gelen katsayıları alıyoruz.
                A, B, C = coff
                #son olarak CM çevrimini yapıyoruz.
                distanceCM = A * distance ** 2 + B * distance + C
                print("Pixel uzaklık: ", distance, " CM uzaklık: " , distanceCM)
                if distanceCM < 30:
                    if x < cx < x + w and y < cy < y + h:
                        counter = 1
                cv2.rectangle(img, (x, y), (x + w, y + h), backgroundColor, 3)
                cvzone.putTextRect(
                    img, f'{int(distanceCM)} cm', (x + 5, y - 10),colorR=backgroundColor)

                if counter > 0:
                    counter += 1
                    circleColor = (0, 255, 0)
                    if counter == 4:
                        if score < 10:
                            cx = random.randint(100, 1100)
                            cy = random.randint(100, 650)
                            circleColor = (255, 0, 0)
                            score += 1
                            counter = 0
                        elif score < 20:
                            cx = random.randint(100, 1100)
                            cy = random.randint(100, 600)
                            backgroundColor = (255,0,255)
                            circleColor = backgroundColor
                            score += 1
                            level = 2
                            counter = 0
                        
                        elif score < 30:
                            cx = random.randint(100, 1100)
                            cy = random.randint(100, 600)
                            backgroundColor = (0,255,255)
                            circleColor = backgroundColor
                            score += 1
                            counter = 0
                            level = 3
                        elif score <39:
                            cx = random.randint(100, 1100)
                            cy = random.randint(100, 600)
                            backgroundColor = (0,0,255)
                            circleColor = backgroundColor
                            score += 1
                            counter = 0
                            level = 3
                        else:
                            score +=1
                            finish = 1
                            counter = 0
                            finishTime = int((totalTime)-(time.time()-timeStart))
                            

            cv2.circle(img, (cx, cy), 50, circleColor, cv2.FILLED)
        elif finish == 1:      
            textWin()
            

        
        if finish == 0:
            status()
    else:
        if finish != 1:
            textLose()
        else:
            textWin()
            

    cv2.imshow("Oyun", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timeStart = time.time()
        score = 0
        finish = 0
        circleColor = (255, 0, 0)
        backgroundColor= (255,0,0)
        level = 1

    if key == ord('q'):
        break
