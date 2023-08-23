# Compare Images (Python 3)

## Important files
Below two files are useful for image comparison
1. **image_mask.py**
   1. Used to generate masks for image comparison
   2. Uses tkinter, numpy, pillow (PIL)
2. **compare_images.py**
   1. Compares two images and highlights difference if any
   2. Uses numpy, pillow (PIL)

## Format of masks used by above files
The basic structure of the format is as shown below. **compare_images.py** expects the below format to be provided as a string.  
`+x1:x2,y1:y2|-x3:x4,y3:y4|...`
1. `+`: Used to denote a positive mask
2. `-`: Used to denote a negative mask
3. `x1:x2`
   1. Starting and ending points in vertical direction.
   2. `x1` starts from the top of the screen.
4. `y1:y2`
   1. Starting and ending points in horizontal direction.
   2. `y1` starts from the left side of the screen.
5. Multiple masks can be applied at the same time. Different masks should be separated by a `|`.

## Definitions
1. Positive mask
   1. if `x1:x2,y1:y2` is prefixed by a `+`, this denotes a positive mask.
   2. The area identified by the mask will be a part of the image.
2. Negative mask
   1. if `x1:x2,y1:y2` is prefixed by a `-`, this denotes a negative mask.
   2. The area identified by the mask will **NOT** be a part of the image.

## How to use the two files
1. Change the `image_file` path and run **image_mask.py**. A UI will open with a field where you can enter masks in the above format.
2. After finalizing the mask, copy it.
3. Open **compare_images.py** and supply the finalized mask as a string to `mask_slice_string`. Optionally you can also add a `diff_tolerance`.
4. Run **compare_images.py**. If the images match, a suitable message is shown in the console. Otherwise an exception is raised and an image with differences is generated.