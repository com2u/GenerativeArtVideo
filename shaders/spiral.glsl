
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            float r = length(uv);
            float a = atan(uv.y, uv.x);
            
            float spiral = a + r * 5.0 - time;
            float d = sin(spiral * 10.0);
            
            vec3 col = 0.5 + 0.5*cos(time + r + vec3(0,2,4));
            col *= smoothstep(0.0, 0.1, abs(d));
            
            f_color = vec4(col, 1.0);
        }
    