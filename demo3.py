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
        green_area = cv2.contourArea(green_contour)
        if green_area < 10:  # Skip very small contours that might be noise
            continue

        green_rect = cv2.boundingRect(green_contour)
        x, y, w, h = green_rect
        green_roi = green_mask[y:y+h, x:x+w]

        # Check if any red contour overlaps with the green contour
        for red_contour in red_contours:
            red_rect = cv2.boundingRect(red_contour)
            rx, ry, rw, rh = red_rect

            # Find the intersection area between green and red rectangles
            intersect_x1 = max(x, rx)
            intersect_y1 = max(y, ry)
            intersect_x2 = min(x + w, rx + rw)
            intersect_y2 = min(y + h, ry + rh)

            if intersect_x1 < intersect_x2 and intersect_y1 < intersect_y2:
                # There is an intersection
                red_roi = red_mask[intersect_y1:intersect_y2, intersect_x1:intersect_x2]
                if cv2.countNonZero(red_roi) > 0 and cv2.countNonZero(green_roi) > 0:
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