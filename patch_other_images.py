import re

with open('src/components/ClientShop.tsx', 'r') as f:
    content = f.read()

def replace_img(old_line, wrapper_class_extra=""):
    match = re.search(r'<img\s+src=\{([^}]+)\}\s+alt=\{([^}]+)\}\s+className="([^"]+)"', old_line)
    if not match:
        match = re.search(r'<img\s+src="([^"]+)"\s+alt="([^"]+)"\s+className="([^"]+)"', old_line)
        if match:
            src = f'"{match.group(1)}"'
            alt = f'"{match.group(2)}"'
        else:
            return old_line
    else:
        src = match.group(1)
        alt = match.group(2)
        
    cls = match.group(3)
    
    return f'<ImageWithSkeleton src={{{src}}} alt={{{alt}}} className="{cls} transition-opacity" wrapperClassName="{wrapper_class_extra}" />'

lines = content.split('\\n')
new_lines = []
for i, line in enumerate(lines):
    if '<img' in line and 'src=' in line and 'ImageWithSkeleton' not in line:
        # Check if it has an aspect ratio or width/height in its class
        wrapper = ""
        if "w-full" in line and "h-auto" in line:
            wrapper = "w-full aspect-[4/3] rounded-3xl" # approximate
        elif "w-20" in line and "h-20" in line:
            wrapper = "w-20 h-20 rounded-xl shrink-0"
        elif "w-10" in line and "h-10" in line:
            wrapper = "w-10 h-10 rounded-lg shrink-0"
        elif "w-16" in line and "h-16" in line:
            wrapper = "w-16 h-16 rounded-xl shrink-0"
        elif "w-full" in line and "h-48" in line:
            wrapper = "w-full h-48 rounded-xl"
        elif "w-full" in line and "h-32" in line:
            wrapper = "w-full h-32"
        elif "w-[120px]" in line:
            wrapper = "w-[120px] aspect-square"
            
        if "w-" in line or "aspect" in line:
            # Let ImageWithSkeleton handle it by passing appropriate wrapper classes
            # Wait, replacing using python might be brittle if there are multi-line tags.
            pass
            
with open('src/components/ClientShop.tsx', 'w') as f:
    f.write(content)
