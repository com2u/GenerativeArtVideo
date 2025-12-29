
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
    