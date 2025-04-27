from ultralytics import YOLO
import os
import json
import cv2

# Load the YOLO model
model = YOLO(os.path.join(os.getcwd(), 'runs/detect/train6/weights/best.pt'))

# Perform inference without saving images automatically
results = model.predict(
    source=os.path.join(os.getcwd(), 'drive/MyDrive/test_data/'),
    imgsz=1280,
    conf=0.25,
    save=False,
    device=0
)

# Prepare the output directory for annotated images
img_out_dir = os.path.join(os.getcwd(), 'pred_test_data0427')
os.makedirs(img_out_dir, exist_ok=True)

# Build predictions JSON and save annotated images
predictions = []
for res in results:
    entry = {
        "image_path": res.path,
        "boxes": []
    }

    # Get annotated image (numpy array) and save it
    annotated_img = res.plot()
    out_name = os.path.basename(res.path)
    out_path = os.path.join(img_out_dir, out_name)
    cv2.imwrite(out_path, cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR))

    # Collect bounding box data
    for xyxy, conf, cls in zip(res.boxes.xyxy, res.boxes.conf, res.boxes.cls):
        x1, y1, x2, y2 = xyxy.tolist()
        entry["boxes"].append({
            "class_id": int(cls),
            "confidence": float(conf),
            "points": [
                [x1, y1],  # top-left
                [x2, y1],  # top-right
                [x2, y2],  # bottom-right
                [x1, y2],  # bottom-left
            ]
        })

    predictions.append(entry)

# Save predictions to JSON
output_path = os.path.join(os.getcwd(), 'yolov8_best_predictions_test_data0427.json')
with open(output_path, 'w') as f:
    json.dump(predictions, f, indent=2)

print(f"✅ {len(predictions)} images annotated → {img_out_dir}")
print(f"✅ JSON saved → {output_path}")
