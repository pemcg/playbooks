#! /usr/bin/python
#
# (c) 2017, Drew Bomhof <dbomhof@redhat.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = '''
module: manageiq_automate
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.manageiq import ManageIQ, manageiq_argument_spec

class ManageIQAutomate(object):
    """
        Object to execute automate workspace management operations in manageiq.
    """

    def __init__(self, manageiq):
        self._manageiq = manageiq
        self._guid = "cf2184c0-096e-4109-a970-f9a1b2691f86"

        self._module = self._manageiq.module
        self._api_url = self._manageiq.api_url
        self._client = self._manageiq.client

    def url(self):
        """
            The url to connect to the workspace
        """
        return '%s/automate_workspaces/%s' % ('http://localhost:3000/api', self._guid)


    def get(self):
        """
            Get any attribute, object from the REST API
        """
        result = self._client.get(self.url())
        return dict(result=result)


    def set(self, data):
        """
            Set any attribute, object from the REST API
        """
        result = self._client.post(self.url(), data)
        return  result


    def validate(self, obj, values):
        """
            Validate all passed objects before attempting to set or get values from them
        """
        #return bool(self.get(obj) == values)


class Workspace(ManageIQAutomate):
    """
        Object to modify and get the Workspace
    """

    def set_attribute(self, attribute):
        """
            Set the attribute called on the object with the passed in value
        """

        #result = self.set(attribute)
        result = attribute
        return dict(changed=True, object=result)

    def get_workspace(self):
        """
            Get the entire Workspace
        """

        workspace = self.get()
        return dict(changed=False, workspace=workspace)


    def get_attribute(self, attribute):
        """
            Get the passed in attribute from the Workspace
        """

        results = self.get()
        return dict(changed=False, workspace_attribute=results, attribute=attribute)


def main():
    """
        The entry point to the module
    """
    module = AnsibleModule(
            argument_spec=dict(
                manageiq_connection=dict(required=True, type='dict',
                                         options=manageiq_argument_spec()),
                get_workspace=dict(type='bool', default=False),
                set_attribute=dict(required=False, type='dict'),
                get_attribute=dict(required=False, type='dict')
                ),
            )

    get_attribute = module.params['get_attribute']
    get_workspace = module.params.get('get_workspace')
    set_attribute = module.params['set_attribute']

    manageiq = ManageIQ(module)
    workspace = Workspace(manageiq)

    result = None
    if get_workspace:
        result = workspace.get_workspace()
        module.exit_json(**result)
    for key, value in dict(get_attribute=get_attribute, set_attribute=set_attribute).iteritems():
        if value:
            result = getattr(workspace, key)(value)
            module.exit_json(**result)
    msg = "No workspace registered, possibly need pass get_workspace: True in the playbook"
    module.exit_json(msg=msg, params=module.params)


if __name__ == "__main__":
    main()
