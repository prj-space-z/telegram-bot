import requests
import io
from settings import Settings


class FaceSwapAPI:
    def __init__(self, url: str):
        self.base_url = url
        self.client = requests.Session()

    def face_swap(self, target, source):
        files = {
            'target': ('1.webp', target, 'image'),
            'source': ('1.jpg', source, 'image'),
        }

        resp = self.client.post(self.base_url + 'face-swap', files=files, stream=True, timeout=60 * 2)
        return io.BytesIO(resp.content)


face_swap = FaceSwapAPI(Settings().faceswap_host)
