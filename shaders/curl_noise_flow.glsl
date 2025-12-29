
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
    