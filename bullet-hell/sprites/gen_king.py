"""King of the Lost Crypt — 64x64 boss sprite + 3x4 spritesheet.

Spritesheet layout (192x256):
  Row 0: FRONT  (boss faces camera / down)
  Row 1: BACK   (boss faces away / up)
  Row 2: RIGHT  (boss faces right)
  Row 3: LEFT   (boss faces left)
Cols: walk frames [left-step | idle | right-step].

Walk animation = vertical hover bob + horizontal sway.
"""

from PIL import Image

W = H = 64

# ---------- Palette ----------
T   = (0, 0, 0, 0)
OL  = (6, 2, 12, 255)
SH  = (28, 16, 42, 255)
WHT = (255, 255, 255, 255)

# Bone
B0 = (38, 30, 48, 255)
B1 = (74, 66, 80, 255)
Bm = (124, 114, 120, 255)
B2 = (180, 170, 168, 255)
B3 = (250, 246, 230, 255)
B4 = (255, 252, 244, 255)

# Royal purple
P1 = (32, 8, 56, 255)
P2 = (78, 28, 124, 255)
P3 = (140, 76, 200, 255)
P4 = (196, 138, 240, 255)
P5 = (228, 192, 255, 255)

# Gold
G1 = (108, 70, 12, 255)
G2 = (210, 160, 36, 255)
G3 = (255, 232, 120, 255)

# Red gem
R1 = (88, 6, 22, 255)
R2 = (220, 36, 52, 255)
R3 = (255, 130, 140, 255)

# Cyan glow
C0 = (4, 30, 70, 255)
C1 = (10, 90, 180, 255)
C2 = (60, 220, 255, 255)
C3 = (220, 252, 255, 255)


# ---------- Active image (reset per cell) ----------
img = None
px = None


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
# Shared post-processing
# ============================================================
def reinforce_silhouette():
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
            if above[3] == 0 or above == OL:
                s(x, y, rim_map[c])


# ============================================================
# FRONT VIEW (full detail)
# ============================================================
def draw_cape_front():
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
                if 38 < y < 56 and d < 0.22:
                    s(x, y, P1)
                else:
                    s(x, y, P3)
        s(L - 1, y, OL)
        s(R + 1, y, OL)
    hl(20, 43, top_y - 1, OL)
    bot_half = int(13 + 17)
    hl(32 - bot_half - 1, 31 + bot_half + 1, bot_y + 1, OL)
    for y_t, c in [(60, G2), (59, G3), (58, G1)]:
        t = (y_t - 28) / 33.0
        half = int(13 + t * 17)
        for x in range(32 - half, 32 + half):
            s(x, y_t, c)
    for x in range(32 - bot_half, 32 + bot_half, 6):
        s(x, 57, G2); s(x + 1, 57, G3); s(x + 2, 57, G2)


def draw_collar_front():
    sx, sy, srx, sry = 32, 23, 11, 10
    for y in range(26, 36):
        for x in range(17, 48):
            nx = (x - sx) / srx
            ny = (y - sy) / sry
            if nx * nx + ny * ny < 1.0:
                continue
            half_at_y = int(11 + (y - 26) * 1.6)
            if abs(x - 32) > half_at_y:
                continue
            d = abs(x - 32) / max(half_at_y, 1)
            if y < 28:
                c = P1 if d > 0.85 else P2
            else:
                c = P1 if d > 0.85 else (P2 if d > 0.5 else P3)
            s(x, y, c)
    hl(20, 43, 25, OL)


def draw_pauldron(cx, cy, rx, ry):
    for y in range(cy - ry - 1, cy + ry + 2):
        for x in range(cx - rx - 1, cx + rx + 2):
            nx = (x - cx) / rx
            ny = (y - cy) / ry
            d = nx * nx + ny * ny
            if d <= 1.0:
                if ny < -0.4 or (abs(nx) > 0.5 and ny < -0.1):
                    s(x, y, G3)
                elif d > 0.65:
                    s(x, y, G1)
                else:
                    s(x, y, G2)
            elif d <= 1.25:
                s(x, y, OL)


