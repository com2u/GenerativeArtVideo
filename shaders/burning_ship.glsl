
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
    