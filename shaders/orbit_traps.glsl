
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
    