import os
import cv2
from ultralytics import YOLO

# Load the YOLO model
model = YOLO(r"D:\pycharm_projects\leaf\weights\ok_healthy.pt")

# Define output folder for saving detected images
output_folder = r"D:\pycharm_projects\leaf\detected"
os.makedirs(output_folder, exist_ok=True)

# Initialize video capture for the integrated camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open integrated camera.")
    exit()

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to retrieve frame from integrated camera.")
        break

    # Perform YOLO prediction
    results = model.predict(frame, conf=0.25)

    # Initialize counters for different levels of disease severity
    no_disease_count = 0
    mild_disease_count = 0
    moderate_disease_count = 0
    severe_disease_count = 0

    # Iterate over each detection result
    for result in results:
        boxes = result.boxes  # all bounding boxes
        for box in boxes:
            # Extract confidence score and bounding box coordinates
            confidence = box.conf[0].item()
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Determine severity level based on confidence score
            if confidence < 0.2:
                label = 'No Disease'
                color = (0, 255, 0)  # Green
                no_disease_count += 1
            elif 0.2 <= confidence < 0.5:
                label = 'Mild Disease'
                color = (0, 255, 255)  # Yellow
                mild_disease_count += 1
            elif 0.5 <= confidence < 0.8:
                label = 'Moderate Disease'
                color = (0, 165, 255)  # Orange
                moderate_disease_count += 1
            else:
                label = 'Severe Disease'
                color = (0, 0, 255)  # Red
                severe_disease_count += 1

            # Draw the bounding box with the color based on severity
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Determine overall classification based on counts
    if severe_disease_count > 0:
        overall_label = "Severe Disease"
        color = (0, 0, 255)  # Red
    elif moderate_disease_count > 0:
        overall_label = "Moderate Disease"
        color = (0, 165, 255)  # Orange
    elif mild_disease_count > 0:
        overall_label = "Mild Disease"
        color = (0, 255, 255)  # Yellow
    else:
        overall_label = "No Disease"
        color = (0, 255, 0)  # Green

    # Add the overall classification to the frame
    cv2.putText(frame, f"Overall: {overall_label}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Display the frame with bounding boxes
    cv2.imshow("Integrated Camera Feed", frame)

    # Save the annotated frame periodically (e.g., every 30 frames)
    if frame_count % 30 == 0:  # Adjust frequency as needed
        save_path = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(save_path, frame)
        print(f"Frame {frame_count} saved with classification: {overall_label}")

    # Increment frame count
    frame_count += 1

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture and close all windows
cap.release()
cv2.destroyAllWindows()