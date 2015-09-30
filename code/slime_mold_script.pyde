# add the needed libs
add_library('video')
add_library('opencv_processing')

# setup global objects
video = None
opencv = None
points = []
# l=0
# m=0
n=1
allconlist = []
def setup():
    # reference global objects
    global video
    global opencv
    #set framerate
    frameRate(20)
    
    # sketch size like video
    size(1920, 1080)
    
    #set color mode to HSB
    colorMode(HSB, 360,360,360)
    background(0)
    
    # load the video
    video = Movie(this, "slime mold final mix hd.mpg")
    
    # init openCV
    opencv = OpenCV(this, 1920, 1080)
    
    # setup background subtraction
    opencv.startBackgroundSubtraction(5, 3, 0.5)
    
    # loop and play the video
    video.loop()
    video.play()
    
    # end of setup


def draw():
    
    global allconlist
    
    #### CAPTURE ####
    opencv.loadImage(video)
    
    #### FILTER ####
    opencv.updateBackground()
   # opencv.dilate()
   # opencv.erode()
    opencv.gray()  # make it grayscale
    
    #opencv.contrast(2)  # raise contrast - dont use destroys picture
    opencv.threshold(200)  # clip all below 200

    #### ANALYZE ####
    contours = opencv.findContours(False,True)
    
    #### DISPLAY ####
    # delete bg
    noStroke()
    noFill()
    stroke(0)
    strokeWeight(0.5)
    
    conlist = []
    if contours.size() > 0:
        i = 0
        for c in contours:
            i = i+1
            if i < 15:
                cbb = c.getBoundingBox()
                conlist.append((cbb.x+cbb.width/2, cbb.y+cbb.height/2))
        allconlist.append(conlist)
        
    
        
        

    # loop all points
    print len(allconlist)
    for i in range(1,len(allconlist)):
        oldconlist = allconlist[i-1]
        newconlist = allconlist[i]
        if oldconlist is not None:
            for oldtuple in oldconlist:
                for newtuple in newconlist:
                    drawline(oldtuple,newtuple)

#compare and draw Lines
def drawline(t1,t2):
    global n
    
    #min distance of two contour-middlepoints
    diff = 15
    diffx = abs(t1[0]-t2[0]) #absolute value from x coordinates difference
    diffy = abs(t1[1]-t2[1]) #absolute value from y coordinates difference
    if diff-(diffx+diffy)<10 and diff-(diffx+diffy) > 0 :
        r = abs(diffx*diffy) 
        r2 = 25*(diffx*diffy)
        
        #change stroke Values depending on lenght of line
        #stroke(350-r2,100+r2,r*r)
        stroke(200+r,r,r*diff)
        line(t1[0],t1[1],t2[0],t2[1])
        print r
    elif diff-(diffx+diffy) > 10:
        r = abs(diffx*diffy) 
        r2 = 25*(diffx*diffy)
        
        #draw lines
        stroke(300+r,100+r,100+r*diff)
        line(t1[0],t1[1],t2[0],t2[1])
        
        #save Frame
        
        n=n+1
        if n == 500:
            saveFrame("frame-######.jpg")
       #     n=7
       
         #Grashalme
#         f = 400
#         m = 1.1
#         line(t1[0]+f,t1[1]+f,m*t2[0]+f,m*t2[1]+f)
#         f = 400
#         m = 1
#         line(t1[0]+f,t1[1]+f,m*t2[0]+f,m*t2[1]+f)
                
def movieEvent(m):
    m.read()

