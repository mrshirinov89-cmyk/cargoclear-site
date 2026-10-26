import base64, math, struct, zlib, sys
W, H = 1200, 630
dots_raw = base64.b64decode(open(sys.argv[1]).read().strip())
land = [(struct.unpack_from("<h", dots_raw, i)[0] / 10, struct.unpack_from("<h", dots_raw, i + 2)[0] / 10) for i in range(0, len(dots_raw) - 3, 4)]
DEG = math.pi / 180; TILT = 22 * DEG; ROT = -55
cx, cy, R = 830, 330, 255
def vec(lon, lat):
    a, b = lon * DEG, lat * DEG
    return (math.cos(b) * math.cos(a), math.cos(b) * math.sin(a), math.sin(b))
def project(v):
    a = -ROT * DEG
    x1 = v[0] * math.cos(a) + v[1] * math.sin(a); y1 = -v[0] * math.sin(a) + v[1] * math.cos(a); z1 = v[2]
    depth = x1 * math.cos(TILT) + z1 * math.sin(TILT); up = -x1 * math.sin(TILT) + z1 * math.cos(TILT)
    return cx + y1 * R, cy - up * R, depth
def slerp(a, b, f):
    d = math.acos(max(-1, min(1, sum(x * y for x, y in zip(a, b)))))
    s1, s2 = math.sin((1 - f) * d) / math.sin(d), math.sin(f * d) / math.sin(d)
    return tuple(x * s1 + y * s2 for x, y in zip(a, b))
img = bytearray(W * H * 3)
for y in range(H):
    for x in range(W):
        d = math.hypot((x - 900) / W, (y - 280) / H)
        t = min(1, d * 1.6)
        c = [round(a + (b - a) * t) for a, b in zip((15, 58, 74), (3, 11, 18))]
        dx, dy = x - cx, y - cy
        if dx * dx + dy * dy <= R * R:
            k = min(1, math.hypot(dx + R * .35, dy + R * .4) / (R * 1.3))
            c = [round(a + (b - a) * k) for a, b in zip((20, 64, 79), (6, 20, 29))]
        i = (y * W + x) * 3; img[i:i + 3] = bytes(c)
def plot(x, y, color, size=2, alpha=1.0):
    for yy in range(int(y), int(y) + size):
        for xx in range(int(x), int(x) + size):
            if 0 <= xx < W and 0 <= yy < H:
                i = (yy * W + xx) * 3
                img[i:i + 3] = bytes(round(o + (n - o) * alpha) for o, n in zip(img[i:i + 3], color))
import random; random.seed(7)
for _ in range(700):
    plot(random.random() * W, random.random() * H, (220, 240, 255), 1, random.random() * .7)
for lon, lat in land:
    px, py, z = project(vec(lon, lat))
    if z > 0.02: plot(px, py, (160, 230, 225), 3, .6)
moscow = vec(37.62, 55.75)
for lon, lat in [(116.4, 39.9), (121.5, 31.2), (72.9, 19.1), (55.3, 25.3), (51.4, 35.7), (28.98, 41.0), (31.2, 30.0), (-7.6, 33.6), (36.8, -1.3), (18.4, -33.9), (-3.7, 40.4), (105.8, 21.0), (69.2, 41.3), (-79.9, -2.2), (100.5, 13.8)]:
    a = vec(lon, lat)
    for k in range(0, 201):
        px, py, z = project(slerp(a, moscow, k / 200))
        if z > 0: plot(px, py, (94, 234, 212), 2, .55)
    px, py, z = project(a)
    if z > 0: plot(px - 3, py - 3, (153, 246, 228), 6, 1)
mx, my, mz = project(moscow)
for r in range(0, 9):
    for ang in range(0, 360, 4):
        plot(mx + r * math.cos(ang * DEG), my + r * math.sin(ang * DEG), (250, 204, 21), 2, 1)
# логотип и текст накладываются отдельно (brand/og.html) — здесь только фон с планетой
rows = b"".join(b"\x00" + bytes(img[y * W * 3:(y + 1) * W * 3]) for y in range(H))
def chunk(t, d): return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d))
open(sys.argv[2], "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b""))
print("ok")
