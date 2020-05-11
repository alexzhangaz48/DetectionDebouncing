import sys
import cv2
import click
import numpy as np
# @click.command()
# @click.option('--video',help = 'input video')
# @click.option('--algorithm',help = 'tracker algorithm')


def spider(video, algorithm,outSize):
    (major_ver, minor_ver, subminor_ver) = cv2.__version__.split(".")
    if int(major_ver) <3:
        tracker = cv2.Tracker_create(algorithm)
    else:
        if algorithm == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()

        if algorithm == 'MIL':
            tracker = cv2.TrackerMIL_create()

        if algorithm == 'KCF':
            tracker = cv2.TrackerKCF_create()

        if algorithm == 'TLD':
            tracker = cv2.TrackerTLD_create()

        if algorithm == 'CSRT':
            tracker = cv2.TrackerCSRT_create()

    #读取视频及确认视频有效
    video_cap = cv2.VideoCapture(video)
    if not video_cap.isOpened():
        print("Video is not here :(")
        sys.exit()
    ok, frame = video_cap.read()
    if not ok:
        print("Something goes wrong with the video :(")
        sys.exit()

    #标注初始框
    bbox = cv2.selectROI(frame, False)
    ok = tracker.init(frame, bbox)
    # 记录原始框信息
    prev = bbox
    current = list(prev)
    dimensions = frame.shape
    
    # 获取窗口大小
    size = (int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print(size)
    print(type(outSize))
    outSize_write=(int(outSize[0]),int(outSize[1]))
    
    # 调用VideoWrite（）函数
    fps = 30
    output = cv2.VideoWriter('MySaveVideo.mp4', cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), fps, outSize_write)
    # 截取信息初始化
    #chopped = frame[current[0]:(current[0]+int(outSize[0])),current[1]:(current[1]+int(outSize[1]))]
    chopped = frame[current[1]:current[1]+outSize[1],current[0]:current[0]+outSize[0]] #纵列，横列

    while True:
        ok, frame = video_cap.read()
        if not ok:
            print("All frames are shown :)")
            break

        timer = cv2.getTickCount()
        ok , bbox = tracker.update(frame)
        fps =  cv2.getTickFrequency() / (cv2.getTickCount() - timer)



        if ok:
            #原本检测结果
            p1 = (int (bbox[0]), int(bbox[1]))
            p2 = (int (bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame,p1,p2,(255,0,0),1,1)

            #加入防抖
            for i in range(0,3):
                if (abs( bbox[i] - prev[i] ) > 5) or (abs(current[i] -bbox[i]) > 6):
                    current[i] = int(prev[i])
            p1 = (int (current[0]), int(current[1]))
            p2 = (int (current[0] + current[2]), int(current[1] + current[3]))
            cv2.rectangle(frame,p1,p2,(0,255,255),4,1)

            #输出视频
            up = current[0]
            left = current[1]
            down = current[2]
            right = current[3]
            # chopped = frame[current[0]:(current[0]+int(outSize[0])),current[1]:(current[1]+int(outSize[1]))]
        
            
            #print("left:",left,"   right:", right, "   up:",up,"   down:",down)
            
            if (current[1] < 0) or (current[1]+outSize[1] > dimensions[0]) or (current[0]<0) or (current[0]+outSize[0] > dimensions[1]):
                print("ERROR：超出范围，无法录制 :(")
            else:
                chopped = frame[current[1]:current[1]+outSize[1],current[0]:current[0]+outSize[0]] #纵列，横列
                output.write(chopped)
            
            
        # else:
        #     cv2.putText(frame,"failure detected")
        prev = bbox

        cv2.imshow("Tracking",chopped)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video_cap.release()
    output.release()



if __name__ == "__main__":
    video1 ="dance_s.MP4"
    algorithm = "KCF"
    size = [200,300]
    spider(video1, algorithm, size)
    
    