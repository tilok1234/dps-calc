"""
King of the Lost Crypt — 64x64 boss sprite.
Oryx-inspired (slightly more detailed). 3/4 top-down view.

Layered draw order (back to front):
  1. Cape
  2. High collar
  3. Pauldrons (with mini skull motifs)
  4. Skeletal arms / torso peek
  5. Robe front + gold trim
  6. Scepter (vertical staff with glowing orb)
  7. Skull head
  8. Crown
"""

from PIL import Image

W = H = 64

# ---------- Palette ----------
T  = (0, 0, 0, 0)          # transparent
OL = (10, 5, 16, 255)      # outline (near black, purple-tint)
SH = (28, 16, 42, 255)     # generic shadow

# Bone
B1 = (88, 78, 62, 255)
B2 = (172, 162, 132, 255)
B3 = (236, 228, 204, 255)

# Royal purple
P1 = (38, 14, 58, 255)
P2 = (76, 30, 116, 255)
P3 = (132, 72, 188, 255)
P4 = (184, 124, 228, 255)

# Gold
G1 = (108, 76, 18, 255)
G2 = (194, 152, 42, 255)
G3 = (248, 218, 102, 255)

# Red gem
R1 = (90, 10, 24, 255)
R2 = (208, 36, 52, 255)
R3 = (252, 108, 116, 255)

# Cyan glow
C1 = (10, 80, 130, 255)
C2 = (44, 204, 248, 255)
C3 = (208, 252, 255, 255)

img = Image.new('RGBA', (W, H), T)
px = img.load()


