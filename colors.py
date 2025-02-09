class Colors:
    pink = [255, 105, 180]
    cyan = [0, 255, 255]
    blue = [0, 191, 255]
    pink2 = [255, 182, 193]
    salmon = [255, 160, 122]
    purple = [147, 112, 219]
    sky_blue = [135, 206, 250]
    background_color = [0, 20, 140]

    @classmethod
    def get_cell_colors(cls):
        return [cls.background_color, cls.cyan, cls.blue, cls.pink2, cls.pink, cls.purple, cls.sky_blue, cls.salmon]
