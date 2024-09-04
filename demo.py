import cv2
import numpy as np

def count_overlapping_green_red_dots(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Define the range for red color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    red_mask = red_mask1 + red_mask2

    # Apply a morphological operation to separate close objects
    kernel = np.ones((3, 3), np.uint8)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_CLOSE, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours for green and red dots
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    green_dot_count = len(green_contours)
    red_dot_count = len(red_contours)

    overlap_count = 0

    # Iterate through all green contours
    for green_contour in green_contours:
        # Create a mask for the current green contour
        green_mask_single = np.zeros_like(green_mask)
        cv2.drawContours(green_mask_single, [green_contour], -1, 255, thickness=cv2.FILLED)

        # Check for overlap with each red contour
        for red_contour in red_contours:
            # Create a mask for the current red contour
            red_mask_single = np.zeros_like(red_mask)
            cv2.drawContours(red_mask_single, [red_contour], -1, 255, thickness=cv2.FILLED)

            # Check if the two masks overlap
            overlap = cv2.bitwise_and(green_mask_single, red_mask_single)
            if cv2.countNonZero(overlap) > 0:  # At least 1 pixel overlapping
                overlap_count += 1

    # Output the counts
    print(f"Green dot count: {green_dot_count}")
    print(f"Red dot count: {red_dot_count}")
    print(f"Overlapping dot count: {overlap_count}")

    # Optionally, draw the contours on the image for visualization
    output_image = image.copy()
    cv2.drawContours(output_image, green_contours, -1, (0, 255, 0), 2)  # Green contours
    cv2.drawContours(output_image, red_contours, -1, (255, 0, 0), 2)    # Red contours

    output_path = './output_with_overlapping_dots.jpg'
    cv2.imwrite(output_path, output_image)
    print(f"Output image saved as {output_path}")

    return green_dot_count, red_dot_count, overlap_count

# Example usage:
count_overlapping_green_red_dots('./uploads/split_image_6_1.jpg')
