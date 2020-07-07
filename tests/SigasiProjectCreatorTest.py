# -*- coding: utf-8 -*-
"""
    :copyright: (c) 2008-2017 Sigasi
    :license: BSD, see LICENSE for more details.
"""
import unittest

import SigasiProjectCreator.Creator as sPC
import SigasiProjectCreator.VerilogVersion as VerilogVersion
import SigasiProjectCreator.VhdlVersion as VhdlVersion
from SigasiProjectCreator.Creator import SigasiProjectCreator


class SigasiProjectCreatorTest(unittest.TestCase):
    # No teardown needed, a new creator is created every instance
    def setUp(self):
        self.creator = SigasiProjectCreator('tutorial')

    def test_check_hdl_versions_both_none(self):
        with self.assertRaises(ValueError) as exc:
            sPC.check_hdl_versions(None, None)
        self.assertTrue(
            '''Only 93, 2002, 2008 is/are allowed as VHDL version number.
Only v2005 is/are allowed as Verilog version number.''' == str(exc.exception))

    def test_check_hdl_versions_vhdl_none(self):
        sPC.check_hdl_versions(None, VerilogVersion.TWENTY_O_FIVE)

    def test_check_hdl_versions_verilog_none(self):
        sPC.check_hdl_versions(VhdlVersion.NINETY_THREE, None)

    def test_check_hdl_versions_both_correct(self):
        sPC.check_hdl_versions(VhdlVersion.NINETY_THREE, VerilogVersion.TWENTY_O_FIVE)

    def test_check_hdl_versions_vhdl_wrong(self):
        with self.assertRaises(ValueError) as exc:
            sPC.check_hdl_versions(VerilogVersion.TWENTY_O_FIVE, VerilogVersion.TWENTY_O_FIVE)
        self.assertTrue("Only 93, 2002, 2008 is/are allowed as VHDL version number." == str(exc.exception))

    def test_check_hdl_versions_verilog_wrong(self):
        with self.assertRaises(ValueError) as exc:
            sPC.check_hdl_versions(VhdlVersion.NINETY_THREE, VhdlVersion.NINETY_THREE)
        self.assertTrue("Only v2005 is/are allowed as Verilog version number." == str(exc.exception))

    def test_check_hdl_versions_both_wrong(self):
        with self.assertRaises(ValueError) as exc:
            sPC.check_hdl_versions(VerilogVersion.TWENTY_O_FIVE, VhdlVersion.NINETY_THREE)
        self.assertTrue(
            '''Only 93, 2002, 2008 is/are allowed as VHDL version number.
Only v2005 is/are allowed as Verilog version number.''' == str(exc.exception))
