
import cv2,time,pandas
from datetime import datetime

begining_frame=None
list_of_status=[None,None]
time_period=[]
picture=cv2.VideoCapture(0)

df=pandas.DataFrame(columns=["Start","End"])

while True:
    check, data_frame=picture.read()
    status=0
    gray_frame=cv2.cvtColor(data_frame,cv2.COLOR_BGR2GRAY)
    gray_frame=cv2.GaussianBlur(gray_frame,(21,21),0)

    if begining_frame is None:
        begining_frame=gray_frame
        continue
    difference_frame=cv2.absdiff(begining_frame,gray_frame)

    threshold_frame=cv2.threshold(difference_frame,30,255,cv2.THRESH_BINARY)[1]

    threshold_frame=cv2.dilate(threshold_frame,None,iterations=2)

    (cnts,_)=cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cnts:
        if cv2.contourArea(contour)<10000:
            continue
        status=1
        (a,b,c,d)=cv2.boundingRect(contour)
        cv2.rectangle(data_frame,(a,b),(a+c,b+d),(0,255,0),3)
    list_of_status.append(status)

    list_of_status=list_of_status[-2:]

    if list_of_status[-1]==1 and list_of_status[-2]==0:
        time_period.append(datetime.now())
    if list_of_status[-1]==0 and list_of_status[-2]==1:
        time_period.append(datetime.now())


    cv2.imshow("Gray Frame",gray_frame)
    cv2.imshow("Difference Frame",difference_frame)
    cv2.imshow("Threshold Frame",threshold_frame)
    cv2.imshow("Colour Frame",data_frame)
    key=cv2.waitKey(1)

    if key==ord('q'):
        if status==1:
            time_period.append(datetime.now())
        break

print(list_of_status)
print(time_period)

for i in range(0,len(time_period),2):
    df=df.append({"Start":time_period[i],"End":time_period[i+1]},ignore_index=True)
df.to_csv("Time_records.csv")

picture.release()
cv2.destroyAllWindows()
