
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform sampler2D prev_frame;
        out vec4 f_color;
        in vec2 v_texcoord;

        float hash(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        float noise(vec3 p) {
            vec3 i = floor(p);
            vec3 f = fract(p);
            f = f * f * (3.0 - 2.0 * f);
            
            float n = i.x + i.y * 157.0 + 113.0 * i.z;
            
            return mix(mix(mix(hash(vec2(n + 0.0, 0.0)), hash(vec2(n + 1.0, 0.0)), f.x),
                           mix(hash(vec2(n + 157.0, 0.0)), hash(vec2(n + 158.0, 0.0)), f.x), f.y),
                       mix(mix(hash(vec2(n + 113.0, 0.0)), hash(vec2(n + 114.0, 0.0)), f.x),
                           mix(hash(vec2(n + 270.0, 0.0)), hash(vec2(n + 271.0, 0.0)), f.x), f.y), f.z);
        }

        void main() {
            vec2 uv = v_texcoord;
            vec2 texel = 1.0 / resolution;

            if (time < 0.5) {
                f_color = vec4(0.0, 0.0, 0.0, 1.0);
                return;
            }

            // We use the texture to store particle density/trails
            // and also to simulate the flow field.
            
            // 1. Decay and Diffusion of trails
            float trail = 0.0;
            for(int y=-1; y<=1; y++) {
                for(int x=-1; x<=1; x++) {
                    trail += texture(prev_frame, uv + vec2(x, y) * texel).a;
                }
            }
            trail /= 9.0;
            trail *= 0.98; // Decay

            // 2. Particle Simulation (Simplified as a density flow)
            // Instead of individual particles, we move density along the flow field
            float angle = noise(vec3(uv * 5.0, time * 0.05)) * 6.2831 * 4.0;
            vec2 dir = vec2(cos(angle), sin(angle));
            
            // Advection: look up where the density came from
            float advected = texture(prev_frame, uv - dir * texel * 3.0).a;
            
            // 3. Add new "particles" (random density spikes)
            float spawn = 0.0;
            if (hash(uv + time) > 0.999) {
                spawn = 1.0;
            }

            float final_density = max(trail, mix(advected, spawn, 0.2));
            
            // Coloring based on density and flow direction
            vec3 col = 0.5 + 0.5 * cos(angle + time + vec3(0, 2, 4));
            col *= final_density;
            
            // Add a background glow
            col += vec3(0.02, 0.01, 0.05);

            f_color = vec4(col, final_density);
        }
    