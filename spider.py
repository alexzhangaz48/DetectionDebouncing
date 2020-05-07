import sys
import cv2
import click
import numpy as np
# @click.command()
# @click.option('--video',help = 'input video')
# @click.option('--algorithm',help = 'tracker algorithm')

def main(video, algorithm):
    
    '''

    :param video: 处理文件
    :param algorithm: 跟踪算法
    :return:
    '''
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

    video_cap = cv2.VideoCapture(video)
    if not video_cap.isOpened():
        print("failed")
        sys.exit()
    ok, frame = video_cap.read()
    if not ok:
        print("Read failed")
        sys.exit()

    bbox = cv2.selectROI(frame, False)
    ok = tracker.init(frame, bbox)

    while True:
        ok, frame = video_cap.read()
        if not ok:
            break

        timer = cv2.getTickCount()
        ok , bbox = tracker.update(frame)
        fps =  cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        if ok:
            p1 = (int (bbox[0]), int(bbox[1]))
            p2 = (int (bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame,p1,p2,(255,0,0),2,1)
        # else:
        #     cv2.putText(frame,"failure detected")
        cv2.imshow("Tracking",frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



if __name__ == "__main__":
    video1 ="dance_s.MP4"
    algorithm = "MIL"
    main(video1, algorithm)
    """打开视频，测试用
    cap = cv2.VideoCapture(video1)
    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows() 
    """
    