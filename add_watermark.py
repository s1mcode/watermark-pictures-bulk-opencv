import cv2
import numpy as np
import glob
import os
import random

ROOT_PATH = r'D:\myTools\add-watermark\images'

logo = cv2.imread("./mylogo.png")
h_logo, w_logo, _ = logo.shape


def iter_pics(root_dir):
    files_path = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            # print(root, " - ", dir, " - ", file)
            file_path = os.path.join(root, file)
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                files_path.append(file_path)
    return files_path


def add_watermark_bulk(images_path):
    print("Adding watermark...")
    for index, img_path in enumerate(images_path):
        print("Watermarking num {} pic".format(str(index + 1)))
        img = cv2.imread(img_path)
        h_img, w_img, _ = img.shape

        position_dict = dict()

        # Put watermark on pic center
        position_dict["center"] = {}
        position_dict["center"]["center_y"] = int(h_img / 2)
        position_dict["center"]["center_x"] = int(w_img / 2)

        # Put watermark on pic bottom_left
        position_dict["bottom_left"] = {}
        position_dict["bottom_left"]["center_y"] = int(h_img) - int(h_logo / 2)
        position_dict["bottom_left"]["center_x"] = int(w_logo / 2)

        # Put watermark on pic top_right
        position_dict["top_right"] = {}
        position_dict["top_right"]["center_y"] = int(h_logo / 2)
        position_dict["top_right"]["center_x"] = int(w_img) - int(w_logo / 2)

        # Get random position
        position = (random.sample(position_dict.keys(), 1))[0]

        center_y = position_dict[position]["center_y"]
        center_x = position_dict[position]["center_x"]

        top_y = center_y - int(h_logo / 2)
        left_x = center_x - int(w_logo / 2)
        bottom_y = top_y + h_logo
        right_x = left_x + w_logo

        # Get ROI
        roi = img[top_y: bottom_y, left_x: right_x]

        # Add the Logo to the Roi
        result = cv2.addWeighted(roi, 1, logo, 0.4, 0)

        # Replace the ROI on the image
        img[top_y: bottom_y, left_x: right_x] = result

        # Get filename and save the image
        cv2.imwrite(img_path, img)
    print("Watermark added to all the images!")


def main():
    pic_list = iter_pics(ROOT_PATH)
    print("Found {} pics".format(len(pic_list)))
    add_watermark_bulk(pic_list)


if __name__ == "__main__":
    main()