def mini_skull(cx, cy):
    rows = [" ### ", "#####", "#o#o#", " #v# ", " ### "]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            x = cx + i - 2
            y = cy + j - 2
            if ch == '#':
                s(x, y, B3)
            elif ch in 'ov':
                s(x, y, OL)


def draw_arm_front(side):
    if side == -1:
        # Left arm hangs straight down at side (no longer clasping center)
        for y in range(40, 50):
            x = 22
            s(x - 1, y, OL); s(x, y, B2); s(x + 1, y, B3); s(x + 2, y, B2); s(x + 3, y, OL)
        # Hand at bottom
        for y in range(50, 54):
            for x in range(22, 27):
                d = abs(x - 24) + abs(y - 52)
                if d <= 2:
                    s(x, y, B2 if (x + y) % 2 else B3)
        s(21, 51, OL); s(21, 52, OL)
        s(27, 51, OL); s(27, 52, OL)
        s(23, 54, OL); s(24, 54, OL); s(25, 54, OL)
    else:
        # Right arm raised — hand grips scepter base at chest level
        # Forearm peeks up from inside the pauldron
        for y in range(40, 44):
            x = 39
            s(x - 1, y, OL); s(x, y, B2); s(x + 1, y, B3); s(x + 2, y, B2); s(x + 3, y, OL)
        # Hand fist at scepter base (around 42, 38)
        for y in range(36, 41):
            for x in range(40, 45):
                d = abs(x - 42) + abs(y - 38)
                if d <= 2:
                    s(x, y, B2 if (x + y) % 2 else B3)
        # Hand outline
        s(39, 37, OL); s(39, 38, OL); s(39, 39, OL)
        s(45, 37, OL); s(45, 38, OL); s(45, 39, OL)
        s(41, 36, OL); s(42, 36, OL); s(43, 36, OL)
        s(40, 40, OL); s(41, 40, OL); s(43, 40, OL); s(44, 40, OL)


def draw_scepter_diagonal_front():
    """Diagonal staff resting on right pauldron, going up to upper-right corner."""
    x0, y0 = 42, 38      # base at right hand
    x1, y1 = 54, 14      # top, just below orb
    dx_t = x1 - x0
    dy_t = y0 - y1
    for y in range(y1, y0 + 1):
        progress = (y0 - y) / dy_t
        x = int(round(x0 + progress * dx_t))
        # Skip pixels inside the hand fist (so the grip remains visible)
        if 36 <= y <= 40 and 40 <= x <= 44 and abs(x - 42) + abs(y - 38) <= 2:
            continue
        s(x, y, G1)
        s(x + 1, y, G2)
        s(x - 1, y, OL)
        s(x + 2, y, OL)
    # Decorative bands at intervals
    for y_b in [32, 24, 17]:
        progress = (y0 - y_b) / dy_t
        x = int(round(x0 + progress * dx_t))
        s(x - 1, y_b, OL); s(x, y_b, G3); s(x + 1, y_b, G3); s(x + 2, y_b, OL)


def draw_robe_front():
    top_y, bot_y = 36, 61
    for y in range(top_y, bot_y + 1):
        t = (y - top_y) / (bot_y - top_y)
        half = int(7 + t * 7)
        L = 32 - half
        R = 31 + half
        for x in range(L, R + 1):
            if px[x, y][3] != 0 and px[x, y] in (B2, B3, OL):
                continue
            d = abs(x - 31.5) / max(half, 1)
            if d > 0.88:
                s(x, y, P1)
            elif d > 0.5:
                s(x, y, P3)
            else:
                s(x, y, P4)
        if px[L - 1, y][3] == 0 or px[L - 1, y] in (P1, P2, P3):
            s(L - 1, y, OL)
        if px[R + 1, y][3] == 0 or px[R + 1, y] in (P1, P2, P3):
            s(R + 1, y, OL)
    for y_b, c in [(56, G1), (57, G2), (58, G3), (59, G2), (60, G1)]:
        t = (y_b - 36) / 25.0
        half = int(7 + t * 7)
        for x in range(32 - half, 32 + half):
            if px[x, y_b] != OL:
                s(x, y_b, c)
    for y in range(38, 56):
        if px[31, y] in (P3, P4):
            s(31, y, G2)
        if px[32, y] in (P3, P4):
            s(32, y, G1)


