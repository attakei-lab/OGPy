"""CLI entrypoint."""

import argparse
import json
import sys
from dataclasses import asdict

from . import types
from .client import fetch

parser = argparse.ArgumentParser(
    description="Parse and display OGP metadata from content."
)
parser.add_argument("--fuzzy", default=False, action="store_true")
parser.add_argument("--format", default="text", choices=["text", "json"])
parser.add_argument("url", type=str, help="Target URL")


def display(data: types.Metadata | types.MetadataFuzzy):
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
        print("image: No items")
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
    if data.site_name:
        print(f"site_name:        {data.site_name}")
    if data.video:
        print(f"video:            {data.video}")
    print("")


def main(argv: list[str] | None = None):
    argv = argv or sys.argv[1:]
    args = parser.parse_args(argv)
    try:
        data = fetch(args.url, args.fuzzy)
        if args.format == "text":
            display(data)
        elif args.format == "json":
            print(json.dumps(asdict(data)))
        else:
            raise ValueError("Invalid format.")
    except Exception as err:
        sys.stderr.write(f"{err}\n")
