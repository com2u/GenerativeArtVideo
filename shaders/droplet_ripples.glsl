
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

            // We use Alpha for current height, and Red for previous height
            // (Red will be overwritten by the visual output, so we must ensure
            // the visual output's Red channel contains the height we need)
            // Actually, let's use Alpha for current height and Green for previous.
            // This is tricky because we want a nice visual output.
            
            // Better: use Alpha for current height, and store the previous height
            // in the Blue channel of the output.
            
            vec4 state = texture(prev_frame, uv);
            float h = state.a;
            float h_prev = state.b;

            // Wave equation
            float neighbors = 0.0;
            neighbors += texture(prev_frame, uv + vec2(texel.x, 0)).a;
            neighbors += texture(prev_frame, uv - vec2(texel.x, 0)).a;
            neighbors += texture(prev_frame, uv + vec2(0, texel.y)).a;
            neighbors += texture(prev_frame, uv - vec2(0, texel.y)).a;
            
            float next_h = (neighbors * 0.5 - h_prev);
            next_h *= 0.98; // Damping

            // Add droplets
            if (hash(vec2(time)) > 0.97) {
                vec2 drop_pos = vec2(hash(vec2(time, 3.0)), hash(vec2(time, 4.0)));
                if (length(uv - drop_pos) < 0.01) {
                    next_h = 1.0;
                }
            }
            
            // Visualization: use height for shading (fake lighting)
            float dx = next_h - texture(prev_frame, uv + vec2(texel.x, 0)).a;
            float dy = next_h - texture(prev_frame, uv + vec2(0, texel.y)).a;
            vec3 normal = normalize(vec3(dx, dy, 0.1));
            vec3 light = normalize(vec3(1.0, 1.0, 2.0));
            float diff = max(0.0, dot(normal, light));
            
            vec3 col = mix(vec3(0.0, 0.2, 0.5), vec3(0.5, 0.8, 1.0), diff);
            col += pow(diff, 20.0); // Specular

            // Store next_h in Alpha, and current h in Blue (for next frame's h_prev)
            f_color = vec4(col.rg, h, next_h);
        }
    