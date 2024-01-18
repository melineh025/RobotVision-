import numpy as np
import cv2
import math

video_capture = cv2.VideoCapture('videoplayback.mp4')
#('videoplayback.mp4')


while(True):
    # Capture the frames
    ret, frame = video_capture.read()
    final = frame

    # change from bgr values to hsv values
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # color bounds of color to be filtered out
    lower_color_bounds = np.array([0, 200, 0])
    upper_color_bounds = np.array([255, 255, 255])
    # threshold shows in black the pixels being filtered out
    threshold = cv2.inRange(hsv, lower_color_bounds, upper_color_bounds)

    # erode to remove noise
    kernel = np.ones((10, 10), np.uint8)
    erode = cv2.erode(threshold, kernel)

    # get the contours
    contours = cv2.findContours(erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    #contours = cv2.findContours(erode, 1, 2)
    cnt = contours[0]
    # bounding box the two largest contours
    #contour_areas = [cv2.contourArea(x) for x in contours]  # get the areas of each contour
    contour_areas = cv2.contourArea(cnt)
    



    contour_indexes = np.argsort(contour_areas)  # sort the indexes of the largest areas
    gate_heights = [] # height of both gates
    for i in contour_indexes[-2:]:  # only look at the two largest contours
        (x,y,w,h) = cv2.boundingRect(contours[i])  # get the location/dimensions of a bounding box for the contour
        gate_heights.append(h) # get gate heights
        cv2.rectangle(final, pt1=(x,y), pt2=(x+w,y+h), color=(255,0,0), thickness=5)  # draw the bounding box on the image

        # for visibility, we will place a background fill on the contour label
        text = "gatepost"
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_PLAIN, 1, 1)
        text_w, text_h = text_size
        cv2.rectangle(final, pt1=(x, y), pt2=(x + text_w, y - 2*text_h), color=(255, 0, 0), thickness=-1)
        cv2.putText(final, "gatepost", org=(x, y-5), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(255, 255, 255), thickness=1)

    # possible Robosub reactions
    if len(gate_heights) >= 2:
        h1 = gate_heights[0]
        h2 = gate_heights[1]

        if abs(h1 - h2) < 100: # if gate heights are roughly the same height, sub moves forwards
            print("forwards")
        else: # else sub needs to position itself correctly first
            print("idle")
    else:
        print("two gates not detected")

    # show frames
    cv2.imshow('original frame',frame)
    cv2.imshow('threshold', threshold)
    cv2.imshow("eroded", erode)
    cv2.imshow("final", final)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
