
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
            
            float t = time * 0.2;
            vec3 col = vec3(0.0);
            
            for(int i=0; i<8; i++) {
                uv = abs(uv) - 0.5;
                float angle = t + float(i) * 0.5;
                mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
                uv = rot * uv;
                uv *= 1.1 + 0.1 * sin(t * 0.5);
                
                float d = length(uv);
                col += 0.1 * (0.5 + 0.5*cos(d * 10.0 + time + vec3(0,2,4)));
            }
            
            f_color = vec4(col, 1.0);
        }
    