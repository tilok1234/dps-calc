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

# ---------- Palette (high-contrast for bullet-hell readability) ----------
T   = (0, 0, 0, 0)          # transparent
OL  = (6, 2, 12, 255)       # outline (near pure black w/ violet tint)
SH  = (28, 16, 42, 255)     # generic shadow
WHT = (255, 255, 255, 255)  # pure white sparkle

# Bone (cool tint)
B0 = (38, 30, 48, 255)       # deepest crevice
B1 = (74, 66, 80, 255)
Bm = (124, 114, 120, 255)    # mid shadow
B2 = (180, 170, 168, 255)
B3 = (250, 246, 230, 255)
B4 = (255, 252, 244, 255)    # bright highlight

# Royal purple
P1 = (32, 8, 56, 255)
P2 = (78, 28, 124, 255)
P3 = (140, 76, 200, 255)
P4 = (196, 138, 240, 255)
P5 = (228, 192, 255, 255)   # rim light

# Gold
G1 = (108, 70, 12, 255)
G2 = (210, 160, 36, 255)
G3 = (255, 232, 120, 255)

# Red gem
R1 = (88, 6, 22, 255)
R2 = (220, 36, 52, 255)
R3 = (255, 130, 140, 255)

# Cyan glow (eye sockets / scepter orb)
C0 = (4, 30, 70, 255)        # deep glow shadow
C1 = (10, 90, 180, 255)
C2 = (60, 220, 255, 255)
C3 = (220, 252, 255, 255)

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
    # Short staff from hand level up to chest, orb in front of chest.
    # Staff: rows 38-50, cols 30-33
    for y in range(38, 51):
        s(30, y, OL)
        s(31, y, G2)
        s(32, y, G1)
        s(33, y, OL)
    # Bands
    for y_b in [42, 47]:
        s(30, y_b, OL); s(31, y_b, G3); s(32, y_b, G3); s(33, y_b, OL)
    # Orb sits at chest level, centered (31.5, 39) — readable, won't be hidden
    # (drawn LAST in main flow so head/crown can't cover it)


# (orb drawn separately at end of file for proper layering)
draw_scepter()


# ============================================================
# SKULL HEAD
# ============================================================
def draw_skull():
    sx, sy, srx, sry = 32, 23, 11, 10

    # === Multi-tone fill — vertical lighting + edge falloff ===
    for y in range(sy - sry - 1, sy + sry + 2):
        for x in range(sx - srx - 1, sx + srx + 2):
            nx = (x - sx) / srx
            ny = (y - sy) / sry
            d = nx * nx + ny * ny
            if d <= 1.0:
                edge = d > 0.78
                if ny < -0.55:
                    base = B3 if edge else B4
                elif ny < 0.0:
                    base = B2 if edge else B3
                elif ny < 0.4:
                    base = B2 if edge else B3
                elif ny < 0.7:
                    base = Bm if edge else B2
                else:
                    base = B1 if edge else Bm
                # Temporal hollows — sides recede
                if abs(nx) > 0.65 and -0.3 < ny < 0.45:
                    base = B1
                s(x, y, base)
            elif d <= 1.18:
                s(x, y, OL)

    # === Cranium suture line (skull plates) — subtle vertical ===
    s(32, 14, Bm); s(32, 16, B1); s(31, 17, Bm)

    # === Brow ridge — heavy band framing eye sockets ===
    hl(23, 30, 18, Bm)
    hl(34, 41, 18, Bm)
    hl(23, 30, 19, B1)
    hl(34, 41, 19, B1)
    # Drop-shadow under brow into upper eye orbit
    s(24, 20, B1); s(29, 20, B1)
    s(34, 20, B1); s(40, 20, B1)

    # === Eye sockets — recessed with B0 rim for depth ===
    def eye(cx, cy):
        # Outer dark rim — gives socket "depth"
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 4, cx + 5):
                dx = (x - cx) / 3.6
                dy = (y - cy) / 3.0
                d2 = dx * dx + dy * dy
                if 0.72 < d2 <= 1.0 and px[x, y] not in (OL,):
                    s(x, y, B0)
        # Inner socket black
        for y in range(cy - 2, cy + 3):
            for x in range(cx - 3, cx + 4):
                dx = (x - cx) / 3.0
                dy = (y - cy) / 2.4
                if dx * dx + dy * dy <= 1.0:
                    s(x, y, OL)
        # Cyan glow with white pinprick
        s(cx - 1, cy - 1, C2); s(cx, cy - 1, C3); s(cx + 1, cy - 1, C2)
        s(cx - 1, cy,     C2); s(cx, cy,     C3); s(cx + 1, cy,     C2)
        s(cx - 1, cy + 1, C1); s(cx, cy + 1, C2); s(cx + 1, cy + 1, C1)
        s(cx, cy - 1, WHT)

    eye(27, 22)
    eye(37, 22)

    # === Cheekbones — bright bumps with shadow hollows below ===
    s(24, 24, B4); s(25, 24, B3)
    s(40, 24, B4); s(39, 24, B3)
    # Hollow under cheekbone
    for x in range(25, 30):
        s(x, 26, B1)
    for x in range(34, 39):
        s(x, 26, B1)
    s(26, 27, Bm); s(27, 27, Bm)
    s(36, 27, Bm); s(37, 27, Bm)

    # === Nasal bridge ridge — highlight between eyes down to nose ===
    s(31, 21, B4); s(32, 21, B4)
    s(31, 22, B3); s(32, 22, B3)
    s(31, 23, B3); s(32, 23, B3)

    # === Nose hole — chunky inverted triangle ===
    s(31, 24, OL); s(32, 24, OL)
    s(30, 25, OL); s(31, 25, OL); s(32, 25, OL); s(33, 25, OL)
    s(30, 26, OL); s(31, 26, OL); s(32, 26, OL); s(33, 26, OL)
    s(31, 27, OL); s(32, 27, OL)
    # Inner nostril shadow
    s(29, 26, B1); s(34, 26, B1)

    # === Maxilla detail — small shadow above teeth row ===
    s(28, 27, Bm); s(35, 27, Bm)

    # === Teeth — clean white with chipped + yellowed details ===
    hl(25, 38, 28, OL)
    teeth = [(25, 26), (28, 29), (31, 32), (34, 35), (37, 38)]
    for (a, b) in teeth:
        for x in range(a, b + 1):
            s(x, 29, B3)
            s(x, 30, B3)
        s(b, 30, B2)  # shadow on right edge of each tooth
    # Chipped corner on second tooth
    s(29, 29, OL)
    # Yellowed/aged tooth (fourth)
    s(35, 30, G1)
    s(34, 30, B2)
    hl(25, 38, 31, OL)

    # === Jaw bottom shadow ===
    for x in range(26, 38):
        nx = (x - sx) / srx
        ny = (32 - sy) / sry
        if nx * nx + ny * ny <= 1.0:
            s(x, 32, B1)


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

    # Big red gem in center spire — bright with white sparkle
    gem = [
        "  ##  ",
        " #rr# ",
        "#rRRr#",
        "#R*Rr#",
        "#rRRr#",
        " #rr# ",
        "  ##  ",
    ]
    # Render with the longest row as the layout reference
    for j, row in enumerate(gem):
        for i, ch in enumerate(row):
            x = 29 + i
            y = 2 + j
            if ch == '#':
                s(x, y, OL)
            elif ch == 'r':
                s(x, y, R2)
            elif ch == 'R':
                s(x, y, R3)
            elif ch == '*':
                s(x, y, WHT)
    # Outer halo — dark red bleed for glow
    s(28, 5, R1); s(35, 5, R1)
    s(31, 1, R2); s(32, 1, R2)
    s(31, 9, R1); s(32, 9, R1)


