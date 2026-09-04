import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pilmoji import Pilmoji
import cv2
import numpy as np

# Festive Colored & Styled Terminal Greeting
print("\033[1;33m" + "✨" * 25 + "\033[0m")
print("\033[1;35m  🦚  H A P P Y   J A N M A S H T A M I !  🦚  \033[0m")
print("\033[1;36m      May Lord Krishna's blessings be with you      \033[0m")
print("\033[1;33m" + "✨" * 25 + "\033[0m\n")

class EdgeDrawerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Happy Krishna Janmashtami 🧿")
        self.root.config(bg="#000000")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.is_running = False

        self.canvas = tk.Canvas(root, width=600, height=600, bg="#000000", highlightthickness=0)
        self.canvas.pack(expand=True) 
       
        self.root.after(1000, self.start_process)   # <<<------- DELAY

    def start_process(self):
        if self.is_running:
            return

        try:
            # IMAGE Controller-----------<<< 
            img = cv2.imread("image.jpg")
            if img is None:
                messagebox.showerror("Error", "Could not find 'image.jpg' in the current folder.")
                self.root.destroy()
                return

            # Resize image to fit nicely within the fixed 600x600 frame with a clean border
            h, w = img.shape[:2]
            max_dim = 480
            if h > max_dim or w > max_dim:
                scaling = max_dim / float(max(h, w))
                new_w = int(w * scaling)
                new_h = int(h * scaling)
                img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
            self.img_h, self.img_w = img.shape[:2]
            
            # <<<<----------------- Boosting brightness and saturation for a vivid, bright tone
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            h_chan, s_chan, v_chan = cv2.split(hsv)
            s_chan = cv2.multiply(s_chan, 1.5)  # Increase saturation
            s_chan = np.clip(s_chan, 0, 255).astype(np.uint8)
            v_chan = np.full_like(v_chan, 255)  # Max out brightness for glowing bright look
            bright_hsv = cv2.merge([h_chan, s_chan, v_chan])
            self.original_img = cv2.cvtColor(bright_hsv, cv2.COLOR_HSV2RGB)

            # <<<<----------------- Detecting edges using Canny
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)

            # <<<<----------------- Extracting edge pixel coordinates
            y_indices, x_indices = np.where(edges > 0)
            
            # Map edge points to their bright colors
            self.edge_points = []
            for y, x in zip(y_indices, x_indices):
                color = self.original_img[y, x]
                self.edge_points.append((y, x, color))

            #<<<<----------------- Sort points by Y-coordinate in reverse (from bottom [H] to top [0])
            self.edge_points.sort(key=lambda p: p[0], reverse=True)

            # <<<<-----------------      Animation configuration (Takes precisely 20 seconds)
            self.total_duration_ms = 20000  # <<<<< ---- ANIMATION SPEED
            self.fps = 30
            self.interval_ms = int(1000 / self.fps) 
            self.total_frames = int(self.total_duration_ms / self.interval_ms)
            
            self.current_frame = 0
            self.is_running = True
            
           
            self.canvas_base = np.zeros((600, 600, 3), dtype=np.uint8)
            
            # Calculate offsets to center the image precisely inside the 600x600 frame
            self.y_offset = (600 - self.img_h) // 2
            self.x_offset = (600 - self.img_w) // 2

            self.animate()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.root.destroy()

    def animate(self):
        if not self.is_running:
            return

        if self.current_frame <= self.total_frames:
            fraction = self.current_frame / self.total_frames
            num_points_to_show = int(fraction * len(self.edge_points))
            
           
            self.canvas_base.fill(0) 
            
            # Ploting the accumulated edge points with bright colors centered in the frame
            for i in range(num_points_to_show):
                y, x, color = self.edge_points[i]
                self.canvas_base[y + self.y_offset, x + self.x_offset] = color

          
            pil_img = Image.fromarray(self.canvas_base)
            self.tk_img = ImageTk.PhotoImage(image=pil_img)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

            self.current_frame += 1
            self.root.after(self.interval_ms, self.animate)
        else:
            self.is_running = False
          
            pil_img = Image.fromarray(self.canvas_base)
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("arial.ttf", 18)
            except IOError:
                font = ImageFont.load_default()

            with Pilmoji(pil_img) as pilmoji:
                
                pilmoji.text((300, 555), "Happy Birthday Krishna Jii 🌸🧿🦚🩵", fill="#FFD700", font=font, align="center", anchor="mm")

            self.tk_img = ImageTk.PhotoImage(image=pil_img)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_img)

if __name__ == "__main__":
    root = tk.Tk()
    app = EdgeDrawerApp(root)
    root.mainloop()