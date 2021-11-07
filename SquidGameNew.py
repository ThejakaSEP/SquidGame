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
    os.system("afplay GunFire.mp3")

def playMusic2():
    os.system("afplay SquidSound2.mp3")

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
previousTime = 0
list1 = []
difference = []
TotalDif = []
level = 0
run_ = True
run2_ = True

while run_ and run2_:
    playMusic2()

    print("=========================")
    print("Start Time: ", time.asctime(time.localtime(time.time())))

    myTime3 = time.time()

    while ((time.time() - myTime3) < 5 ) and run2_:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        cv2.imshow("Image", img)
        try:
            if len(list1) != 0:
                difference = np.array(list1) - np.array(lmList)
                difference = abs(difference)
                sumOfDif = sum(sum(difference))
                level += 1
                TotalDif.append(sumOfDif)

                if sumOfDif > 100 :
                    # time.sleep(3)
                    # cv2.imshow("Image", img)
                    # playDeadSound()
                    cv2.putText(img, "You are Dead!!!", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                    cv2.putText(img,"Level: %s "% str(int(level)), (170, 170), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                    cv2.imshow("Image", img)
                    playDeadSound()
                    img2 = img
                    # run_ = False
                    # break
                    run2_ = False

                else:
                    cv2.putText(img, "Ela", (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    cv2.imshow("Image", img)
        except:
            pass

        try:
            list1 = lmList
        except:
            pass

        k = cv2.waitKey(1)
        # cv2.waitKey(0)
        # print("Stop!!!")
        # if (time.time()-myTime)>5:
        #     break
        # if k == 27:  # close on ESC key#
        #     break

    try:
        print("Average : ",np.average(TotalDif))
        print("Max:", max(TotalDif))
        print("Min: ",min(TotalDif))
        print("Current Time : ", time.asctime(time.localtime(time.time())))
        print("Level: ", level)

    except:
        pass

cv2.imshow("Image", img2)
# k = cv2.waitKey(1)
# if k == 27:# close on ESC key#
#     quit()
cv2.waitKey(0)

