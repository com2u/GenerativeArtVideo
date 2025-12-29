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
        self.timer.start(16)  # ~60 FPS

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