# ImagePanelPlotter
## A GUI Tool for Creating Custom Image Panels from Microscopy Data 
ImagePanelPlotter is a Python-based graphical user interface (GUI) designed to streamline the process of generating image panels from .tiff files. This tool is particularly useful for microscopy data, where observing trends or generating representative figures can be time-consuming. The script allows users to apply false-color look-up tables (LUTs) from ImageJ, adjust contrast, and synchronize zooming with ease.

### Features
- Batch Processing: Load an entire directory of .tiff images.
- Custom Panel Creation: Select images for custom labeling, order, and arrangement in panels.
- False Coloring: Apply LUTs from ImageJ for enhanced visual interpretation.
- Min/Max Contrast Adjustments: Set individual contrast levels to highlight image details.
- Linked Zoom: Enable linked zooming across subplots to easily observe the same x, y region in each image.
- User-friendly GUI: Intuitive interface for easy navigation and usage.

### Installation
pip install -r requirements.txt

### Usage
python ImagePanelPlotter.py

### Example
Images obtained from: https://www.leica-microsystems.com/science-lab/life-science/multicolor-microscopy-the-importance-of-multiplexing/
