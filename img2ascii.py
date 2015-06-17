from PIL import Image


class Img2ascii:
    chars = [' ', '.', '1', '+', '*', '#', '%', 'M']

    def getchar(self, pi):
        for i in range(8):
            if pi < (i + 1) * 32:
                return self.chars[7-i]

    def __init__(self, src):
        self.img = Image.open(src)
        if self.img.mode == 'P' or self.img.mode == 'RGBA':
            im = Image.new('RGB', self.img.size, 'white')
            im.paste(self.img.convert('RGBA'), self.img.convert('RGBA'))
            self.img = im
        self.img = self.img.convert('L')

    def get_data(self, resize=1.0):
        w, h = self.img.size
        h /= 2
        w = int(w*resize)
        h = int(h*resize)
        temp = self.img.resize((w, h), Image.ANTIALIAS)
        pixs = temp.load()
        self.data = []
        for i in range(0, h):
            line = ''
            for j in range(0, w):
                line += self.getchar(pixs[j, i])
            self.data.append(line)
        return self.data
