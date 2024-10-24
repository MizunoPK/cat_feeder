import os
import cv2
import shutil

img_folder = "./data/SinglePhotos/yarn"
nori_folder = "./data/CatPics/nori"
bento_folder = "./data/CatPics/bento"

img_list = os.listdir(img_folder)

for img_name in img_list:
    img_full_path = os.path.join(img_folder, img_name)
    img = cv2.imread(img_full_path)
    # img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
    cv2.imshow("output", img)
    cv2.waitKey(1)
    selection = input("Nori (1), Bento (2) or Trash (3): ")

    if selection == "3":
        os.remove(img_full_path)
        continue

    dest_dir = nori_folder if selection == "1" else bento_folder
    dest_file = os.path.join(dest_dir, img_name)
    shutil.move(img_full_path, dest_file)