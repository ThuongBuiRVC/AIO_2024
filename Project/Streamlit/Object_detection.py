import cv2
import numpy as np
from PIL import Image
import streamlit as st

# Model and prototxt paths
MODEL = "model/MobileNetSSD_deploy.caffemodel"
PROTOTXT = "model/MobileNetSSD_deploy.prototxt.txt"

# Function to process the image using the SSD model
def process_image(image):
    # Prepare the image as input for the model
    blob = cv2.dnn.blobFromImage(
        cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5
    )
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)
    net.setInput(blob)
    detections = net.forward()
    return detections

# Function to annotate the image with bounding boxes
def annotate_image(image, detections, confidence_threshold=0.5):
    (h, w) = image.shape[:2]
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
    return image

def main():
    st.title('Object Detection for Images')
    
    # File uploader for the user to upload an image
    file = st.file_uploader('Upload Image', type=['jpg', 'png', 'jpeg'])
    if file is not None:
        st.image(file, caption='Uploaded Image')

        # Convert the uploaded file to an image
        image = Image.open(file)
        image = np.array(image)

        # Process the image to detect objects
        detections = process_image(image)

        # Annotate the image with bounding boxes
        processed_image = annotate_image(image.copy(), detections)

        # Display the processed image
        st.image(processed_image, caption='Processed Image')

if __name__ == "__main__":
    main()
