#!/usr/bin/env python3

from mnamer.argument import ArgParser
from mnamer.const import IS_DEBUG
from mnamer.frontends import *
from mnamer.settings import Settings
from mnamer.types import MessageType


def main(gui=False):  # pragma: no cover
    """
    A wrapper for the program entrypoint that formats uncaught exceptions in a
    crash report template.
    """
    try:
        settings = Settings(load_configuration=True, load_arguments=True)
    except MnamerException as e:
        tty.msg(str(e), MessageType.ERROR)
        raise SystemExit(1)
    frontend = Gui if gui or settings.gui else Cli
    if frontend is Cli and not settings.has_valid_arguments:
        tty.msg(ArgParser.usage, MessageType.ERROR)
        raise SystemExit(1)
    if IS_DEBUG:
        # allow exceptions to raised when debugging
        frontend(settings).launch()
    else:
        # wrap exceptions in crash report under normal operation
        try:
            frontend(settings).launch()
        except SystemExit:
            raise
        except:
            tty.crash_report()


def main_gui():  # pragma: no cover
    main(gui=True)


if __name__ == "__main__":  # pragma: no cover
    main()
