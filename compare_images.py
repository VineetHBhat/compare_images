from builtins import slice

import numpy as np
from PIL import Image


class CompareImages:
    def __init__(self, image1_path: str, image2_path: str):
        self.image1_path = image1_path
        self.image2_path = image2_path
        self.output_image_path = "highlighted_differences.png"

    def read_input_images(self) -> tuple:
        img1 = Image.open(self.image1_path).convert("RGB")
        img2 = Image.open(self.image2_path).convert("RGB")
        return img1, img2

    def highlight_differences(self, image1_arr: np.ndarray, image2_arr: np.ndarray):
        differences = image1_arr != image2_arr
        mask = np.any(~differences, axis=-1)
        new_diff_arr = np.where(mask, False, True)
        diff_array = image1_arr.copy()
        diff_array[new_diff_arr] = [255, 0, 0]
        diff_image = Image.fromarray(np.uint8(diff_array))
        diff_image.save(self.output_image_path)

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

    def compare_images(self, mask_slice_string: str = "", diff_tolerance: float = 0.0):
        img1, img2 = self.read_input_images()
        if img1.size != img2.size:
            raise ValueError("Images don't have the same dimensions.")

        img1_arr = np.array(img1)
        img2_arr = np.array(img2)
        if mask_slice_string:
            positive_mask, negative_mask = None, None
            masks = self.get_masks_from_string(mask_slice_string)
            for mask_type, mask_values in masks.items():
                for value in mask_values:
                    if mask_type == "positive_mask":
                        if positive_mask is None:
                            positive_mask = np.zeros(img1_arr.shape[:2], dtype=bool)
                        positive_mask[value[0], value[1]] = True
                    elif mask_type == "negative_mask":
                        if negative_mask is None:
                            negative_mask = np.ones(img1_arr.shape[:2], dtype=bool)
                        negative_mask[value[0], value[1]] = False
            if positive_mask is not None:
                img1_arr = np.where(positive_mask[:, :, np.newaxis], img1_arr, 0)
                img2_arr = np.where(positive_mask[:, :, np.newaxis], img2_arr, 0)
            if negative_mask is not None:
                img1_arr = np.where(negative_mask[:, :, np.newaxis], img1_arr, 0)
                img2_arr = np.where(negative_mask[:, :, np.newaxis], img2_arr, 0)
        difference = np.abs(img1_arr - img2_arr)
        mean_difference = np.mean(difference)
        print("Mean Difference: {}".format(mean_difference))
        if mean_difference > diff_tolerance:
            self.highlight_differences(img1_arr, img2_arr)
            raise Exception("Images DON'T MATCH! Diff image \"{}\" has been generated.".format(self.output_image_path))
        else:
            print("Images MATCH! No diff image \"{}\" has been generated.".format(self.output_image_path))


if __name__ == "__main__":
    expected = "desktop_background.png"
    actual = "desktop_background - Copy.png"

    comparator = CompareImages(expected, actual)
    # comparator.compare_images(diff_tolerance=0)
    # comparator.compare_images(mask_slice_string="-500:600,400:600", diff_tolerance=0)
    # comparator.compare_images(mask_slice_string="+500:600,400:600", diff_tolerance=0)
    comparator.compare_images(mask_slice_string="+400:900,100:1300|-400:650,700:950|+200:300,400:1300",
                              diff_tolerance=0)
