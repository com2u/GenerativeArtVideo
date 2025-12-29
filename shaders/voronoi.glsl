
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
    