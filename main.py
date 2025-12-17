"""
Contrast Adjustment Techniques for Low-Light Images
This project includes different contrast enhancement techniques for low-light images.

Usage:
    python main.py                    # Process the dataset
    python main.py --create           # Create the folder structure
"""

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================================
# CONTRAST ENHANCEMENT FUNCTIONS
# ============================================================================

def power_law_transformation(image, gamma=1.5):
    """
    Contrast enhancement using Power-Law Transformation (Gamma Correction)
    This method was implemented by Enes.
    
    Parameters:
    ----------
    image : numpy.ndarray
        Input image (in BGR format)
    gamma : float
        Gamma value. gamma < 1: increases brightness, gamma > 1: decreases brightness
    
    Returns:
    -------
    enhanced_image : numpy.ndarray
        Contrast-enhanced image
    """
    # Normalize the image to the range 0–1
    normalized = image.astype(np.float32) / 255.0
    
    # Apply power-law transformation: s = c * r^gamma
    # Here, c is taken as 1
    enhanced = np.power(normalized, gamma)
    
    # Convert back to the range 0–255
    enhanced_image = (enhanced * 255).astype(np.uint8)
    
    return enhanced_image


def clahe_enhancement(image):
    """
    Contrast enhancement using CLAHE (Contrast Limited Adaptive Histogram Equalization)
    This method increases contrast by equalizing the local histogram of the image
    while limiting excessive brightness amplification.

    Parameters:
    ------------
    image : numpy.ndarray
        Input image (in BGR format)

    Returns:
    --------
    enhanced_image : numpy.ndarray
        Contrast-enhanced image with CLAHE applied
    """

    # Convert the color image to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

    # Create the CLAHE object (clipLimit and tileGridSize parameters can be adjusted)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))

    # Apply CLAHE only to the lightness (L) channel
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])

    # Convert back from LAB color space to BGR
    clahe_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    return clahe_image


