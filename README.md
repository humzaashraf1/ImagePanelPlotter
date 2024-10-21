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
<img src="https://github.com/user-attachments/assets/d478542a-4e18-42e0-a37a-e9f71c41c923" alt="GUI" width="200"/>
<img src="https://github.com/user-attachments/assets/cdf14b68-bdc5-448c-8f66-2323dcc6e45c" alt="GUI" width="400"/>
Images obtained from: https://www.leica-microsystems.com/science-lab/life-science/multicolor-microscopy-the-importance-of-multiplexing/
