
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        float hash(float n) { return fract(sin(n)*43758.5453); }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            vec3 col = vec3(0.0);
            for(float i=0.0; i<200.0; i++) {
                float t = time * (0.3 + hash(i)*0.4);
                vec2 pos = vec2(sin(t + hash(i*13.0)*6.28), cos(t*0.7 + hash(i*17.0)*6.28)) * 0.6;
                float d = length(uv - pos);
                float size = 0.005 + 0.01 * hash(i*23.0);
                col += 0.4 * (0.5 + 0.5*cos(time + i + vec3(0,2,4))) * smoothstep(size, 0.0, d);
            }
            
            f_color = vec4(col, 1.0);
        }
    