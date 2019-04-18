from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import pkg_resources


class Cover(object):

    def __init__(self):
        self.draw = None
        self.row = 1
        self.step = 50
        self.font = self.set_font("normal")
        self.color = 'rgb(255, 255, 255)'  # white color

    def set_font(self, scale):
        ttf = pkg_resources.resource_filename(
            "bookmanager",
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
        elif scale == "smaller":
            self.font = ImageFont.truetype(
                ttf,
                size=int(self.step * .3))

        elif scale == "credit":
            self.font = ImageFont.truetype(ttf,
                                           size=int(self.step * .25))

        else:
            self.font = ImageFont.truetype(ttf,
                                           size=int(self.step * .7))
        return self.font

    def reset(self, row=None):
        if row is None:
            self.row = 1
        else:
            self.row = row

    def skip(self, n):
        self.row = self.row + n

    def mesg(self, x, text, step=50, scale="normal"):
        lines = text.split("\n")
        for line in lines:
            font = self.set_font(scale)
            self.draw.text((self.step * x, self.step * self.row), line,
                           fill=self.color, font=self.font)
            self.row = self.row + 1

    def line(self, start, stop, width=10):

        self.draw.line((start * self.step, self.step * self.row,
                        stop * self.step, self.step * self.row),
                       fill=self.color,
                       width=width)

    def credit(self, n):
        self.mesg(n,
                  "Created by Cloudmesh & Cyberaide Bookmanager, "
                  "https://github.com/cyberaide/bookmanager ",
                  scale="credit")

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
            background = pkg_resources.resource_filename(
                "bookmanager",
                'template/epub/cover/cover-image.png')

        canvas = Image.open(background)
        self.draw = ImageDraw.Draw(canvas)

        if date is None:
            date = "{:%B %d, %Y - %I:%M %p}".format(datetime.now())

        self.reset()
        self.mesg(1, title, scale="large")
        self.mesg(1, subtitle, scale="normal")
        self.skip(2)
        self.line(1, 13)
        self.skip(1)
        self.mesg(2, author)
        self.mesg(2, subauthor, scale="tiny")
        self.skip(1)
        self.mesg(5, email, scale="small")
        self.skip(1)
        self.line(1, 13)
        self.skip(1)
        self.mesg(1, webpage, scale="tiny")

        self.reset(1)
        self.skip(16)

        self.mesg(2, date, scale="tiny")
        self.credit(1.5)

        canvas.save(image)