def draw_scepter_staff_front():
    for y in range(38, 51):
        s(30, y, OL); s(31, y, G2); s(32, y, G1); s(33, y, OL)
    for y_b in [42, 47]:
        s(30, y_b, OL); s(31, y_b, G3); s(32, y_b, G3); s(33, y_b, OL)


def draw_skull_front():
    sx, sy, srx, sry = 32, 23, 11, 10
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
                if abs(nx) > 0.65 and -0.3 < ny < 0.45:
                    base = B1
                s(x, y, base)
            elif d <= 1.18:
                s(x, y, OL)
    s(32, 14, Bm); s(32, 16, B1); s(31, 17, Bm)
    hl(23, 30, 18, Bm); hl(34, 41, 18, Bm)
    hl(23, 30, 19, B1); hl(34, 41, 19, B1)
    s(24, 20, B1); s(29, 20, B1); s(34, 20, B1); s(40, 20, B1)

    def eye(cx, cy):
        for y in range(cy - 3, cy + 4):
            for x in range(cx - 4, cx + 5):
                dx = (x - cx) / 3.6
                dy = (y - cy) / 3.0
                d2 = dx * dx + dy * dy
                if 0.72 < d2 <= 1.0 and px[x, y] not in (OL,):
                    s(x, y, B0)
        for y in range(cy - 2, cy + 3):
            for x in range(cx - 3, cx + 4):
                dx = (x - cx) / 3.0
                dy = (y - cy) / 2.4
                if dx * dx + dy * dy <= 1.0:
                    s(x, y, OL)
        s(cx - 1, cy - 1, C2); s(cx, cy - 1, C3); s(cx + 1, cy - 1, C2)
        s(cx - 1, cy,     C2); s(cx, cy,     C3); s(cx + 1, cy,     C2)
        s(cx - 1, cy + 1, C1); s(cx, cy + 1, C2); s(cx + 1, cy + 1, C1)
        s(cx, cy - 1, WHT)

    eye(27, 22); eye(37, 22)

    s(24, 24, B4); s(25, 24, B3)
    s(40, 24, B4); s(39, 24, B3)
    for x in range(25, 30): s(x, 26, B1)
    for x in range(34, 39): s(x, 26, B1)
    s(26, 27, Bm); s(27, 27, Bm); s(36, 27, Bm); s(37, 27, Bm)

    s(31, 21, B4); s(32, 21, B4)
    s(31, 22, B3); s(32, 22, B3); s(31, 23, B3); s(32, 23, B3)
    s(31, 24, OL); s(32, 24, OL)
    s(30, 25, OL); s(31, 25, OL); s(32, 25, OL); s(33, 25, OL)
    s(30, 26, OL); s(31, 26, OL); s(32, 26, OL); s(33, 26, OL)
    s(31, 27, OL); s(32, 27, OL)
    s(29, 26, B1); s(34, 26, B1)
    s(28, 27, Bm); s(35, 27, Bm)

    hl(25, 38, 28, OL)
    teeth = [(25, 26), (28, 29), (31, 32), (34, 35), (37, 38)]
    for (a, b) in teeth:
        for x in range(a, b + 1):
            s(x, 29, B3); s(x, 30, B3)
        s(b, 30, B2)
    s(29, 29, OL); s(35, 30, G1); s(34, 30, B2)
    hl(25, 38, 31, OL)
    for x in range(26, 38):
        nx = (x - sx) / srx
        ny = (32 - sy) / sry
        if nx * nx + ny * ny <= 1.0:
            s(x, 32, B1)


