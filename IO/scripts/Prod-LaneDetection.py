import cv2
import numpy as np
import time
import smbus

# Diagnostic info
droppedframes = 0
totalframes = 0
isLane = False


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


# Function to detect shape of contour
def check_shape(c):
    area = cv2.contourArea(c)
    if area < 100:
        return False

    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 4:
        # this is a rectangle
        return True
        # compute the bounding box of the contour and use the
        # bounding box to compute the aspect ratio
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        '''
        if ar > 1:
            # if width is greater than height, it is not a lane segment
            return False
        else:
            return True
        '''
    else:
        # shape has more than 4 corners
        return False

# change m (number of standard deviations)
def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]

        # Check position of car against center of lane
def checkpos(lanecenter, threshold = 0, imXCenter = 270):
    leftbound = imXCenter - threshold
    rightbound = imXCenter + threshold
    if lanecenter > rightbound or lanecenter < leftbound:
        return (lanecenter - imXCenter)
    else:
        return 0

# Begin timing
start_time = time.time()

# Read video
cap = cv2.VideoCapture(-1)
previous_turn = 0;
while cap.isOpened():

    __, image = cap.read()

    try:
        # Image dimensions
        imHeight = image.shape[0]
        imWidth = image.shape[1]
        imXCenter = imWidth / 2
    except AttributeError:
        break

    totalframes += 1

    scalefactor = 540.0

    # resize if necessary:
    # Record aspect ratio after scaling width
    r = scalefactor / imWidth
    dim = (int(scalefactor), int(imHeight * r))

    # perform the actual resizing of the image and show it
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    # cv2.imshow("image", image)
    # cv2.waitKey(0)

    # slice the image into tenths and compute lines locally
    sections = 10                      # amount to divide image into
    chunk = image.shape[0]/sections     # number of vertical pixels

    frames = []

    line1 = [[]]
    line1x = []
    line1y = []
    line2 = [[]]
    line2x = []
    line2y = []

    for slice in range(0, sections):

        frame = image[slice*chunk: slice*chunk+chunk, 0:]
        #cv2.imshow("cropped", frame)

        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if np.var(gray, dtype=np.float64) < 400:
                print "blurry"
                is_blurry = 1
                continue
            else:
                is_blurry = 0

            # apply Otsu and Binary thresholding
            ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

            contours, hierarchy = cv2.findContours(thresh, 1, 2)

            # cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
            # cv2.imshow("contours", frame)

            # Number of lanes detected
            centercount = 0
            xCent = []
            yCent = []

            centpoints = []

            contourcount = 0

            oddcount = 0

            # loop over the contours
            for c in contours:
                contourcount += 1
                isLane = check_shape(c)
                if isLane:
                    try:
                        # compute the center of the contour
                        M = cv2.moments(c)
                        # print " M[m00]) %s" %(M["m00"])
                        cX = int(M["m10"] / M["m00"])
                        cY = int(M["m01"] / M["m00"])
                    except ZeroDivisionError:
                        continue
                else:
                    continue

                cpoint = [cX, cY]
                centercount += 1
                centpoints.append([cpoint])
                # xCent.append(cX)
                # yCent.append(cY)

                oddcount += 1

                # print centpoints

                # draw the contour and center of the shape on the image
                if oddcount % 2 == 0:
                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                    line1.append([cpoint])
                    line1x.append(cX)
                    line1y.append(cY + slice*chunk)
                else:
                    cv2.drawContours(frame, [c], -1, (0, 0, 255), 2)
                    line2.append([cpoint])
                    line2x.append(cX)
                    line2y.append(cY + slice * chunk)
                # cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(frame, "center", (cX - 20, cY - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

                # show the image
                # cv2.imshow("cngs", frame)
                # cv2.waitKey(0)
                #k = cv2.waitKey(5) & 0xFF
                #if k == 27:
                    #break

            print "ccount: %s" %contourcount

            if centercount == 2:
                print "2 lanes detected!"
                # print "lanecenter = %s" %(centX[0]-centX[1])
            elif centercount == 1:
                print "1 lane detected. Move"
            elif centercount > 3:
                continue

            frames.append(frame)

        except cv2.error:
            droppedframes += 1
            continue

    try:
        newframe = frames[0]
    except IndexError:
        droppedframes += 1
        continue
    for i in range(1, len(frames)):
        # combine images
        newframe = np.vstack([newframe, frames[i]])

    print "line 1:"

    # Make the two arrays equal in size
    if len(line1x) < len(line2x):
        newsize = len(line2x) - len(line1x)
        line2x = line2x[0:len(line2x)-newsize]
    elif len(line2x) < len(line1x):
        newsize = len(line1x) - len(line2x)
        line1x = line1x[0:len(line1x) - newsize]

    if len(line1y) < len(line2y):
        newsize = len(line2y) - len(line1y)
        line2y = line2y[0:len(line2y)-newsize]
    elif len(line2y) < len(line1y):
        newsize = len(line1y) - len(line2y)
        line1y = line1y[0:len(line1y) - newsize]

    line1x = np.asarray(line1x)
    line2x = np.asarray(line2x)

    line1y = np.asarray(line1y)
    line2y = np.asarray(line2y)

    #line1x = reject_outliers(line1x)

    # Coordinates of center of lane
    midlinex = (line1x + line2x)/2
    
    print "bob's wife", midlinex
    offset = 0
    if midlinex.shape[0] != 0:
        offset = checkpos(midlinex[0])
        


    slopes = []

    for ind in range(1, midlinex.shape[0]):
        m = 99999999 if midlinex[ind-1] == midlinex[ind] else (line1y[ind-1] - line1y[ind]) / (midlinex[ind] - midlinex[ind-1])
        slopes.append(m)

    slopes = np.asarray(slopes)
    

    slope = 0.000000001

    if len(slopes) != 0:
        slope = np.mean(slopes)


    angle = np.rad2deg(np.arctan(1 / slope))

    if angle == float("nan"):
        angle = 90
        print "BOB THE Builder"
    try:
        bob = angle - 5
    except Exception:
        angle = 90
    scale = 3*1.411
    turn_offset = -(int(angle*scale) + offset)/2
    if line1y.shape[0] == 0 or line1x.shape[0] == 0:
        turn_offset = -previous_turn
        print "bob's secret wife", turn_offset
    if line2y.shape[0] == 0 or line2x.shape[0] == 0:
        turn_offset = -previous_turn
        print "bob's secret husband", turn_offset
    
    i2c = smbus.SMBus(1)
    DEVICE_ADDRESS = 0x0a
    #driver.sendData(int(angle*scale))
    print "Bob's second wife", type(int(angle*scale))
    print "not bob's child", type(offset)
    print "bob's secret child", offset
    
    if turn_offset > 127:
        turn_offset = 127
    if turn_offset < -127:
        turn_offset = -127
    # Register write control commands
    # Initializing byte 99
    i2c.write_byte(DEVICE_ADDRESS, 99)
    # vCom setting forward drive (0-255)
    i2c.write_byte(DEVICE_ADDRESS, 75)
    # sCom setting steering (127 (standby), 126-0(max) left, 128-255(max) right)
    i2c.write_byte(DEVICE_ADDRESS, 127 - turn_offset)
    #time.sleep(0.1)
    #127 - int(angle*scale)
    previous_turn = turn_offset
    print "slope: ", slope
    print "angle: ", angle


    line1 = np.asarray(line1)


    # print line1


    try:

        for ind in range (1, midlinex.shape[0]):
            cv2.line(newframe, (midlinex[ind-1], line1y[ind-1]), (midlinex[ind], line1y[ind]), (255, 255, 255), 5)

        '''
        cv2.line(newframe, (line1x[2], line1y[2]), (line1x[5], line1y[5]), (255, 0, 0), 5)
        cv2.line(newframe, (midlinex[2], line1y[2]), (midlinex[5], line1y[5]), (255, 255, 255), 5)
        cv2.circle(newframe, (line2x[2], line2y[2]), 9, (255, 255, 0), -1)
        cv2.circle(newframe, (line2x[5], line2y[5]), 9, (255, 255, 0), -1)
        # cv2.circle(newframe, (0, 0), 9, (255, 255, 0), -1)
        # cv2.circle(newframe, (200, 100), 9, (255, 255, 0), -1)

        cv2.line(newframe, (line1x[2], line1y[2]), (line1x[5], line1y[5]), (255, 0, 0), 5)
        '''

    except IndexError:
        print "whoopsies"
        pass






    '''
    try:
        rows, cols = newframe.shape[:2]
        [vx, vy, x, y] = cv2.fitLine(line1, abs(cv2.DIST_L2), 0, 0.01, 0.01)
        lefty = int((-x * vy / vx) + y)
        righty = int(((cols - x) * vy / vx) + y)
        cv2.line(newframe, (cols - 1, righty), (0, lefty), (255, 0, 0), 5)
    except cv2.error:
        continue
    except OverflowError:
        continue
    '''

    # show the combined image
    cv2.imshow("processed", newframe)
    cv2.waitKey(10)

    # print len(frames)

   

        # Find center of lane
        # xpts = [x1, x2]
        # xavg = np.mean(xpts)  # x-coordinate of center of lane



        
'''

        # Make adjustment
        def adjust(offset):
            if offset > 0:
                print "move right"
            else:
                print "move left"


        checkpos(xavg, 10)

    print("execution times: %s seconds" % (time.time() - start_time))
        '''

# Check how many frames were dropped due to error
print droppedframes
# 9 for sample 1
# 8 for sample 2
# 69 for sample 3

# got 576 and 190 something is off

# print "total frames %s" %(totalframes)



cap.release()
cv2.destroyAllWindows()

