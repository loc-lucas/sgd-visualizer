import cv2
import numpy as np


def prepare_texture(size, in_files, out_file):
    images = [cv2.resize(cv2.cvtColor(cv2.imread(file), cv2.COLOR_BGR2RGB), size) for file in in_files]
    texture = np.concatenate(images, axis=1)
    cv2.imwrite(out_file, texture)

size = (500, 500)
in_files_1 = ["./image/thuylinh.jpeg",
          "./image/tieuvi.jpeg"
          ]
out_file_1 = "image/texture1.jpeg"
in_files_2 = ["./image/ledinh.jpeg",
              "./image/lotu.jpeg"
              ]
out_file_2 = "image/texture2.jpeg"
prepare_texture(size, in_files_1, out_file_1)
prepare_texture(size, in_files_2, out_file_2)