def draw_crown_front():
    for y in range(12, 16):
        for x in range(20, 44):
            if y == 12: s(x, y, G3)
            elif y == 13: s(x, y, G2)
            elif y == 14: s(x, y, G2)
            else: s(x, y, G1)
    hl(20, 43, 11, OL); hl(20, 43, 16, OL)
    vl(19, 12, 15, OL); vl(44, 12, 15, OL)
    for gx in [23, 28, 36, 40]:
        s(gx, 13, R2); s(gx, 14, R1)

    def spire(cl, cr, top_y, base_y):
        h = base_y - top_y
        bw = cr - cl + 1
        for y in range(top_y, base_y + 1):
            prog = (y - top_y) / max(h, 1)
            cur_w = max(1, int(round(bw * prog)))
            L = cl + (bw - cur_w) // 2
            R = L + cur_w - 1
            for x in range(L, R + 1):
                if y == top_y: s(x, y, G3)
                elif x == L or x == R: s(x, y, G1)
                else: s(x, y, G2)
            if cur_w > 1:
                s(L - 1, y, OL); s(R + 1, y, OL)
            else:
                s(L - 1, y, OL); s(L + 1, y, OL)

    spire(29, 34, 2, 11)
    spire(22, 26, 5, 11); spire(37, 41, 5, 11)
    spire(15, 19, 8, 11); spire(44, 48, 8, 11)

    gem = [
        "  ##  ",
        " #rr# ",
        "#rRRr#",
        "#R*Rr#",
        "#rRRr#",
        " #rr# ",
        "  ##  ",
    ]
    for j, row in enumerate(gem):
        for i, ch in enumerate(row):
            x = 29 + i
            y = 2 + j
            if ch == '#': s(x, y, OL)
            elif ch == 'r': s(x, y, R2)
            elif ch == 'R': s(x, y, R3)
            elif ch == '*': s(x, y, WHT)
    s(28, 5, R1); s(35, 5, R1)
    s(31, 1, R2); s(32, 1, R2)
    s(31, 9, R1); s(32, 9, R1)


def draw_scepter_orb():
    """Orb at top of diagonal scepter, upper-right area."""
    cx, cy = 55, 11
    for y in range(cy - 4, cy + 5):
        for x in range(cx - 4, cx + 5):
            dx = x - cx + 0.5
            dy = y - cy + 0.5
            d2 = dx * dx + dy * dy
            if d2 <= 12:
                if d2 <= 2: s(x, y, WHT)
                elif d2 <= 5: s(x, y, C3)
                elif d2 <= 9: s(x, y, C2)
                else: s(x, y, C1)
            elif d2 <= 16:
                s(x, y, OL)
    # Halo bleed
    for (hx, hy) in [(cx - 4, cy), (cx + 4, cy), (cx, cy - 4), (cx, cy + 4),
                      (cx - 3, cy - 3), (cx + 3, cy - 3),
                      (cx - 3, cy + 3), (cx + 3, cy + 3)]:
        if 0 <= hx < W and 0 <= hy < H and px[hx, hy] == OL:
            s(hx, hy, C0)


def render_front():
    draw_cape_front()
    draw_collar_front()
    draw_pauldron(15, 36, 8, 6)
    draw_pauldron(48, 36, 8, 6)
    mini_skull(15, 37); mini_skull(48, 37)
    draw_arm_front(-1); draw_arm_front(+1)
    draw_robe_front()
    draw_scepter_diagonal_front()
    draw_skull_front()
    draw_crown_front()
    reinforce_silhouette()
    add_rim_highlights()
    draw_scepter_orb()


