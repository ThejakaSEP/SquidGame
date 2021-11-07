#Example of how to use the Created Class
import cv2
import time
import MotionDetectionModule as pm
import numpy as np
import schedule
import pygame
import sys
import os

soundPath1 = "SquidGame.mp3"
soundPath2 = "GunFire.mp3"

def playMusic():
    pygame.mixer.init()
    pygame.mixer.music.load(soundPath1)
    pygame.mixer.music.play()

def playDeadSound():
    pygame.mixer.init()
    pygame.mixer.music.load(soundPath2)
    pygame.mixer.music.play()

def playMusic2():
    os.system("afplay SquidGame.mp3")

def func1():
    cap = cv2.VideoCapture(0)
    detector = pm.poseDetector()
    previousTime = 0
    list1 = []
    difference = []
    TotalDif = []
    myTime = time.time()
    print("=========================")
    print("Start Time: ",time.asctime(time.localtime(myTime)))

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        try:
            if len(list1) != 0:
                difference = np.array(list1) - np.array(lmList)
                difference = abs(difference)
                sumOfDif = sum(sum(difference))
                # sumOfDif = sum(difference)

                # print(sumOfDif)
                # print("===================")
                TotalDif.append(sumOfDif)
                # print(lmList[0])
                if sumOfDif > 100 :
                    cv2.putText(img, "You are Dead!!!", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                    # playDeadSound()
                    # break


        except:
            pass

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        # cv2.putText(img, str(int(fps)), (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        cv2.imshow("Image", img)

        try:
            list1 = lmList
            # print(list1)

        except:
            pass

        k = cv2.waitKey(1)
        # cv2.waitKey(0)
        # print("Stop!!!")
        if (time.time()-myTime)>5:
            break
        # if k == 27:  # close on ESC key#
        #     break
    #
    try:
        print("Average : ",np.average(TotalDif))
        print("Max:", max(TotalDif))
        print("Min: ",min(TotalDif))
        print("Current Time : ", time.asctime(time.localtime(currentTime)))
    except:
        pass

schedule.every(5).seconds.do(func1)
schedule.every(5).seconds.do(playMusic)

while 1:
    schedule.run_pending()
    time.sleep(1)