def s(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        px[x, y] = c


def hl(x0, x1, y, c):
    for x in range(x0, x1 + 1):
        s(x, y, c)


def vl(x, y0, y1, c):
    for y in range(y0, y1 + 1):
        s(x, y, c)


def rect(x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            s(x, y, c)


# ============================================================
# CAPE — trapezoid, behind everything
# ============================================================
def draw_cape():
    top_y, bot_y = 28, 61
    for y in range(top_y, bot_y + 1):
        t = (y - top_y) / (bot_y - top_y)
        half = int(13 + t * 17)
        L = 32 - half
        R = 31 + half
        for x in range(L, R + 1):
            d = abs(x - 31.5) / max(half, 1)
            if d > 0.88:
                s(x, y, P1)
            elif d > 0.55:
                s(x, y, P2)
            else:
                # body shadow stripe down center under torso
                if 38 < y < 56 and d < 0.22:
                    s(x, y, P1)
                else:
                    s(x, y, P3)
        s(L - 1, y, OL)
        s(R + 1, y, OL)
    # top edge of cape
    hl(20, 43, top_y - 1, OL)
    # bottom edge
    bot_half = int(13 + 17)
    hl(32 - bot_half - 1, 31 + bot_half + 1, bot_y + 1, OL)

    # Gold trim along cape bottom
    for y_t, c in [(60, G2), (59, G3), (58, G1)]:
        t = (y_t - 28) / 33.0
        half = int(13 + t * 17)
        for x in range(32 - half, 32 + half):
            s(x, y_t, c)
    # Decorative scallops
    for x in range(32 - bot_half, 32 + bot_half, 6):
        s(x, 57, G2)
        s(x + 1, 57, G3)
        s(x + 2, 57, G2)


draw_cape()


# ============================================================
# HIGH COLLAR — purple, wraps behind/around skull
# ============================================================
def draw_collar():
    for y in range(26, 36):
        for x in range(17, 48):
            # Skull oval mask — skip where head goes
            sx, sy, srx, sry = 32, 23, 11, 10
            nx = (x - sx) / srx
            ny = (y - sy) / sry
            if nx * nx + ny * ny < 1.0:
                continue
            # Don't extend past collar shape
            shape_top = 28
            shape_bot = 35
            # Triangular flare to shoulders
            half_at_y = int(11 + (y - 26) * 1.6)
            if abs(x - 32) > half_at_y:
                continue
            d = abs(x - 32) / max(half_at_y, 1)
            if y < shape_top:
                if d > 0.85:
                    s(x, y, P1)
                else:
                    s(x, y, P2)
            else:
                if d > 0.85:
                    s(x, y, P1)
                elif d > 0.5:
                    s(x, y, P2)
                else:
                    s(x, y, P3)
    # Outline collar top (where it peeks above shoulders)
    hl(20, 43, 25, OL)


draw_collar()


# ============================================================
# PAULDRONS — gold ovals with mini-skull motifs
# ============================================================
def draw_pauldron(cx, cy, rx, ry):
    for y in range(cy - ry - 1, cy + ry + 2):
        for x in range(cx - rx - 1, cx + rx + 2):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            d = nx * nx + ny * ny
            if d <= 1.0:
                # Highlight on top-outer
                if ny < -0.4 or (abs(nx) > 0.5 and ny < -0.1):
                    s(x, y, G3)
                elif d > 0.65:
                    s(x, y, G1)
                else:
                    s(x, y, G2)
            elif d <= 1.25:
                s(x, y, OL)


draw_pauldron(15, 36, 8, 6)
draw_pauldron(48, 36, 8, 6)


def mini_skull(cx, cy):
    # 6x5 stylized skull
    rows = [
        " ### ",
        "#####",
        "#o#o#",
        " #v# ",
        " ### ",
    ]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            x = cx + i - 2
            y = cy + j - 2
            if ch == '#':
                s(x, y, B3)
            elif ch == 'o':
                s(x, y, OL)
            elif ch == 'v':
                s(x, y, OL)


mini_skull(15, 37)
mini_skull(48, 37)


# ============================================================
# SKELETAL ARMS — humerus + forearm, hands meet at center
# ============================================================
def draw_arm(side):
    """side = -1 (left) or +1 (right)"""
    # Upper arm: vertical-ish, just below shoulder
    if side == -1:
        # left arm
        for y in range(40, 47):
            x = 22
            s(x - 1, y, OL)
            s(x, y, B2)
            s(x + 1, y, B3)
            s(x + 2, y, B2)
            s(x + 3, y, OL)
        # Forearm angles inward
        for i, y in enumerate(range(46, 51)):
            base_x = 22 + i
            s(base_x - 1, y, OL)
            s(base_x, y, B2)
            s(base_x + 1, y, B3)
            s(base_x + 2, y, B2)
            s(base_x + 3, y, OL)
        # Hand grasping scepter
        for y in range(49, 53):
            for x in range(27, 31):
                d = abs(x - 28) + abs(y - 51)
                if d <= 3:
                    s(x, y, B2 if (x + y) % 2 else B3)
        # Outline hand
        s(26, 50, OL); s(26, 51, OL); s(26, 52, OL)
        s(27, 49, OL); s(28, 49, OL)
        s(31, 50, OL); s(31, 51, OL)
        s(28, 53, OL); s(29, 53, OL)
    else:
        for y in range(40, 47):
            x = 38
            s(x - 1, y, OL)
            s(x, y, B2)
            s(x + 1, y, B3)
            s(x + 2, y, B2)
            s(x + 3, y, OL)
        for i, y in enumerate(range(46, 51)):
            base_x = 38 - i
            s(base_x - 1, y, OL)
            s(base_x, y, B2)
            s(base_x + 1, y, B3)
            s(base_x + 2, y, B2)
            s(base_x + 3, y, OL)
        for y in range(49, 53):
            for x in range(33, 37):
                d = abs(x - 35) + abs(y - 51)
                if d <= 3:
                    s(x, y, B2 if (x + y) % 2 else B3)
        s(37, 50, OL); s(37, 51, OL); s(37, 52, OL)
        s(35, 49, OL); s(36, 49, OL)
        s(32, 50, OL); s(32, 51, OL)
        s(34, 53, OL); s(35, 53, OL)


draw_arm(-1)
draw_arm(+1)


# ============================================================
# ROBE FRONT — purple, in front of cape, between arms
# ============================================================
def draw_robe_front():
    top_y, bot_y = 36, 61
    for y in range(top_y, bot_y + 1):
        t = (y - top_y) / (bot_y - top_y)
        half = int(7 + t * 7)
        L = 32 - half
        R = 31 + half
        for x in range(L, R + 1):
            # Don't overwrite arms
            if px[x, y][3] != 0 and px[x, y] in (B2, B3, OL):
                continue
            d = abs(x - 31.5) / max(half, 1)
            if d > 0.88:
                s(x, y, P1)
            elif d > 0.5:
                s(x, y, P3)
            else:
                s(x, y, P4)
        # outline
        if px[L - 1, y][3] == 0 or px[L - 1, y] in (P1, P2, P3):
            s(L - 1, y, OL)
        if px[R + 1, y][3] == 0 or px[R + 1, y] in (P1, P2, P3):
            s(R + 1, y, OL)
    # Gold band near hem
    for y_b, c in [(56, G1), (57, G2), (58, G3), (59, G2), (60, G1)]:
        t = (y_b - 36) / 25.0
        half = int(7 + t * 7)
        for x in range(32 - half, 32 + half):
            # Don't overwrite outlines
            if px[x, y_b] != OL:
                s(x, y_b, c)
    # vertical gold seam down center
    for y in range(38, 56):
        if px[31, y] in (P3, P4):
            s(31, y, G2)
        if px[32, y] in (P3, P4):
            s(32, y, G1)


draw_robe_front()


# ============================================================
# SCEPTER — vertical staff, glowing cyan orb at top
# Held between hands at row ~50-51
# ============================================================
def draw_scepter():
    # Staff goes from above hands up to ~row 18 (just below crown)
    for y in range(20, 51):
        # Don't overwrite head
        if px[31, y][3] != 0 and px[31, y] not in (P1, P2, P3, P4):
            # head/cape pixels — only overwrite if cape
            if px[31, y] in (B1, B2, B3, OL):
                continue
        s(30, y, OL)
        s(31, y, G1)
        s(32, y, G2)
        s(33, y, OL)

    # Decorative bands on staff
    for y_b in [25, 35, 45]:
        s(30, y_b, OL); s(31, y_b, G3); s(32, y_b, G3); s(33, y_b, OL)

    # Orb at top, centered around (31.5, 16)
    for y in range(11, 21):
        for x in range(26, 38):
            dx = x - 31.5
            dy = y - 15.5
            d2 = dx * dx + dy * dy
            if d2 <= 16:
                # Highlight upper-left
                if dx < -0.5 and dy < -0.5 and d2 < 6:
                    s(x, y, C3)
                elif d2 < 6:
                    s(x, y, C2)
                elif d2 < 12:
                    s(x, y, C2)
                else:
                    s(x, y, C1)
            elif d2 <= 22:
                s(x, y, OL)
    # bright sparkle
    s(29, 13, C3)
    s(28, 14, C3)


draw_scepter()


# ============================================================
# SKULL HEAD
# ============================================================
def draw_skull():
    sx, sy, srx, sry = 32, 23, 11, 10
    for y in range(sy - sry - 1, sy + sry + 2):
        for x in range(sx - srx - 1, sx + srx + 2):
            nx = (x - sx) / srx
            ny = (y - sy) / sry
            d = nx * nx + ny * ny
            if d <= 1.0:
                # Top-lit
                if ny < -0.5:
                    s(x, y, B3)
                elif ny < 0.1:
                    s(x, y, B2)
                else:
                    s(x, y, B1)
            elif d <= 1.18:
                s(x, y, OL)

    # Eye sockets — dark hollow with cyan glow
    def eye(cx, cy):
        for y in range(cy - 2, cy + 3):
            for x in range(cx - 3, cx + 4):
                dx = (x - cx) / 3
                dy = (y - cy) / 2.2
                if dx * dx + dy * dy <= 1.0:
                    s(x, y, OL)
        # Cyan inner glow
        s(cx, cy, C3)
        s(cx - 1, cy, C2); s(cx + 1, cy, C2)
        s(cx, cy - 1, C2); s(cx, cy + 1, C1)
        s(cx - 1, cy + 1, C1); s(cx + 1, cy + 1, C1)

    eye(27, 22)
    eye(37, 22)

    # Brow ridge shadow above eyes
    hl(24, 30, 19, B1)
    hl(34, 40, 19, B1)

    # Nose hole
    s(31, 26, OL); s(32, 26, OL)
    s(30, 27, OL); s(31, 27, OL); s(32, 27, OL); s(33, 27, OL)
    s(31, 28, OL); s(32, 28, OL)

    # Cheekbone shading
    s(23, 25, B1); s(24, 26, B1); s(25, 27, B1)
    s(41, 25, B1); s(40, 26, B1); s(39, 27, B1)

    # Teeth row
    for x in range(26, 39):
        s(x, 30, OL)
    for x in [26, 28, 30, 32, 34, 36, 38]:
        s(x, 31, OL)
    # Jaw bottom
    hl(27, 37, 32, B1)


draw_skull()


# ============================================================
# CROWN — 5 spires + jeweled band
# ============================================================
def draw_crown():
    # Crown band (rests on skull at row 12-15)
    for y in range(12, 16):
        for x in range(20, 44):
            if y == 12:
                s(x, y, G3)
            elif y == 13:
                s(x, y, G2)
            elif y == 14:
                s(x, y, G2)
            else:
                s(x, y, G1)
    hl(20, 43, 11, OL)
    hl(20, 43, 16, OL)
    vl(19, 12, 15, OL)
    vl(44, 12, 15, OL)

    # Small gems on band
    for gx, col in [(23, R2), (28, R2), (36, R2), (40, R2)]:
        s(gx, 13, col)
        s(gx, 14, R1)

    # Spires
    def spire(cl, cr, top_y, base_y):
        h = base_y - top_y
        bw = cr - cl + 1
        for y in range(top_y, base_y + 1):
            prog = (y - top_y) / max(h, 1)
            cur_w = max(1, int(round(bw * prog)))
            L = cl + (bw - cur_w) // 2
            R = L + cur_w - 1
            for x in range(L, R + 1):
                if y == top_y:
                    s(x, y, G3)
                elif x == L or x == R:
                    s(x, y, G1)
                else:
                    s(x, y, G2)
            # Outlines
            if cur_w > 1:
                s(L - 1, y, OL)
                s(R + 1, y, OL)
            else:
                s(L - 1, y, OL)
                s(L + 1, y, OL)

    # Center spire (tallest) — will hold gem
    spire(29, 34, 2, 11)
    # Side spires
    spire(22, 26, 5, 11)
    spire(37, 41, 5, 11)
    # Outer spires
    spire(15, 19, 8, 11)
    spire(44, 48, 8, 11)

    # Big red gem in center spire
    # Diamond shape centered at (31.5, 6)
    gem = [
        "  ##  ",
        " #rr# ",
        "#rRRr#",
        "#rRRr#",
        " #rr# ",
        "  ##  ",
    ]
    for j, row in enumerate(gem):
        for i, ch in enumerate(row):
            x = 29 + i
            y = 3 + j
            if ch == '#':
                s(x, y, OL)
            elif ch == 'r':
                s(x, y, R2)
            elif ch == 'R':
                s(x, y, R3)


draw_crown()


# ============================================================
# Final pass — drop a few floating ember sparkles around boss
# ============================================================
def sparkles():
    # Tiny embers at edges to give "evil aura"
    pts = [(6, 18), (58, 16), (4, 40), (60, 44), (10, 8), (54, 6)]
    for (x, y) in pts:
        s(x, y, R3)
        s(x + 1, y, R2)
        s(x, y + 1, R2)


sparkles()


# Save
out = '/home/user/dps-calc/bullet-hell/sprites/king_lost_crypt.png'
img.save(out)
# Also save 4x scaled-up version for preview
big = img.resize((W * 6, H * 6), Image.NEAREST)
big.save('/home/user/dps-calc/bullet-hell/sprites/king_lost_crypt_x6.png')
print(f"Saved: {out}")
