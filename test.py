import cv2
import numpy as np
import easyocr
import os
import re

# Initialize the OCR reader. Using GPU for better performance and accuracy (if available).
reader = easyocr.Reader(['en'], gpu=True)

# Define a regular expression to match license plate formats (example: Indian plates).
# Adjust this regex for other regions as needed.
LICENSE_PLATE_PATTERN = re.compile(r'^[A-Z0-9]{6,10}$')

def preprocess_image(img):
    """ 
    Preprocess the image to improve OCR results by:
    1. Converting it to grayscale.
    2. Applying CLAHE to enhance contrast.
    3. Denoising to reduce noise.
    4. Using adaptive thresholding for better binarization.
    5. Performing morphological operations to improve edge detection.
    """
    # Convert the image to grayscale for easier processing.
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Use CLAHE (Contrast Limited Adaptive Histogram Equalization) for better contrast.
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Apply fast Non-Local Means Denoising to remove image noise.
    gray = cv2.fastNlMeansDenoising(gray, h=30)

    # Use adaptive thresholding for binarization (handles varying lighting conditions).
    binary = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # Use dilation to emphasize edges and contours.
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.dilate(binary, kernel, iterations=1)

    return binary

def detect_license_plate(image_path):
    """ 
    Detect and extract license plate text from the given image.
    The function:
    1. Preprocesses the image.
    2. Finds contours to detect possible license plate regions.
    3. Filters regions based on aspect ratio and size.
    4. Runs OCR on candidate regions.
    5. Returns the best match based on confidence.
    """
    # Load the image from the given path.
    img = cv2.imread(image_path)

    # Resize image if width is greater than 800px to maintain consistent OCR performance.
    height, width = img.shape[:2]
    if width > 800:
        img = cv2.resize(img, (800, int(800 * height / width)))

    # Preprocess the image to prepare it for contour detection.
    binary = preprocess_image(img)

    # Find contours in the preprocessed binary image.
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    plate_candidates = []

    # Loop through contours and filter them based on aspect ratio and size.
    for contour in sorted(contours, key=cv2.contourArea, reverse=True)[:15]:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h

        # Check if the contour matches typical license plate dimensions.
        if 2.0 <= aspect_ratio <= 5.0 and w > 100:
            plate_candidates.append((x, y, w, h))

    results = []  # Store detected license plates and confidence scores.

    # Process each detected region to apply OCR.
    for (x, y, w, h) in plate_candidates:
        # Add padding to the detected region for better OCR results.
        padding = 10
        x1, y1 = max(0, x - padding), max(0, y - padding)
        x2, y2 = min(img.shape[1], x + w + padding), min(img.shape[0], y + h + padding)
        plate_region = img[y1:y2, x1:x2]

        # Apply OCR to the detected plate region.
        ocr_results = reader.readtext(
            plate_region,
            allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',  # Restrict characters to alphanumeric.
            height_ths=0.5,  # Adjust threshold for text height in region.
            width_ths=0.5    # Adjust threshold for text width in region.
        )

        # Filter OCR results using the regex pattern for license plates.
        for (bbox, text, conf) in ocr_results:
            if LICENSE_PLATE_PATTERN.match(text):
                results.append((text, conf))

    # If no plates are found, try a fallback OCR on the full image.
    if not results:
        ocr_results = reader.readtext(
            img,
            allowlist='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ',
            height_ths=0.5,
            width_ths=0.5
        )
        for (bbox, text, conf) in ocr_results:
            if LICENSE_PLATE_PATTERN.match(text):
                results.append((text, conf))

    # Return the best result based on the highest confidence score.
    if results:
        results.sort(key=lambda x: x[1], reverse=True)
        return results[0]  # Return the text and confidence of the best match.

    return None, 0.0  # No valid license plate detected.

def main():
    """ 
    Main function to process all images in the specified folder.
    For each image:
    1. Detect license plates and extract text.
    2. Calculate the average confidence of all successful detections.
    """
    folder_path = "./images"  # Folder containing images to process.
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')

    total_confidence = 0.0  # Sum of all confidence scores.
    num_detections = 0      # Count of successful detections.

    # Loop through all files in the folder and process valid images.
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            print(f"\nProcessing {filename}...")
            img_path = os.path.join(folder_path, filename)

            try:
                # Detect license plate and get the result.
                result = detect_license_plate(img_path)
                if result:
                    text, confidence = result
                    print(f"Detected Text: {text}")
                    print(f"Confidence: {confidence:.2f}")

                    # Accumulate confidence scores and count successful detections.
                    total_confidence += confidence
                    num_detections += 1
                else:
                    print("No license plate detected")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    # Calculate and display the average confidence score.
    if num_detections > 0:
        avg_confidence = total_confidence / num_detections
        print(f"\nAverage Confidence: {avg_confidence:.2f}")
    else:
        print("\nNo valid license plates detected in any image.")

# Entry point of the script.
if __name__ == "__main__":
    main()
