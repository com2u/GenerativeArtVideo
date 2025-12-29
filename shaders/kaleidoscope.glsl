
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
            
            float sides = 6.0;
            float tau = 6.283185;
            a = mod(a, tau/sides);
            a = abs(a - tau/sides/2.0);
            
            uv = r * vec2(cos(a), sin(a));
            
            float d = sin(uv.x*10.0 + time) * sin(uv.y*10.0 + time);
            vec3 col = 0.5 + 0.5*cos(time + uv.xyx + vec3(0,2,4));
            col *= d;
            
            f_color = vec4(col, 1.0);
        }
    