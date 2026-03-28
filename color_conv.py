#!/usr/bin/env python3
"""color_conv - Convert between hex, RGB, and HSL color formats."""
import sys, colorsys

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b): return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return round(h*360), round(s*100), round(l*100)

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return round(r*255), round(g*255), round(b*255)

if __name__ == "__main__":
    if len(sys.argv) < 3: print("Usage: color_conv <hex|rgb|hsl> <value>"); sys.exit(1)
    fmt = sys.argv[1]
    if fmt == "hex":
        r, g, b = hex_to_rgb(sys.argv[2])
        h, s, l = rgb_to_hsl(r, g, b)
        print(f"RGB: ({r}, {g}, {b})  HSL: ({h}°, {s}%, {l}%)")
    elif fmt == "rgb":
        parts = [int(x) for x in sys.argv[2].split(",")]
        print(f"Hex: {rgb_to_hex(*parts)}  HSL: {rgb_to_hsl(*parts)}")
    elif fmt == "hsl":
        parts = [int(x) for x in sys.argv[2].split(",")]
        r, g, b = hsl_to_rgb(*parts)
        print(f"Hex: {rgb_to_hex(r, g, b)}  RGB: ({r}, {g}, {b})")
