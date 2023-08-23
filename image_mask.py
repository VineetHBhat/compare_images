import tkinter as tk

import numpy as np
from PIL import Image, ImageTk


class ImageMask:
    def __init__(self, img_src: str):
        self.current_image_label = None
        self.img_src = img_src
        self.img_photo = None
        self.entry = None
        self.frame = None

    @staticmethod
    def get_masks_from_string(mask_slice_string: str) -> dict:
        masks = {"positive_mask": [], "negative_mask": []}
        mask_slices_split = mask_slice_string.split("|")
        for mask_slices in mask_slices_split:
            mask_components = []
            mask_slice_list = mask_slices[1:].split(",")
            for mask_slice in mask_slice_list:
                temp = mask_slice.split(":")
                i = int(temp[0])
                j = int(temp[1])
                mask_components.append(slice(i, j))
            if mask_slices[0] == "+":
                masks["positive_mask"].append(mask_components)
            elif mask_slices[0] == "-":
                masks["negative_mask"].append(mask_components)
        return masks

    def load_image_then_apply_mask(self, mask_slice_string: str):
        input_image = Image.open(fp=self.img_src)
        image_array = np.asarray(input_image)
        if mask_slice_string:
            positive_mask, negative_mask = None, None
            masks = self.get_masks_from_string(mask_slice_string)
            for mask_type, mask_values in masks.items():
                for value in mask_values:
                    if mask_type == "positive_mask":
                        if positive_mask is None:
                            positive_mask = np.zeros(image_array.shape[:2], dtype=bool)
                        positive_mask[value[0], value[1]] = True
                    elif mask_type == "negative_mask":
                        if negative_mask is None:
                            negative_mask = np.ones(image_array.shape[:2], dtype=bool)
                        negative_mask[value[0], value[1]] = False
            if positive_mask is not None:
                image_array = np.where(positive_mask[:, :, np.newaxis], image_array, 0)
            if negative_mask is not None:
                image_array = np.where(negative_mask[:, :, np.newaxis], image_array, 0)
        masked_image = Image.fromarray(image_array)
        self.img_photo = ImageTk.PhotoImage(masked_image)

    @staticmethod
    def create_main_window(title: str = "Create Mask") -> tk.Tk:
        main = tk.Tk()
        main.title(title)
        main.geometry("1280x600")
        return main

    def process_input(self, event: tk.Event) -> None:
        if self.entry:
            input_text = self.entry.get()
            self.load_image_then_apply_mask(mask_slice_string=input_text)
            if self.current_image_label:
                self.current_image_label.destroy()
            image_label = tk.Label(self.frame, image=self.img_photo)
            image_label.pack()
            self.current_image_label = image_label
        else:
            raise Exception("Class fields: 'entry' & 'output_label' are not defined. Use 'start()' to define them.")

    def start(self):
        main = self.create_main_window()

        input_label = tk.Label(main, text="ENTER MASK")
        input_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.entry = tk.Entry(main, width=100)
        self.entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry.insert(0, "+100:900,100:1800|-400:650,700:950")

        syntax_label = tk.Label(main, text="Example: +1500:2500,1000:2000|-2000:2100,1500:1600")
        syntax_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")

        canvas = tk.Canvas(main)
        canvas.grid(row=1, columnspan=3, padx=5, pady=5, sticky="nsew")
        main.grid_columnconfigure(2, weight=1)
        main.grid_rowconfigure(1, weight=1)

        v_scrollbar = tk.Scrollbar(main, orient="vertical", command=canvas.yview)
        v_scrollbar.grid(row=1, column=3, sticky="ns")

        h_scrollbar = tk.Scrollbar(main, orient="horizontal", command=canvas.xview)
        h_scrollbar.grid(row=2, columnspan=3, sticky="ew")

        canvas.configure(yscrollcommand=v_scrollbar.set)
        canvas.configure(xscrollcommand=h_scrollbar.set)

        self.frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.entry.bind("<Return>", self.process_input)
        self.frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        self.current_image_label = None

        main.after(ms=1000)
        main.mainloop()


if __name__ == "__main__":
    image_file = "actual_image.jpg"
    # image_file = "desktop_background.png"
    masking = ImageMask(img_src=image_file)
    masking.start()
