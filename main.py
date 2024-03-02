import cv2
import tkinter as tk
from tkinter import Entry, Canvas, StringVar, Label, Button
from PIL import Image, ImageTk

startFlag = True
lower_limit_var = 50
upper_limit_var = 250
def canny_edge_detection(frame, upper_limit, lower_limit):
    # Convert the frame to grayscale for edge detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise and smoothen edges
    blurred = cv2.GaussianBlur(src=gray, ksize=(3, 5), sigmaX=0.5)
    
    if isinstance(lower_limit, int) and isinstance(upper_limit, int):
        # Perform Canny edge detection
        edges = cv2.Canny(blurred, lower_limit, upper_limit)
    return blurred, edges
	
	
def update(window, canvas, cap, upper_limit_var, lower_limit_var):
    ret, frame = cap.read()
    if ret:
        try:
            upper_limit = int(upper_limit_var.get())
            lower_limit = int(lower_limit_var.get())
        except:
            upper_limit = 0
            lower_limit = 250 
		# Calculate edges
        blurred, edges = canny_edge_detection(frame, upper_limit, lower_limit)
        
        # Display the edges
        img = Image.fromarray(edges)
        photo = ImageTk.PhotoImage(image=img)
        canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.image = photo

    window.after(10, lambda: update(window, canvas, cap, upper_limit_var, lower_limit_var))

def Algorithm(window):
    global startFlag
    if startFlag:
        for widget in window.winfo_children():
            widget.destroy()
        startFlag = False

    upper_limit_var = StringVar()
    lower_limit_var = StringVar()
    
    upper_limit_label = Label(window, text="Upper limit", bg="green")
    lower_limit_label = Label(window, text="Lower limit", bg="green")
    upper_limit_label.place(x=250, y=50)
    lower_limit_label.place(x=250, y=0)
    upper_limit_entry = Entry(window, textvariable=upper_limit_var, width=10)
    upper_limit_entry.place(x=320, y=50)

    lower_limit_entry = Entry(window, textvariable=lower_limit_var, width=10)
    lower_limit_entry.place(x=320, y=0)

    canvas = Canvas(window, width=640, height=480)
    canvas.place(x=0, y=80)

    cap = cv2.VideoCapture(0)
    update(window, canvas, cap, upper_limit_var, lower_limit_var)

    window.mainloop()
def main():
    window = tk.Tk()
    window.title("Edge detecting GUI")
    window.geometry("640x600")  # Set the window size to 640x600 pixels
    window.iconbitmap("icon.ico")

    # Load the image
    pil_image = Image.open("icon.jpg").resize((640, 600))
    tk_image = ImageTk.PhotoImage(pil_image)    # Create a Label widget with the image
    label = Label(window, text="Edge Detector", image=tk_image)
    label.pack()

    StartButton = Button(window, text='Start', command=lambda: Algorithm(window), width=25, height=3, bg='green')
    StartButton.place(x=450, y=540)

    window.mainloop()

if __name__ == "__main__":
    main()