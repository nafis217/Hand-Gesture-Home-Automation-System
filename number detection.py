import cv2
import mediapipe
import time

ctime=0
ptime=0
start = 0
sum = 0
n = 0

cap=cv2.VideoCapture(0)

medhands=mediapipe.solutions.hands
hands=medhands.Hands(max_num_hands=1,min_detection_confidence=0.7)
draw=mediapipe.solutions.drawing_utils

patterns = [[0]]

room = "1,"

def print_pattern():
    global patterns
    p = patterns[-1]
    if(p.count(2) == 1 and len(p)==1):
        print("Index")
        send_message(room+"Disco on")
    elif(p.count(3) == 1 and len(p)==1):
        print("Middle")
        send_message(room+"Disco off")
    elif(p.count(4) == 1 and len(p)==1):
        print("Ring")
        send_message(room+"Bulb on")
    elif(p.count(5) == 1 and len(p)==1):
        print("Pinky")
        send_message(room+"Bulb off")
    # elif(p.count(2) == 1 and p.count(3) == 1 and len(p)==2):
    #     print("V")
    #     send_message("V")
    # elif(p.count(2) == 1 and p.count(5) == 1 and len(p)==2):
    #     print("SpiderMan")
    #     send_message("SpiderMan")
    # elif(len(p)==5):
    #     print("Init")
    #     send_message("Init")
    # elif(p.count(1) == 1 and len(p)==1):
    #     print("Thumb")
    #     send_message("Thumb")
    # elif(p.count(1) == 1 and p.count(2) == 1 and len(p)==2):
    #     print("Perp")
    #     send_message("Perp")


def send_message(content_to_write):
    file_path = "sample.txt"
    try:
        with open(file_path, 'w+') as file:
            # Write the content to the file
            file_content = file.read()
            if(len(file_content) == 0 ):
                file.write(content_to_write)
        # print(f"Content has been successfully written to '{file_path}'.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

while True:
    success, img=cap.read()
    img = cv2.flip(img,1)
    imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    res = hands.process(imgrgb)
    start = time.time()
    
    lmlist=[]
    tipids=[4,8,12,16,20] #list of all landmarks of the tips of fingers
    
    cv2.rectangle(img,(20,350),(90,440),(0,255,204),cv2.FILLED)
    cv2.rectangle(img,(20,350),(90,440),(0,0,0),5)
    
    if res.multi_hand_landmarks:
        for handlms in res.multi_hand_landmarks:
            for id,lm in enumerate(handlms.landmark):
                
                h,w,c= img.shape
                cx,cy=int(lm.x * w) , int(lm.y * h)
                lmlist.append([id,cx,cy])
                if len(lmlist) != 0 and len(lmlist)==21:
                    fingerlist=[]
                    
                    #thumb and dealing with flipping of hands
                    if lmlist[12][1] > lmlist[20][1]:
                        if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
                            fingerlist.append(1)
                            # print("Thumb\n")
                        else:
                            fingerlist.append(0)
                    else:
                        if lmlist[tipids[0]][1] < lmlist[tipids[0]-1][1]:
                            fingerlist.append(1)
                            # print("Thumb\n")
                        else:
                            fingerlist.append(0)
                    
                    #others
                    for id in range (1,5):
                        if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
                            fingerlist.append(id+1)
                            # print(str(id)+"\n")
                        else:
                            fingerlist.append(0)
                    
                    
                    if len(fingerlist)!=0:
                        fingerlist = [x for x in fingerlist if x != 0]
                        fingercount=len(fingerlist)
                        p = patterns[-1]
                        c = False
                        if len(p) != fingercount:
                            c = True
                        else:
                            for i in range(len(fingerlist)):
                                if(p[i] != fingerlist[i]):
                                    c = True
                        
                        if c:
                            patterns.append(fingerlist)
                            print_pattern()
                    
                    cv2.putText(img,str(fingercount),(25,430),cv2.FONT_HERSHEY_PLAIN,6,(0,0,0),5)
                    
                #change color of points and lines
                draw.draw_landmarks(img,handlms,medhands.HAND_CONNECTIONS,draw.DrawingSpec(color=(0,255,204),thickness=2,circle_radius=2),draw.DrawingSpec(color=(0,0,0),thickness=2,circle_radius=3))
    
    #fps counter
    ctime = time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    sum = start - ptime
    n+=1
    # print(sum/n)
    
    #fps display
    cv2.putText(img,f'FPS:{str(int(fps))}',(0,12),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),1)
          
    cv2.imshow("hand gestures",img)
    
    #press q to quit
    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.destroyAllWindows()
