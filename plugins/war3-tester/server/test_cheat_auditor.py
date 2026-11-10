# -*- coding: utf-8 -*-
"""
test_cheat_auditor.py -- 静态作弊特征审计器与三盒定级分类器 (v0.22.1)

功能：
1. 静态扫描测试脚本中的 5 大白盒作弊毒药特征：
   - 虚构时间变量 (fake_time, e.g. _G.__adv_test_seconds, __test_time_warp)
   - 定身敌怪 (pause_unit, e.g. PauseUnit, PauseUnitBJ)
   - 核弹秒杀与强杀 (kill_unit, e.g. KillUnit, 1e12, 1000000000000)
   - 伪造死亡回调 (fake_death, e.g. mock_death, fireEvent.*death)
   - 私有变量篡改 (private_tamper, e.g. ._private, rawset)
2. 推断三盒定级 (box_tier: 'black_box' | 'gray_box' | 'white_box_stub')
3. 识别伪黑盒风险 (is_spoofed_blackbox: 脚本声称是黑盒/e2e，但含有作弊特征)
4. 目录级别纯度体检与统计 (audit_directory)
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Union


class TestCheatAuditor:
    """War3 自动化测试用例作弊审计与三盒定级分类器"""

    # 5 大作弊特征的正则表达式规则
    CHEAT_PATTERNS = {
        'fake_time': [
            r'__adv_test_seconds',
            r'__test_time_warp',
            r'_G\.__time',
            r'advance_test_time',
        ],
        'pause_unit': [
            r'PauseUnit\s*\(',
            r'PauseUnitBJ\s*\(',
            r':pause\s*\(',
        ],
        'kill_unit': [
            r'KillUnit\s*\(',
            r'KillUnitBJ\s*\(',
            r'1e12',
            r'1000000000000',
            r'999999999',
            r':set_hp\s*\(\s*0\s*\)',
        ],
        'fake_death': [
            r'mock_death',
            r'fake_death',
            r'fireEvent\s*\(\s*[\'"][^\'"]*death',
            r'on_death\s*\(',
        ],
        'private_tamper': [
            r'\._[a-zA-Z0-9]+',
            r'rawset\s*\(',
        ],
    }

    # 黑盒用例名称与内容特征
    BLACKBOX_INDICATORS = [
        r'e2e',
        r'black_?box',
        r'黑盒',
        r'拟真',
    ]

    # 桌面单测特征
    UNIT_INDICATORS = [
        r'unit',
        r'mock',
        r'jass_mock',
        r'单测',
    ]

    @classmethod
    def audit_file(cls, file_path: Union[str, Path]) -> Dict[str, Any]:
        """审计单个测试文件的作弊特征与三盒纯度"""
        path = Path(file_path)
        filename = path.name
        content = ""
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            pass

        detected_cheats: List[str] = []
        for cheat_type, patterns in cls.CHEAT_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, content):
                    if cheat_type not in detected_cheats:
                        detected_cheats.append(cheat_type)
                    break

        has_cheats = len(detected_cheats) > 0

        # 判断是否声称是黑盒
        claims_blackbox = any(
            re.search(ind, filename, re.IGNORECASE) or re.search(ind, content, re.IGNORECASE)
            for ind in cls.BLACKBOX_INDICATORS
        )

        # 判断是否是单元测试
        is_unit = any(
            re.search(ind, filename, re.IGNORECASE)
            for ind in cls.UNIT_INDICATORS
        ) or "jass_mock" in content

        # 推断三盒定级
        if is_unit or (has_cheats and not claims_blackbox):
            box_tier = "white_box_stub"
        elif claims_blackbox and has_cheats:
            box_tier = "white_box_stub"  # 含作弊降级为白盒桩
        elif claims_blackbox and not has_cheats:
            box_tier = "black_box"
        else:
            box_tier = "gray_box"

        is_spoofed_blackbox = claims_blackbox and has_cheats

        return {
            'file': filename,
            'filename': filename,
            'path': str(path),
            'box_tier': box_tier,
            'has_cheats': has_cheats,
            'cheat_types': detected_cheats,
            'is_spoofed_blackbox': is_spoofed_blackbox,
        }

    @classmethod
    def audit_directory(cls, dir_path: Union[str, Path]) -> Dict[str, Any]:
        """审计整个测试目录，输出三盒纯度分布与伪黑盒告警清单"""
        directory = Path(dir_path)
        spoofed = []
        black_box = []
        gray_box = []
        white_box = []

        if directory.exists() and directory.is_dir():
            for f in sorted(directory.glob("test_*.lua")):
                audit = cls.audit_file(f)
                tier = audit['box_tier']
                if audit['is_spoofed_blackbox']:
                    spoofed.append(audit)
                if tier == 'black_box':
                    black_box.append(audit)
                elif tier == 'gray_box':
                    gray_box.append(audit)
                else:
                    white_box.append(audit)

        return {
            "spoofed_blackbox": spoofed,
            "black_box": black_box,
            "gray_box": gray_box,
            "white_box_stub": white_box,
            "total": len(black_box) + len(gray_box) + len(white_box),
        }
