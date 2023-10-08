```gifrom tkinter import Tk, Label, PhotoImage, Toplevel, Button, Canvas, filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np

def open_new_window():
    new_window = Toplevel(root)
    current_file = None

def start_webcam():
    cap = cv2.VideoCapture(0)  # 0 represents the default webcam

    frame_counter = 0  # Counter for frames

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1

        # Skip frames and process alternative frames
        if frame_counter % 2 == 0:
            continue

        frame = cv2.resize(frame, (320, 240))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect pedestrians in the frame
        frame, count = detect_pedestrians_frame(frame)

        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the canvas with the current frame
        canvas.create_image(0, 0, anchor="nw", image=imgtk)
        canvas.image = imgtk

        # Control the traffic signal based on pedestrian count
        if count >= 3:
            traffic_label.config(text="Traffic Signal: CROSS")
        else:
            traffic_label.config(text="Traffic Signal: STOP")

        root.update()

    cap.release()

def upload_image():
    start_webcam()

def clear_image():
    canvas.delete("all")

def detect_pedestrians_frame(frame):
    # Load the pedestrian detection model
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Resize the frame for faster processing
    frame = cv2.resize(frame, (640, 480))

    # Detect pedestrians in the frame
    boxes, weights = hog.detectMultiScale(frame, winStride=(4, 4), padding=(8, 8), scale=1.05)

    # Draw bounding boxes around pedestrians
    count = 0
    for (x, y, w, h) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        count += 1
    print(count)
    return frame, count

root = Tk()
root.title("PEDOX TOOL")
root.withdraw()  # Hide the root window initially

# Show welcome screen with an image
welcome_screen = Toplevel(root, width=600, height=600)
welcome_screen.title("Welcome")

welcome_image_path = "input.png"
welcome_image = Image.open(welcome_image_path)

welcome_image = welcome_image.resize((600, 600))
welcome_photo = ImageTk.PhotoImage(welcome_image)

welcome_image_label = Label(welcome_screen, image=welcome_photo)
welcome_image_label.pack()

text_label = Label(welcome_screen, text="Welcome....", font=("Arial", 16))
text_label.pack(side="bottom", pady=10)

# Move to the main window after 3500 milliseconds (3.5 seconds)
welcome_screen.after(3500, lambda: [welcome_screen.destroy(), root.deiconify()])


# Create canvas to display the image
canvas = Canvas(root, width=600, height=600)
canvas.pack()

# Create buttons
upload_button = Button(root, text="Start Webcam", command=upload_image)
upload_button.pack(side="bottom", padx=10, pady=10)

clear_button = Button(root, text="Clear Image", command=clear_image)
clear_button.pack(side="bottom", padx=10, pady=10)

# Create traffic signal label
traffic_label = Label(root, text="Traffic Signal: STOP", font=("Arial", 16))
traffic_label.pack(side="bottom", pady=10)

# Start the main event loop
root.mainloop()
