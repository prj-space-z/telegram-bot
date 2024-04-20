import httpx
import io


class FaceSwapAPI:
    base_url = 'http://127.0.0.1:8000/'

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=60 * 2)

    async def face_swap(self, target: io.BytesIO, source: io.BytesIO):
        files = {
            'target': ('1.webp', target.read(), 'image'),
            'source': ('1.png', source.read(), 'image'),
        }

        resp = await self.client.post(self.base_url + 'face-swap', files=files)
        return io.BytesIO(resp.content)


face_swap = FaceSwapAPI()

if __name__ == '__main__':
    import asyncio

    async def main():
        with open('../tmp.WEBP', 'rb') as f:
            t = io.BytesIO(f.read())

        with open('../tmp.WEBP', 'rb') as f:
            s = io.BytesIO(f.read())

        face = FaceSwapAPI()
        o = await face.face_swap(t, s)

        with open('../tmp2.WEBP', 'wb') as f:
            f.write(o.read())


    asyncio.run(main())
