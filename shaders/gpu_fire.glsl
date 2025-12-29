
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

        void main() {
            vec2 uv = v_texcoord;
            vec2 texel = 1.0 / resolution;

            // Advection: look up where the "heat" came from
            // Use noise to create a turbulent upward flow
            float n = noise(uv * 5.0 + vec2(0.0, -time * 2.0));
            vec2 velocity = vec2(n - 0.5, 1.0 + n * 0.5) * 0.005;
            
            vec2 back_uv = uv - velocity;
            float heat = texture(prev_frame, back_uv).a; // Read heat from Alpha

            // Temperature decay
            heat *= 0.96;

            // Heat source at the bottom
            if (uv.y < 0.05) {
                float source = hash(uv + time);
                if (source > 0.8) heat = 1.0;
            }

            // Color mapping (Black -> Red -> Orange -> Yellow -> White)
            vec3 col = vec3(0.0);
            col = mix(col, vec3(1.0, 0.1, 0.0), smoothstep(0.1, 0.4, heat));
            col = mix(col, vec3(1.0, 0.6, 0.0), smoothstep(0.4, 0.7, heat));
            col = mix(col, vec3(1.0, 1.0, 0.8), smoothstep(0.7, 0.95, heat));

            f_color = vec4(col, heat); // Store heat in Alpha
        }
    