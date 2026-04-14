import cv2
import os

image_folder = "dataset/images"
label_folder = "dataset/labels"

files = os.listdir(image_folder)

for image_name in files:

    image_path = os.path.join(image_folder, image_name)

    # Match label file
    label_name = os.path.splitext(image_name)[0] + ".txt"
    label_path = os.path.join(label_folder, label_name)

    # Read image
    image = cv2.imread(image_path)

    if image is None:
        continue

    image = cv2.resize(image, (800, 600))

    height, width, _ = image.shape

    # Read label file
    with open(label_path, "r") as f:

        line = f.readline().split()

        class_id = int(line[0])

        # Get class name
        if class_id == 0:
            label_text = "Unripe"
        elif class_id == 1:
            label_text = "Ripe"
        else:
            label_text = "Unknown"

        # Read bounding box values
        x_center = float(line[1])
        y_center = float(line[2])
        box_width = float(line[3])
        box_height = float(line[4])

    # Convert YOLO format → pixel coordinates
    x_center = int(x_center * width)
    y_center = int(y_center * height)

    box_width = int(box_width * width)
    box_height = int(box_height * height)

    x1 = int(x_center - box_width / 2)
    y1 = int(y_center - box_height / 2)

    x2 = int(x_center + box_width / 2)
    y2 = int(y_center + box_height / 2)

    # Draw rectangle
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Draw label text
    cv2.putText(
        image,
        label_text,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.imshow("Bounding Box", image)

    key = cv2.waitKey(0)

    if key == 27:  # Press ESC to stop
        break

cv2.destroyAllWindows()