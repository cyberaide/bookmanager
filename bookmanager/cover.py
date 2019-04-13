from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pkg_resources

class Cover(object):


    def __init__(self):
        self.line = 1
        self.step = 50
        self.font = self.set_font("normal")
        self.color = 'rgb(255, 255, 255)'  # white color

    def set_font(self, scale):
        ttf = pkg_resources.resource_filename("bookmanager",
                                              'template/epub/fonts/OpenSans-Bold.ttf')

        if scale == "large":
            self.font = ImageFont.truetype(ttf,
                                           size=int(self.step * .9))
        elif scale == "tiny":
            self.font = ImageFont.truetype(ttf,
                                           size=int(self.step * .3))
        elif scale == "small":
            self.font = ImageFont.truetype(
                ttf,
                size=int(self.step * .4))

        else:
            self.font = ImageFont.truetype(ttf,
                                           size=int(self.step * .7))
        return self.font

    def reset(self):
        self.line = 1

    def skip(self, n):
        self.line = self.line + n

    def msg(self, x, text, step=50, scale="normal"):
        font = self.set_font(scale)
        self.draw.text((self.step * x, self.step * self.line), text,
                       fill=self.color, font=self.font)
        self.line = self.line + 1

    def hline(self, start, stop):
        self.draw.line((start * self.step, self.step * self.line,
                        stop * self.step, self.step * self.line),
                       fill=self.color,
                       width=10)

    def generate(self,
                 image="cover.png",
                 background=None,
                 title="Title",
                 subtitle="Subtitle",
                 author='Author',
                 subauthor="Editor",
                 email="laszewski@gmail.com",
                 webpage="https://github.com/cyberaide/bookmanager",
                 date=None):


        if background is None:
            background = pkg_resources.resource_filename("bookmanager",
                                                  'template/epub/cover/cover-image.png')
        print(">>>>>",background)
        print(">>>>>",image)

        canvas = Image.open(background)
        self.draw = ImageDraw.Draw(canvas)

        if date is None:
            date = "{:%B %d, %Y - %I:%M %p}".format(datetime.now())

        self.reset()
        self.msg(1, title, scale="large")
        self.msg(1, subtitle, scale="normal")
        self.skip(4)
        self.hline(1, 10)
        self.skip(1)
        self.msg(2, author)
        self.msg(2, subauthor, scale="tiny")
        self.skip(1)
        self.msg(5, email, scale="small")
        self.skip(5)
        self.msg(2, date, scale="tiny")
        self.msg(2, webpage, scale="small")

        canvas.save(image)



