#!/usr/bin/env python3
"""color_conv - Color space converter (RGB, HSL, HSV, HEX, CMYK)."""
import sys, math

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def rgb_to_hsl(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    l = (mx+mn)/2
    if mx == mn:
        return 0, 0, round(l*100, 1)
    d = mx - mn
    s = d/(2-mx-mn) if l > 0.5 else d/(mx+mn)
    if mx == r: h = (g-b)/d + (6 if g<b else 0)
    elif mx == g: h = (b-r)/d + 2
    else: h = (r-g)/d + 4
    return round(h*60, 1), round(s*100, 1), round(l*100, 1)

def hsl_to_rgb(h, s, l):
    s, l = s/100, l/100
    if s == 0:
        v = int(l*255)
        return v, v, v
    def hue2rgb(p, q, t):
        if t < 0: t += 1
        if t > 1: t -= 1
        if t < 1/6: return p + (q-p)*6*t
        if t < 1/2: return q
        if t < 2/3: return p + (q-p)*(2/3-t)*6
        return p
    q = l*(1+s) if l < 0.5 else l+s-l*s
    p = 2*l - q
    h /= 360
    return (int(hue2rgb(p,q,h+1/3)*255), int(hue2rgb(p,q,h)*255), int(hue2rgb(p,q,h-1/3)*255))

def rgb_to_hsv(r, g, b):
    r, g, b = r/255, g/255, b/255
    mx, mn = max(r,g,b), min(r,g,b)
    v = mx
    d = mx - mn
    s = 0 if mx == 0 else d/mx
    if mx == mn: h = 0
    elif mx == r: h = (g-b)/d + (6 if g<b else 0)
    elif mx == g: h = (b-r)/d + 2
    else: h = (r-g)/d + 4
    return round(h*60, 1), round(s*100, 1), round(v*100, 1)

def rgb_to_cmyk(r, g, b):
    if r == g == b == 0:
        return 0, 0, 0, 100
    c, m, y = 1-r/255, 1-g/255, 1-b/255
    k = min(c, m, y)
    return (round((c-k)/(1-k)*100,1), round((m-k)/(1-k)*100,1),
            round((y-k)/(1-k)*100,1), round(k*100,1))

def color_distance(c1, c2):
    return math.sqrt(sum((a-b)**2 for a,b in zip(c1, c2)))

def complement(r, g, b):
    return 255-r, 255-g, 255-b

def blend(c1, c2, t=0.5):
    return tuple(int(a + (b-a)*t) for a, b in zip(c1, c2))

def test():
    assert hex_to_rgb("#ff0000") == (255, 0, 0)
    assert rgb_to_hex(255, 0, 0) == "#ff0000"
    assert rgb_to_hsl(255, 0, 0) == (0, 100.0, 50.0)
    assert hsl_to_rgb(0, 100, 50) == (255, 0, 0)
    h, s, v = rgb_to_hsv(255, 0, 0)
    assert h == 0 and s == 100 and v == 100
    c, m, y, k = rgb_to_cmyk(255, 0, 0)
    assert c == 0 and k == 0
    assert complement(255, 0, 0) == (0, 255, 255)
    assert blend((0,0,0), (255,255,255), 0.5) == (127, 127, 127)
    assert color_distance((0,0,0), (255,255,255)) > 400
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    elif len(sys.argv) > 1:
        c = sys.argv[1]
        if c.startswith("#"):
            r,g,b = hex_to_rgb(c)
            print(f"RGB: ({r},{g},{b})")
            print(f"HSL: {rgb_to_hsl(r,g,b)}")
            print(f"HSV: {rgb_to_hsv(r,g,b)}")
            print(f"CMYK: {rgb_to_cmyk(r,g,b)}")
    else:
        print("Usage: color_conv.py #hexcolor | test")
