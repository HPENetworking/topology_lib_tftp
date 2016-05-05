# -*- coding: utf-8 -*-
#
# Copyright (C) 2016 Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
This library contains functions to configure and start a TFTP server on
Linux Workstations
"""

from __future__ import unicode_literals, absolute_import
from __future__ import print_function, division


def start_server(enode, path):
    """
    Start or restart the tftp server. Looks for xined config file followed
        by tftpd-hpa config file and uses the first service found.

    :param str path: sets the root folder for the tftp server
    """

    path = path.replace('/', '\/')

    if(enode('[ -f /etc/xinetd.d/tftp ] && echo "Y"') == 'Y'):
        cfg_file = "/etc/xinetd.d/tftp"
        enode("sed -i '/disable/ s/yes/no/' {}".format(cfg_file))
        enode("sed -i '/server_args/ s/=.*/= -s {}/' {}".format(path,
              cfg_file))
        enode("service xinetd restart")
    elif(enode('[ -f /etc/default/tftpd-hpa ] && echo "Y"') == 'Y'):
        cfg_file = "/etc/default/tftpd-hpa"
        enode("sed -i '/DIRECTORY/ s/=.*/=\"{}\"/' {}".format(path, cfg_file))
        enode("service tftpd-hpa restart")
    else:
        raise Exception(
            "Cannot find supported tftp service (no config file found)."
        )


def stop_server(enode):
    """
    Stop the TFTP server.
    """

    if(enode('[ -f /etc/xinetd.d/tftp ] && echo "Y"') == 'Y'):
        enode("service xinetd stop")
    elif(enode('[ -f /etc/default/tftpd-hpa ] && echo "Y"') == 'Y'):
        enode("service tftpd-hpa stop")
    else:
        raise Exception(
            "Cannot find supported tftp service (no config file found)."
        )

__all__ = [
    'start_server',
    'stop_server'
]
