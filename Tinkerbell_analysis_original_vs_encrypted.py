import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog

def calculate_uaci(image1_path, image2_path):
    img1 = Image.open(image1_path).convert('L')
    img2 = Image.open(image2_path).convert('L')
    img2 = img2.resize(img1.size)
    img1_array = np.array(img1)
    img2_array = np.array(img2)
    diff = np.abs(img1_array - img2_array)
    uaci = np.sum(diff) / (img1_array.size * 255.0) * 100
    return uaci

def calculate_npcr(image1_path, image2_path):
    img1 = Image.open(image1_path).convert('L')
    img2 = Image.open(image2_path).convert('L')
    img2 = img2.resize(img1.size)
    img1_array = np.array(img1)
    img2_array = np.array(img2)
    diff_pixels = np.not_equal(img1_array, img2_array).sum()
    npcr = (diff_pixels / img1_array.size) * 100
    return npcr

def browse_files():
    root = tk.Tk()
    root.withdraw()
    print("Select the original image:")
    image1_path = filedialog.askopenfilename(title="Select the original image")
    print(f"Selected original image: {image1_path}")
    print("Select the encrypted image:")
    image2_path = filedialog.askopenfilename(title="Select the encrypted image")
    print(f"Selected encrypted image: {image2_path}")
    return image1_path, image2_path

image1_path, image2_path = browse_files()
uaci_value = calculate_uaci(image1_path, image2_path)
print(f'UACI: {uaci_value}%')
npcr_value = calculate_npcr(image1_path, image2_path)
print(f'NPCR: {npcr_value}%')
