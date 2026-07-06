# -*- coding: utf-8 -*-
"""Genera icone PWA pulite per Diagnosi Energetica (gradiente verde + fulmine)."""
from PIL import Image, ImageDraw, ImageFilter

SS = 4                      # supersampling per anti-aliasing
MASTER = 512 * SS           # 2048

# --- palette (coordinata con l'app) ---
TOP    = (52, 211, 122)     # verde chiaro  (alto-sx)
BOTTOM = (7,  74,  38)      # verde scuro   (basso-dx)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def diagonal_gradient(size, c1, c2):
    """Gradiente diagonale top-left -> bottom-right."""
    grad = Image.new("RGB", (size, size))
    px = grad.load()
    maxd = (size - 1) * 2
    for y in range(size):
        for x in range(size):
            px[x, y] = lerp(c1, c2, (x + y) / maxd)
    return grad

def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m

def bolt_points(size, scale=0.80):
    """Fulmine centrato, ridotto nella safe-zone (maskable) e scalato a `size`."""
    pts = [
        (0.575, 0.085),
        (0.305, 0.520),
        (0.470, 0.520),
        (0.398, 0.915),
        (0.730, 0.430),
        (0.560, 0.430),
        (0.640, 0.085),
    ]
    cx, cy = 0.505, 0.5      # leggera spinta a sinistra per equilibrio ottico
    pts = [(cx + (x - 0.5) * scale, cy + (y - 0.5) * scale) for (x, y) in pts]
    return [(x * size, y * size) for (x, y) in pts]

def build_master():
    size = MASTER
    # base trasparente
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    # sfondo con gradiente + angoli arrotondati
    grad = diagonal_gradient(size, TOP, BOTTOM).convert("RGBA")
    mask = rounded_mask(size, radius=int(size * 0.235))
    img.paste(grad, (0, 0), mask)

    # highlight morbido in alto-sinistra (molto sfumato, nessun bordo netto)
    gloss = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gloss)
    gd.ellipse([-size*0.45, -size*0.75, size*0.85, size*0.30],
               fill=(255, 255, 255, 60))
    gloss = gloss.filter(ImageFilter.GaussianBlur(size * 0.10))
    gloss = Image.composite(gloss, Image.new("RGBA", (size, size), (0,0,0,0)), mask)
    img = Image.alpha_composite(img, gloss)

    pts = bolt_points(size)

    # ombra del fulmine (morbida)
    shadow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    off = int(size * 0.012)
    sd.polygon([(x + off, y + off) for (x, y) in pts], fill=(3, 40, 20, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(size * 0.02))
    img = Image.alpha_composite(img, shadow)

    # fulmine bianco
    bolt = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bolt)
    bd.polygon(pts, fill=(255, 255, 255, 255))
    img = Image.alpha_composite(img, bolt)

    return img

def main():
    master = build_master()
    for out in (512, 192):
        master.resize((out, out), Image.LANCZOS).save(f"icon-{out}.png")
        print("scritto icon-%d.png" % out)

if __name__ == "__main__":
    main()
