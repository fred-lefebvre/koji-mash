# Copyright (c) 2013 - Mathieu Bridon
#
# This plugin is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This plugin is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this plugin.  If not, see <http://www.gnu.org/licenses/>.


import logging

import koji
from koji.context import context


# FIXME: This is pretty disgusting
kojihub = {"__name__": "anything but __main__"}
execfile("/usr/share/koji-hub/kojihub.py", kojihub)
make_task = kojihub["make_task"]


log = logging.getLogger("koji.plugin.kojihub_mash_handler")


def mash_tree(mash_target, build_tag, mash_opts, priority=None):
    """Mash the repository tree"""
    log.debug("Mashing '%s'..." % mash_target)

    context.session.assertPerm("admin")

    task_opts = {'channel': 'mash'}
    if priority is not None:
        task_opts["priority"] = koji.PRIO_DEFAULT + priority

    return make_task('mashTree', [mash_target, build_tag, mash_opts],
                     **task_opts)


# Export the handler so it is accessible through the Hub's XMLRPC API
mash_tree.exported = True
