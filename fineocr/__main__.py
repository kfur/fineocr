import asyncio
import sys
import aiofiles
import aiohttp
import logging
import os
import pickle
from os import path
from .finescanner import DocExportType, DocLangType, FineScannerTask, FineUser
from .spinner import LineSpinner
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
parser.add_argument('-ll', action=_ListLangsAction,
                    help='list available languages')
parser.add_argument('-t', metavar='format', required=True, type=format,
                    help='target format(example: -t epub)')
parser.add_argument('-l', metavar='languages', required=True, type=lang, help='source file languages,'
                    ' allowed up to 3 '
                    'simultaneous(example: -l English+French)')
parser.add_argument('-o', metavar='output', required=False,
                    help='output destination file name')
parser.add_argument('source_file', help='source file path')
# parser.
args = parser.parse_args()


async def start() -> None:
    pass
    fine_scanner_session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=1800,
                                                                               connect=100,
                                                                               sock_connect=100))
    fstat = os.stat(args.source_file)
    fname = os.path.basename(args.source_file)
    config_path = path.expanduser("~") + path.sep + '.fineocr'
    # load creadits or create one
    try:
        fine_user_uuid = pickle.load(open(config_path, mode='rb'))
        fine_user = FineUser(fine_user_uuid, fine_scanner_session)
    except FileNotFoundError:
        fine_user = await FineUser.create_new(fine_scanner_session)
        pickle.dump(fine_user.uuid, open(config_path, mode='wb'))
    token = await fine_user.get_token()
    ftask = FineScannerTask(token, fine_scanner_session)

    # uploading file to server
    line_spinner = LineSpinner(message='Uploading to server... ')
    async with aiofiles.open(args.source_file, mode='rb') as file:
        upload_task = asyncio.get_event_loop().create_task(
            ftask.upload_file(file, fname, fstat.st_size))
        while upload_task.done() is not True:
            await asyncio.sleep(0.5)
            line_spinner.next()

    # run convering and wait for competance
    line_spinner.message = 'Converting... '
    await ftask.run_task(args.t, args.l)
    while True:
        status = await ftask.task_status()
        if status['Status'] == 'Processing' or status['Status'] == 'Awaiting':
            # wait 15 seconds like official apps do
            c = 30
            while c:
                await asyncio.sleep(0.5)
                line_spinner.next()
                c -= 1
        else:
            break
    result = status['ResultStatus']
    if result == 'Success':
        # saving file
        line_spinner.writeln('Downloading file')
        async with aiofiles.open(args.o if args.o else f"{os.getcwd()}/{status['ResultFilename']}", 'wb') as rfile:
            async for data in await ftask.get_result():
                await rfile.write(data)
        line_spinner.writeln('Done')
    else:
        line_spinner.writeln(f"Failed OCR: {result}")

    line_spinner.finish()
    await fine_scanner_session.close()


def main():
    try:
        asyncio.get_event_loop().run_until_complete(start())
    except Exception as e:
        logging.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
