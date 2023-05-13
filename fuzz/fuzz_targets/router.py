#!/usr/bin/env python3

import atheris
import sys
import os

with atheris.instrument_imports():
    from quart import Quart

def TestOneInput(input):
    fdp = atheris.FuzzedDataProvider(input)
    app = Quart(__name__)

    def view_func(*args, **kargs):
        pass

    for i in range(fdp.ConsumeIntInRange(1, 64)):
        try:
            app.add_url_rule(
                fdp.ConsumeUnicodeNoSurrogates(fdp.ConsumeIntInRange(0, 4096)),
                view_func
            )
        except ValueError:
            pass
        
def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()

if __name__ == "__main__":
    main()
