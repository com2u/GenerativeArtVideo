import os
from shaders import SHADERS

os.makedirs('shaders', exist_ok=True)

for name, code in SHADERS.items():
    filename = name.lower().replace(' ', '_').replace('/', '_') + '.glsl'
    with open(f'shaders/{filename}', 'w') as f:
        f.write(code)

print("Shaders extracted to shaders/ directory")