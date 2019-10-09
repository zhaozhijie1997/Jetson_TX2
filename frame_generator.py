
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--video", type=str, help="Video file name here")
args = parser.parse_args()




cv2.VideoCapture(args.video)
count = 0
frame_no = 0
while(True):
	ret, frame = cap.read()
	count = count+1
	if count%5==0 :
		frame_no +=
		img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		cv2.imwrite('data/frame{}'.format(frame_no), img)


cv2.destroyAllWindows()

