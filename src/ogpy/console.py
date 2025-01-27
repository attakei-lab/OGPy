"""CLI entrypoint."""

import argparse
import sys

from . import types
from .client import fetch

parser = argparse.ArgumentParser(
    description="Parse and display OGP metadata from content."
)
parser.add_argument("url", type=str, help="Target URL")


def display(data: types.Metadata):
    """Display metadata as user-readable on console."""
    print("## Basic metadata")
    print("")
    print(f"title: {data.title}")
    print(f"url:   {data.url}")
    print(f"type:  {data.type}")
    if data.images:
        print(f"image: {len(data.images)} items")
        for image in data.images:
            print(f"\t- url:    {image.url}")
            print(f"\t  alt:    {image.alt or '(none)'}")
            print(f"\t  width:  {image.width or '(none)'}")
            print(f"\t  height: {image.height or '(none)'}")
    else:
        print("image:\t(none)")
    print("")
    #
    print("## Optional metadata")
    print("")
    if data.audio:
        print(f"audio:            {data.audio}")
    if data.description:
        print(f"description:      {data.description}")
    if data.determiner:
        print(f"determiner:       {data.determiner}")
    if data.locale:
        print(f"locale:           {data.locale}")
    if data.locale_alternates:
        print(f"locale:alternate: {','.join(data.locale_alternates)}")
    if data.video:
        print(f"video:            {data.video}")
    print("")


def main(argv: list[str] | None = None):
    argv = argv or sys.argv[1:]
    args = parser.parse_args(argv)
    try:
        data = fetch(args.url)
        display(data)
    except Exception as err:
        sys.stderr.write(f"{err}\n")
