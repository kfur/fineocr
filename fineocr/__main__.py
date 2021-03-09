import asyncio
import sys
import aiofiles
import aiohttp
import logging
import os
from .finescanner import DocExportType, DocLangType, FineScannerTask, FineUser

import argparse

def format(format_str):
    for dtype in DocExportType:
        if format_str.lower() == dtype.value.lower():
            return dtype
    raise ValueError

def lang(lang_str):
    lsstr = lang_str.split('+')
    result = []
    for ls in lsstr:
        for ltype in DocLangType:
            if ls.lower() == ltype.value.lower():
                result.append(ltype)
    if result:
        return result
    else:
        raise ValueError

class _ListLangsAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help=None):
        super(_ListLangsAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        for dlang in DocLangType:
            print(dlang.value)
        parser.exit()

class _ListFormatsAction(argparse.Action):

    def __init__(self,
                 option_strings,
                 dest=argparse.SUPPRESS,
                 default=argparse.SUPPRESS,
                 help=None):
        super(_ListFormatsAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            default=default,
            nargs=0,
            help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        for dtype in DocExportType:
            print(dtype.value)
        parser.exit()

parser = argparse.ArgumentParser()
parser.add_argument('-lf', action=_ListFormatsAction,
                    help='list available formats')
parser.add_argument('-ll', action=_ListLangsAction, help='list available languages')
parser.add_argument('-t', metavar='FORMAT', required=True, type=format,
                    help='target format(example: -t epub)')
parser.add_argument('-l', metavar='langs', required=True, type=lang, help='source file languages,'
                                                               ' allowed up to 3 '
                                                               'simultaneous(example: -l English+French)')
parser.add_argument('source_file', help='source file path')
# parser.
args = parser.parse_args()

async def start() -> None:
    pass
    fine_scanner_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1800,
                                                                               connect=100,
                                                                               sock_connect=100,
                                                                               sock_read=60))
    fstat = os.stat(args.source_file)
    fname = os.path.basename(args.source_file)
    token = await (await FineUser.create_new(fine_scanner_session)).get_token()
    ftask = FineScannerTask(token, fine_scanner_session)
    async with aiofiles.open(args.source_file, mode='rb') as file:
        await ftask.upload_file(file, fname, fstat.st_size)

    await ftask.run_task(args.t, args.l)

    while True:
        status = await ftask.task_status()
        if status['Status'] == 'Processing' or status['Status'] == 'Awaiting':
            await asyncio.sleep(15)
        else:
            break
    result = status['ResultStatus']
    if result == 'Success':
        async with aiofiles.open(f"{os.getcwd()}/{status['ResultFilename']}", 'wb') as rfile:
            async for data in await ftask.get_result():
                await rfile.write(data)
    else:
        raise status

    await fine_scanner_session.close()

try:
    asyncio.get_event_loop().run_until_complete(start())
except Exception as e:
    logging.exception(e)
    sys.exit(1)