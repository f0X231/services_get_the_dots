

def count_overlapping_dots(image_path, green_color_range, red_color_range):
    """
    Counts the number of overlapping green and red dots in an image.

    Args:
        image_path: Path to the image file.
        green_color_range: Tuple of (lower_green, upper_green) color boundaries.
        red_color_range: Tuple of (lower_red, upper_red) color boundaries.

    Returns:
        Number of overlapping dots.
    """

    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Create masks for green and red dots
    green_mask = cv2.inRange(hsv, green_color_range[0], green_color_range[1])
    red_mask = cv2.inRange(hsv, red_color_range[0], red_color_range[1])

    # Combine the masks to find overlapping regions
    overlap_mask = cv2.bitwise_and(green_mask, red_mask)

    # Find contours in the overlap mask
    contours, _ = cv2.findContours(overlap_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Count the number of overlapping dots
    num_overlapping_dots = len(contours)

    return num_overlapping_dots

# Example usage
image_path = '../uploads/split_image_6_4.jpg'
green_color_range = ((50, 100, 100), (70, 255, 255))
red_color_range = ((0, 100, 100), (20, 255, 255))

num_overlapping_dots = count_overlapping_dots(image_path, green_color_range, red_color_range)
print("Number of overlapping dots:", num_overlapping_dots)





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

    print(f"Number of overlapping green and red dots: {overlap_count}")

    # Optionally, draw the contours on the image for visualization
    output_image = image.copy()
    cv2.drawContours(output_image, green_contours, -1, (0, 255, 0), 2)  # Green contours
    cv2.drawContours(output_image, red_contours, -1, (255, 0, 0), 2)    # Red contours

    output_path = 'output_with_overlapping_dots.jpg'
    cv2.imwrite(output_path, output_image)
    print(f"Output image saved as {output_path}")

    return overlap_count


# Example usage:
count_red_dots('../uploads/split_image_6_4.jpg')
count_green_dots('../uploads/split_image_6_4.jpg')
count_overlapping_green_red_dots('../uploads/split_image_6_4.jpg')


def count_dots(image_path):
  """Counts green, red, and overlapping dots in an image.

  Args:
    image_path: Path to the image file.

  Returns:
    Tuple of (num_green, num_red, num_overlapping).
  """

  # Load the image
  img = cv2.imread(image_path)

  # Convert to HSV
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

  # Define color ranges (adjust as needed)
  green_lower = np.array([50, 100, 100])
  green_upper = np.array([70, 255, 255])
  red_lower = np.array([0, 100, 100])
  red_upper = np.array([20, 255, 255])

  # Create masks
  green_mask = cv2.inRange(hsv, green_lower, green_upper)
  red_mask = cv2.inRange(hsv, red_lower, red_upper)

  # Find overlapping dots
  overlap_mask = cv2.bitwise_and(green_mask, red_mask)

  # Find contours
  _, green_contours = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  _, red_contours = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  _, overlap_contours = cv2.findContours(overlap_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  # Count dots
  num_green = len(green_contours)
  num_red = len(red_contours)
  num_overlapping = len(overlap_contours)

  return num_green, num_red, num_overlapping
