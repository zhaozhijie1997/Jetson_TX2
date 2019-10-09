
import cv2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--video", type=str, help="Video file name here")
parser.add_argument("--output", type=str, help="Jpg output name here")
parser.add_argument("--frames", type=int, default=2, help="no of images per second ")
args, unknown = parser.parse_known_args()




get = args.frames

to_get = int(10/get)

name = args.output
cap = cv2.VideoCapture(args.video)
count = 0
frame_no = 0
while(cap.isOpened()):
	ret, frame = cap.read()
	count = count + 1
	if ret == True:
		if count%to_get==0 :
			frame_no = frame_no + 1
			#img = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
			cv2.imwrite('../data/{}.jpg'.format(name+str(frame_no)), frame)
			count=0
	else:
		break

cap.release()
cv2.destroyAllWindows()