# ============================================================
# BACK VIEW (no face, no scepter — back of king)
# ============================================================
def draw_skull_back():
    sx, sy, srx, sry = 32, 23, 11, 10
    for y in range(sy - sry - 1, sy + sry + 2):
        for x in range(sx - srx - 1, sx + srx + 2):
            nx = (x - sx) / srx
            ny = (y - sy) / sry
            d = nx * nx + ny * ny
            if d <= 1.0:
                edge = d > 0.78
                # Brighter top (lit by crown), darker neck shadow at bottom
                if ny < -0.55:
                    base = B3 if edge else B4
                elif ny < 0.2:
                    base = B2 if edge else B3
                elif ny < 0.6:
                    base = Bm if edge else B2
                else:
                    base = B1 if edge else Bm
                if abs(nx) > 0.7 and -0.2 < ny < 0.4:
                    base = B1
                s(x, y, base)
            elif d <= 1.18:
                s(x, y, OL)
    # Cranium suture line — more prominent on back
    vl(32, 14, 26, B1)
    s(32, 18, B0); s(32, 22, B0)
    # Side hairline
    s(28, 17, Bm); s(36, 17, Bm)
    # Neck base — dark band where head meets collar
    hl(26, 37, 32, B1)


def draw_arm_back(side):
    """Bone arms hanging straight down at the king's sides, visible from behind."""
    if side == -1:
        x = 17  # left side, just inside the pauldron
    else:
        x = 46
    # Upper + forearm in one straight column (slight outward angle on forearm)
    for y in range(41, 52):
        s(x - 1, y, OL); s(x, y, B2); s(x + 1, y, B3); s(x + 2, y, B2); s(x + 3, y, OL)
    # Elbow joint highlight
    s(x, 46, B1); s(x + 1, 46, B2); s(x + 2, 46, B1)
    # Hand at the bottom — small bone fist
    hx = x + (-1 if side == -1 else 1)
    for y in range(51, 55):
        for cx in range(hx, hx + 4):
            d = abs(cx - (hx + 1)) + abs(y - 53)
            if d <= 2:
                s(cx, y, B2 if (cx + y) % 2 else B3)
    # Hand outline
    s(hx - 1, 52, OL); s(hx - 1, 53, OL)
    s(hx + 4, 52, OL); s(hx + 4, 53, OL)
    s(hx + 1, 55, OL); s(hx + 2, 55, OL)


def render_back():
    draw_cape_front()
    draw_collar_front()
    draw_pauldron(15, 36, 8, 6)
    draw_pauldron(48, 36, 8, 6)
    # No mini-skulls on back of pauldrons — those are on the front face.
    # Add a small gold rivet/stud cluster instead to suggest pauldron back.
    for (px_, py_) in [(15, 36), (48, 36)]:
        s(px_, py_, G1); s(px_ - 2, py_ - 1, G3); s(px_ + 2, py_ - 1, G3)
        s(px_, py_ - 2, G3); s(px_, py_ + 2, G1)
    # Arms hanging behind/at the sides
    draw_arm_back(-1)
    draw_arm_back(+1)
    # Robe back — same shape, no gold seam
    top_y, bot_y = 36, 61
    for y in range(top_y, bot_y + 1):
        t = (y - top_y) / (bot_y - top_y)
        half = int(7 + t * 7)
        L = 32 - half; R = 31 + half
        for x in range(L, R + 1):
            # Don't overwrite arms
            if px[x, y][3] != 0 and px[x, y] in (B2, B3, OL):
                continue
            d = abs(x - 31.5) / max(half, 1)
            if d > 0.88: s(x, y, P1)
            elif d > 0.5: s(x, y, P2)
            else: s(x, y, P3)
        if px[L - 1, y][3] == 0 or px[L - 1, y] in (P1, P2, P3):
            s(L - 1, y, OL)
        if px[R + 1, y][3] == 0 or px[R + 1, y] in (P1, P2, P3):
            s(R + 1, y, OL)
    for y_b, c in [(56, G1), (57, G2), (58, G3), (59, G2), (60, G1)]:
        t = (y_b - 36) / 25.0
        half = int(7 + t * 7)
        for x in range(32 - half, 32 + half):
            if px[x, y_b] != OL:
                s(x, y_b, c)
    draw_skull_back()
    draw_crown_front()
    reinforce_silhouette()
    add_rim_highlights()


