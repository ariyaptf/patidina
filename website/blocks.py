from wagtail import blocks
from coderedcms.blocks import BaseBlock

from django.utils.translation import gettext_lazy as _


class VerseBlock(blocks.StructBlock):
    verse = blocks.TextBlock()

    class Meta:
        icon = 'pilcrow'
        label = _('Verse Line')


class StanzaBlock(blocks.StructBlock):
    verses = blocks.ListBlock(VerseBlock())

    class Meta:
        icon = 'openquote'
        label = _('Stanza')


class PoetryBlock(BaseBlock):
    stanzas = blocks.ListBlock(StanzaBlock())

    class Meta:
        template = 'website/blocks/poetry_block.html'
        icon = 'edit'
        label = _('Poetry')
