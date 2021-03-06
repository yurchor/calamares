#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <https://github.com/calamares> ===
#
#   Copyright 2014 - 2015, Philip Müller <philm@manjaro.org>
#   Copyright 2014, Teo Mrnjavac <teo@kde.org>
#   Copyright 2017, Alf Gaida <agaida@siduction.org>
#   Copyright 2017-2018, Gabriel Craciunescu <crazy@frugalware.org>
#   Copyright 2019, Adriaan de Groot <groot@kde.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import libcalamares

import gettext
_ = gettext.translation("calamares-python",
                        localedir=libcalamares.utils.gettext_path(),
                        languages=libcalamares.utils.gettext_languages(),
                        fallback=True).gettext


def pretty_name():
    return _("Setting hardware clock.")


def run():
    """
    Set hardware clock.
    """
    hwclock_rtc = ["hwclock", "--systohc", "--utc"]
    hwclock_isa = ["hwclock", "--systohc", "--utc", "--directisa"]
    is_broken_rtc = False
    is_broken_isa = False

    ret = libcalamares.utils.target_env_call(hwclock_rtc)
    if ret != 0:
        is_broken_rtc = True
        libcalamares.utils.debug("Hwclock returned error code {}".format(ret))
        libcalamares.utils.debug("  .. RTC method failed, trying ISA bus method.")
    else:
        libcalamares.utils.debug("Hwclock set using RTC method.")
    if is_broken_rtc:
        ret = libcalamares.utils.target_env_call(hwclock_isa)
        if  ret != 0:
            is_broken_isa = True
            libcalamares.utils.debug("Hwclock returned error code {}".format(ret))
            libcalamares.utils.debug("  .. ISA bus method failed.")
        else:
            libcalamares.utils.debug("Hwclock set using ISA bus method.")
    if is_broken_rtc and is_broken_isa:
        libcalamares.utils.debug("BIOS or Kernel BUG: Setting hwclock failed.")

    return None
