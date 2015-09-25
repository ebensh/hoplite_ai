import cv2
from grid_lib import *
import numpy as np

# Draws heavily on http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html

MIN_MATCH_COUNT = 10

def main():
  # This scene contains a Sword Monster.
  scene = cv2.imread('hex_images/hex_-1_-1_2.png', cv2.IMREAD_COLOR)
  mon_sword = cv2.imread('hoplite_assets/mon_sword_1.png', cv2.IMREAD_COLOR)
  mon_bow = cv2.imread('hoplite_assets/mon_bow_1.png', cv2.IMREAD_COLOR)
  mon_wizard = cv2.imread('hoplite_assets/mon_wizard_1.png',
                          cv2.IMREAD_COLOR)
  
  sift = cv2.xfeatures2d.SURF_create()
  # find the keypoints and descriptors with SIFT
  keypoints_scene, descriptors_scene = sift.detectAndCompute(scene, None)
  for mon in [mon_sword, mon_bow, mon_wizard]:
    keypoints_mon, descriptors_mon = sift.detectAndCompute(mon, None)
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(descriptors_scene, descriptors_mon, k=2)
    # store all the good matches as per Lowe's ratio test.
    good = []
    for m, n in matches:
      if m.distance < 0.7 * n.distance:
        good.append(m)

    if len(good) > MIN_MATCH_COUNT:
      src_pts = np.float32([keypoints_scene[m.queryIdx].pt for m in good]).reshape(-1,1,2)
      dst_pts = np.float32([keypoints_mon[m.trainIdx].pt for m in good]).reshape(-1,1,2)

      M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
      matchesMask = mask.ravel().tolist()

      h,w = scene.shape
      pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
      dst = cv2.perspectiveTransform(pts,M)

      mon = cv2.polylines(mon,[np.int32(dst)], True, 255, 3, cv2.LINE_AA)

    else:
      print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
      matchesMask = None

    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)

    result = cv2.drawMatches(scene, keypoints_scene, mon, keypoints_mon,
                             good,None,**draw_params)

    cv2.namedWindow('result', cv2.WINDOW_AUTOSIZE)
    cv2.imshow('result', result)
    cv2.waitKey(0)
  cv2.destroyAllWindows()  

if __name__ == '__main__':
  main()
