# -*- coding: utf-8 -*-
import unittest
import tempfile
from pathlib import Path
from test_cheat_auditor import TestCheatAuditor

class TestCheatAuditorTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.dir_path = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_clean_blackbox(self):
        f = self.dir_path / "test_hero_e2e.lua"
        f.write_text("""
        -- 黑盒测试：模拟玩家输入
        test('select hero', function()
            s:step('select')
        end)
        """, encoding="utf-8")
        res = TestCheatAuditor.audit_file(f)
        self.assertEqual(res['box_tier'], 'black_box')
        self.assertFalse(res['has_cheats'])
        self.assertFalse(res['is_spoofed_blackbox'])

    def test_spoofed_blackbox_with_pause_unit(self):
        f = self.dir_path / "test_boss_e2e.lua"
        f.write_text("""
        -- 黑盒测试
        PauseUnit(boss, true)
        """, encoding="utf-8")
        res = TestCheatAuditor.audit_file(f)
        self.assertEqual(res['box_tier'], 'white_box_stub')
        self.assertTrue(res['has_cheats'])
        self.assertIn('pause_unit', res['cheat_types'])
        self.assertTrue(res['is_spoofed_blackbox'])

    def test_white_box_unit(self):
        f = self.dir_path / "test_damage_unit.lua"
        f.write_text("""
        require 'jass_mock'
        assert(calc_damage(100, 20) == 80)
        """, encoding="utf-8")
        res = TestCheatAuditor.audit_file(f)
        self.assertEqual(res['box_tier'], 'white_box_stub')

    def test_audit_directory(self):
        (self.dir_path / "test_a_e2e.lua").write_text("PauseUnit(u)", encoding="utf-8")
        (self.dir_path / "test_b_e2e.lua").write_text("s:step('move')", encoding="utf-8")
        (self.dir_path / "test_c.lua").write_text("EventBus:fire('abc')", encoding="utf-8")

        purity = TestCheatAuditor.audit_directory(self.dir_path)
        self.assertEqual(len(purity['spoofed_blackbox']), 1)
        self.assertEqual(len(purity['black_box']), 1)
        self.assertEqual(len(purity['gray_box']), 1)
        self.assertEqual(purity['total'], 3)

if __name__ == '__main__':
    unittest.main()
