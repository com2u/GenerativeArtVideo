
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
            
            vec3 finalColor = vec3(0.0);
            
            for (float i = 0.0; i < 4.0; i++) {
                uv = fract(uv * 1.5) - 0.5;

                float d = length(uv) * exp(-length(uv));

                vec3 col = 0.5 + 0.5 * cos(time + uv.xyx * 2.0 + vec3(0,2,4));

                d = sin(d * 8.0 + time) / 8.0;
                d = abs(d);

                d = pow(0.01 / d, 1.2);

                finalColor += col * d;
            }
                
            f_color = vec4(finalColor, 1.0);
        }
    