import numpy as np
from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox

a = 0.9
b = -0.6013
c = 2.0
d = 0.5

original_image = None
encrypted_color_image = None
encrypted_grayscale_image = None

def generate_tinkerbell_sequence(length, x0, y0):
    x = [x0]
    y = [y0]
    for _ in range(length - 1):
        x_new = x[-1]**2 - y[-1]**2 + a * x[-1] + b * y[-1]
        y_new = 2 * x[-1] * y[-1] + c * x[-1] + d * y[-1]
        x.append(x_new)
        y.append(y_new)
    return np.array(x), np.array(y)

def process_image(image, key):
    pixels = np.array(image)
    flat_pixels = pixels.flatten()
    x, y = generate_tinkerbell_sequence(len(flat_pixels), *key)
    chaotic_sequence = ((x + y) * 255).astype(np.uint8)
    encrypted_pixels = np.bitwise_xor(flat_pixels, chaotic_sequence)
    return encrypted_pixels.reshape(pixels.shape)

def browse_image():
    global original_image
    image_path = filedialog.askopenfilename(title="Select Image File",
                                            filetypes=(("PNG files", "*.png"), ("JPG files", "*.jpg")))

    original_image = Image.open(image_path)
    display_image(original_image, original_label)

def perform_encryption():
    global encrypted_color_image, encrypted_grayscale_image

    key = (0.1, 0.0)
    encrypted_color_image_array = process_image(original_image, key)
    encrypted_color_image = Image.fromarray(encrypted_color_image_array)
    encrypted_color_image = encrypted_color_image.resize(original_image.size)  # Resize to original size

    grayscale_image = original_image.convert('L')
    encrypted_grayscale_image_array = process_image(grayscale_image, key)
    encrypted_grayscale_image = Image.fromarray(encrypted_grayscale_image_array)
    encrypted_grayscale_image = encrypted_grayscale_image.resize(original_image.size)  # Resize to original size

    display_image(encrypted_color_image, encrypted_color_label)
    display_image(encrypted_grayscale_image, encrypted_grayscale_label)

def save_image(image, title):
    if image is None:
        messagebox.showerror("Error", "No image to save.")
        return

    save_path = filedialog.asksaveasfilename(title=title, defaultextension=".png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
    if not save_path:
        return

    image.save(save_path)
    messagebox.showinfo("Success", f"Image saved as {save_path}")

def display_image(image, label):
    image.thumbnail((200, 200))
    photo = ImageTk.PhotoImage(image)
    label.config(image=photo)
    label.image = photo

root = tk.Tk()
root.title("Image Encryption and Decryption Using Tinker Bell Chaotic Map")
root.geometry("950x500")

original_frame = tk.Frame(root, bg='lavender', bd=2, relief=tk.SUNKEN)
original_frame.grid(row=0, column=0, padx=20, pady=20)
encrypted_color_frame = tk.Frame(root, bg='lavender', bd=2, relief=tk.SUNKEN)
encrypted_color_frame.grid(row=0, column=1, padx=20, pady=20)
encrypted_grayscale_frame = tk.Frame(root, bg='lavender', bd=2, relief=tk.SUNKEN)
encrypted_grayscale_frame.grid(row=0, column=2, padx=20, pady=20)

original_label = tk.Label(original_frame)
original_label.pack(padx=20, pady=20)
encrypted_color_label = tk.Label(encrypted_color_frame)
encrypted_color_label.pack(padx=20, pady=20)
encrypted_grayscale_label = tk.Label(encrypted_grayscale_frame)
encrypted_grayscale_label.pack(padx=20, pady=20)

browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.grid(row=1, column=0, pady=10)

encrypt_button = tk.Button(root, text="Encrypt/Decrypt Image", command=perform_encryption)
encrypt_button.grid(row=1, column=1, pady=10)

save_encrypted_button = tk.Button(root, text="Save Encrypted Image", command=lambda: save_image(encrypted_color_image, "Save Processed Color Image"))
save_encrypted_button.grid(row=2, column=1, pady=10)

save_grayscale_button = tk.Button(root, text="Save Grayscale Encrypted Image", command=lambda: save_image(encrypted_grayscale_image, "Save Processed Grayscale Image"))
save_grayscale_button.grid(row=2, column=2, pady=10)

root.mainloop()
