#!/usr/bin/env python3
"""Color space converter."""
import colorsys

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    return round(h*360, 1), round(s*100, 1), round(l*100, 1)

def hsl_to_rgb(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h/360, l/100, s/100)
    return round(r*255), round(g*255), round(b*255)

def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    return round(h*360, 1), round(s*100, 1), round(v*100, 1)

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0: return 0, 0, 0, 100
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c, m, y)
    return round((c-k)/(1-k)*100,1), round((m-k)/(1-k)*100,1), round((y-k)/(1-k)*100,1), round(k*100,1)

def complement(r, g, b):
    return 255-r, 255-g, 255-b

if __name__ == "__main__":
    import sys
    c = sys.argv[1] if len(sys.argv) > 1 else "#ff6600"
    rgb = hex_to_rgb(c)
    print(f"RGB: {rgb}\nHSL: {rgb_to_hsl(*rgb)}\nHSV: {rgb_to_hsv(*rgb)}\nCMYK: {rgb_to_cmyk(*rgb)}")

def test():
    assert hex_to_rgb("#ff0000") == (255, 0, 0)
    assert rgb_to_hex(255, 0, 0) == "#ff0000"
    assert rgb_to_hex(*hex_to_rgb("#abcdef")) == "#abcdef"
    h, s, l = rgb_to_hsl(255, 0, 0)
    assert abs(h) < 1 and abs(s - 100) < 1 and abs(l - 50) < 1
    r, g, b = hsl_to_rgb(0, 100, 50)
    assert r == 255 and g == 0 and b == 0
    assert rgb_to_cmyk(0, 0, 0) == (0, 0, 0, 100)
    assert rgb_to_cmyk(255, 255, 255) == (0, 0, 0, 0)
    assert complement(255, 0, 0) == (0, 255, 255)
    print("  color_conv: ALL TESTS PASSED")
