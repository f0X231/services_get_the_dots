import cv2
import numpy as np

def count_red_dots(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # Combine both masks to capture the full range of red
    mask = mask1 + mask2
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of contours (i.e., red dots)
    red_dot_count = len(contours)
    # print(f"Number of red dots found: {red_dot_count}")

    # Optionally, draw the contours on the image
    # output_image = image.copy()
    # cv2.drawContours(output_image, contours, -1, (0, 255, 0), 2)

    # Save the output image with contours drawn
    # output_path = 'output_with_dots.jpg'
    # cv2.imwrite(output_path, output_image)
    # print(f"Output image saved as {output_path}")

    return red_dot_count


def count_green_dots(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV (Hue, Saturation, Value) color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of green color in HSV
    lower_green = np.array([40, 40, 40])
    upper_green = np.array([80, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of contours (i.e., green dots)
    green_dot_count = len(contours)
    # print(f"Number of green dots found: {green_dot_count}")

    # Optionally, draw the contours on the image
    # output_image = image.copy()
    # cv2.drawContours(output_image, contours, -1, (0, 0, 255), 2)  # Red contours for visibility

    # Save the output image with contours drawn
    # output_path = 'output_with_green_dots.jpg'
    # cv2.imwrite(output_path, output_image)
    # print(f"Output image saved as {output_path}")

    return green_dot_count

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

    # Find contours for green and red dots
    green_contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

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
            if cv2.countNonZero(overlap) > 0:
                overlap_count += 1

    # print(f"Number of overlapping green and red dots: {overlap_count}")

    # Optionally, draw the contours on the image for visualization
    # output_image = image.copy()
    # cv2.drawContours(output_image, green_contours, -1, (0, 255, 0), 2)  # Green contours
    # cv2.drawContours(output_image, red_contours, -1, (255, 0, 0), 2)    # Red contours

    # output_path = 'output_with_overlapping_dots.jpg'
    # cv2.imwrite(output_path, output_image)
    # print(f"Output image saved as {output_path}")

    return overlap_count


# Example usage
# image_path = '../uploads/split_image_6_4.jpg'
# result = count_dots(image_path)
# print("Green dots:", result[0])
# print("Red dots:", result[1])
# print("Overlapping dots:", result[2])