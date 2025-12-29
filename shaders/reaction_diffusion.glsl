
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

            // Initial state: Seed with multiple spots and noise
            if (time < 0.5) {
                float seed = 0.0;
                for(int i=0; i<15; i++) {
                    vec2 pos = vec2(hash(vec2(float(i), 1.23)), hash(vec2(float(i), 4.56)));
                    seed += smoothstep(0.04, 0.01, length(uv - pos));
                }
                if (hash(uv * 13.0 + 7.89) > 0.98) seed = 1.0;
                // Store state in B and A (U=1.0, V=seed)
                f_color = vec4(0.0, 0.0, 1.0, clamp(seed, 0.0, 1.0));
                return;
            }

            // Gray-Scott Parameters
            float Du = 0.209;
            float Dv = 0.105;
            
            // Vary parameters across the screen to show multiple pattern types
            // F: Feed rate, k: Kill rate
            float F = mix(0.015, 0.055, uv.x);
            float k = mix(0.045, 0.068, uv.y);

            vec2 center = texture(prev_frame, uv).ba;
            
            // Laplacian using 3x3 kernel
            vec2 laplacian = vec2(0.0);
            laplacian += texture(prev_frame, uv + vec2(-texel.x, 0.0)).ba * 0.2;
            laplacian += texture(prev_frame, uv + vec2(texel.x, 0.0)).ba * 0.2;
            laplacian += texture(prev_frame, uv + vec2(0.0, -texel.y)).ba * 0.2;
            laplacian += texture(prev_frame, uv + vec2(0.0, texel.y)).ba * 0.2;
            laplacian += texture(prev_frame, uv + vec2(-texel.x, -texel.y)).ba * 0.05;
            laplacian += texture(prev_frame, uv + vec2(texel.x, -texel.y)).ba * 0.05;
            laplacian += texture(prev_frame, uv + vec2(-texel.x, texel.y)).ba * 0.05;
            laplacian += texture(prev_frame, uv + vec2(texel.x, texel.y)).ba * 0.05;
            laplacian -= center;

            float u = center.r;
            float v = center.g;
            float uvv = u * v * v;

            float du = Du * laplacian.r - uvv + F * (1.0 - u);
            float dv = Dv * laplacian.g + uvv - (F + k) * v;

            float next_u = clamp(u + du, 0.0, 1.0);
            float next_v = clamp(v + dv, 0.0, 1.0);

            // Color mapping: More vibrant and "impressive"
            float val = clamp(next_u - next_v, 0.0, 1.0);
            vec3 col1 = vec3(0.05, 0.02, 0.1); // Deep background
            vec3 col2 = 0.5 + 0.5 * cos(time * 0.2 + val * 3.0 + vec3(0, 2, 4)); // Shifting pattern color
            vec3 col3 = vec3(1.0, 1.0, 0.9); // Bright highlights
            
            vec3 final_col = mix(col1, col2, smoothstep(0.1, 0.4, val));
            final_col = mix(final_col, col3, smoothstep(0.4, 0.8, next_v));
            
            f_color = vec4(next_u, next_v, val, 1.0);
            // We store the simulation state in RG, but the visual output can be RGB
            // Wait, the renderer uses the whole RGBA for the next frame.
            // If I overwrite RGB with final_col, I might lose the simulation state.
            // Actually, the simulation state is in next_u and next_v.
            // I should store them in R and G, and I can use B and A for whatever.
            // But the visual output is what's copied to the screen.
            
            // Let's store state in R and G, and visual in RGB?
            // No, the renderer copies .rgb to the screen.
            // So if I want the user to see final_col, I must put it in .rgb.
            // But then the next frame will read final_col.rg as the state!
            // This will break the simulation.
            
            // Solution: Store state in R and G, and use a different channel for visual?
            // Or just make the visual mapping reversible? (Hard)
            // Or use the Alpha channel for one of the states?
            
            // Let's look at how other feedback shaders do it.
            // Game of Life uses Alpha for state.
            // Smooth Life uses Alpha for state.
            // Flame uses Alpha for heat.
            
            // I'll use R and G for state, and I'll have to be careful.
            // Wait, if I want to show a color, I can't easily store R and G separately.
            
            // Actually, I can store state in B and A!
            f_color = vec4(final_col, 1.0);
            f_color.b = next_u;
            f_color.a = next_v;
        }
    