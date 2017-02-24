#! /usr/bin/env python
#coding=utf-8

from uliweb import settings
from PIL import Image,ImageDraw,ImageFont,ImageFilter
import logging
import random
import string
import os

logger = logging.getLogger('generate_verification_code')

def gene_code(username, size = settings.VERIFICATIONCODE.SIZE,
              number = settings.VERIFICATIONCODE.NUMBER,
              bgcolor = settings.VERIFICATIONCODE.BG_COLOR,
              fontcolor = settings.VERIFICATIONCODE.FONT_COLOR,
              linecolor = settings.VERIFICATIONCODE.LINE_COLOR,
              draw_line = settings.VERIFICATIONCODE.DRAW_LINE,
              draw_point = settings.VERIFICATIONCODE.DRAW_POINT,
              font_type = settings.VERIFICATIONCODE.FONT_TYPE,
              line_number = settings.VERIFICATIONCODE.LINE_NUMBER,
              point_chance = settings.VERIFICATIONCODE.POINT_CHANCE,
              path = settings.VERIFICATIONCODE.VERIFICATIONCODE_STORE_PATH):
    '''generate verification code'''
    if not username:
        logger.error("-- generate verification code failed (username needed)")
        return

    def gene_text():
        ''' generate text randomly '''
        source = list(string.letters)
        for index in range(0,10):
            source.append(str(index))
        return ''.join(random.sample(source, number))

    def gene_line(draw,width,height):
        ''' generate interference line '''
        line_num = random.randint(*line_number)
        for i in range(line_num):
            begin = (random.randint(0, width), random.randint(0, height))
            end = (random.randint(0, width), random.randint(0, height))
            draw.line([begin, end], fill = linecolor)

    def gene_point(draw,width,height):
        ''' generate interference point '''
        chance = min(100, max(0,int(point_chance)))
        for w in xrange(width):
            for h in xrange(height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    width,height = size
    image = Image.new('RGBA',(width,height),bgcolor)
    font = ImageFont.truetype(font_type, 25)
    draw = ImageDraw.Draw(image)
    text = gene_text()
    logger.info("-- verification code text: %s" % (text))
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number),text,
            font = font,fill = fontcolor)
    if draw_line:
        gene_line(draw,width,height)
    if draw_point:
        gene_point(draw, width, height)
    # Twist
    image = image.transform((width+20,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, "%s.%s" % (username, settings.VERIFICATIONCODE.VERIFICATION_PICTYPE))
    image.save(path)
    logger.info("-- generate verification code success")
    return text