def thresholding_enhancement(image, threshold_type='adaptive', C=2):
    """
    Contrast enhancement using the Adaptive Thresholding method
    Implemented by: Büşra Yıldız

    With this method, the image is separated into color channels and thresholding
    is applied independently to each channel. This reveals details lost in low-light
    conditions and sharp boundaries more clearly, thereby increasing contrast.
 
    Parameters:
    ------------
    image : numpy.ndarray
        Input image (OpenCV standard BGR format).
    threshold_type : str
        Threshold type: 'adaptive' (Recommended), 'otsu', or 'binary'
    C : int
        Constant value for adaptive thresholding
        (Value subtracted from the mean to reduce noise).
    
    Returns:
    --------
    enhanced_image : numpy.ndarray
        Contrast-enhanced image with emphasized details
    """
    max_val = 255
    block = 11   # Fixed value (Change here if you want to modify it)

    # Helper method that applies thresholding to a single channel (grayscale layer)
    def apply_threshold(channel):
        if threshold_type == 'adaptive':
            # Adaptive Gaussian: determines a local threshold based on the weighted mean of neighbors
            return cv2.adaptiveThreshold(
                channel, max_val, 
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 
                block, C
            )
        elif threshold_type == 'otsu':
            # Automatic global thresholding based on histogram distribution
            _, result = cv2.threshold(channel, 0, max_val, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            return result
        else:
            # Standard fixed thresholding using a predefined constant value
            _, result = cv2.threshold(channel, 127, max_val, cv2.THRESH_BINARY)
            return result

    # 1. Split the image into B-G-R channels
    channels = cv2.split(image)
    
    # 2. Apply the selected thresholding method independently to each channel
    processed_channels = [apply_threshold(ch) for ch in channels]
    
    # 3. Merge the processed channels back together
    enhanced_image = cv2.merge(processed_channels)
    
    return enhanced_image

def load_image(image_path):
    """
    Load the image
    
    Parameters:
    ------------
    image_path : str
        Path to the image file
    
    Returns:
    --------
    image : numpy.ndarray
        Loaded image
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image could not be loaded: {image_path}")
    return image


# ============================================================================
# DATASET PROCESSING FUNCTIONS
# ============================================================================

def create_comparison_image(original, power_law, histogram, thresholding, image_name, save_path):
    """
    Creates a comparison image that displays the original image and the results
    of three methods side by side
    
    Parameters:
    ------------
    original : numpy.ndarray
        Original image (BGR)
    power_law : numpy.ndarray
        Power-Law Transformation result (BGR)
    clahe : numpy.ndarray
        CLAHE Enhancement result (BGR)
    thresholding : numpy.ndarray
        Thresholding result (BGR)
    image_name : str
        Image name
    save_path : str
        Output save path
    """
    # Convert from BGR to RGB (for matplotlib)
    original_rgb = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)
    power_law_rgb = cv2.cvtColor(power_law, cv2.COLOR_BGR2RGB)
    clahe_rgb = cv2.cvtColor(histogram, cv2.COLOR_BGR2RGB)
    threshold_rgb = cv2.cvtColor(thresholding, cv2.COLOR_BGR2RGB)
    
    # Display 4 images side by side
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    
    axes[0].imshow(original_rgb)
    axes[0].set_title('Original', fontsize=14, fontweight='bold')
    axes[0].axis('off')
    
    axes[1].imshow(power_law_rgb)
    axes[1].set_title('Power-Law (γ=0.5)', fontsize=14, fontweight='bold')
    axes[1].axis('off')
    
    axes[2].imshow(clahe_rgb)
    axes[2].set_title('CLAHE Enhancement', fontsize=14, fontweight='bold')
    axes[2].axis('off')
    
    axes[3].imshow(threshold_rgb)
    axes[3].set_title('Thresholding (Adaptive)', fontsize=14, fontweight='bold')
    axes[3].axis('off')
    
    plt.suptitle(f'Comparison: {image_name}', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()  # Clear memory

def process_dataset(dataset_folder="dataset", output_folder="results/dataset_results"):
    """
    Applies contrast enhancement methods to all images in the dataset
    
    Parameters:
    ------------
    dataset_folder : str
        Folder containing dataset images
    output_folder : str
        Folder where results will be saved
    """
    # Create main output directory
    Path(output_folder).mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories for each method
    methods = ["power_law", "clahe", "thresholding"]
    for method in methods:
        Path(f"{output_folder}/{method}").mkdir(parents=True, exist_ok=True)
    
    # Folder for comparison images
    Path(f"{output_folder}/comparisons").mkdir(parents=True, exist_ok=True)
    
    # Supported image formats
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    
    # Find all images in the dataset folder
    image_files = []
    if os.path.exists(dataset_folder):
        for file in os.listdir(dataset_folder):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files.append(os.path.join(dataset_folder, file))
    else:
        print(f"Warning: '{dataset_folder}' folder not found!")
        print("Please create the dataset folder first and add images.")
        print("Example: place your images inside the dataset/ folder.")
        return
    
    if len(image_files) == 0:
        print(f"Warning: No images found in the '{dataset_folder}' folder!")
        return
    
    print("Dataset processing started...")
    print(f"Folder: {dataset_folder}")
    print(f"Total {len(image_files)} images found\n")
    
    # Process each image
    for idx, image_path in enumerate(image_files, 1):
        image_name = os.path.basename(image_path)
        image_name_no_ext = os.path.splitext(image_name)[0]
        
        print(f"[{idx}/{len(image_files)}] Processing: {image_name}")
        
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                print(f"  Error: Image could not be loaded: {image_name}")
                continue
            
            # 1. Power-Law Transformation (gamma=0.5)
            enhanced_power_law = power_law_transformation(image, gamma=0.5)
            cv2.imwrite(
                f"{output_folder}/power_law/{image_name_no_ext}_power_law.jpg",
                enhanced_power_law
            )
            
            # 2. Histogram Equalization
            enhanced_clahe = clahe_enhancement(image)
            cv2.imwrite(
                f"{output_folder}/clahe/{image_name_no_ext}_clahe.jpg",
                enhanced_clahe
            )
            
            # 3. Thresholding Enhancement
            enhanced_threshold = thresholding_enhancement(image, threshold_type='adaptive', C=2)
            cv2.imwrite(
                f"{output_folder}/thresholding/{image_name_no_ext}_thresholding.jpg",
                enhanced_threshold
            )
            
            # Create comparison image (Original + 3 methods side by side)
            create_comparison_image(
                image,
                enhanced_power_law,
                enhanced_clahe,
                enhanced_threshold,
                image_name_no_ext,
                f"{output_folder}/comparisons/{image_name_no_ext}_comparison.png"
            )
            
            print(f"  Completed: {image_name}")
            
        except Exception as e:
            print(f"  Error: {image_name} - {str(e)}")
            continue
    
    print("\nProcessing completed!")
    print(f"Results: {output_folder}/")
    print(f"   ├── power_law/     ({len(image_files)} images)")
    print(f"   ├── clahe/         ({len(image_files)} images)")
    print(f"   ├── thresholding/  ({len(image_files)} images)")
    print(f"   └── comparisons/   ({len(image_files)} comparison images)")


def create_sample_structure():
    """
    Creates a sample dataset folder structure
    """
    folders = [
        "dataset",
        "results/dataset_results/power_law",
        "results/dataset_results/clahe",
        "results/dataset_results/thresholding",
        "results/dataset_results/comparisons"
    ]
    
    for folder in folders:
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    print("Folder structure created:")
    print("   dataset/  <- Place your images here")
    print("   results/dataset_results/   <- Results will be saved here")


# ============================================================================
# MAIN PROGRAM
# ============================================================================

if __name__ == "__main__":
    import sys
    
    # If the '--create' argument is provided, create the folder structure
    if len(sys.argv) > 1 and sys.argv[1] == "--create":
        create_sample_structure()
        print("\nNow add your images to the 'dataset/' folder")
        print("Then run the script again: python main.py")
    else:
        # Process the dataset
        process_dataset()
