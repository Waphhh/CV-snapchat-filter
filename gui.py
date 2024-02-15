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
    def __init__(self, images, rows, cols, padx=100, pady=20):
        super().__init__()
        # Intialing window key items
        self.title("Photo Grid")
        self.images = images
        self.rows = rows
        self.cols = cols
        self.padx = padx
        self.pady = pady

        self.create_grid()

    def create_grid(self):
        for i in range(self.rows):
            for j in range(self.cols):
                index = i * self.cols + j
                if index < len(self.images):
                    img = Image.open(self.images[index])
                    img = img.resize((150, 150), Image.Resampling.LANCZOS) # Resize icons
                    photo = ImageTk.PhotoImage(img)
                    frame = tk.Frame(self, padx=self.padx, pady=self.pady) # Icon padding
                    label = tk.Label(frame, image=photo)
                    label.image = photo
                    label.pack()

                    caption = tk.Label(frame, text=((self.images[index]).split("/")[1]).split(".")[0])
                    caption.pack()

                    frame.grid(row=i, column=j)
                    label.bind("<Button-1>", lambda filler, index = index: self.image_clicked(index))
                    # the lambda function just runs the image_clicked function, "filler" is just a filler variable that the event handler will return and we have no use of

    # Closes and defines the selected icon
    def image_clicked(self, index):
        print("Image clicked:", index)
        self.selected_image = index
        self.close_window()

    def return_selected_image(self):
        return self.selected_image # Returns selected icon

    def close_window(self):
        self.destroy()
