
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

            // Initial state
            if (time < 0.5) {
                f_color = vec4(0.0, 0.0, 0.0, 1.0);
                return;
            }

            // Simple fluid-like motion using curl of noise for velocity
            // and density advection.
            
            // Read density from Alpha channel
            float density = texture(prev_frame, uv).a;
            float buoyancy = density * 0.002;
            
            // Vorticity-like effect: look at neighbors to create swirls
            float n1 = texture(prev_frame, uv + vec2(texel.x, 0)).a;
            float n2 = texture(prev_frame, uv - vec2(texel.x, 0)).a;
            float n3 = texture(prev_frame, uv + vec2(0, texel.y)).a;
            float n4 = texture(prev_frame, uv - vec2(0, texel.y)).a;
            
            vec2 curl = vec2(n3 - n4, n2 - n1) * 0.01;
            vec2 velocity = vec2(0.0, buoyancy) + curl;
            
            // Advection
            float next_density = texture(prev_frame, uv - velocity).a;
            
            // Diffusion & Decay
            next_density = mix(next_density, (n1+n2+n3+n4)*0.25, 0.1);
            next_density *= 0.99;

            // Source
            if (length(uv - vec2(0.5, 0.1)) < 0.02) {
                next_density = 1.0;
            }
            // Random ink drops
            if (hash(vec2(time)) > 0.98) {
                if (length(uv - vec2(hash(vec2(time, 1.0)), hash(vec2(time, 2.0)))) < 0.03) {
                    next_density = 1.0;
                }
            }

            vec3 col = mix(vec3(1.0), vec3(0.1, 0.2, 0.4), next_density);
            if (next_density < 0.01) col = vec3(0.95, 0.95, 1.0); // Water color

            f_color = vec4(col, next_density);
        }
    