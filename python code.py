#!/usr/bin/env python
# coding: utf-8

# In[7]:


import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

class ImageCompressionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Compression Tool")
        self.root.configure(bg='#F0F0F0')

        self.original_image = None
        self.image_preview = None
        self.image_id = None

        # Create and pack widgets
        self.create_widgets()

    def create_widgets(self):
        # Browse button
        self.browse_button = tk.Button(self.root, text="Browse Image", command=self.browse_image, bg='#4CAF50', fg='white')
        self.browse_button.pack(pady=10, padx=20, fill=tk.X)

        # Frame for resizing options
        self.resize_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.resize_frame.pack(pady=10)

        # Resizing buttons
        resize_options = [("Low", "low"), ("Better", "better"), ("Best", "best")]
        for text, option in resize_options:
            button = tk.Button(self.resize_frame, text=text, command=lambda opt=option: self.resize_image(opt))
            button.pack(side=tk.LEFT, padx=10)

        # Compress button
        self.compress_button = tk.Button(self.root, text="Compress Image", command=self.compress_image, bg='#4CAF50', fg='white')
        self.compress_button.pack(pady=10, padx=20, fill=tk.X)

        # Frame for Image Preview with Scrollbars
        self.preview_frame = tk.Frame(self.root, bg='#F0F0F0')
        self.preview_frame.pack(pady=10, expand=True, fill=tk.BOTH)

        # Canvas for Image Preview
        self.canvas = tk.Canvas(self.preview_frame, bg='#F0F0F0', highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Scrollbars
        self.scrollbar_vertical = tk.Scrollbar(self.preview_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar_vertical.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar_horizontal = tk.Scrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.scrollbar_horizontal.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(yscrollcommand=self.scrollbar_vertical.set, xscrollcommand=self.scrollbar_horizontal.set)

    def browse_image(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.original_image = Image.open(filename)
            self.image_preview = self.resize_image_to_fit_canvas(self.original_image)
            self.image_id = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_preview)
            self.update_canvas_scrollbars()

    def resize_image(self, resize_option):
        if self.original_image:
            if resize_option == "low":
                resized_image = self.original_image.resize((300, 300))
            elif resize_option == "better":
                resized_image = self.original_image.resize((600, 600))
            elif resize_option == "best":
                resized_image = self.original_image.resize((900, 900))
            else:
                resized_image = self.original_image

            self.image_preview = self.resize_image_to_fit_canvas(resized_image)
            self.canvas.itemconfig(self.image_id, image=self.image_preview)
            self.update_canvas_scrollbars()

    def resize_image_to_fit_canvas(self, image):
        if image:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            image_width, image_height = image.size
            if image_width > canvas_width or image_height > canvas_height:
                aspect_ratio = min(canvas_width / image_width, canvas_height / image_height)
                new_width = int(image_width * aspect_ratio)
                new_height = int(image_height * aspect_ratio)
                return ImageTk.PhotoImage(image.resize((new_width, new_height)))
            else:
                return ImageTk.PhotoImage(image)
        else:
            return None

    def update_canvas_scrollbars(self):
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

    def compress_image(self):
        if self.original_image:
            # Convert RGBA image to RGB mode
            if self.original_image.mode == 'RGBA':
                self.original_image = self.original_image.convert('RGB')

            # Save the compressed image
            compressed_filename = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                                filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
            if compressed_filename:
                self.original_image.save(compressed_filename, optimize=True, quality=50)
                messagebox.showinfo("Compression Complete", "Image compressed and saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCompressionApp(root)
    root.mainloop()


# In[ ]:




