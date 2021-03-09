import typing
from aiohttp import ClientSession, ClientTimeout, TCPConnector, hdrs


class DumbReader(typing.BinaryIO):
    def write(self, s: typing.Union[bytes, bytearray]) -> int:
        pass

    def mode(self) -> str:
        pass

    def name(self) -> str:
        pass

    def close(self) -> None:
        pass

    def closed(self) -> bool:
        pass

    def fileno(self) -> int:
        pass

    def flush(self) -> None:
        pass

    def isatty(self) -> bool:
        pass

    def readable(self) -> bool:
        pass

    def readline(self, limit: int = -1) -> typing.AnyStr:
        pass

    def readlines(self, hint: int = -1) -> typing.List[typing.AnyStr]:
        pass

    def seek(self, offset: int, whence: int = 0) -> int:
        pass

    def seekable(self) -> bool:
        pass

    def tell(self) -> int:
        pass

    def truncate(self, size: int = None) -> int:
        pass

    def writable(self) -> bool:
        pass

    def write(self, s: typing.AnyStr) -> int:
        pass

    def writelines(self, lines: typing.List[typing.AnyStr]) -> None:
        pass

    def __enter__(self) -> 'typing.IO[typing.AnyStr]':
        pass

    def __exit__(self, type, value, traceback) -> None:
        pass


class URLReader(DumbReader):
    def __init__(self, session):
        self._buf = b''
        self.session = session

    @staticmethod
    async def create(url, session, headers=None):
        u = URLReader(session)
        u.request = await u.session.get(url, headers=headers)
        u.request.raise_for_status()
        # u.request = await asks.get(url, headers=headers, stream=True, max_redirects=5)
        # u.body = u.request.body(timeout=14400)
        return u

    def get_file_name(self):
        return self.request.content_disposition.filename

    def get_file_size(self):
        return self.request.headers.get(hdrs.CONTENT_LENGTH, f'{100*1024*1024}')

    async def read(self, n: int = -1):
        buf = b''
        if len(self._buf) != 0:
            buf += self._buf
            self._buf = b''
        if n == -1:
            return await self.request.read()

        while len(buf) < n:
            _data = await self.request.content.read(n)
            if len(_data) == 0:
                break
            buf += _data
        if len(buf) > n != -1:
            self._buf = buf[n:]
            return buf[:n]
        else:
            return buf

    async def close(self) -> None:
        # self.request.release()
        await self.session.__aexit__(exc_type=None, exc_val=None, exc_tb=None)

    def __aiter__(self):
        return self

    async def __anext__(self):
        b = await self.read(512 * 1024)
        if len(b) == 0:
            raise StopAsyncIteration()
        else:
            return b
