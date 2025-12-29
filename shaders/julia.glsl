
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
    