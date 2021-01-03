from common import Const, Utils
from PIL import Image, ImageDraw
import json


class Methods(object):
    @staticmethod
    def _dist(color_a, color_b):
        r1, g1, b1 = color_a
        r2, g2, b2 = color_b
        rm = (r1 + r2) / 2
        R, G, B = r1 - r2, g1 - g2, b1 - b2
        return ((2 + rm / 256) * (R ** 2) + 4 * (G ** 2) +
                (2 + (255 - rm) / 256) * (B ** 2)) ** 0.5

    @staticmethod
    def _approx(color):
        cid, d_min = 0, Methods._dist(color, Const.PA_colors[0])
        for i, c in enumerate(Const.PA_colors):
            d_cur = Methods._dist(color, c)
            if d_cur < d_min:
                d_min, cid = d_cur, i
        return cid

    @staticmethod
    def average(pixels):
        result = [0, 0, 0]
        for px in pixels:
            result = [result[k] + px[k] for k in range(3)]
        result = [result[k] // len(pixels) for k in range(3)]
        return Methods._approx(result)


class PixelArt(object):
    def __init__(self, path, block_size, save=None, show=False, outline=False):
        self.path = path
        self.block_size = block_size
        self.save = save
        self.show = show
        self.outline = outline
        self.im = Image.open(self.path).convert("RGB")
        self.pixels = self.im.load()
        self.size = self.im.size
        self.width, self.height = self.size
        self.cols = self.width // self.block_size
        self.rows = self.height // self.block_size

    def loads(self):
        result = Utils.array2d(self.cols, self.rows)
        blocks = Utils.array2d(self.cols, self.rows, list)
        for i in range(self.cols):
            for j in range(self.rows):
                sx, ex = i * self.block_size, (i + 1) * self.block_size
                sy, ey = j * self.block_size, (j + 1) * self.block_size
                for x in range(sx, ex):
                    for y in range(sy, ey):
                        blocks[i][j].append(self.pixels[x, y])
                result[i][j] = getattr(
                    Methods, Const.PA_method)(blocks[i][j])
        if self.save is not None or self.show:
            om = Image.new("RGB", [self.cols * self.block_size,
                                   self.rows * self.block_size], (255, 255, 255))
            draw = ImageDraw.Draw(om)
            for i in range(self.cols):
                for j in range(self.rows):
                    sx, ex = i * self.block_size, (i + 1) * self.block_size
                    sy, ey = j * self.block_size, (j + 1) * self.block_size
                    pos = [sx, sy, ex - 1, ey - 1]
                    cur_color = Const.PA_colors[result[i][j]]
                    outline = (0, 0, 0) if self.outline else None
                    draw.rectangle(pos, fill=cur_color,  outline=outline)
            if self.save is not None:
                om.save(self.save)
            if self.show:
                om.show()
        return {"cols": self.cols, "rows": self.rows, "data": result}


if __name__ == "__main__":
    print("[Path]")
    name, suffix = input().strip().split(".")
    print("[Size]")
    size = int(input().strip())
    path_src = "./data/src/{}.{}".format(name, suffix)
    path_dst = "./data/dst/{}.json".format(name)
    path_pa = "./data/pa/{}.{}".format(name, "png")
    r = PixelArt(path_src, size, save=path_pa,
                 show=True, outline=False).loads()
    with open(path_dst, "w") as f:
        f.write(json.dumps(r))
    print("ok")
