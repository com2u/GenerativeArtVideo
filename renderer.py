import moderngl
import numpy as np

class Renderer:
    def __init__(self, ctx):
        self.ctx = ctx
        self.fbo = self.ctx.screen
        self.feedback_textures = [
            self.ctx.texture((1024, 1024), 4, dtype='f4'),
            self.ctx.texture((1024, 1024), 4, dtype='f4')
        ]
        self.feedback_fbos = [
            self.ctx.framebuffer(color_attachments=[self.feedback_textures[0]]),
            self.ctx.framebuffer(color_attachments=[self.feedback_textures[1]])
        ]
        self.current_feedback = 0
        
        # Simple copy shader for feedback display
        self.copy_program = self.ctx.program(
            vertex_shader="""
                #version 330
                in vec2 in_vert;
                in vec2 in_texcoord;
                out vec2 v_texcoord;
                void main() {
                    gl_Position = vec4(in_vert, 0.0, 1.0);
                    v_texcoord = in_texcoord;
                }
            """,
            fragment_shader="""
                #version 330
                uniform sampler2D tex;
                in vec2 v_texcoord;
                out vec4 f_color;
                void main() {
                    f_color = vec4(texture(tex, v_texcoord).rgb, 1.0);
                }
            """
        )
        
        self.quad_buffer = self.ctx.buffer(np.array([
            # x, y, u, v
            -1.0,  1.0, 0.0, 1.0,
            -1.0, -1.0, 0.0, 0.0,
             1.0,  1.0, 1.0, 1.0,
             1.0, -1.0, 1.0, 0.0,
        ], dtype='f4'))
        
        self.vertex_shader = """
        #version 330
        in vec2 in_vert;
        in vec2 in_texcoord;
        out vec2 v_texcoord;
        void main() {
            gl_Position = vec4(in_vert, 0.0, 1.0);
            v_texcoord = in_texcoord;
        }
        """
        
        self.fragment_shader = """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform vec2 mouse;
        uniform float zoom;
        uniform vec2 offset;
        
        out vec4 f_color;
        in vec2 v_texcoord;

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            // Placeholder for generative art logic
            float d = length(uv);
            vec3 col = 0.5 + 0.5 * cos(time + uv.xyx + vec3(0, 2, 4));
            col *= exp(-d * 2.0);
            
            f_color = vec4(col, 1.0);
        }
        """
        self.program = None
        self.vao = None

    def render(self, time, resolution, zoom=1.0, offset=(0.0, 0.0), fbo=None, is_feedback=False):
        if not self.vao:
            return
        
        if is_feedback:
            # Ping-pong for feedback effects like Game of Life
            prev_idx = self.current_feedback
            curr_idx = 1 - prev_idx
            
            # Render to current FBO
            self.feedback_fbos[curr_idx].use()
            self.feedback_textures[prev_idx].use(0)
            
            if 'prev_frame' in self.program:
                self.program['prev_frame'].value = 0
            
            # For feedback shaders like Game of Life, the resolution should match the texture
            self._set_uniforms(time, (1024, 1024), zoom, offset)
            self.vao.render(moderngl.TRIANGLE_STRIP)
            
            # Now render the result to the screen using the copy shader
            target_fbo = fbo if fbo else self.fbo
            target_fbo.use()
            self.feedback_textures[curr_idx].use(0)
            
            # Create a temporary VAO for the copy operation if needed,
            # or just use the existing quad_buffer with the copy_program
            copy_vao = self.ctx.vertex_array(self.copy_program, [(self.quad_buffer, '2f 2f', 'in_vert', 'in_texcoord')])
            copy_vao.render(moderngl.TRIANGLE_STRIP)
            
            self.current_feedback = curr_idx
        else:
            # Normal single-pass rendering
            target_fbo = fbo if fbo else self.fbo
            target_fbo.use()
            self.ctx.clear(0.1, 0.2, 0.3)
            self._set_uniforms(time, resolution, zoom, offset)
            self.vao.render(moderngl.TRIANGLE_STRIP)

    def _set_uniforms(self, time, resolution, zoom, offset):
        if 'time' in self.program:
            self.program['time'].value = time
        if 'resolution' in self.program:
            self.program['resolution'].value = resolution
        if 'zoom' in self.program:
            self.program['zoom'].value = zoom
        if 'offset' in self.program:
            self.program['offset'].value = offset

    def update_shader(self, fragment_source):
        try:
            new_program = self.ctx.program(vertex_shader=self.vertex_shader, fragment_shader=fragment_source)
            self.program = new_program
            self.vao = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'in_vert', 'in_texcoord')])
            return True, "Shader updated"
        except Exception as e:
            return False, str(e)
