# Auto White Balance

This Python script performs automatic white balancing on an input image using the Von Kries model. It adjusts the color temperature of the image to match a specified target color temperature.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How it Works](#how-it-works)

## Requirements

- Python 3.x
- OpenCV
- NumPy
- Matplotlib
- Argparse

## Installation

1. Clone the repository or download the source code
2. Navigate to the project directory:
3. Install the required dependencies:

```bash
cd auto-white-balance
pip install -r requirements.txt
```

## Usage

Run the script with the following command:
```bash
# Color_Temperature only for A, B, C, D65, D93, E
python test.py -p /path/to/input/image.jpg -t Color_Temperature

# For example:
python test.py -p images/img_1.jpg -t D65
```

he script will process the input image and save the white-balanced output image as `out/WB_image.jpg`. Additionally, it will save a comparison image `output.jpg` showing the original and white-balanced images side by side.

## How it Works

The `to_A_color` function performs the white balancing operation using the Von Kries model. Here's a brief explanation of the steps involved:

1. The script first checks if the specified color temperature is valid. If not, it returns an error message.
2. If the input image is already pure white (all pixels have RGB values of 255, 255, 255), it converts the image to the XYZ color space and applies the Von Kries adjustment directly using the maximum XYZ values.
3. If the input image is not pure white, it converts the image to the XYZ color space, finds the top 5% of the brightest pixels (assumed to be white), and calculates the mean XYZ values of these pixels.
4. The Von Kries adjustment is then applied using the target color temperature XYZ values and the mean XYZ values of the brightest pixels.
5. The adjusted XYZ image is clipped to the valid range (0-255) and converted back to the BGR color space.
