import cv2
import mediapipe as mp
import time

class poseDetector():

    def __init__(self,mode=False,complexity=1,smooth_landmarks=True,segmentation=False,smooth=True,detectionCon=0.5,trackingCon=0.5):

        self.mode = mode
        self.complexity = complexity
        self.smooth_landmarks=smooth_landmarks
        self.segmentation = segmentation
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackingCon = trackingCon


        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                     self.segmentation, self.smooth, self.detectionCon,
                                     self.trackingCon)

    def findPose(self,img,draw=True):

        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)

        if self.results.pose_landmarks:
            if draw:
             self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,
                                       self.mpPose.POSE_CONNECTIONS)

        return img
    def getPosition(self,img,draw=True):
        lmList = []
        if self.results.pose_landmarks:
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                height,width,channel = img.shape
                # print(id,lm)
                cx, cy = int(lm.x*width),int(lm.y*height) #To get the pixel value from the ration decimals shown otherwise
                lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,0),cv2.FILLED)
        return lmList

def main():
    cap = cv2.VideoCapture('PoseVideos/Video3.mp4')
    previousTime = 0

    detector = poseDetector()

    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        if 11 < len(lmList):
            print(lmList[11])
            cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

        currentTime = time.time()
        fps = 1 / (currentTime - previousTime)
        previousTime = currentTime

        cv2.putText(img, str(int(fps)), (70, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
        cv2.imshow("Image", img)

        cv2.waitKey(1)

if __name__ == "__main__":
    main()