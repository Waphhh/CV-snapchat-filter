import tkinter as tk
from PIL import ImageTk, Image

# It has been noticed that sometimes when clicking the buttons the event is not properly registered
# https://github.com/PySimpleGUI/PySimpleGUI/issues/5036

class errorButton(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("No Face Detected")

        # Window dimensions
        window_height = 150
        window_width = 300

        # Alert text
        text = tk.Label(self, text="No faces have been detected!", wraplength=300, font=('Times New Roman', 32, 'bold'))
        text.pack()

        # Exit button and function
        exit_button = tk.Button(self, text="OK!", command=self.destroy)
        exit_button.pack(pady=10)

        # Centreing the alert
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))

        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

class ImageGrid(tk.Tk):
    def __init__(self, image1, image2, image3, padx=100, pady=20):
        super().__init__()
        self.title("Photo Grid")
        # self.parent = parent
        self.padx = padx
        self.pady = pady
        self.images = [image1, image2, image3]
        self.selected_image = []
        self.create_grid()
        self.image_count = 0
        self.update_grid(self.images[self.image_count])

    def create_grid(self):
        self.grid_frame = tk.Frame(self)
        self.grid_frame.pack()

    def update_grid(self, images):
        self.clear_grid()
        for i, img_path in enumerate(images):
            img = Image.open(img_path)
            img = img.resize((150, 150), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            label = tk.Label(self.grid_frame, image=photo)
            label.image = photo

            caption_text = ((images[i]).split("/")[1]).split(".")[0]
            caption = tk.Label(self.grid_frame, text=caption_text)
            caption.grid(row=(i // 2) * 2 + 1, column=i % 2, padx=self.padx, pady=self.pady)

            label.grid(row=i // 2 * 2, column=i % 2, padx=self.padx, pady=self.pady)

            label.bind("<Button-1>", lambda event, index=i: self.image_clicked(index))


    def clear_grid(self):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()

    def image_clicked(self, index):
        print("Image clicked:", index)
        self.selected_image.append(index)
        self.image_count += 1
        if self.image_count == 3:
            self.close_window()
        else:
            self.update_grid(self.images[self.image_count])

    def return_selected_image(self):
        return self.selected_image

    def close_window(self):
        self.destroy()
