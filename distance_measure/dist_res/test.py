import cv2
import numpy as np

video_capture = cv2.VideoCapture(0)

def estimate_distance(object_width_pixels, focal_length_mm, real_object_width_mm):
    # Estimate distance using simple size-based scaling
    distance_mm = (focal_length_mm * real_object_width_mm) / object_width_pixels
    return distance_mm

def main():
    # Parameters to be adjusted based on your camera and setup
    focal_length_mm = 35  # Focal length of the camera lens in millimeters
    real_object_width_mm = 150  # The real width of the object in millimeters

    # Load an image from your camera
    image = cv2.imread('your_image.jpg')  # Replace 'your_image.jpg' with your image file

    # Assuming you already have the bounding box or contour of the detected object
    object_width_pixels = 50  # Replace with the actual width of the detected object in pixels

    # Estimate the distance
    distance_mm = estimate_distance(object_width_pixels, focal_length_mm, real_object_width_mm)

    print(f"Estimated Distance: {distance_mm} millimeters")

if __name__ == "__main__":
    main()