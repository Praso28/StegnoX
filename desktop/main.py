import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sys
import os

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MAX_IMAGE_SIZE = (512, 512)

class SteganographyHandler:
    @staticmethod
    def encode_message(image_path, message, output_path):
        img = Image.open(image_path)
        img = img.convert("RGB")
        img.thumbnail(MAX_IMAGE_SIZE)
        width, height = img.size

        message_bytes = message.encode() + b"####"
        binary_message = ''.join(format(byte, '08b') for byte in message_bytes)
        message_len = len(binary_message)

        if message_len > width * height * 3:
            raise ValueError("Message is too long to hide in this image.")

        pixels = img.load()
        index = 0

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                if index < message_len:
                    r = (r & 0xFE) | int(binary_message[index])
                    index += 1
                if index < message_len:
                    g = (g & 0xFE) | int(binary_message[index])
                    index += 1
                if index < message_len:
                    b = (b & 0xFE) | int(binary_message[index])
                    index += 1
                pixels[x, y] = (r, g, b)
                if index >= message_len:
                    break
            if index >= message_len:
                break

        img.save(output_path, "PNG")

    @staticmethod
    def decode_message(image_path):
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size

        binary_message = ""
        pixels = img.load()
        terminator = ''.join(format(ord('#'), '08b') * 4)

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)

                if terminator in binary_message:
                    binary_message = binary_message[:binary_message.index(terminator)]
                    break
            else:
                continue
            break

        if len(binary_message) % 8 != 0:
            return "Corrupted or invalid hidden message."

        message_bytes = bytes(int(binary_message[i:i + 8], 2) for i in range(0, len(binary_message), 8))
        return message_bytes.decode('utf-8')

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry('400x480')
        self.root.configure(bg='#f0f0f0')

        self.image_path = None
        self.image_label = tk.Label(root, text="No Image Selected", bg='#f0f0f0', font=('Arial', 12))
        self.image_label.pack(pady=10)

        tk.Button(root, text="Select Image", command=self.select_image, bg='#4CAF50', fg='white',
                  font=('Arial', 12)).pack(pady=5)

        self.message_entry = tk.Entry(root, width=50, font=('Arial', 12))
        self.message_entry.pack(pady=5)
        self.message_entry.bind("<FocusIn>", self.clear_placeholder)
        self.message_entry.insert(0, "Enter your message here...")

        encode_button = tk.Button(root, text="Hide Message", command=self.hide_message, bg='#2196F3', fg='white',
                                  font=('Arial', 12))
        encode_button.pack(pady=5)

        decode_button = tk.Button(root, text="Reveal Message", command=self.reveal_message, bg='#FF5722', fg='white',
                                  font=('Arial', 12))
        decode_button.pack(pady=5)

        clear_button = tk.Button(root, text="Clear Entries", command=self.clear_entries, bg='#9C27B0', fg='white',
                                  font=('Arial', 12))
        clear_button.pack(pady=5)

    def clear_placeholder(self, event):
        if self.message_entry.get() == "Enter your message here...":
            self.message_entry.delete(0, tk.END)

    def select_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
        if file_path:
            self.image_path = file_path
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            img_display = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_display, text='')
            self.image_label.image = img_display

    def hide_message(self):
        message = self.message_entry.get()
        if not self.image_path or not message:
            messagebox.showerror("Error", "Please select an image and enter a message!")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if output_path:
            try:
                SteganographyHandler.encode_message(self.image_path, message, output_path)
                messagebox.showinfo("Success", f"Message hidden in {output_path}")
            except Exception as e:
                messagebox.showerror("Encoding Error", f"Failed to hide message: {str(e)}")

    def reveal_message(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please select an image!")
            return
        try:
            message = SteganographyHandler.decode_message(self.image_path)
            messagebox.showinfo("Hidden Message", f"Message: {message}")
        except Exception as e:
            messagebox.showerror("Decoding Error", f"Failed to reveal message: {str(e)}")

    def clear_entries(self):
        self.message_entry.delete(0, tk.END)
        self.message_entry.insert(0, "Enter your message here...")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()
