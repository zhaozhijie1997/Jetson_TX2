#
# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#



import socket
import datetime

import jetson.inference
import jetson.utils
import cv2
import argparse
import numpy as np
import time
# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
						   formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage())

parser.add_argument("--network", type=str, default="SSD-Inception-v2", help="pre-trained model to load, see below for options")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use")
parser.add_argument("--camera", type=str, default="1", help="index of the MIPI CSI camera to use (NULL for CSI camera 0)\nor for VL42 cameras the /dev/video node to use.\nby default, MIPI CSI camera 0 will be used.")
parser.add_argument("--width", type=int, default=1280, help="desired width of camera stream (default is 1280 pixels)")
parser.add_argument("--height", type=int, default=720, help="desired height of camera stream (default is 720 pixels)")

opt, argv = parser.parse_known_args()

# load the object detection network
net = jetson.inference.detectNet(opt.network, argv, opt.threshold)

# create the camera and display
#camera = jetson.utils.gstCamera(opt.width, opt.height, opt.camera)
display = jetson.utils.glDisplay()
cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)
width = int(cap.get(3))  # float
height = int(cap.get(4))



ip_addr = "10.169.45.246"
port_num = 4859
print("Connnecting to Server ...")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ip_addr, port_num))
print("Server Connected")




# process frames until user exits
while(True):
	# capture the image
	start = time.time()
	ret, img = cap.read()
	img = cv2.cvtColor(img,cv2.COLOR_BGR2RGBA)
	print(type(img))
	#img, width, height = camera.CaptureRGBA()
	img = jetson.utils.cudaFromNumpy(img)

  
	# detect objects in the image (with overlay)
	detections = net.Detect(img, width, height)
	fps = 1/(time.time()-start)
	print("FPS is %.2f"%(fps))
	# print the detections
	print("detected {:d} objects in image".format(len(detections)))

	for detection in detections:
		msg = detection
		client_socket.send(str(msg).encode())

		print(msg)


	# render the image
	display.RenderOnce(img, width, height)

	# update the title bar
	display.SetTitle("{:s} | Network {:.0f} FPS".format(opt.network, 1000.0 / net.GetNetworkTime()))

	# synchronize with the GPU
	if len(detections) > 0:
		jetson.utils.cudaDeviceSynchronize()

	# print out performance info
	net.PrintProfilerTimes()
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()

