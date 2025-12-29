
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
            
            vec2 g = abs(fract(uv * 10.0) - 0.5);
            float d = min(g.x, g.y);
            
            float mask = smoothstep(0.01, 0.02, d);
            vec3 col = 0.5 + 0.5*cos(time + uv.xyx + vec3(0,2,4));
            col *= (1.0 - mask);
            
            f_color = vec4(col, 1.0);
        }
    