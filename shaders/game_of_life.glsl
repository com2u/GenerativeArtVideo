
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform sampler2D prev_frame;
        out vec4 f_color;
        in vec2 v_texcoord;

        float hash(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        void main() {
            vec2 uv = v_texcoord;
            vec2 texel = 1.0 / resolution;

            // Initial state or periodic re-seeding to prevent total darkness
            // Increased re-seeding probability and made it more localized
            if (time < 0.5 || hash(uv + floor(time*10.0)) > 0.999) {
                float r = hash(uv + time);
                if (r > 0.995) {
                    f_color = vec4(1.0, 1.0, 1.0, 1.0);
                    return;
                }
            }

            float neighbors = 0.0;
            for(int y=-1; y<=1; y++) {
                for(int x=-1; x<=1; x++) {
                    if(x == 0 && y == 0) continue;
                    // Use Alpha channel for state, which is more stable
                    neighbors += texture(prev_frame, uv + vec2(x, y) * texel).a;
                }
            }

            vec4 prev = texture(prev_frame, uv);
            float current = prev.a;
            
            // Smooth GoL rules using sigmoid-based step functions
            // Survival: [1.5, 3.5], Birth: [2.5, 3.5]
            float survival = 1.0 / (1.0 + exp(-(neighbors - 1.5) * 10.0)) * (1.0 - 1.0 / (1.0 + exp(-(neighbors - 3.5) * 10.0)));
            float birth = 1.0 / (1.0 + exp(-(neighbors - 2.5) * 10.0)) * (1.0 - 1.0 / (1.0 + exp(-(neighbors - 3.5) * 10.0)));
            
            float next = mix(birth, survival, current);
            
            // Temporal smoothing for a more fluid look
            next = mix(current, next, 0.2);

            // Smooth color transitions and persistence
            vec3 target_col = prev.rgb;
            if (next > 0.5) {
                if (current < 0.5) {
                    // New born: Bright Orange/Yellow/Pink
                    target_col = 0.5 + 0.5 * cos(time + uv.xyx + vec3(0, 2, 4));
                } else {
                    // Survivor: Shift color slightly
                    target_col = mix(prev.rgb, 0.5 + 0.5 * cos(time * 0.1 + uv.xyx), 0.02);
                }
            } else {
                // Dying: Fade out
                target_col *= 0.98;
            }

            // Add a bit of "glow" from neighbors
            if (neighbors > 0.1) {
                target_col += vec3(0.01, 0.02, 0.03) * neighbors / 8.0;
            }

            // Store state in Alpha for the next frame
            f_color = vec4(target_col, next);
        }
    