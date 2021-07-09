import requests

from django.core.files.temp import NamedTemporaryFile


def get_downloaded_img(image_url: str) -> NamedTemporaryFile:
    r = requests.get(image_url)
    img_temp = NamedTemporaryFile(delete=True)
    img_temp.write(r.content)
    img_temp.flush()
    return img_temp
