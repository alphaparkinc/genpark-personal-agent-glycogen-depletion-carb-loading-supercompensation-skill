# -*- coding: utf-8 -*-
"""MCP Server for Muscle Glycogen Depletion & Carb-Loading Supercompensation Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import GlycogenCarbLoadingSupercompensationPlanner

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "calculate_supercompensation_carb_needs",
        "description": "Calculate precision carbohydrate intake (g/kg/day) and total hydration requirements to maximize skeletal muscle glycogen stores prior to race day.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "body_weight_kg": {
                    "type": "number"
                },
                "target_event_duration_hours": {
                    "type": "number"
                },
                "loading_window_days": {
                    "type": "integer",
                    "enum": [
                        1,
                        2,
                        3
                    ]
                }
            },
            "required": [
                "body_weight_kg",
                "target_event_duration_hours"
            ]
        }
    },
    {
        "name": "synthesize_low_fiber_meal_cadence",
        "description": "Synthesize a low-residue, low-fiber 36-hour fueling plan to minimize gastrointestinal distress while hitting 9g CHO/kg.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "daily_target_carbs_grams": {
                    "type": "integer"
                },
                "dietary_preference": {
                    "type": "string",
                    "enum": [
                        "standard",
                        "plant_based",
                        "gluten_free"
                    ]
                }
            },
            "required": [
                "daily_target_carbs_grams"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-glycogen-depletion-carb-loading-supercompensation-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(GlycogenCarbLoadingSupercompensationPlanner, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-personal-agent-glycogen-depletion-carb-loading-supercompensation-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-personal-agent-glycogen-depletion-carb-loading-supercompensation-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
