# Programmed By Ujjwal Humagain
# Date of Completion 11 February 2021
# Copyright (c) 2021 Ujjwal Humagain
from gpiozero import LED # initalizing GPIO pins 
green = LED(14) #setting green LED in pin 14
orange = LED(15) #setting orange LED in pin 15

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input # for preprocessing input
from tensorflow.keras.preprocessing.image import img_to_array #for converting image file to aray
from tensorflow.keras.models import load_model # loading the model created 
from imutils.video import VideoStream # for starting the video streaming 
import numpy as np # imported numpy 
import argparse # for parsing the argument 
import imutils # imported imutils library
import time # imported time 
import cv2 # imported open cv 
import os # imported os
import door

# function 
def predict_mask_detected(videoFrame, faceDisplayed, maskUsed):
	# grab the dimensions of the frame and then construct a blob
	# from it
	(h, w) = videoFrame.shape[:2] # height and width of the frame
	blob = cv2.dnn.blobFromImage(videoFrame, 1.0, (300, 300),
		(104.0, 177.0, 123.0)) # Binary Large Object (blob) is used in open cv and deep neural network

	# pass the blob through the network and obtain the face detections
	faceDisplayed.setInput(blob)
	detections = faceDisplayed.forward()

	# initialize our list of faces, their corresponding locations,
	# and the list of predictions from our face mask network
	faces = []
	locs = []
	preds = []

	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the detection
		confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the confidence is
		# greater than the minimum confidence
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# ensure the bounding boxes fall within the dimensions of
			# the frame
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))

			# extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
			face = videoFrame[startY:endY, startX:endX]
			face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
			face = cv2.resize(face, (224, 224))
			face = img_to_array(face)
			face = preprocess_input(face)

			# add the face and bounding boxes to their respective
			# lists
			faces.append(face)
			locs.append((startX, startY, endX, endY))

	# only make a predictions if at least one face was detected
	if len(faces) > 0:
		# for faster inference we'll make batch predictions on *all*
		# faces at the same time rather than one-by-one predictions
		# in the above `for` loop
		faces = np.array(faces, dtype="float32")
		preds = maskUsed.predict(faces, batch_size=32)

	# return a 2-tuple of the face locations and their corresponding
	# locations
	return (locs, preds)

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,
	default="face_detector",
	help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
	default="mask_detector.model",
	help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load previously trained face detector model 
print("Wait the face detection model is loading...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
faceDisplayed = cv2.dnn.readNet(prototxtPath, weightsPath)
maskUsed = load_model(args["model"])

# initialize the video stream and allow the camera sensor to warm up
print("Starting Video streaming in two seconds")
vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
	videoFrame = vs.read()
	videoFrame = imutils.resize(videoFrame, width=500)

	# detect faces in the frame and determine if they are wearing a
	# face mask or not
	(locs, preds) = predict_mask_detected(videoFrame, faceDisplayed, maskUsed)

	# loop over the detected face locations and their corresponding
	# locations
	for (box, pred) in zip(locs, preds):
		# unpack the bounding box and predictions
		(startX, startY, endX, endY) = box
		(mask, withoutMask) = pred
		# determine the class label and color we'll use to draw
		# the bounding box and text
		if mask > withoutMask:
			label = ""
			color = (0, 0, 0)
			green.on()
			orange.off()
			door.unlock()
			time.sleep(5)
			door.lock()
			green.off()
		else:
			label = ""
			color = (0, 0, 0)
			green.off()
			orange.on()
		
		# display the label and bounding box rectangle on the output
		# frame
		cv2.putText(videoFrame, label, (startX-50, startY - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
		cv2.rectangle(videoFrame, (startX, startY), (endX, endY), color, 2)
	# show the output frame
	cv2.imshow("Face Mask Detector", videoFrame)
	key = cv2.waitKey(1) & 0xFF
	# if the `s` key was pressed, break from the loop
	if key == ord("s"):
            green.off()
            orange.off()
            break

cv2.destroyAllWindows()
vs.stop()
