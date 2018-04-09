from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile
import argparse

from os import PathLike
from typing import Union


def zip_dir(zip_name: str, source_dir: Union[str, PathLike], like_file: str):
    src_path = Path(source_dir).expanduser().resolve(strict=True)
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zf:
        for file in src_path.rglob(like_file):
            zf.write(file, file.relative_to(src_path.parent))

def help_msg():
    """ help to describe the script"""
    help_str = """
               """
    return help_str


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=help_msg())
    parser.add_argument('-d', '--directory_report',
                        default='C:\Working\\rgarofal_DOCUMENT\\Fastweb\RCO_BPA\\NPS_ASSISTENZA_TECNICA',
                        help='Directory dove risiedono i report ', required=False)

    args = parser.parse_args()
    list_files = ['NPS SINGLE CONTACT TECNICA 2.0.docx', 'NPS SINGLE CONTACT TECNICA 2.0_new.docx']

    directory = args.directory_report
    print(directory)
    zip_dir("prova_file.zip", directory, "NPS SINGLE CONTACT TECNICA*.docx")
