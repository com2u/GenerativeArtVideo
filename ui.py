import sys
import time
import numpy as np
import cv2
from PySide6 import QtCore, QtWidgets, QtOpenGLWidgets, QtGui
import moderngl
from renderer import Renderer
from shaders import SHADERS

class GLWidget(QtOpenGLWidgets.QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.renderer = None
        self.current_shader_name = "Default"
        self.start_time = time.time()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(16) # ~60 FPS

        self.zoom = 1.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.is_recording = False
        self.auto_animate = False
        self.frames = []

    def initializeGL(self):
        print("Initializing GL...")
        try:
            # Ensure the context is current before creating ModernGL context
            self.makeCurrent()
            self.ctx = moderngl.create_context()
            # Detect the framebuffer created by PySide
            self.fbo = self.ctx.detect_framebuffer()

            print(f"Context created: {self.ctx.info}")
            print(f"Vendor: {self.ctx.info['GL_VENDOR']}")
            print(f"Renderer: {self.ctx.info['GL_RENDERER']}")
            print(f"FBO detected: {self.fbo}")

            self.renderer = Renderer(self.ctx)
            # Set initial shader
            success, msg = self.renderer.update_shader(SHADERS["Default"])
            if not success:
                print(f"Initial shader error: {msg}")
            else:
                print("Initial shader loaded successfully")
        except Exception as e:
            print(f"Failed to initialize GL: {e}")
            import traceback
            traceback.print_exc()

    def paintGL(self):
        if self.renderer:
            try:
                # Detect the current framebuffer for this paint call
                fbo = self.ctx.detect_framebuffer()

                current_time = time.time() - self.start_time

                # Apply auto-animation if enabled
                render_zoom = self.zoom
                render_offset = (self.offset_x, self.offset_y)

                if self.auto_animate:
                    render_zoom *= (1.0 + 0.5 * np.sin(current_time * 0.5))
                    render_offset = (
                        self.offset_x + 0.2 * np.cos(current_time * 0.3),
                        self.offset_y + 0.2 * np.sin(current_time * 0.4)
                    )

                # Use physical pixels for resolution
                ratio = self.devicePixelRatio()
                w, h = int(self.width() * ratio), int(self.height() * ratio)
                res = (w, h)

                # Update viewport to match physical pixels
                self.ctx.viewport = (0, 0, w, h)

                # Check if current shader needs feedback
                is_feedback = self.current_shader_name in ["Game of Life", "Smooth Life", "Flame", "Reaction Diffusion", "Slime Mold", "Cellular Automata 3D", "GPU Fire", "Smoke / Ink", "Droplet Ripples", "Flow Field Simulation"]

                self.renderer.render(current_time, res, zoom=render_zoom, offset=render_offset, fbo=fbo, is_feedback=is_feedback)

                # Check for GL errors
                err = self.ctx.error
                if err != 'no_error':
                    # Only print if it's not no_error
                    pass
            except Exception as e:
                print(f"Render error: {e}")

            if self.is_recording:
                # Read pixels for recording from the current framebuffer
                data = fbo.read(components=3)
                # Ensure we have enough data before reshaping
                if len(data) == w * h * 3:
                    image = np.frombuffer(data, dtype='u1').reshape(h, w, 3)
                    image = np.flipud(image)
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    self.frames.append(image)
                    if len(self.frames) % 60 == 0:
                        print(f"Captured {len(self.frames)} frames...")

    def resizeGL(self, w, h):
        self.ctx.viewport = (0, 0, w, h)

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