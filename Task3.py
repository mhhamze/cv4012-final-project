import os
import cv2
import numpy as np

#
#
# path = "C:/Users/Asus/Desktop/CV-Final-Project/Chessboard.png"
# chessboard = cv2.imread(path)
# directory = "C:/Users/Asus/Desktop/CV-Final-Project/chess-pieces/"
# pieces = os.listdir(directory)
# copy = chessboard.copy()
# i = 0
# j = 0
# for piece in pieces:
#     piece_image = cv2.imread(os.path.join(directory, piece))
#     piece_image = cv2.resize(piece_image, (60, 60))
#     mask1 = (piece_image == 0)
#     mask2 = (piece_image == 255)
#     mask = mask1 + mask2
#     if j < 480:
#         copy[i:i + 60, j:j + 60] = chessboard[i:i + 60, j:j + 60] * ~mask + piece_image * mask
#     else:
#         i += 60
#         j = 0
#         copy[i:i + 60, j:j + 60] = chessboard[i:i + 60, j:j + 60] * ~mask + piece_image * mask
#     cv2.imshow("Chessboard", copy)
#     cv2.waitKey(0)
#     j += 60

board_path = "C:/Users/Asus/Desktop/CV-Final-Project/Chessboard.png"
board = cv2.imread(board_path)
points1 = np.array(
    [(0, 0),
     (0, 479),
     (479, 479),
     (479, 0),
     ]
).astype(np.float32)
corners_dir = "C:/Users/Asus/Desktop/CV-Final-Project/test/corners/"
images_dir = "C:/Users/Asus/Desktop/CV-Final-Project/test/images/1024/"
boxes_dir = "C:/Users/Asus/Desktop/CV-Final-Project/test/boxes/"
for f in os.listdir(corners_dir):
    file = open(os.path.join(corners_dir, f), "r")
    corners = []
    for line in file:
        if line:
            x = line.replace("\n", '').split(",")
            corners.append((int(x[0]), int(x[1])))
    points2 = np.array(corners).astype(np.float32)
    H = cv2.getPerspectiveTransform(points2, points1)
    I2 = cv2.imread(os.path.join(images_dir, f[:-4] + ".jpg"))
    output_size = (480, 480)
    J = cv2.warpPerspective(I2, H, output_size)
    # cv2.imshow('board', board)
    # cv2.waitKey(0)
    # cv2.imshow('I2', I2)
    # cv2.waitKey(0)
    # cv2.imshow('J', J)
    # cv2.waitKey(0)
    file = open(os.path.join(boxes_dir, f), "r")
    counter = 0
    p = 0
    pieces_dir = "C:/Users/Asus/Desktop/CV-Final-Project/chess-pieces/"
    copy = board.copy()
    for line in file:
        if counter % 2 == 0:
            piece_number = line.replace("\n", "").replace("[", "").replace("]", "").split(".")
            if piece_number[0]:
                piece = cv2.imread(os.path.join(pieces_dir, str(int(piece_number[0])) + ".png"))
                piece = cv2.resize(piece, (60, 60))
                mask1 = (piece == 0)
                mask2 = (piece == 255)
                mask = mask1 + mask2
        elif counter % 2 == 1:

            data = line.replace("\n", '').replace("[", "").replace("]", "").replace(",", '').split()
            if data:
                x1 = int(data[0].split(".")[0])
                y1 = int(data[1].split(".")[0])
                x2 = int(data[2].split(".")[0])
                y2 = int(data[3].split(".")[0])
                coordinates1 = np.array([
                    [(x1 + x2) / 2],
                    [y2],
                    [1]
                ]).astype(np.float32)
                coordinates2 = np.matmul(H, coordinates1)
                print(coordinates2)
                i = float(coordinates2[0][0])
                i /= coordinates2[2][0]
                i = int(i)
                i -= i % 60

                j = float(coordinates2[1][0])
                j /= coordinates2[2][0]
                j = int(j)
                j -= j % 60
                p = 1

        if p == 1:
            p = 0
            print(i, j)
            copy[i:i + 60, j:j + 60] = board[i:i + 60, j:j + 60] * ~mask + piece * mask
        counter += 1
    cv2.imshow(f[:-4] + ".jpg", copy)
    cv2.waitKey(0)
