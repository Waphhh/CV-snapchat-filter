import tkinter as tk
from PIL import ImageTk, Image

class ImageGrid(tk.Tk):
    def __init__(self, images, rows, cols, padx=100, pady=20):
        super().__init__()
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
                    img = img.resize((150, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    frame = tk.Frame(self, padx=self.padx, pady=self.pady)
                    label = tk.Label(frame, image=photo)
                    label.image = photo
                    label.pack()
                    frame.grid(row=i, column=j)
                    label.bind("<Button-1>", lambda filler, index = index: self.image_clicked(index))
                    # the lambda function just runs the image_clicked function, "filler" is just a filler variable that the event handler will return and we have no use of

    def image_clicked(self, index):
        print("Image clicked:", index)
        self.selected_image = index
        self.close_window()

    def return_selected_image(self):
        return self.selected_image

    def close_window(self):
        self.destroy()

if __name__ == "__main__":
    images1 = ["assets/cat_nose.png", "assets/nose.png", "assets/pig_nose.png", "assets/red_nose.png"]  # Paths to your images
    images2 = ["assets/cowboy_hat.png", "assets/wrmask.png", "assets/mask.png", "assets/swag.png"]  # Paths to your images
    rows = 2
    cols = 2
    app = ImageGrid(images1, rows, cols)
    app.mainloop()
    selected_nose = app.return_selected_image()
    app = ImageGrid(images2, rows, cols)
    app.mainloop()
    selected_top = app.return_selected_image()

    print(f"selected nose is: {selected_nose}, selected top is: {selected_top}, selected theme is: {selected_theme}")