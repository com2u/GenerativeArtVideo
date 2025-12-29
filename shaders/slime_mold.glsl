
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

            // Initial state: R=Trail, G=Heading, B=AgentDensity
            if (time < 0.5) {
                float r = hash(uv);
                f_color = vec4(0.0, hash(uv + 1.23), r > 0.99 ? 1.0 : 0.0, 1.0);
                return;
            }

            // 1. Trail Map (R): Diffusion and Decay
            float trail = 0.0;
            for(int y=-1; y<=1; y++) {
                for(int x=-1; x<=1; x++) {
                    trail += texture(prev_frame, uv + vec2(x, y) * texel).r;
                }
            }
            trail /= 9.0;
            trail *= 0.97; // Slower decay for better persistence

            // 2. Agent Simulation: Read state from B (density) and G (heading)
            vec4 state = texture(prev_frame, uv);
            float heading = state.g * 6.2831;
            
            // Sensors look at the Trail Map (R)
            float sa = 0.6;  // Sensor angle
            float sd = 15.0; // Sensor distance
            
            float c = texture(prev_frame, uv + vec2(cos(heading), sin(heading)) * sd * texel).r;
            float l = texture(prev_frame, uv + vec2(cos(heading - sa), sin(heading - sa)) * sd * texel).r;
            float r = texture(prev_frame, uv + vec2(cos(heading + sa), sin(heading + sa)) * sd * texel).r;
            
            float next_heading = state.g;
            if (c > l && c > r) {
                // Stay on course
            } else if (c < l && c < r) {
                // Random jitter
                next_heading += (hash(uv + time) - 0.5) * 0.15;
            } else if (l > r) {
                next_heading -= 0.07;
            } else if (r > l) {
                next_heading += 0.07;
            }
            
            // 3. Movement: Pull agent density from previous position
            vec2 dir = vec2(cos(next_heading * 6.2831), sin(next_heading * 6.2831));
            float next_agent = texture(prev_frame, uv - dir * texel * 2.0).b;
            
            // Deposit agent density into the trail map
            float next_trail = clamp(trail + next_agent * 0.4, 0.0, 1.0);
            
            // Periodic re-seeding of agents to prevent extinction
            if (hash(uv - time * 0.2) > 0.9998) next_agent = 1.0;

            // Color mapping: Vibrant Bio-luminescent look
            vec3 col = mix(vec3(0.01, 0.0, 0.04), vec3(0.0, 0.6, 1.0), next_trail);
            col = mix(col, vec3(0.8, 1.0, 0.5), next_agent);
            
            // Store state: Trail in R, Heading in G, Agent in B
            f_color = vec4(next_trail, fract(next_heading), next_agent, 1.0);
            f_color.rgb = col;
        }
    