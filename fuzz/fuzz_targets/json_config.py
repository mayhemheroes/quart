#!/usr/bin/env python3

import atheris
import sys
import os

with atheris.instrument_imports():
    from quart import Quart
    import json
    import toml

def TestOneInput(input):
    fdp = atheris.FuzzedDataProvider(input)

    app = Quart(__name__)

    config_str = fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(0, 4096))
    with open("fuzz/fuzz_targets/filename.toml", "w") as file:
        file.write(config_str)
    with open("fuzz/fuzz_targets/filename.json", "w") as file:
        file.write(config_str)

    try:
        app.config.from_file("filename.json", json.load)
    except json.decoder.JSONDecodeError:
        pass

    try:
        app.config.from_file("filename.toml", toml.load)
    except toml.decoder.TomlDecodeError:
        pass

def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