# ============================================================
# RIGHT VIEW (boss faces right; we see his right side)
# ============================================================
def render_right():
    # === CAPE — sweeps left behind king ===
    for y in range(28, 62):
        t = (y - 28) / 33.0
        L = int(28 - t * 24)
        R = int(34 + t * 4)
        for x in range(L, R + 1):
            d = (x - L) / max(R - L, 1)
            if d < 0.12: s(x, y, P1)
            elif d < 0.45: s(x, y, P2)
            elif d < 0.85: s(x, y, P3)
            else: s(x, y, P2)
        s(L - 1, y, OL); s(R + 1, y, OL)
    hl(28, 34, 27, OL)
    for y_t, c in [(60, G2), (59, G3), (58, G1)]:
        t = (y_t - 28) / 33.0
        L = int(28 - t * 24); R = int(34 + t * 4)
        for x in range(L, R + 1):
            s(x, y_t, c)

    # === ROBE BODY — vertical, leans forward (right) ===
    top_y, bot_y = 36, 61
    for y in range(top_y, bot_y + 1):
        t = (y - top_y) / (bot_y - top_y)
        half = int(7 + t * 5)
        cx = 35
        L = cx - half; R = cx + half
        for x in range(L, R + 1):
            d = (x - L) / max(R - L, 1)
            if d < 0.15: s(x, y, P1)
            elif d < 0.55: s(x, y, P3)
            else: s(x, y, P4)
        s(L - 1, y, OL); s(R + 1, y, OL)
    for y_b, c in [(57, G2), (58, G3), (59, G2), (60, G1)]:
        t = (y_b - 36) / 25.0
        half = int(7 + t * 5)
        for x in range(35 - half, 35 + half + 1):
            if px[x, y_b] != OL:
                s(x, y_b, c)

    # === FAR PAULDRON (back-left, mostly hidden) ===
    for y in range(34, 41):
        for x in range(26, 32):
            cx, cy = 29, 37
            rx, ry = 3, 3
            nx = (x - cx) / rx; ny = (y - cy) / ry
            d = nx * nx + ny * ny
            if d <= 1.0:
                if d > 0.6: s(x, y, G1)
                else: s(x, y, G2)
            elif d <= 1.3:
                s(x, y, OL)

    # === NEAR PAULDRON (right shoulder) — dominant ===
    for y in range(31, 44):
        for x in range(36, 53):
            cx, cy = 44, 37
            rx, ry = 7, 6
            nx = (x - cx) / rx; ny = (y - cy) / ry
            d = nx * nx + ny * ny
            if d <= 1.0:
                if ny < -0.4 or (nx > 0.4 and ny < -0.1):
                    s(x, y, G3)
                elif d > 0.65: s(x, y, G1)
                else: s(x, y, G2)
            elif d <= 1.25:
                s(x, y, OL)
    # Mini skull (5x5) on near pauldron
    rows = [" ### ", "#####", "#o#o#", " #v# ", " ### "]
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            x = 44 + i - 2; y = 38 + j - 2
            if ch == '#': s(x, y, B3)
            elif ch in 'ov': s(x, y, OL)

    # === ARM extending forward holding scepter ===
    for i, y in enumerate(range(40, 47)):
        bx = 45 + i // 3
        s(bx - 1, y, OL); s(bx, y, B2); s(bx + 1, y, B3); s(bx + 2, y, OL)
    for y in range(47, 51):
        for x in range(46, 51):
            if abs(x - 48) + abs(y - 48) <= 2:
                s(x, y, B2 if (x + y) % 2 else B3)
    s(45, 47, OL); s(45, 48, OL)
    s(51, 47, OL); s(51, 48, OL)
    s(47, 50, OL); s(48, 50, OL); s(49, 50, OL)

    # === SCEPTER STAFF ===
    for y in range(36, 48):
        s(47, y, OL); s(48, y, G2); s(49, y, G1); s(50, y, OL)
    s(47, 41, OL); s(48, 41, G3); s(49, 41, G3); s(50, 41, OL)

    # === SKULL PROFILE — facing right ===
    sx, sy, srx, sry = 29, 22, 9, 10
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
                else:
                    base = Bm if edge else B2
                # Back of head recedes
                if nx < -0.55:
                    base = B1
                s(x, y, base)
            elif d <= 1.18:
                s(x, y, OL)

    # === BROW RIDGE on profile (above eye) ===
    hl(31, 38, 18, Bm)
    hl(31, 38, 19, B1)

    # === NOSE — pronounced protrusion to the right ===
    s(38, 21, B4); s(39, 21, B3)
    s(38, 22, B3); s(39, 22, B2); s(40, 22, B1)
    s(38, 23, B3); s(39, 23, Bm); s(40, 23, OL)
    s(38, 24, B2); s(39, 24, B1); s(40, 24, OL)
    s(38, 25, Bm); s(39, 25, OL)
    # Nostril (under nose tip)
    s(38, 26, OL); s(39, 26, OL)
    s(37, 26, B1)

    # === EYE — large glowing socket like front view ===
    cx, cy = 35, 22
    for y in range(cy - 2, cy + 3):
        for x in range(cx - 3, cx + 3):
            dx = (x - cx) / 2.8
            dy = (y - cy) / 2.2
            if dx * dx + dy * dy <= 1.0:
                s(x, y, OL)
    s(cx - 1, cy - 1, C2); s(cx, cy - 1, C3); s(cx + 1, cy - 1, C2)
    s(cx - 1, cy,     C2); s(cx, cy,     C3); s(cx + 1, cy,     C2)
    s(cx - 1, cy + 1, C1); s(cx, cy + 1, C2); s(cx + 1, cy + 1, C1)
    s(cx, cy - 1, WHT)

    # === CHEEKBONE highlight + hollow (defines face shape) ===
    s(34, 24, B4); s(35, 24, B3)
    s(33, 25, B1); s(34, 25, Bm)
    s(36, 25, B1)

    # === MOUTH — visible teeth row in profile ===
    hl(33, 38, 28, OL)
    s(33, 29, B3); s(34, 29, B3)
    s(35, 29, OL)  # gap
    s(36, 29, B3); s(37, 29, B3)
    s(38, 29, OL)  # gap
    # Yellowed front tooth
    s(38, 29, G1)
    hl(33, 38, 30, OL)

    # === JAW LINE — strong shadow under face ===
    hl(30, 36, 31, B1)
    s(31, 32, OL); s(32, 32, OL); s(33, 32, OL)

    # === CROWN — clean side profile, 3 spires only ===
    for y in range(12, 16):
        for x in range(22, 41):
            if y == 12: s(x, y, G3)
            elif y == 13: s(x, y, G2)
            elif y == 14: s(x, y, G2)
            else: s(x, y, G1)
    hl(22, 40, 11, OL); hl(22, 40, 16, OL)
    vl(21, 12, 15, OL); vl(41, 12, 15, OL)
    for gx in [25, 31, 37]:
        s(gx, 13, R2); s(gx, 14, R1)

    def spire(cl, cr, top_y, base_y):
        h = base_y - top_y
        bw = cr - cl + 1
        for y in range(top_y, base_y + 1):
            prog = (y - top_y) / max(h, 1)
            cur_w = max(1, int(round(bw * prog)))
            L = cl + (bw - cur_w) // 2
            R = L + cur_w - 1
            for x in range(L, R + 1):
                if y == top_y: s(x, y, G3)
                elif x == L or x == R: s(x, y, G1)
                else: s(x, y, G2)
            if cur_w > 1:
                s(L - 1, y, OL); s(R + 1, y, OL)
            else:
                s(L - 1, y, OL); s(L + 1, y, OL)

    # Three clean spires: back, center (tallest, with gem), front
    spire(23, 27, 5, 11)        # back spire
    spire(29, 34, 2, 11)        # center spire (gem)
    spire(36, 40, 5, 11)        # front spire

    # === BIG RED GEM in center spire ===
    gem = [
        "  ##  ",
        " #rr# ",
        "#rRRr#",
        "#R*Rr#",
        "#rRRr#",
        " #rr# ",
        "  ##  ",
    ]
    for j, row in enumerate(gem):
        for i, ch in enumerate(row):
            x = 28 + i; y = 2 + j
            if ch == '#': s(x, y, OL)
            elif ch == 'r': s(x, y, R2)
            elif ch == 'R': s(x, y, R3)
            elif ch == '*': s(x, y, WHT)
    s(27, 5, R1); s(34, 5, R1)
    s(30, 1, R2); s(31, 1, R2)

    # === SCEPTER ORB — large, like front view ===
    cx, cy = 49, 33
    for y in range(cy - 5, cy + 6):
        for x in range(cx - 5, cx + 6):
            dx = x - cx + 0.5; dy = y - cy + 0.5
            d2 = dx * dx + dy * dy
            if d2 <= 16:
                if d2 <= 2: s(x, y, WHT)
                elif d2 <= 6: s(x, y, C3)
                elif d2 <= 12: s(x, y, C2)
                else: s(x, y, C1)
            elif d2 <= 22:
                s(x, y, OL)
    # Halo
    for (hx, hy) in [(cx - 5, cy), (cx + 5, cy), (cx, cy - 5), (cx, cy + 5)]:
        if 0 <= hx < W and 0 <= hy < H and px[hx, hy] == OL:
            s(hx, hy, C0)

    reinforce_silhouette()
    add_rim_highlights()


