SHADERS = {
    "Default": """
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
            float d = length(uv);
            vec3 col = 0.5 + 0.5 * cos(time + uv.xyx + vec3(0, 2, 4));
            col *= exp(-d * 2.0);
            f_color = vec4(col, 1.0);
        }
    """,
    "Mandelbrot": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        vec3 palette(float t) {
            vec3 a = vec3(0.5, 0.5, 0.5);
            vec3 b = vec3(0.5, 0.5, 0.5);
            vec3 c = vec3(1.0, 1.0, 1.0);
            vec3 d = vec3(0.263, 0.416, 0.557);
            return a + b * cos(6.28318 * (c * t + d + time * 0.1));
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            
            // Automatic zoom and rotation
            float auto_zoom = zoom * (1.5 + sin(time * 0.2) * 0.5);
            float angle = time * 0.1;
            mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
            
            vec2 c = (rot * uv) * auto_zoom + offset;
            c += vec2(-0.745, 0.186); // Interesting spot
            
            vec2 z = vec2(0.0);
            float iter = 0.0;
            const float max_iter = 128.0;
            
            for(float i=0; i<max_iter; i++) {
                z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
                if(length(z) > 4.0) break;
                iter++;
            }
            
            if(iter == max_iter) {
                f_color = vec4(0.0, 0.0, 0.0, 1.0);
            } else {
                // Smooth coloring
                float dist = length(z);
                float fraction = log2(log(dist) / log(2.0));
                iter = iter + 1.0 - fraction;
                
                vec3 col = palette(iter / 32.0);
                f_color = vec4(col, 1.0);
            }
        }
    """,
    "Julia": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        vec3 palette(float t) {
            vec3 a = vec3(0.5, 0.5, 0.5);
            vec3 b = vec3(0.5, 0.5, 0.5);
            vec3 c = vec3(1.0, 1.0, 1.0);
            vec3 d = vec3(0.3, 0.2, 0.2);
            return a + b * cos(6.28318 * (c * t + d + time * 0.05));
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            
            float auto_zoom = zoom * (1.0 + 0.2 * sin(time * 0.3));
            vec2 z = uv * auto_zoom + offset;
            
            // Animated Julia constant
            vec2 c = vec2(0.355 + 0.1*sin(time*0.1), 0.355 + 0.1*cos(time*0.15));
            
            float iter = 0.0;
            const float max_iter = 150.0;
            for(float i=0; i<max_iter; i++) {
                z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
                if(length(z) > 4.0) break;
                iter++;
            }
            
            if(iter == max_iter) {
                f_color = vec4(0.0, 0.0, 0.0, 1.0);
            } else {
                float dist = length(z);
                float fraction = log2(log(dist) / log(2.0));
                iter = iter + 1.0 - fraction;
                vec3 col = palette(iter / 64.0);
                f_color = vec4(col, 1.0);
            }
        }
    """,
    "Noise": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;
        
        float hash(vec2 p) {
            p = fract(p * vec2(123.34, 456.21));
            p += dot(p, p + 45.32);
            return fract(p.x * p.y);
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            float n = hash(uv + time*0.1);
            vec3 col = vec3(n);
            f_color = vec4(col, 1.0);
        }
    """,
    "Kaleidoscope": """
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
            
            float r = length(uv);
            float a = atan(uv.y, uv.x);
            
            float sides = 6.0;
            float tau = 6.283185;
            a = mod(a, tau/sides);
            a = abs(a - tau/sides/2.0);
            
            uv = r * vec2(cos(a), sin(a));
            
            float d = sin(uv.x*10.0 + time) * sin(uv.y*10.0 + time);
            vec3 col = 0.5 + 0.5*cos(time + uv.xyx + vec3(0,2,4));
            col *= d;
            
            f_color = vec4(col, 1.0);
        }
    """,
    "Spiral": """
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
            
            float r = length(uv);
            float a = atan(uv.y, uv.x);
            
            float spiral = a + r * 5.0 - time;
            float d = sin(spiral * 10.0);
            
            vec3 col = 0.5 + 0.5*cos(time + r + vec3(0,2,4));
            col *= smoothstep(0.0, 0.1, abs(d));
            
            f_color = vec4(col, 1.0);
        }
    """,
    "Geometric": """
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
            
            vec2 g = abs(fract(uv * 10.0) - 0.5);
            float d = min(g.x, g.y);
            
            float mask = smoothstep(0.01, 0.02, d);
            vec3 col = 0.5 + 0.5*cos(time + uv.xyx + vec3(0,2,4));
            col *= (1.0 - mask);
            
            f_color = vec4(col, 1.0);
        }
    """,
    "Cosmic": """
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
    """,
    "Burning Ship": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            vec2 c = uv * zoom + offset;
            c += vec2(-1.75, -0.03);
            
            vec2 z = vec2(0.0);
            float iter = 0.0;
            const float max_iter = 100.0;
            
            for(float i=0; i<max_iter; i++) {
                z = vec2(abs(z.x), abs(z.y));
                z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
                if(length(z) > 4.0) break;
                iter++;
            }
            
            float f = iter / max_iter;
            vec3 col = vec3(f*f, f, pow(f, 0.5));
            f_color = vec4(col, 1.0);
        }
    """,
    "Tree": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        float sdLine(vec2 p, vec2 a, vec2 b) {
            vec2 pa = p-a, ba = b-a;
            float h = clamp(dot(pa,ba)/dot(ba,ba), 0.0, 1.0);
            return length(pa - ba*h);
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            uv.y += 0.5;
            
            float d = 1e10;
            vec2 p = uv;
            
            vec2 a = vec2(0.0, 0.0);
            vec2 b = vec2(0.0, 0.3);
            d = min(d, sdLine(p, a, b));
            
            // Simple recursive-like branching using a loop
            for(int i=0; i<6; i++) {
                float t = time * 0.2 + float(i);
                p = abs(p - b) - 0.1;
                float angle = 0.5 + 0.2 * sin(t);
                mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
                p = rot * p;
                d = min(d, sdLine(p, vec2(0.0), vec2(0.0, 0.2)));
            }
            
            vec3 col = vec3(0.2, 0.1, 0.05) + vec3(0.1, 0.5, 0.1) * smoothstep(0.01, 0.0, d);
            f_color = vec4(col, 1.0);
        }
    """,
    "Stacking": """
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
            
            vec2 gv = fract(uv * 5.0) - 0.5;
            vec2 id = floor(uv * 5.0);
            
            float m = 0.0;
            float t = time * 2.0;
            
            for(float y=-1.0; y<=1.0; y++) {
                for(float x=-1.0; x<=1.0; x++) {
                    vec2 offs = vec2(x, y);
                    float d = length(gv - offs);
                    float r = 0.3 + 0.2 * sin(t + (id.x+offs.x)*0.5 + (id.y+offs.y)*0.5);
                    m += smoothstep(r, r-0.02, d);
                }
            }
            
            vec3 col = 0.5 + 0.5 * cos(time + id.xyx + vec3(0,2,4));
            f_color = vec4(col * m, 1.0);
        }
    """,
    "Voronoi": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        vec2 hash2(vec2 p) {
            return fract(sin(vec2(dot(p,vec2(127.1,311.7)),dot(p,vec2(269.5,183.3))))*43758.5453);
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            // Increase density by scaling UV
            uv *= 30.0;
            
            vec2 n = floor(uv);
            vec2 f = fract(uv);
            
            float m_dist = 1.0;
            vec2 m_point;
            
            for(int j=-1; j<=1; j++) {
                for(int i=-1; i<=1; i++) {
                    vec2 g = vec2(float(i),float(j));
                    vec2 o = hash2(n + g);
                    o = 0.5 + 0.5*sin(time + 6.2831*o);
                    vec2 r = g + o - f;
                    float d = dot(r,r);
                    if(d < m_dist) {
                        m_dist = d;
                        m_point = o;
                    }
                }
            }
            
            vec3 col = 0.5 + 0.5*cos(time + m_point.xyx + vec3(0,2,4));
            col *= 1.0 - smoothstep(0.0, 0.1, m_dist);
            f_color = vec4(col, 1.0);
        }
    """,
    "Reaction Diffusion": """
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
    """,
    "Slime Mold": """
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
    """,
    "Cellular Automata 3D": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform sampler2D prev_frame;
        out vec4 f_color;
        in vec2 v_texcoord;

        // 3D Grid: 64x64x64 mapped to 512x512
        // Each 64x64 slice is a block in the 512x512 texture (8x8 blocks)
        
        vec3 get_3d_coord(vec2 uv) {
            vec2 grid_pos = uv * 512.0;
            vec2 block = floor(grid_pos / 64.0);
            vec2 local = mod(grid_pos, 64.0);
            float z = block.y * 8.0 + block.x;
            return vec3(local, z);
        }

        vec2 get_2d_coord(vec3 p) {
            p = clamp(p, 0.0, 63.0);
            float z = floor(p.z);
            vec2 block = vec2(mod(z, 8.0), floor(z / 8.0));
            return (block * 64.0 + p.xy) / 512.0;
        }

        float get_cell(vec3 p) {
            return texture(prev_frame, get_2d_coord(p)).r > 0.5 ? 1.0 : 0.0;
        }

        float hash(vec3 p) {
            return fract(sin(dot(p, vec3(12.9898, 78.233, 45.543))) * 43758.5453);
        }

        void main() {
            vec2 uv = v_texcoord;
            
            // Raymarching visualization of the 3D grid
            // We use the full screen for visualization, and the simulation happens in the background
            // or we can use a small portion for the simulation data.
            // Actually, the simulation data is stored in the texture.
            
            // Raymarching visualization
            vec3 ro = vec3(32.0, 32.0, -60.0);
            vec3 rd = normalize(vec3((uv - 0.5) * 2.0, 1.5));
            
            // Rotate camera
            float a = time * 0.3;
            mat2 rot = mat2(cos(a), -sin(a), sin(a), cos(a));
            ro.xz *= rot;
            rd.xz *= rot;
            ro += 32.0;

            float acc = 0.0;
            vec3 col = vec3(0.0);
            for(int i=0; i<100; i++) {
                vec3 p_ray = ro + rd * float(i) * 0.8;
                if(all(greaterThanEqual(p_ray, vec3(0.0))) && all(lessThan(p_ray, vec3(64.0)))) {
                    float val = get_cell(p_ray);
                    if (val > 0.5) {
                        acc += 0.05;
                        col += 0.5 + 0.5 * cos(time + p_ray * 0.1 + vec3(0, 2, 4));
                    }
                }
            }
            
            // Simulation logic (only for a small part of the texture to store state)
            // We'll use the bottom-left 512x512 area of the 1024x1024 texture for state
            if (uv.x < 0.5 && uv.y < 0.5) {
                vec3 p_sim = get_3d_coord(uv / 0.5);

                // Initial state or periodic re-seeding
                if (time < 0.5 || hash(p_sim + floor(time)) > 0.9999) {
                    float h = hash(p_sim + time);
                    f_color = vec4(vec3(h > 0.98 ? 1.0 : 0.0), 1.0);
                    return;
                }

                // 3D CA Rules (Life-like: 4-5/5)
                float neighbors = 0.0;
                for(int z=-1; z<=1; z++) {
                    for(int y=-1; y<=1; y++) {
                        for(int x=-1; x<=1; x++) {
                            if(x==0 && y==0 && z==0) continue;
                            neighbors += get_cell(p_sim + vec3(x, y, z));
                        }
                    }
                }

                float current = get_cell(p_sim);
                float next = 0.0;
                if(current > 0.5) {
                    if(neighbors >= 4.0 && neighbors <= 5.0) next = 1.0;
                } else {
                    if(neighbors == 5.0) next = 1.0;
                }
                
                // Persistence/Fade for visualization
                float visual = mix(texture(prev_frame, uv).g, next, 0.1);
                f_color = vec4(next, visual, 0.0, 1.0);
            } else {
                f_color = vec4(col * 0.1 + vec3(0.0, 0.0, 0.1), 1.0);
            }
        }
    """,
    "Flow Field": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        float noise(vec2 p) {
            return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            vec3 col = vec3(0.0);
            for(float i=0.0; i<5.0; i++) {
                float angle = noise(floor(uv * 10.0) + i) * 6.2831 + time * 0.2;
                vec2 dir = vec2(cos(angle), sin(angle));
                float d = abs(dot(fract(uv * 10.0) - 0.5, dir));
                col += 0.2 * vec3(0.5 + 0.5*sin(time + i), 0.5 + 0.5*cos(time + i), 1.0) * smoothstep(0.05, 0.0, d);
                uv += dir * 0.1;
            }
            
            f_color = vec4(col, 1.0);
        }
    """,
    "Particles": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        float hash(float n) { return fract(sin(n)*43758.5453); }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            vec3 col = vec3(0.0);
            for(float i=0.0; i<200.0; i++) {
                float t = time * (0.3 + hash(i)*0.4);
                vec2 pos = vec2(sin(t + hash(i*13.0)*6.28), cos(t*0.7 + hash(i*17.0)*6.28)) * 0.6;
                float d = length(uv - pos);
                float size = 0.005 + 0.01 * hash(i*23.0);
                col += 0.4 * (0.5 + 0.5*cos(time + i + vec3(0,2,4))) * smoothstep(size, 0.0, d);
            }
            
            f_color = vec4(col, 1.0);
        }
    """,
    "Game of Life": """
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
    """,
    "Smooth Life": """
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
    """,
    "Flame": """
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
    """,
    "Orbit Traps": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            vec2 c = uv * zoom + offset;
            vec2 z = vec2(0.0);
            
            float trap = 1e10;
            for(int i=0; i<64; i++) {
                z = vec2(z.x*z.x - z.y*z.y, 2.0*z.x*z.y) + c;
                
                // Orbit trap: distance to a moving point
                vec2 p = vec2(sin(time*0.5), cos(time*0.3)) * 0.5;
                trap = min(trap, length(z - p));
                
                if(length(z) > 4.0) break;
            }
            
            vec3 col = 0.5 + 0.5 * cos(log(trap) * 3.0 + time + vec3(0,2,4));
            f_color = vec4(col, 1.0);
        }
    """,
    "IFS Morphing": """
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
            
            float t = time * 0.2;
            vec3 col = vec3(0.0);
            
            for(int i=0; i<8; i++) {
                uv = abs(uv) - 0.5;
                float angle = t + float(i) * 0.5;
                mat2 rot = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
                uv = rot * uv;
                uv *= 1.1 + 0.1 * sin(t * 0.5);
                
                float d = length(uv);
                col += 0.1 * (0.5 + 0.5*cos(d * 10.0 + time + vec3(0,2,4)));
            }
            
            f_color = vec4(col, 1.0);
        }
    """,
    "Curl Noise Flow": """
        #version 330
        uniform float time;
        uniform vec2 resolution;
        uniform float zoom;
        uniform vec2 offset;
        out vec4 f_color;
        in vec2 v_texcoord;

        vec3 hash3(vec2 p) {
            vec3 q = vec3( dot(p,vec2(127.1,311.7)),
                           dot(p,vec2(269.5,183.3)),
                           dot(p,vec2(419.2,371.9)) );
            return fract(sin(q)*43758.5453);
        }

        float noise(vec2 p) {
            vec2 i = floor(p);
            vec2 f = fract(p);
            vec2 u = f*f*(3.0-2.0*f);
            return mix( mix( dot( hash3(i+vec2(0,0)).xy-0.5, f-vec2(0,0) ),
                             dot( hash3(i+vec2(1,0)).xy-0.5, f-vec2(1,0) ), u.x),
                        mix( dot( hash3(i+vec2(0,1)).xy-0.5, f-vec2(0,1) ),
                             dot( hash3(i+vec2(1,1)).xy-0.5, f-vec2(1,1) ), u.x), u.y);
        }

        vec2 curl(vec2 p) {
            float eps = 0.1;
            float n1 = noise(p + vec2(0, eps));
            float n2 = noise(p - vec2(0, eps));
            float n3 = noise(p + vec2(eps, 0));
            float n4 = noise(p - vec2(eps, 0));
            return vec2(n1 - n2, n4 - n3) / (2.0 * eps);
        }

        void main() {
            vec2 uv = (v_texcoord - 0.5) * resolution / min(resolution.y, resolution.x);
            uv = uv * zoom + offset;
            
            vec2 p = uv;
            vec3 col = vec3(0.0);
            
            // Define influence points (Attractors/Repellers)
            vec2 attractors[4];
            float charges[4];
            for(int j=0; j<4; j++) {
                float t = time * 0.3 + float(j) * 1.5;
                attractors[j] = vec2(sin(t * 1.1), cos(t * 0.8)) * 0.6;
                charges[j] = (j % 2 == 0) ? 1.0 : -1.2; // Alternating attract/repel
            }
            
            for(int i=0; i<25; i++) {
                vec2 v = curl(p * 1.5 + time * 0.05);
                
                // Particle interaction: Attract/Repel from moving centers
                for(int j=0; j<4; j++) {
                    vec2 diff = attractors[j] - p;
                    float d2 = dot(diff, diff) + 0.2;
                    v += charges[j] * diff / d2 * 0.15;
                }
                
                p += v * 0.04;
                float d = length(uv - p);
                
                // Color variety based on iteration and time
                vec3 p_col = 0.5 + 0.5*cos(time * 0.5 + float(i) * 0.2 + vec3(0, 2, 4));
                if (i % 3 == 1) p_col = p_col.gbr;
                if (i % 3 == 2) p_col = p_col.brg;
                
                col += 0.012 * p_col / (d + 0.18);
            }
            
            // Add a subtle vignette
            col *= 1.0 - dot(uv, uv) * 0.2;
            
            f_color = vec4(col, 1.0);
        }
    """,
    "Magnetic Fields": """
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
            
            vec3 col = vec3(0.0);
            const int num_sources = 5;
            vec2 sources[num_sources];
            float charges[num_sources];
            
            for(int i=0; i<num_sources; i++) {
                float t = time * (0.3 + float(i)*0.1);
                sources[i] = vec2(sin(t), cos(t*0.7)) * 0.6;
                charges[i] = sin(time + float(i));
            }
            
            vec2 field = vec2(0.0);
            for(int i=0; i<num_sources; i++) {
                vec2 diff = uv - sources[i];
                float d = length(diff);
                field += charges[i] * diff / (d * d * d + 0.01);
            }
            
            float strength = length(field);
            float pattern = sin(strength * 0.5 - time * 2.0);
            
            col = 0.5 + 0.5 * cos(strength * 0.1 + time + vec3(0,2,4));
            col *= smoothstep(0.0, 0.1, abs(pattern));
            
            f_color = vec4(col, 1.0);
        }
    """,
    "GPU Fire": """
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
    """,
    "Smoke / Ink": """
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
    """,
    "Droplet Ripples": """
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
    """,
    "Flow Field Simulation": """
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
    """
}
