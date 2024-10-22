import tkinter as tk
from ocr import knn

class PixelEditor:
    def __init__(self, master, width=28, height=28, pixel_size=15):
        self.master = master
        self.width = width
        self.height = height
        self.pixel_size = pixel_size
        self.eraser_mode = 0  # 0 for draw, 1 for erase
        self.large_number = 0  # Initial large number

        # Create a frame for pixel art
        self.pixel_frame = tk.Frame(master)
        self.pixel_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Create the canvas for pixel art
        self.canvas = tk.Canvas(self.pixel_frame, width=width * pixel_size, height=height * pixel_size, bg='black')
        self.canvas.pack()

        self.control_frame = tk.Frame(self.pixel_frame)
        self.control_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Clear button
        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT)

        # Toggle button for eraser
        self.toggle_button = tk.Button(self.control_frame, text="Erase", command=self.toggle_eraser)
        self.toggle_button.pack(side=tk.RIGHT)
        
        
        # Initialize pixel data
        self.pixels = [[0] * width for _ in range(height)]

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw_pixel)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Draw initial pixels
        self.draw_canvas()

        # Create a frame for controls
        self.identify_frame = tk.Frame(master)
        self.identify_frame.pack(side=tk.LEFT, padx=10, pady=10)

        # Identify button
        self.identify_button = tk.Button(self.identify_frame, text="    Identify    ", command=self.identify)
        self.identify_button.pack(side=tk.LEFT)

        # Label for large number
        self.number_label = tk.Label(master, text=str(self.large_number), font=("Arial", 48))
        self.number_label.pack(side=tk.RIGHT, padx=20)

        self.drawing = False  # Flag to check if drawing is in progress

    def toggle_eraser(self):
        self.eraser_mode = 1 - self.eraser_mode  # Toggle between 0 and 1
        state_text = "Draw" if self.eraser_mode == 0 else "Erase"
        self.toggle_button.config(text=f"{state_text}")

    def start_drawing(self, event):
        self.drawing = True  # Set drawing flag
        self.draw_pixel(event)  # Draw pixel at the initial position

    def draw_pixel(self, event):
        if self.drawing:
            x = event.x // self.pixel_size
            y = event.y // self.pixel_size

            if 0 <= x < self.width and 0 <= y < self.height:
                if self.eraser_mode == 0:
                    self.pixels[y][x] = 1  # Draw
                    if(0 <= x+1 < self.width):
                        self.pixels[y][x+1]=1
                    if(0 <= x-1 < self.width):
                        self.pixels[y][x-1]=1
                    if(0 <= y+1 < self.height):
                        self.pixels[y+1][x]=1
                    if(0 <= y-1 < self.width):
                        self.pixels[y-1][x]=1                      
                else:
                    self.pixels[y][x] = 0  # Erase
                self.draw_canvas()  # Redraw canvas

    def stop_drawing(self, event):
        self.drawing = False  # Reset drawing flag

    def draw_canvas(self):
        self.canvas.delete("all")
        for y in range(self.height):
            for x in range(self.width):
                if self.pixels[y][x] == 1:
                    self.canvas.create_rectangle(
                        x * self.pixel_size,
                        y * self.pixel_size,
                        (x + 1) * self.pixel_size,
                        (y + 1) * self.pixel_size,
                        fill='white'
                    )

    def clear_canvas(self):
        self.pixels = [[0] * self.width for _ in range(self.height)]  # Reset pixels
        self.draw_canvas()  # Redraw canvas

    def identify(self):
        self.identify_button.config(text="Identifying...")
        self.master.after(100, self.identification_process)
        

    def identification_process(self):
        colored_pixels=[]
        for row in self.pixels:
            pixel_row=[]
            for pixel in row:
                if pixel == 1:
                    pixel_row.append(255)
                else:
                    pixel_row.append(0)
            colored_pixels.append(pixel_row)
            
        result = knn([colored_pixels])
        self.update_large_number(result[0])

        self.identify_button.config(text="    Identify    ")

    def update_large_number(self, new_value):
        self.large_number = new_value
        self.number_label.config(text=str(self.large_number))

    def load_dataset():
        pass

if __name__ == "__main__":
    root = tk.Tk()
    editor = PixelEditor(root)
    root.title("OCR")
    root.mainloop()