# ============================================================
# Render dispatcher
# ============================================================
def render_cell(direction, frame):
    global img, px
    img = Image.new('RGBA', (W, H), T)
    px = img.load()

    if direction == 'front':
        render_front()
    elif direction == 'back':
        render_back()
    elif direction == 'right':
        render_right()
    elif direction == 'left':
        render_right()
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    # Walk-cycle offsets — float bob + sway
    if frame == 0:
        bobbed = Image.new('RGBA', (W, H), T)
        bobbed.paste(img, (-1, -1), img)
        img = bobbed
    elif frame == 2:
        bobbed = Image.new('RGBA', (W, H), T)
        bobbed.paste(img, (1, -1), img)
        img = bobbed

    return img


# ============================================================
# Build outputs
# ============================================================
SHEET_W = W * 3
SHEET_H = H * 4
sheet = Image.new('RGBA', (SHEET_W, SHEET_H), T)
for row, direction in enumerate(['front', 'back', 'right', 'left']):
    for col in range(3):
        cell = render_cell(direction, col)
        sheet.paste(cell, (col * W, row * H), cell)

base = '/home/user/dps-calc/bullet-hell/sprites'
sheet.save(f'{base}/king_spritesheet.png')
sheet.resize((SHEET_W * 4, SHEET_H * 4), Image.NEAREST).save(f'{base}/king_spritesheet_x4.png')

# Single front sprite (idle frame) for backward compat
front = render_cell('front', 1)
front.save(f'{base}/king_lost_crypt.png')
front.resize((W * 6, H * 6), Image.NEAREST).save(f'{base}/king_lost_crypt_x6.png')

print(f'Saved spritesheet ({SHEET_W}x{SHEET_H}) and single sprite.')
