"""
MCP Server for Ocular Corneal Hysteresis Biomechanics (ORA) Skill.
Exposes tools for dynamic applanation biomechanics, IOP compensation, and interocular asymmetry detection.
"""

import sys
import json
from typing import Any, Dict
from client import OcularCornealBiomechanicsClient


def format_response(data: Any) -> str:
    return json.dumps(data, indent=2)


def main():
    """Simple FastMCP-compatible stdio JSON-RPC interface."""
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
        except Exception:
            continue

        method = req.get("method")
        params = req.get("params", {})
        req_id = req.get("id")

        if method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "compute_corneal_biomechanics",
                            "description": "Calculates Corneal Hysteresis (CH), Corneal Resistance Factor (CRF), Goldmann-correlated IOP (IOPg), and Corneal-Compensated IOP (IOPcc) from air-pulse applanation peaks.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "target_eye": {
                                        "type": "string",
                                        "description": "Target eye ('OD', 'OS', or 'OU'). Default: 'OD'."
                                    },
                                    "p1_applanation_pressure_mmhg": {
                                        "type": "number",
                                        "description": "Inward applanation peak pressure in mmHg."
                                    },
                                    "p2_applanation_pressure_mmhg": {
                                        "type": "number",
                                        "description": "Outward applanation recovery peak pressure in mmHg."
                                    },
                                    "central_corneal_thickness_um": {
                                        "type": "number",
                                        "description": "Optional Central Corneal Thickness (CCT) in micrometers."
                                    },
                                    "peak1_amplitude": {
                                        "type": "number",
                                        "description": "Optional infrared applanation peak 1 signal amplitude."
                                    },
                                    "peak2_amplitude": {
                                        "type": "number",
                                        "description": "Optional infrared applanation peak 2 signal amplitude."
                                    }
                                },
                                "required": ["p1_applanation_pressure_mmhg", "p2_applanation_pressure_mmhg"]
                            }
                        },
                        {
                            "name": "assess_bilateral_asymmetry",
                            "description": "Analyzes interocular biomechanical asymmetry between right and left eyes to screen for unilateral ectasia or asymmetric glaucomatous damage.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "od_results": {
                                        "type": "object",
                                        "description": "Output dictionary from compute_corneal_biomechanics for OD."
                                    },
                                    "os_results": {
                                        "type": "object",
                                        "description": "Output dictionary from compute_corneal_biomechanics for OS."
                                    }
                                },
                                "required": ["od_results", "os_results"]
                            }
                        }
                    ]
                }
            }
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()

        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            target_eye = args.get("target_eye", "OD")
            client = OcularCornealBiomechanicsClient(target_eye=target_eye)

            try:
                if name == "compute_corneal_biomechanics":
                    p1 = args.get("p1_applanation_pressure_mmhg")
                    p2 = args.get("p2_applanation_pressure_mmhg")
                    cct = args.get("central_corneal_thickness_um")
                    pk1 = args.get("peak1_amplitude")
                    pk2 = args.get("peak2_amplitude")
                    result = client.compute_corneal_biomechanics(p1, p2, cct, pk1, pk2)
                elif name == "assess_bilateral_asymmetry":
                    od_res = args.get("od_results", {})
                    os_res = args.get("os_results", {})
                    result = client.assess_bilateral_asymmetry(od_res, os_res)
                else:
                    result = {"error": f"Unknown tool name: {name}"}

                sys.stdout.write(json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {"content": [{"type": "text", "text": format_response(result)}]}
                }) + "\n")
                sys.stdout.flush()
            except Exception as e:
                sys.stdout.write(json.dumps({
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32000, "message": str(e)}
                }) + "\n")
                sys.stdout.flush()


if __name__ == "__main__":
    main()
