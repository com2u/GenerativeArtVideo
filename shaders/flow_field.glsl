
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        float noise(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            vec3 col = vec3(0.0);
            for(float i=0.0; i<5.0; i++) {
                float angle = noise(floor(uv * 10.0) + i) * 6.2831 + time * 0.2;
                vec2 dir = vec2(cos(angle), sin(angle));
                float d = abs(dot(fract(uv * 10.0) - 0.5, dir));
                col += 0.2 * vec3(0.5 + 0.5*sin(time + i), 0.5 + 0.5*cos(time + i), 1.0) * smoothstep(0.05, 0.0, d);
                uv += dir * 0.1;
            }
            
            f_color = vec4(col, 1.0);
        }
    