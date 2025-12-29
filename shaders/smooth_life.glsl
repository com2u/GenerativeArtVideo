
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform sampler2D prev_frame;
        out vec4 f_color;
        in vec2 v_texcoord;

        float hash(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        // Smooth step functions
        float sigma(float x, float a, float alpha) {
            return 1.0 / (1.0 + exp(-(x - a) * 4.0 / alpha));
        }

        float step_func(float x, float a, float b, float alpha) {
            return sigma(x, a, alpha) * (1.0 - sigma(x, b, alpha));
        }

        void main() {
            vec2 uv = v_texcoord;
            vec2 texel = 1.0 / resolution;

            if (time < 0.5) {
                float r = hash(uv);
                f_color = vec4(vec3(r > 0.9 ? 1.0 : 0.0), r > 0.9 ? 1.0 : 0.0);
                return;
            }

            // Larger kernel for SmoothLife
            float inner = 0.0;
            float outer = 0.0;
            float ri = 3.0;
            float ra = 9.0;
            
            for(float y=-ra; y<=ra; y++) {
                for(float x=-ra; x<=ra; x++) {
                    float d = length(vec2(x, y));
                    float val = texture(prev_frame, uv + vec2(x, y) * texel).a;
                    if (d <= ri) {
                        inner += val;
                    } else if (d <= ra) {
                        outer += val;
                    }
                }
            }
            
            inner /= (3.14159 * ri * ri);
            outer /= (3.14159 * (ra * ra - ri * ri));

            float current = texture(prev_frame, uv).a;
            
            // SmoothLife rules (simplified)
            // Birth: outer in [0.278, 0.365]
            // Survival: outer in [0.267, 0.445]
            float birth = step_func(outer, 0.278, 0.365, 0.02);
            float survival = step_func(outer, 0.267, 0.445, 0.02);
            
            float next = mix(birth, survival, sigma(inner, 0.5, 0.02));
            
            // Temporal smoothing
            next = mix(current, next, 0.1);

            // Coloring
            vec3 col = 0.5 + 0.5 * cos(time * 0.1 + next * 3.0 + vec3(0, 2, 4));
            col *= next;
            
            f_color = vec4(col, next);
        }
    