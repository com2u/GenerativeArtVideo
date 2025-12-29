
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
    