draw_crown()


# ============================================================
# Post-processing — readability passes
# ============================================================
def reinforce_silhouette():
    """Ensure every transparent pixel adjacent (8-neighbor) to a
    non-outline colored pixel becomes outline. Gives a clean,
    consistent dark border around the whole boss."""
    edges = []
    for y in range(H):
        for x in range(W):
            if px[x, y][3] != 0:
                continue
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        c = px[nx, ny]
                        if c[3] != 0 and c != OL:
                            edges.append((x, y))
                            break
                else:
                    continue
                break
    for x, y in edges:
        s(x, y, OL)


def add_rim_highlights():
    """Lighten upper-facing edges of major color zones for top-down readability."""
    # Snapshot since we'll be writing
    src = [[px[x, y] for y in range(H)] for x in range(W)]
    rim_map = {
        P1: P3, P2: P4, P3: P5, P4: P5,
        G1: G3, G2: G3,
        B1: B3, B2: B3,
    }
    for y in range(1, H):
        for x in range(W):
            c = src[x][y]
            if c not in rim_map:
                continue
            above = src[x][y - 1]
            # Top edge if pixel above is transparent or outline
            if above[3] == 0 or above == OL:
                s(x, y, rim_map[c])


def draw_scepter_orb():
    """Big glowing cyan orb centered on chest (in front of body)."""
    cx, cy = 31, 39
    for y in range(cy - 5, cy + 6):
        for x in range(cx - 5, cx + 6):
            dx = x - cx + 0.5
            dy = y - cy + 0.5
            d2 = dx * dx + dy * dy
            if d2 <= 16:
                if d2 <= 2:
                    s(x, y, WHT)
                elif d2 <= 6:
                    s(x, y, C3)
                elif d2 <= 12:
                    s(x, y, C2)
                else:
                    s(x, y, C1)
            elif d2 <= 22:
                s(x, y, OL)
    # Outer halo of darker cyan (extends the silhouette glow)
    for (hx, hy) in [(cx - 5, cy), (cx + 5, cy), (cx, cy - 5), (cx, cy + 5),
                      (cx - 4, cy - 3), (cx + 4, cy - 3),
                      (cx - 4, cy + 3), (cx + 4, cy + 3)]:
        if px[hx, hy] == OL:
            s(hx, hy, C0)


def sparkles():
    pts = [(6, 18), (58, 16), (4, 40), (60, 44), (10, 8), (54, 6)]
    for (x, y) in pts:
        s(x, y, R3)
        s(x + 1, y, R2)
        s(x, y + 1, R2)


reinforce_silhouette()
add_rim_highlights()
draw_scepter_orb()
sparkles()


# Save
out = '/home/user/dps-calc/bullet-hell/sprites/king_lost_crypt.png'
img.save(out)
# Also save 4x scaled-up version for preview
big = img.resize((W * 6, H * 6), Image.NEAREST)
big.save('/home/user/dps-calc/bullet-hell/sprites/king_lost_crypt_x6.png')
print(f"Saved: {out}")
