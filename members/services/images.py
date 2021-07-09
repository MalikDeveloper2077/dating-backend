import os
from io import BytesIO

from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from members.models import Member


def _add_watermark(img):
    watermark = Image.open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static/members/watermark.png'),
        mode='r'
    ).convert("RGBA")
    img.paste(watermark, (0, 0), watermark)
    return img


def _get_watermarked_image(image_field) -> ContentFile:
    img = _add_watermark(Image.open(image_field, mode='r').convert("RGBA"))
    image_file = BytesIO()
    img.save(image_file, format='png')
    return ContentFile(image_file.getvalue())


def add_member_photo_watermark(member: Member):
    """Add a watermark to Member.photo and save it"""
    watermarked_photo = _get_watermarked_image(member.photo)
    member.photo.save(os.path.basename(member.photo.name), InMemoryUploadedFile(
        watermarked_photo, None, member.photo.name, 'image/png', watermarked_photo.tell, None
    ))
    member.save(update_fields=('photo',))
