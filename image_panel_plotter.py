import sys
import numpy as np
import os
import tifffile as tiff
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from scipy.interpolate import interp1d
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, 
                             QListWidget, QPushButton, QSpinBox, QLabel, 
                             QComboBox, QFileDialog, QListWidgetItem, 
                             QMessageBox, QLineEdit, QScrollArea, QFormLayout, 
                             QCheckBox)
from PyQt5.QtCore import Qt

class ImagePanelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Panel Plotter")

        # Initialize variables
        self.image_directory = ""
        self.selected_files = []
        self.checked_files = []
        self.custom_labels = []
        self.order_indices = []
        self.lut_indices = []
        self.min_values = []
        self.max_values = []
        self.LUTs = self.load_luts()  # Load LUTs from a directory
        self.font_size = 6  # Set the font size for the labels
        self.rows = 2  # Default rows
        self.columns = 2  # Default columns
        self.link_plots = False  # Initialize Link Plots to False

        # Initialize UI components
        self.init_ui()

    def init_ui(self):
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # Button to load images at the top
        load_button = QPushButton("Load TIFF Images")
        load_button.clicked.connect(self.load_images)
        layout.addWidget(load_button)

        # Add UI elements for file selection
        self.selected_list = QListWidget()
        self.selected_list.itemChanged.connect(self.update_custom_labels)
        layout.addWidget(self.selected_list)

        # Custom label input section (scrollable area)
        self.custom_label_area = QScrollArea()
        self.custom_label_area.setWidgetResizable(True)
        self.custom_label_widget = QWidget()
        self.custom_label_layout = QFormLayout(self.custom_label_widget)
        self.custom_label_area.setWidget(self.custom_label_widget)
        layout.addWidget(QLabel("Enter Custom Labels:"))
        layout.addWidget(self.custom_label_area)

        # Set Order input section (scrollable area)
        self.order_area = QScrollArea()
        self.order_area.setWidgetResizable(True)
        self.order_widget = QWidget()
        self.order_layout = QFormLayout(self.order_widget)
        self.order_area.setWidget(self.order_widget)
        layout.addWidget(QLabel("Plot Order:"))
        layout.addWidget(self.order_area)

        # Set LUT input section (scrollable area)
        self.lut_area = QScrollArea()
        self.lut_area.setWidgetResizable(True)
        self.lut_widget = QWidget()
        self.lut_layout = QFormLayout(self.lut_widget)
        self.lut_area.setWidget(self.lut_widget)
        layout.addWidget(QLabel("Select False Color:"))
        layout.addWidget(self.lut_area)

        # Set Min/Max input section (scrollable area)
        self.minmax_area = QScrollArea()
        self.minmax_area.setWidgetResizable(True)
        self.minmax_widget = QWidget()
        self.minmax_layout = QFormLayout(self.minmax_widget)
        self.minmax_area.setWidget(self.minmax_widget)
        layout.addWidget(QLabel("Set Min/Max Values:"))
        layout.addWidget(self.minmax_area)

        # Add spin boxes for rows and columns
        self.row_spin = QSpinBox()
        self.row_spin.setRange(1, 10)
        self.row_spin.setValue(self.rows)
        layout.addWidget(QLabel("Rows:"))
        layout.addWidget(self.row_spin)

        self.column_spin = QSpinBox()
        self.column_spin.setRange(1, 10)
        self.column_spin.setValue(self.columns)
        layout.addWidget(QLabel("Columns:"))
        layout.addWidget(self.column_spin)

        # Link Plots checkbox
        self.link_plots_checkbox = QCheckBox("Link Plots")
        self.link_plots_checkbox.stateChanged.connect(self.toggle_link_plots)
        layout.addWidget(self.link_plots_checkbox)

        # Update and Plot button at the bottom
        update_button = QPushButton("Update Selections and Plot")
        update_button.clicked.connect(self.update_plot)
        layout.addWidget(update_button)

    def load_images(self):
        """Open a file dialog to load TIFF images."""
        options = QFileDialog.Options()
        self.image_directory = QFileDialog.getExistingDirectory(self, "Select Image Directory")
        if self.image_directory:
            self.selected_files = [os.path.join(self.image_directory, f) for f in os.listdir(self.image_directory) if f.endswith(('.tif', '.tiff'))]
            self.update_selected_list()

    def update_selected_list(self):
        """Update the display list of selected images."""
        self.selected_list.clear()
        self.custom_labels.clear()
        self.order_indices.clear()
        self.lut_indices.clear()
        self.min_values.clear()
        self.max_values.clear()

        for file in self.selected_files:
            item = QListWidgetItem(file)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.selected_list.addItem(item)

        self.clear_custom_label_inputs()

    def clear_custom_label_inputs(self):
        """Clear all custom label and order input fields."""
        for i in reversed(range(self.custom_label_layout.count())):
            self.custom_label_layout.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.order_layout.count())):
            self.order_layout.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.lut_layout.count())):
            self.lut_layout.itemAt(i).widget().deleteLater()
        for i in reversed(range(self.minmax_layout.count())):
            self.minmax_layout.itemAt(i).widget().deleteLater()

    def update_custom_labels(self):
        """Update custom labels, order, LUT selections based on currently selected images."""
        self.clear_custom_label_inputs()
        self.custom_labels = []
        self.order_indices = []
        self.lut_indices = []
        self.min_values = []
        self.max_values = []

        self.checked_files = [self.selected_files[i] for i in range(self.selected_list.count()) if self.selected_list.item(i).checkState() == Qt.Checked]

        for file in self.checked_files:
            filename = os.path.basename(file)
            label_edit = QLineEdit()
            label_edit.setPlaceholderText("Custom Labels")
            order_spin = QSpinBox()
            order_spin.setRange(1, len(self.checked_files))
            order_spin.setValue(len(self.custom_labels) + 1)

            lut_combo = QComboBox()
            lut_combo.addItems(list(self.LUTs.keys()))
            lut_combo.setCurrentIndex(0)

            min_spin = QSpinBox()
            min_spin.setRange(0, 65535)
            min_spin.setValue(0)

            max_spin = QSpinBox()
            max_spin.setRange(0, 65535)
            max_spin.setValue(65535)

            self.custom_label_layout.addRow(f"{filename}:", label_edit)
            self.order_layout.addRow(f"{filename}:", order_spin)
            self.lut_layout.addRow(f"{filename}:", lut_combo)
            self.minmax_layout.addRow(f"Min Value for {filename}:", min_spin)
            self.minmax_layout.addRow(f"Max Value for {filename}:", max_spin)

            self.custom_labels.append(label_edit)
            self.order_indices.append(order_spin)
            self.lut_indices.append(lut_combo)
            self.min_values.append(min_spin)
            self.max_values.append(max_spin)

    def load_luts(self):
        """Load LUTs from a specified directory."""
        lut_directory = os.path.join(os.path.dirname(__file__), 'LUTS')
        lut_files = {}
        for f in os.listdir(lut_directory):
            if f.endswith(('.tif', '.tiff')):
                lut_image = tiff.imread(os.path.join(lut_directory, f))
                lut_files[f] = self._custom_colormap(lut_image)
        return lut_files

    def _custom_colormap(self, img):
        """Converts an RGB tiff image to a custom colormap."""
        rows, cols, _ = img.shape
        parts = 255
        part_size = cols // parts
        color_values = np.zeros((parts, 3))
        for i in range(parts):
            start_x = i * part_size
            end_x = (i + 1) * part_size
            x = (start_x + end_x) // 2
            y = rows // 2
            color_values[i, :] = img[y, x, :]

        color_values = color_values / 255.0
        cmap = np.flipud(color_values)
        x = np.linspace(0, 1, cmap.shape[0])
        f = interp1d(x, cmap, kind='cubic', axis=0)
        cmap = f(np.linspace(0, 1, 255))
        cmap = cmap[::-1]
        cmap_rgb = ListedColormap(cmap)
        return cmap_rgb

    def toggle_link_plots(self, state):
        """Toggle the linking of plots based on the checkbox state."""
        self.link_plots = (state == Qt.Checked)

    def connect_zoom(self, fig, axs):
        """Connect zoom functionality to the matplotlib figure."""
        def on_zoom(event):
            if self.link_plots:
                # Sync zoom across all axes if linked
                for ax in axs:
                    if event.inaxes == ax:
                        current_xlim = ax.get_xlim()
                        current_ylim = ax.get_ylim()
                        xdata, ydata = event.xdata, event.ydata
                        zoom_factor = 1.1 if event.button == 'down' else 0.9
                        new_xlim = [xdata - (xdata - x) * zoom_factor for x in current_xlim]
                        new_ylim = [ydata - (ydata - y) * zoom_factor for y in current_ylim]

                        for a in axs:
                            a.set_xlim(new_xlim)
                            a.set_ylim(new_ylim)
                        plt.draw()
                        break
            else:
                # Individual zoom for each axis
                for ax in axs:
                    if event.inaxes == ax:
                        current_xlim = ax.get_xlim()
                        current_ylim = ax.get_ylim()
                        xdata, ydata = event.xdata, event.ydata
                        zoom_factor = 1.1 if event.button == 'down' else 0.9
                        new_xlim = [xdata - (xdata - x) * zoom_factor for x in current_xlim]
                        new_ylim = [ydata - (ydata - y) * zoom_factor for y in current_ylim]
                        ax.set_xlim(new_xlim)
                        ax.set_ylim(new_ylim)
                        plt.draw()

        fig.canvas.mpl_connect('scroll_event', on_zoom)

    def update_plot(self):
        """Update the plot based on selected images and settings."""
        images = []
        titles = []

        for index, file in enumerate(self.checked_files):
            img = tiff.imread(file)

            custom_label = self.custom_labels[index].text()
            lut_index = self.lut_indices[index].currentText()
            min_value = self.min_values[index].value()
            max_value = self.max_values[index].value()

            img = np.clip((img - min_value) / (max_value - min_value), 0, 1)

            colormap = self.LUTs[lut_index] if lut_index in self.LUTs else None
            if colormap is not None:
                img_colored = colormap(img)
            else:
                img_colored = img

            images.append(img_colored)
            titles.append(custom_label)

        fig, axs = plt.subplots(self.row_spin.value(), self.column_spin.value(), figsize=(10, 5))
        axs = axs.flatten() if self.row_spin.value() * self.column_spin.value() > 1 else [axs]

        for i, (img, title) in enumerate(zip(images, titles)):
            if i >= len(axs):
                break

            axs[i].imshow(img, vmin=0, vmax=1)
            axs[i].text(0.05, 0.95, title, fontsize=self.font_size, color='white', ha='left', va='top', transform=axs[i].transAxes)
            axs[i].axis('off')

        self.connect_zoom(fig, axs)  # Connect zoom functionality after plotting

        plt.tight_layout()
        plt.show()

# Run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImagePanelApp()
    window.show()
    sys.exit(app.exec_())
