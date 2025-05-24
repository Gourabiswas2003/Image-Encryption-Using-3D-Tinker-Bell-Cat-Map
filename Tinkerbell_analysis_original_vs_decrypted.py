import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import numpy as np


def open_image1():
    global img1, img1_path, img1_display
    img1_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if img1_path:
        img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
        img1_display = cv2.resize(img1, (250, 250))
        display_image(img1_display, img_label1)


def open_image2():
    global img2, img2_path, img2_display
    img2_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if img2_path:
        img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
        img2_display = cv2.resize(img2, (250, 250))
        display_image(img2_display, img_label2)


def display_image(img, img_label):
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    img_label.configure(image=img)
    img_label.image = img


def calculate_metrics():
    if img1 is None or img2 is None:
        messagebox.showerror("Error", "Please select both images.")
        return

    img2_resized = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    mse = np.mean((img1 - img2_resized) ** 2)

    if mse == 0:
        psnr = float('inf')
    else:
        psnr = 20 * np.log10(255.0 / np.sqrt(mse))

    ncc = np.corrcoef(img1.flatten(), img2_resized.flatten())[0, 1]

    result_text.set(f"MSE: {mse:.4f}\nPSNR: {psnr:.4f} dB\nNCC: {ncc:.4f}")


root = tk.Tk()
root.title("Image Metrics Calculator")

img1 = None
img2 = None
img1_path = ""
img2_path = ""
img1_display = None
img2_display = None

img_label1 = tk.Label(root)
img_label1.grid(row=0, column=0, padx=10, pady=10)
img_label2 = tk.Label(root)
img_label2.grid(row=0, column=1, padx=10, pady=10)

btn_open_image1 = tk.Button(root, text="Open Image 1", command=open_image1)
btn_open_image1.grid(row=1, column=0, padx=10, pady=10)

btn_open_image2 = tk.Button(root, text="Open Image 2", command=open_image2)
btn_open_image2.grid(row=1, column=1, padx=10, pady=10)

btn_calculate = tk.Button(root, text="Calculate Metrics", command=calculate_metrics)
btn_calculate.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
