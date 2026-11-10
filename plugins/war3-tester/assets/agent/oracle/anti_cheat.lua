-- ============================================================================
-- oracle/anti_cheat.lua - 黑盒防作弊看门狗 Oracle (v0.22.1)
-- ============================================================================

local oracle = require 'script.src.auto-test.agent.oracle.init'
local entity_ref = require 'script.src.auto-test.agent.entity_ref'

oracle.register({
    name = "anti_cheat",
    interval = 1.0,
    severity = "fatal",
    check = function(ctx)
        local violations = {}

        -- 1. 监控全局变量篡改（如虚构时间流逝）
        if _G.__adv_test_seconds or _G.__test_time_warp then
            table.insert(violations, {
                subject = "global",
                msg = "检测到全局时间篡改变量污染（如 _G.__adv_test_seconds）",
                data = { time_warp = tostring(_G.__adv_test_seconds or _G.__test_time_warp) }
            })
        end

        -- 2. 监控敌方/Boss 单位非法定身 (PauseUnit)
        if Game and Game.curState and Game.curState().engine then
            local units = Game.curState().engine:getEntitiesWithComponent('UnitComp') or {}
            for _, u in pairs(units) do
                if u.handle and u.isAlive and u:isAlive() and u.isEnemy and u:isEnemy() then
                    local is_paused = IsUnitPaused and IsUnitPaused(u.handle)
                    if is_paused and not u._legit_stunned then
                        local ref = entity_ref.get_ref(u)
                        table.insert(violations, {
                            subject = ref,
                            msg = "检测到敌方/Boss 单位被非法定身 (PauseUnit)",
                            data = { ref = ref, handle = tostring(u.handle) }
                        })
                    end
                end
            end
        end

        return #violations > 0 and violations or nil
    end
})
