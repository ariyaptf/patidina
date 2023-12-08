from django import template
from custom_media.models import CustomImage as Image

register = template.Library()

@register.simple_tag
def get_image_by_name(name):
    return Image.objects.filter(title=name).first()