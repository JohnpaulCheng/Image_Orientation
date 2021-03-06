import cv2
import numpy as np
from matplotlib import pyplot as plt

img_base = cv2.imread('figures/0.jpeg')
img_rotate_orig = cv2.imread('figures/10.jpeg')
img_base = cv2.cvtColor(img_base, cv2.COLOR_BGR2GRAY)
img_rotate_orig = cv2.cvtColor(img_rotate_orig, cv2.COLOR_BGR2GRAY)
img_rotate = cv2.GaussianBlur(img_rotate_orig,(3,3),0)

w, h = img_base.shape[:2]
rotate_angle = -15
scale_ratio = 5
img_base = cv2.resize(img_base, (int(h/scale_ratio), int(w/scale_ratio)))
img_rotate = cv2.resize(img_rotate, (int(h/scale_ratio), int(w/scale_ratio)))
img_L = img_base
img_R = img_rotate

sift = cv2.xfeatures2d.SIFT_create()

kp1, des1 = sift.detectAndCompute(img_L, None)
kp2, des2 = sift.detectAndCompute(img_R, None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)

# 利用FLANN匹配器
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2)

good = []
pts1 = []
pts2 = []

# 寻找匹配点对
for i, (m, n) in enumerate(matches):
    if m.distance < 0.2 * n.distance:
        good.append(m)
        pts1.append(kp1[m.queryIdx].pt)
        pts2.append(kp2[m.trainIdx].pt)

pts1 = np.float32(pts1)
pts2 = np.float32(pts2)
# 根据匹配点对计算基础矩阵
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)

# 寻则内部点
pts1 = pts1[mask.ravel() == 1]
pts2 = pts2[mask.ravel() == 1]


# 绘制极线的函数
def drawlines(img1, img2, lines, pts1, pts2):
    r, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for r, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -r[2] / r[1]])  # 映射成整数值
        x1, y1 = map(int, [c, -(r[2] + r[1] * c) / r[1]])
        cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        cv2.circle(img1, tuple(pt1), 5, color, -1)
        cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2


# 计算并绘制两幅图像中的极线
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
lines1 = lines1.reshape(-1, 3)
img5, img6 = drawlines(img_L, img_R, lines1, pts1, pts2)

lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 2, F)
lines2 = lines2.reshape(-1, 3)
img3, img4 = drawlines(img_R, img_L, lines2, pts2, pts1)

plt.subplot(121), plt.imshow(img5), plt.title('leftImage'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(img3), plt.title('rightImage'), plt.xticks([]), plt.yticks([])
plt.show()