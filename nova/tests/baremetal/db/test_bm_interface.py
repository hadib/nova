# Copyright (c) 2012 NTT DOCOMO, INC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Baremetal DB testcase for PXE IP
"""

from nova import exception
from nova.tests.baremetal.db import base
from nova.virt.baremetal import db


class BareMetalPxeIpTestCase(base.BMDBTestCase):

    def setUp(self):
        super(BareMetalPxeIpTestCase, self).setUp()

    def test_unique_address(self):
        pif1_id = db.bm_interface_create(self.context, 1, '11:11:11:11:11:11',
                                         '0x1', 1)
        self.assertRaises(exception.DBError,
                          db.bm_interface_create,
                          self.context, 2, '11:11:11:11:11:11', '0x2', 2)

        # succeed after delete pif1
        db.bm_interface_destroy(self.context, pif1_id)
        pif2_id = db.bm_interface_create(self.context, 2, '11:11:11:11:11:11',
                                         '0x2', 2)
        self.assertTrue(pif2_id is not None)

    def test_unique_vif_uuid(self):
        pif1_id = db.bm_interface_create(self.context, 1, '11:11:11:11:11:11',
                                        '0x1', 1)
        pif2_id = db.bm_interface_create(self.context, 2, '22:22:22:22:22:22',
                                         '0x2', 2)
        db.bm_interface_set_vif_uuid(self.context, pif1_id, 'AAAA')
        self.assertRaises(exception.DBError,
                          db.bm_interface_set_vif_uuid,
                          self.context, pif2_id, 'AAAA')
