import setuptools


setuptools.setup(
    name="fineocr",
    version="0.1",
    url="https://github.com/kfur/fineocr",
    download_url='https://github.com/kfur/fineocr/archive/refs/tags/v0.1.tar.gz',

    author="Denis Skovpen",
    author_email="deniskovpen@gmail.com",

    description="FineScanner Mobile OCR for free",
    keywords=['OCR'],

    packages=['fineocr'],

    install_requires=[
        "aiohttp>=3.6",
        "aiofiles>=0.5",
    ],
    python_requires="~=3.7",

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Framework :: AsyncIO",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    entry_points="""
        [console_scripts]
        fineocr=fineocr.__main__:main
    """,
)
