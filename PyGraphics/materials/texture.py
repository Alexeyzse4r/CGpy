import numpy as np
from PIL import Image
from vmath import mathUtils
from vmath.mathUtils import Vec2
from transforms.transform2 import Transform2
from materials.rgb import RGB


class Texture(object):
    def __init__(self, _w: int = 0, _h: int = 0, _bpp: int = 0):
        self.__source_file: str = ""
        self.transform: Transform2 = Transform2()
        self.colors: [np.uint8] = None
        self.__width = _w
        self.__height = _h
        self.__bpp = _bpp
        # self.transform.scale = vec2(_w, -_h);
        self.clear_color()

    @property
    def source_file_path(self) -> str:
        return self.__source_file

    @source_file_path.setter
    def source_file_path(self, path: str) -> None:
        if path == self.__source_file:
            return
        self.load(path)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def bpp(self) -> int:
        return self.__bpp

    @property
    def texture_pixel_size(self):
        return self.__height * self.__width

    @property
    def tile(self) -> Vec2:
        return self.transform.scale

    @property
    def offset(self) -> Vec2:
        return self.transform.origin

    @property
    def texture_byte_size(self):
        return self.__bpp * self.__height * self.__width

    @property
    def rotation(self) -> float:
        return self.transform.az

    @tile.setter
    def tile(self, xy: Vec2):
        self.transform.scale = xy

    @offset.setter
    def offset(self, xy: Vec2):
        self.transform.origin = xy

    @rotation.setter
    def rotation(self, angle: float):
        self.transform.az = mathUtils.deg_to_rad(angle)

    @property
    def image_data(self) -> Image:
        if self.bpp == 3:
            return Image.frombytes('RGB', (self.__width, self.__height), self.colors)
        if self.bpp == 4:
            return Image.frombytes('RGBA', (self.__width, self.__height), self.colors)

    def load(self, origin: str):
        if not (self.colors is None):
            del self.colors
            self.__width = -1
            self.__height = -1
            self.__bpp = 0
        self.__source_file = origin
        im = Image.open(self.__source_file)
        self.__width, self.__height = im.size
        self.__bpp = im.layers
        self.colors: [np.uint8] = (np.asarray(im, dtype=np.uint8)).ravel()

    def set_color(self, i: int, j: int, color: RGB):
        pix = round((i + j * self.__width) * self.__bpp)
        if pix < 0:
            return
        if pix >= self.__width * self.__height * self.__bpp - 2:
            return
        self.colors[pix] = color.r
        self.colors[pix + 1] = color.g
        self.colors[pix + 2] = color.b

    def get_color(self, i: int, j: int) -> RGB:
        pix = round((i + j * self.__width) * self.__bpp)
        if pix < 0:
            return RGB(np.uint8(0), np.uint8(0), np.uint8(0))
        if pix >= self.__width * self.__height * self.__bpp - 2:
            return RGB(np.uint8(0), np.uint8(0), np.uint8(0))
        return RGB(self.colors[pix],
                   self.colors[pix + 1],
                   self.colors[pix + 2])

    # uv:: uv.x in range[0,1], uv.y in range[0,1]
    def set_color_uv(self, uv: Vec2, color: RGB):
        uv_ = self.transform.inv_transform_vect(uv, 1)
        pix = round((uv_.x + uv_.y * self.__width) * self.__bpp)
        if pix < 0:
            return
        if pix >= self.__width * self.__height * self.__bpp - 2:
            return
        self.colors[pix] = color.r
        self.colors[pix + 1] = color.g
        self.colors[pix + 2] = color.b

    # uv:: uv.x in range[0,1], uv.y in range[0,1]
    def get_color_uv(self, uv: Vec2) -> RGB:
        uv_ = self.transform.transform_vect(uv, 1)
        uv_x = abs(round(uv_.x * self.__width) % self.__width)
        uv_y = abs(round(uv_.y * self.__height) % self.__height)
        pix = (uv_x + uv_y * self.__width) * self.__bpp
        return RGB(self.colors[pix], self.colors[pix + 1], self.colors[pix + 2])

    def show(self):
        self.image_data.show()

    def clear_color(self, color: RGB = RGB(np.uint8(125), np.uint8(125), np.uint8(125))):
        if self.texture_byte_size == 0:
            return
        if not(self.colors is None):
            del self.colors
        self.colors = np.zeros((self.__height * self.__width * self.__bpp), dtype=np.uint8)
        rgb = [color.r, color.g, color.g]
        for i in range(0, len(self.colors)):
            self.colors[i] = rgb[i % 3]