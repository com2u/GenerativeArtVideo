
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
    