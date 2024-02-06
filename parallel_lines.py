import cv2
import numpy as np
import math
 
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('videoplayback.mp4')
 
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")
 
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
 
    
    src =  cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dst = cv2.Canny(src, 100, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 40, None, 0, 0)
    cdstP = np.copy(cdst)

    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))

                # Get the endpoints of the line
            x1 = int(x0 + 1000 * (-b))
            y1 = int(y0 + 1000 * (a))
            x2 = int(x0 - 1000 * (-b))
            y2 = int(y0 - 1000 * (a))

            # Find the midpoint
            midpoint_x = (x1 + x2) // 2
            midpoint_y = (y1 + y2)  // 2

            #cv2.line(cdst, (x1, y1), (x2, y2), (0, 255, 255), 2)
            #cv2.circle(cdst, (midpoint_x, midpoint_y), 5, (255, 0, 0sssssss), -1)

            # filter for straight lines representing the gate
            if(theta < 5 and theta > 0):
               cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)
               #cv2.line(cdst, (x1, y1), (x2, y2), (0, 255, 255), 2)
               cv2.circle(cdst, (0 , 0), 5, (255, 0, 0), -1)

    #average liness
    

               
    

    linesP = cv2.HoughLinesP(dst, 1, np.pi / 180, 30, None, 50, 10)
    
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]

            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)


    cv2.imshow('Frame',frame)
    cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    
    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)

  

    # Press Q on keyboard to  exit
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
 
  # Break the loop
  else: 
    break
 
# When everything done, release the video capture object
cap.release()
 
# Closes all the frames
cv2.destroyAllWindows()
