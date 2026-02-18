# Image Processing and Enhancement
# Blurring, Grayscaling, Scaling, Transformations, Histogram Equalization

import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load and Show Original 
image_path = 'cats_dogs.webp'
image = cv2.imread(image_path)

# Resize for display
resized_image = cv2.resize(image, (900, 500))
resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

plt.imshow(resized_image_rgb)
plt.title('Original Image')
plt.axis('off')
plt.show()


# Grayscaling
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow('Original', image)
cv2.imshow('Grayscale', gray_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Scaling (Zoom In / Zoom Out) 
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
scale_factor_1 = 2.0   # Zoom In
scale_factor_2 = 0.5   # Zoom Out

height, width = image_rgb.shape[:2]

# Zoom In
zoomed_image = cv2.resize(image_rgb,
                          (int(width*scale_factor_1), int(height*scale_factor_1)),
                          interpolation=cv2.INTER_CUBIC)

# Zoom Out
scaled_image = cv2.resize(image_rgb,
                          (int(width*scale_factor_2), int(height*scale_factor_2)),
                          interpolation=cv2.INTER_AREA)

fig, axs = plt.subplots(1, 3, figsize=(12, 5))
axs[0].imshow(image_rgb)
axs[0].set_title('Original Image\n'+str(image_rgb.shape))
axs[1].imshow(zoomed_image)
axs[1].set_title('Zoomed Image\n'+str(zoomed_image.shape))
axs[2].imshow(scaled_image)
axs[2].set_title('Scaled Image\n'+str(scaled_image.shape))

for ax in axs:
    ax.set_xticks([])
    ax.set_yticks([])
plt.tight_layout()
plt.show()


# ---------- Intensity Transformation (Log Transform) ----------
c = 255/(np.log(1 + np.max(image)))
log_transformed = c * np.log(1 + image)
log_transformed = np.array(log_transformed, dtype=np.uint8)

cv2.imshow("Log Transformed", log_transformed)
cv2.waitKey(0)
cv2.destroyAllWindows()


# ---------- Histogram Equalization ----------
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
equ = cv2.equalizeHist(gray)
res = np.hstack((gray, equ))

plt.figure(figsize=(10, 5))
plt.imshow(res, cmap='gray')
plt.title("Original Grayscale vs Equalized")
plt.axis('off')
plt.show()


# ---------- Convert to another color ---------
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
cv2.imshow("HSV Image", hsv_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ------- In different colors ---

# Python program to read image as LAB color space

# Reads the image
img = cv2.imread('cats_dogs.webp')

# Converts to LAB color space
lab_img = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

# Shows the image
cv2.imshow('LAB Image', lab_img) 

cv2.waitKey(0)         
cv2.destroyAllWindows()




# 4. Advance image Manipulation

# Reading the damaged image
damaged_img = cv2.imread("cats_dogs.webp")

# Get the shape of the image
height, width = damaged_img.shape[:2]

# Converting all pixels greater than zero to black while black becomes white
for i in range(height):
    for j in range(width):
        if damaged_img[i, j].sum() > 0:
            damaged_img[i, j] = 0
        else:
            damaged_img[i, j] = [255, 255, 255]

# Saving the mask 
mask = damaged_img
cv2.imwrite('mask.jpg', mask)

# Displaying mask
cv2.imshow("damaged image mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()



# Image Registration

# Open the image files
img1_color = cv2.imread("cats_dogs.webp")  # Image to be aligned
img2_color = cv2.imread("cats_dogs.webp")  # Reference image (same for now)

# Convert to grayscale
img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)
height, width = img2.shape

# Create ORB detector with 5000 features
orb_detector = cv2.ORB_create(5000)

# Find keypoints and descriptors
kp1, d1 = orb_detector.detectAndCompute(img1, None)
kp2, d2 = orb_detector.detectAndCompute(img2, None)

# Brute Force matcher with Hamming distance
matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors
matches = matcher.match(d1, d2)

# Sort matches by distance
matches = sorted(matches, key=lambda x: x.distance)

# Take top 90% matches
matches = matches[:int(len(matches) * 0.9)]
no_of_matches = len(matches)

# Create arrays to store corresponding points
p1 = np.zeros((no_of_matches, 2))
p2 = np.zeros((no_of_matches, 2))

for i in range(no_of_matches):
    p1[i, :] = kp1[matches[i].queryIdx].pt
    p2[i, :] = kp2[matches[i].trainIdx].pt

# Find homography
homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)

# Apply homography to align image
transformed_img = cv2.warpPerspective(img1_color, homography, (width, height))

# Save the output
cv2.imwrite("output.jpg", transformed_img)

# Show the result
cv2.imshow("Aligned Image", transformed_img)
cv2.waitKey(0)
cv2.destroyAllWindows()




# Background Subtraction

import cv2

# Load single image
frame = cv2.imread("cats_dogs.webp")

# Create background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2()

# Apply background subtraction
fgmask = fgbg.apply(frame)

# Show results
cv2.imshow("Original Frame", frame)
cv2.imshow("Foreground Mask", fgmask)

cv2.waitKey(0)
cv2.destroyAllWindows()




# Concept of Running Average.



# Load the image instead of webcam
img = cv2.imread("cats_dogs.webp")

# Convert to float for accumulateWeighted
averageValue1 = np.float32(img)

while True:
    # Feed the same image repeatedly
    cv2.accumulateWeighted(img, averageValue1, 0.02)

    # Convert back to 8-bit for display
    resultingFrames1 = cv2.convertScaleAbs(averageValue1)

    # Show both original and background model
    cv2.imshow('Original Frame', img)
    cv2.imshow('Background (Running Average)', resultingFrames1)

    # Exit on Esc key
    if cv2.waitKey(30) & 0xFF == 27:
        break

# Cleanup
cv2.destroyAllWindows()



# Foreground Extraction

# Python program to illustrate foreground extraction using GrabCut algorithm

import numpy as np
import cv2
from matplotlib import pyplot as plt

# Load input image
image = cv2.imread('cats_dogs.webp')

# Create an initial mask
mask = np.zeros(image.shape[:2], np.uint8)

# Models for background and foreground (used internally by GrabCut)
backgroundModel = np.zeros((1, 65), np.float64)
foregroundModel = np.zeros((1, 65), np.float64)

# Define a rectangle around the foreground object
# (x, y, width, height) - adjust these values according to your image
rectangle = (50, 50, image.shape[1]-100, image.shape[0]-100)

# Apply GrabCut
cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 3, cv2.GC_INIT_WITH_RECT)

