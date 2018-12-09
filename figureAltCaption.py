"""
Generates a Caption for Figures for each Image which stands alone in a paragraph,
similar to pandoc#s handling of images/figures

--------------------------------------------

Licensed under the GPL 2 (see LICENSE.md)

Copyright 2015 - Jan Dittrich by
building upon the markdown-figures Plugin by
Copyright 2013 - [Helder Correia](http://heldercorreia.com) (GPL2)

--------------------------------------------

Examples:
    Bla bla bla

    ![this is the caption](http://lorempixel.com/400/200/)

    Next paragraph starts here

would generate a figure like this:

    <figure>
        <img src="http://lorempixel.com/400/200/">
        <figcaption>this is the caption</figcaption>
    </figure>
"""


from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import IMAGE_LINK_RE, IMAGE_REFERENCE_RE
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree
import re #regex

import logging
logger = logging.getLogger('MARKDOWN')

FIGURES = [u'^\s*'+IMAGE_LINK_RE, u'^\s*'+IMAGE_REFERENCE_RE] #is: linestart, any whitespace (even none), image, any whitespace (even none), line ends.
CAPTION = r'\[(?P<caption>[^\]]*)\]' # Get the contents within the first set of brackets
ATTR = r'\{(?P<attributes>[^\}]*)\}'

# This is the core part of the extension
class FigureCaptionProcessor(BlockProcessor):
    FIGURES_RE = re.compile('|'.join(f for f in FIGURES)) # Identifies the figures
    CAPTION_RE = re.compile(CAPTION) # Identifies the figure caption
    ATTR_RE = re.compile(ATTR) # Identifies the figure caption

    def test(self, parent, block): # is the block relevant
        # Wenn es ein Bild gibt und das Bild alleine im paragraph ist, und das Bild nicht schon einen figure parent hat, returne True
        isImage = bool(self.FIGURES_RE.search(block))
        isOnlyOneLine = (len(block.splitlines())== 1)
        isInFigure = (parent.tag == 'figure')
        
        # print(block, isImage, isOnlyOneLine, isInFigure, "T,T,F")
        if (isImage and isOnlyOneLine and not isInFigure):
            print(block)
            return True
        else:
            return False

    def run(self, parent, blocks): # how to process the block?
        raw_block = blocks.pop(0)
        captionText = self.CAPTION_RE.search(raw_block).group('caption')
        try:
            attrText = self.ATTR_RE.search(raw_block).group('attributes') # Get the caption text
        except:
            attrText = None

        # create figure
        figure = etree.SubElement(parent, 'figure')

        if attrText:
            figure.set('id',attrText)

        # render image in figure
        figure.text = raw_block

        # create caption
        figcaptionElem = etree.SubElement(figure,'figcaption')
        figcaptionElem.text = captionText #no clue why the text itself turns out as html again and not raw. Anyhow, it suits me, the blockparsers annoyingly wrapped everything into <p>.

class FigureCaptionExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        """ Add an instance of FigcaptionProcessor to BlockParser. """
        md.parser.blockprocessors.add('figureAltcaption',
                                      FigureCaptionProcessor(md.parser),
                                      '<ulist')

def makeExtension(**kwargs):
    return FigureCaptionExtension(**kwargs)
