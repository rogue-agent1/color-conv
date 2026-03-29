import argparse, re, colorsys

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return round(h*360), round(s*100), round(l*100)

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return round(r*255), round(g*255), round(b*255)

def main():
    p = argparse.ArgumentParser(description="Color format converter")
    p.add_argument("color", help="#hex, rgb(r,g,b), or hsl(h,s,l)")
    args = p.parse_args()
    c = args.color.strip()
    if c.startswith("#"):
        r, g, b = hex_to_rgb(c)
        h, s, l = rgb_to_hsl(r, g, b)
        print(f"HEX: {c}\nRGB: rgb({r},{g},{b})\nHSL: hsl({h},{s}%,{l}%)")
    elif c.startswith("rgb"):
        nums = [int(x) for x in re.findall(r"\d+", c)]
        r, g, b = nums[:3]
        h, s, l = rgb_to_hsl(r, g, b)
        print(f"HEX: {rgb_to_hex(r,g,b)}\nRGB: rgb({r},{g},{b})\nHSL: hsl({h},{s}%,{l}%)")
    elif c.startswith("hsl"):
        nums = [int(x) for x in re.findall(r"\d+", c)]
        h, s, l = nums[:3]
        r, g, b = hsl_to_rgb(h, s, l)
        print(f"HEX: {rgb_to_hex(r,g,b)}\nRGB: rgb({r},{g},{b})\nHSL: hsl({h},{s}%,{l}%)")

if __name__ == "__main__":
    main()
