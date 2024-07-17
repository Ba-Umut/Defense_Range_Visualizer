from ultralytics import YOLO
import cv2

def detect(image_path,model_path):
    # Load the image
    image = cv2.imread(image_path)
    overlay = image.copy() #for transparent image

    # Load a model
    model = YOLO(model_path)  # pretrained YOLOv8n model
    results = model(image_path)  # return a list of Results objects

    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs

        for box in boxes:
            class_id = int(box.cls[0])  # Assuming the class ID is in box.cls[0]

            prob = box.conf  # Get the confidence score of the bounding box
            if prob < 0.70: # Skip processing if confidence is below 0.70 
                  continue
            
            # Extract coordinates
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Calculate the midpoint
            midpoint = ((x1 + x2) // 2, (y1 + y2) // 2)
            
            class_name = model.names[class_id]
            # Draw shooting area and name
            cv2.putText(image, f'{class_name}', (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 3)
            cv2.ellipse(overlay, midpoint, (200,160), 0, 0, 360, (0,0,200), -1)
            cv2.ellipse(overlay, midpoint, (200,160), 0, 0, 360, (30,30,255), 3)
            
            
    alpha = 0.3  # Transparency factor.
    image_new = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)

    cv2.imwrite(save_path, image_new)
    # Display the result
    cv2.imshow("result", image_new)  # display the image with bounding boxes
    if cv2.waitKey(0) & 0xFF == ord('q'):
                cv2.destroyAllWindows()


model_path="C:/Users/1548u/Desktop/clash_of_clans/best.pt"
image_path = "C:/Users/1548u/Desktop/clash_of_clans/test/356.jpg"
save_path = 'C:/Users/1548u/Desktop/clash_of_clans/test/processed_test356.jpg'
# Usage
detect(image_path,model_path)

