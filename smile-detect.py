#!/usr/bin/env python
import cv2.cv as cv
import cv2
import time
import Image
import threading
###########################
import matplotlib
import datetime
import matplotlib.dates as md
import time
##########################

cv.NamedWindow("camera", 1)
capture = cv.CreateCameraCapture(0)

#font = cv.CvFont
font = cv.InitFont(1, 1, 1, 1, 1, 1)

width = None
height = None
width = 640#480 #320
height = 480 #360#240
smileness = 0
smilecount = 0

if width is None:
    width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,width)    

if height is None:
    height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
else:
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,height) 

result = cv.CreateImage((width,height),cv.IPL_DEPTH_8U,3) 

mqLoop = 0




def DetectRedEyes(image, faceCascade, smileCascade):
    min_size = (20,20)
    image_scale = 2
    haar_scale = 1.2
    min_neighbors = 2
    haar_flags = 0

    # Allocate the temporary images
    gray = cv.CreateImage((image.width, image.height), 8, 1)
    smallImage = cv.CreateImage((cv.Round(image.width / image_scale),cv.Round (image.height / image_scale)), 8 ,1)

    # Convert color input image to grayscale
    cv.CvtColor(image, gray, cv.CV_BGR2GRAY)

    # Scale input image for faster processing
    cv.Resize(gray, smallImage, cv.CV_INTER_LINEAR)

    # Equalize the histogram
    cv.EqualizeHist(smallImage, smallImage)

    # Detect the faces
    faces = cv.HaarDetectObjects(smallImage, faceCascade, cv.CreateMemStorage(0),
    haar_scale, min_neighbors, haar_flags, min_size)

    # If faces are found
    if faces:
        
        #print faces

        for ((x, y, w, h), n) in faces:
        # the input to cv.HaarDetectObjects was resized, so scale the
        # bounding box of each face and convert it to two CvPoints
            #print "face"
            pt1 = (int(x * image_scale), int(y * image_scale))
            pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
            # print pt1
            # print pt2
            #cv.Rectangle(image, pt1, pt2, cv.RGB(255, 0, 0), 1, 8, 0)
            #corner 1
            #str(pt2[1] - pt1[1])
            #cv.PutText(image, "hi!", pt1, font, cv.RGB(255, 0, 0))
            
            #cv.PutText(image, "(pt1[0],pt1[1])", pt1, font, cv.RGB(255, 0, 0))
            #corner 2
            #cv.PutText(image, "(pt2[0],pt1[1])", (pt2[0],pt1[1]), font, cv.RGB(255, 0, 0))
            #corner 3
            #cv.PutText(image, "(pt1[0],pt2[1])", (pt1[0],pt2[1]), font, cv.RGB(255, 0, 0))
            #corner 4
            #cv.PutText(image, "(pt2[0],pt2[1])", pt2, font, cv.RGB(255, 0, 0))
            #face_region = cv.GetSubRect(image,(x,int(y + (h/4)),w,int(h/2)))            
            #split face
            #cv.Rectangle(image, (pt1[0],(pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))), pt2, cv.RGB(0,255,0), 1, 8, 0)
            #cv.PutText(image, "isolating lower", (pt1[0],(pt1[1] + (abs(pt1[1]-pt2[1]) / 2 ))), font, cv.RGB(0, 255, 0))
            
            cv.SetImageROI(image, (pt1[0],
                               (pt1[1] + int(abs(pt1[1]-pt2[1]) / 1.6 )),
                               pt2[0] - pt1[0],
                               int((pt2[1] - (pt1[1] + int(abs(pt1[1]-pt2[1]) / 1.6 ))))))
            
            smiles = cv.HaarDetectObjects(image, smileCascade, cv.CreateMemStorage(0), 1.1, 5, 0, (15,15))
            
            if smiles:
                #print smiles
                
                for smile in smiles:
                    #cv.Rectangle(image,
                    #(smile[0][0],smile[0][1]),
                    #(smile[0][0] + smile[0][2], smile[0][1] + smile[0][3]),
                    #cv.RGB(0, 0, 255), 1, 8, 0)

                    #cv.PutText(image, "smile", (smile[0][0],smile[0][1]), font, cv.RGB(0, 0, 255))
                    
                    #cv.PutText(image,str(smile[1]), (smile[0][0], smile[0][1] + smile[0][3]), font, cv.RGB(0, 0, 255))
                    
                    
                    #print ((abs(smile[0][1] - smile[0][2]) / abs(pt1[0] - pt2[0])) * 100)
                    cv.ResetImageROI(image)
                    if smile[1] + smile[0][3] > 45:
                        cv.Circle(image, ( (pt1[0] +pt2[0])/2 ,(pt1[1] + pt2[1])/2 ), w, (47,255,173), -1, lineType=8, shift=0)
                        #cv.SetImageROI(image,(pt1[0] +pt2[0])/2 ,(pt1[1] + pt2[1])/2 ) ,)
                        smilept1 = (int((pt1[0] + (pt1[0]+pt2[0])/2)/2),int((pt2[1] + (pt1[1] + pt2[1])/2 ))/2)
                        smilept2 = (int(((pt1[0]+pt2[0])/2+pt2[0])/2),pt2[1])# int(((pt1[1]+pt2[1])/2 + pt2[1])/2))
                        #cv.Rectangle(image, smilept1, smilept2, cv.RGB(0,255,0), 1, 8, 0)
                        #cv2.ellipse(image,(256,256),(100,50),0,0,180,255,-1)
                        #cv.SetImageROI(image, (smilept1[0], smilept1[1], smilept2[0]-smilept1[0], smilept2[1]-smilept1[1]))
                        #cv.Circle(image, ( (pt1[0] +pt2[0])/2,(pt1[1] + pt2[1])/2+40), int(w/1.2), (0,0,0), -1, lineType=8, shift=0)
                        cv.Ellipse(image,  ((pt1[0] +pt2[0])/2 ,(pt1[1] + pt2[1])/2 + int(w/7) ), (int(w/1.7),h/2), 270, 90, 270, (0,0,0), thickness=4, lineType=4, shift=0)
                        eyept1 = (int((pt1[0] + (pt1[0]+pt2[0])/2)/2),int((pt1[1] + (pt1[1] + pt2[1])/2 ))/2)
                        eyept2 = (int(((pt1[0]+pt2[0])/2+pt2[0])/2),int(((pt1[1]+pt2[1])/2 + pt1[1])/2))
                        cv.Circle(image, eyept1, int(w/9), (0,0,0), -1, lineType=8, shift=0)
                        cv.Circle(image, eyept2, int(w/9), (0,0,0), -1, lineType=8, shift=0)
                    
                    global smileness 
                    smileness = smile[1]
                    cv.SetImageROI(image, (pt1[0],
                               (pt1[1] + int(abs(pt1[1]-pt2[1]) / 1.6 )),
                               pt2[0] - pt1[0],
                               int((pt2[1] - (pt1[1] + (abs(pt1[1]-pt2[1]) / 1.6 ))))))
            else:
                cv.ResetImageROI(image)
                cv.Circle(image, ( (pt1[0] +pt2[0])/2 ,(pt1[1] + pt2[1])/2 ), w, (0,0,255), -1, lineType=8, shift=0)
                eyept1 = (int((pt1[0] + (pt1[0]+pt2[0])/2)/2),int((pt1[1] + (pt1[1] + pt2[1])/2 ))/2)
                eyept2 = (int(((pt1[0]+pt2[0])/2+pt2[0])/2),int(((pt1[1]+pt2[1])/2 + pt1[1])/2))
                cv.Circle(image, eyept1, int(w/9), (0,0,0), -1, lineType=8, shift=0)
                cv.Circle(image, eyept2, int(w/9), (0,0,0), -1, lineType=8, shift=0)
                smilept1 = (int((pt1[0] + (pt1[0]+pt2[0])/2)/2),int((pt2[1] + (pt1[1] + pt2[1])/2 ))/2)
                smilept2 = (int(((pt1[0]+pt2[0])/2+pt2[0])/2),int(((pt1[1]+pt2[1])/2 + pt2[1])/2))
                cv.Line(image, smilept1, smilept2, (0,0,0), thickness=3, lineType=8, shift=0)
                cv.SetImageROI(image, (pt1[0],
                               (pt1[1] + int(abs(pt1[1]-pt2[1]) / 1.6 )),
                               pt2[0] - pt1[0],
                               int((pt2[1] - (pt1[1] + int(abs(pt1[1]-pt2[1]) / 1.6 ))))))
            cv.ResetImageROI(image)
    cv.ResetImageROI(image)
    return image

faceCascade = cv.Load("haarcascade_frontalface_alt.xml")
#eyeCascade = cv.Load("haarcascade_eye.xml")
smileCascade = cv.Load("smileD/smiled_01.xml")
#smileCascade = cv.Load("haarcascade_smile.xml")


while True:
    img = cv.QueryFrame(capture)
    
    if img:
        image = DetectRedEyes(img, faceCascade, smileCascade)
        cv.ShowImage("camera", image)
    #print smileness
    
    k = cv.WaitKey(5);
    if k == 27:
        break
    
cv.DestroyAllWindows()
