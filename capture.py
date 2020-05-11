
import cv2 as cv
 
# 调用摄像头
videoCapture = cv.VideoCapture("dance_s.MP4")
 
# 设置帧率
fps = 30

# 获取窗口大小
size = (int(videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)), int(videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)))
print(size)
outSize=(100,200)

# 调用VideoWrite（）函数
videoWrite = cv.VideoWriter('MySaveVideo.mp4', cv.VideoWriter_fourcc('M', 'P', '4', 'V'), fps, outSize)
 
# 先获取一帧，用来判断是否成功调用摄像头
success, frame = videoCapture.read()

chopped = frame[200:400,450:550]
# 通过循环保存帧
while success: 
    success, frame = videoCapture.read()
    chopped = frame[200:400,450:550]
    cv.imshow("Tracking",chopped)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    videoWrite.write(chopped)


# 释放摄像头
videoCapture.release()
videoWrite.release()