# Modify the mask - 0,2 -> background, 1,3 -> foreground
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

# Multiply mask with the original image to get segmented output
image_segmented = image * mask2[:, :, np.newaxis]

# Show original and segmented images
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title('Segmented Image')
plt.imshow(cv2.cvtColor(image_segmented, cv2.COLOR_BGR2RGB))
plt.axis('off')

plt.show()





# 5. Feature Detection and Description

## Line Detection

# Feature Detection and Description on cats_dogs.webp

import cv2
import numpy as np
import matplotlib.pyplot as plt

# ---------- Line Detection ----------
img = cv2.imread('cats_dogs.webp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize=3)
lines = cv2.HoughLines(edges, 1, np.pi/180, 200)

if lines is not None:
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * r
        y0 = b * r
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imwrite('linesDetected.jpg', img)


# ---------- Circle Detection ----------
img = cv2.imread("cats_dogs.webp")
output = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)

circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1,
    minDist=100,
    param1=100,
    param2=40,
    minRadius=30,
    maxRadius=60
)

if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)

cv2.imshow('Detected Circle', output)
cv2.waitKey(0)
cv2.destroyAllWindows()


# ---------- Corner Detection ----------
img = cv2.imread('cats_dogs.webp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(
    gray, maxCorners=50, qualityLevel=0.01, minDistance=10
)
corners = np.intp(corners)
for corner in corners:
    x, y = corner.ravel()
    cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Corners on Cats & Dogs')
plt.axis('off')
plt.show()


# ---------- Shi-Tomasi Corner Detection ----------
img = cv2.imread('cats_dogs.webp')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(gray_img, 100, 0.01, 10)
corners = np.int32(corners)
for i in corners:
    x, y = i.ravel()
    cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Shi-Tomasi on Cats & Dogs')
plt.axis('off')
plt.show()


# ---------- Harris Corner Detection ----------
img = cv2.imread('cats_dogs.webp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = np.float32(gray)
dest = cv2.cornerHarris(gray, 17, 21, 0.01)
dest = cv2.dilate(dest, None)
img[dest > 0.01 * dest.max()] = [0, 0, 255]

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Harris Corner Detection')
plt.axis('off')
plt.show()


# ---------- Feature Extraction (Edges) ----------
image = cv2.imread('cats_dogs.webp')
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray_image, 100, 200)

plt.imshow(edges, cmap='gray')
plt.title('Edges of Cats & Dogs')
plt.axis('off')
plt.show()
