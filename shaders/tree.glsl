
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        float sdLine(vec2 p, vec2 a, vec2 b) {
            vec2 pa = p-a, ba = b-a;
            float h = clamp(dot(pa,ba)/dot(ba,ba), 0.0, 1.0);
            return length(pa - ba*h);
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            uv.y += 0.5;
            
            float d = 1e10;
            vec2 p = uv;
            
            vec2 a = vec2(0.0, 0.0);
            vec2 b = vec2(0.0, 0.3);
            d = min(d, sdLine(p, a, b));
            
            // Simple recursive-like branching using a loop
            for(int i=0; i<6; i++) {
                float t = time * 0.2 + float(i);
                p = abs(p - b) - 0.1;
                float angle = 0.5 + 0.2 * sin(t);
                mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
                p = rot * p;
                d = min(d, sdLine(p, vec2(0.0), vec2(0.0, 0.2)));
            }
            
            vec3 col = vec3(0.2, 0.1, 0.05) + vec3(0.1, 0.5, 0.1) * smoothstep(0.01, 0.0, d);
            f_color = vec4(col, 1.0);
        }
    