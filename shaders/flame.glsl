
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform sampler2D prev_frame;
        out vec4 f_color;
        in vec2 v_texcoord;

        float hash(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        float noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            float a = hash(i);
            float b = hash(i + vec2(1.0, 0.0));
            float c = hash(i + vec2(0.0, 1.0));
            float d = hash(i + vec2(1.0, 1.0));
            vec2 u = f * f * (3.0 - 2.0 * f);
            return mix(a, b, u.x) + (c - a) * u.y * (1.0 - u.x) + (d - b) * u.x * u.y;
        }

        float fbm(vec2 p) {
            float v = 0.0;
            float a = 0.5;
            for (int i = 0; i < 5; i++) {
                v += a * noise(p);
                p *= 2.0;
                a *= 0.5;
            }
            return v;
        }

        void main() {
            vec2 uv = v_texcoord;
            vec2 texel = 1.0 / resolution;

            // Advection with noise-based velocity
            // We want the flame to rise and swirl
            float n = fbm(uv * 2.0 + vec2(0.0, -time * 1.2));
            vec2 velocity = vec2(n - 0.5, 1.2 + n * 0.4) * 0.006;
            
            // Look back to get previous heat (stored in Alpha)
            vec2 back_uv = uv - velocity;
            float heat = texture(prev_frame, back_uv).a;

            // Diffusion (blur)
            float avg_heat = 0.0;
            avg_heat += texture(prev_frame, uv + vec2(texel.x, 0)).a;
            avg_heat += texture(prev_frame, uv - vec2(texel.x, 0)).a;
            avg_heat += texture(prev_frame, uv + vec2(0, texel.y)).a;
            avg_heat += texture(prev_frame, uv - vec2(0, texel.y)).a;
            avg_heat *= 0.25;
            
            heat = mix(heat, avg_heat, 0.15);

            // Cooling
            heat *= 0.96;
            heat -= 0.002 * (1.0 + uv.y); // Faster cooling as it rises

            // Heat source at the bottom
            if (uv.y < 0.1) {
                float source = fbm(uv * 8.0 + vec2(time * 1.5, 0.0));
                // Mask source to the center
                float mask = smoothstep(0.1, 0.3, uv.x) * smoothstep(0.9, 0.7, uv.x);
                source *= mask;
                if (source > 0.3) heat = max(heat, source);
            }
            
            // Random sparks/embers
            if (hash(uv + time) > 0.9996) {
                heat = 1.0;
            }

            heat = clamp(heat, 0.0, 1.0);

            // Color mapping (Black -> Deep Red -> Orange -> Yellow -> White)
            vec3 col = vec3(0.0);
            col = mix(col, vec3(0.7, 0.1, 0.0), smoothstep(0.1, 0.4, heat));
            col = mix(col, vec3(1.0, 0.4, 0.0), smoothstep(0.4, 0.7, heat));
            col = mix(col, vec3(1.0, 0.8, 0.3), smoothstep(0.7, 0.9, heat));
            col = mix(col, vec3(1.0, 1.0, 0.8), smoothstep(0.9, 0.98, heat));
            
            // Add a bit of blue at the very base for a "hot" look
            if (uv.y < 0.15) {
                col = mix(col, vec3(0.1, 0.2, 0.8), (1.0 - uv.y/0.15) * heat * 0.5);
            }

            f_color = vec4(col, heat);
        }
    