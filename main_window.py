import sys
import time
import cv2
from PySide6 import QtCore, QtWidgets, QtGui
from gl_widget import GLWidget
from shaders import SHADERS


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generative Art Studio")
        self.resize(1200, 800)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QHBoxLayout(central_widget)

        # Left side: Preview
        self.gl_widget = GLWidget()
        layout.addWidget(self.gl_widget, stretch=3)

        # Right side: Controls
        controls_panel = QtWidgets.QWidget()
        controls_layout = QtWidgets.QVBoxLayout(controls_panel)
        layout.addWidget(controls_panel, stretch=1)

        # Zoom Control
        controls_layout.addWidget(QtWidgets.QLabel("Zoom"))
        self.zoom_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.zoom_slider.setRange(1, 1000)
        self.zoom_slider.setValue(100)
        self.zoom_slider.valueChanged.connect(self.update_params)
        controls_layout.addWidget(self.zoom_slider)

        # Offset X
        controls_layout.addWidget(QtWidgets.QLabel("Offset X"))
        self.offset_x_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.offset_x_slider.setRange(-100, 100)
        self.offset_x_slider.setValue(0)
        self.offset_x_slider.valueChanged.connect(self.update_params)
        controls_layout.addWidget(self.offset_x_slider)

        # Offset Y
        controls_layout.addWidget(QtWidgets.QLabel("Offset Y"))
        self.offset_y_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.offset_y_slider.setRange(-100, 100)
        self.offset_y_slider.setValue(0)
        self.offset_y_slider.valueChanged.connect(self.update_params)
        controls_layout.addWidget(self.offset_y_slider)

        # Shader Selection
        controls_layout.addWidget(QtWidgets.QLabel("Shader Type"))
        self.shader_combo = QtWidgets.QComboBox()
        self.shader_combo.addItems(["Default", "Mandelbrot", "Julia", "Burning Ship", "Orbit Traps", "IFS Morphing", "Tree", "Stacking", "Voronoi", "Reaction Diffusion", "Slime Mold", "Cellular Automata 3D", "Flow Field", "Flow Field Simulation", "Curl Noise Flow", "Magnetic Fields", "Particles", "Game of Life", "Smooth Life", "Flame", "GPU Fire", "Smoke / Ink", "Droplet Ripples", "Noise", "Kaleidoscope", "Spiral", "Geometric", "Cosmic"])
        self.shader_combo.currentIndexChanged.connect(self.change_shader)
        controls_layout.addWidget(self.shader_combo)

        # Recording
        self.record_btn = QtWidgets.QPushButton("Start Recording")
        self.record_btn.clicked.connect(self.toggle_recording)
        controls_layout.addWidget(self.record_btn)

        self.save_btn = QtWidgets.QPushButton("Save Video")
        self.save_btn.clicked.connect(self.save_video)
        self.save_btn.setEnabled(False)
        controls_layout.addWidget(self.save_btn)

        # Auto Animate
        self.animate_cb = QtWidgets.QCheckBox("Auto Animate")
        self.animate_cb.stateChanged.connect(self.toggle_animation)
        controls_layout.addWidget(self.animate_cb)

        controls_layout.addStretch()

    def toggle_animation(self, state):
        # state is 0 for Unchecked, 2 for Checked
        self.gl_widget.auto_animate = (state != 0)

    def update_params(self):
        self.gl_widget.zoom = self.zoom_slider.value() / 100.0
        self.gl_widget.offset_x = self.offset_x_slider.value() / 50.0
        self.gl_widget.offset_y = self.offset_y_slider.value() / 50.0

    def change_shader(self):
        shader_type = self.shader_combo.currentText()
        self.gl_widget.current_shader_name = shader_type
        if shader_type in ["Game of Life", "Smooth Life", "Flame", "Reaction Diffusion", "Slime Mold", "Cellular Automata 3D", "GPU Fire", "Smoke / Ink", "Droplet Ripples", "Flow Field Simulation"]:
            self.gl_widget.start_time = time.time()
        if shader_type in SHADERS and self.gl_widget.renderer:
            success, msg = self.gl_widget.renderer.update_shader(SHADERS[shader_type])
            if not success:
                QtWidgets.QMessageBox.critical(self, "Shader Error", msg)

    def toggle_recording(self):
        if not self.gl_widget.is_recording:
            self.gl_widget.is_recording = True
            self.gl_widget.frames = []
            self.record_btn.setText("Stop Recording")
            self.save_btn.setEnabled(False)
            print("Recording started...")
        else:
            self.gl_widget.is_recording = False
            self.record_btn.setText("Start Recording")
            self.save_btn.setEnabled(True)
            print(f"Recording stopped. Captured {len(self.gl_widget.frames)} frames.")

    def save_video(self):
        print(f"Attempting to save video with {len(self.gl_widget.frames)} frames")
        if not self.gl_widget.frames:
            QtWidgets.QMessageBox.warning(self, "No Frames", "No frames captured to save.")
            return

        try:
            path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save Video", "output.mp4", "Video Files (*.mp4)")
            print(f"Selected path: {path}")
            if path:
                height, width, _ = self.gl_widget.frames[0].shape
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(path, fourcc, 60.0, (width, height))
                if not out.isOpened():
                    raise Exception("Could not open VideoWriter. Check if the path is writable.")

                for frame in self.gl_widget.frames:
                    out.write(frame)
                out.release()
                QtWidgets.QMessageBox.information(self, "Success", f"Video saved to {path}")
                print(f"Video saved successfully to {path}")
        except Exception as e:
            print(f"Error saving video: {e}")
            QtWidgets.QMessageBox.critical(self, "Save Error", f"Failed to save video: {str(e)}")