#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def build_profile(vector_path: Path, revision: str):
    direct = json.loads(vector_path.read_text(encoding="utf-8"))["direct_rail_v1"]
    task = direct["task_hash"]["inputs"]
    report = direct["inputs"]
    return {
        "implementation": "osr21/flop-protocol-reproducibility-audits",
        "revision": revision,
        "input": {
            "genesisHashHex": task["genesis_hash_hex"],
            "agentAccountId32Hex": task["agent_account_id32_hex"],
            "nonce": task["nonce"],
            "modelHashHex": task["model_hash_hex"],
            "payloadHashHex": task["payload_hash_hex"],
            "commitHashHex": task["commit_hash_hex"],
            "gnWeight": report["gn_weight"],
            "latencyMs": report["latency_ms"],
            "outputHashHex": report["output_hash_hex"],
            "decodePolicyHashHex": report["decode_policy_hash_hex"],
            "teeTypeScaleHex": f'{report["tee_type"]["scale_tag"]:02x}',
        },
        "observed": {
            "taskHashHex": direct["task_hash"]["hash_hex"],
            "reportDataHex": direct["report_data_hex"],
            "legacyTaskU64Accepted": False,
            "legacyTaskU32Accepted": False,
            "bareReportDataAccepted": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vector", type=Path, default=Path(__file__).parent / "evidence" / "direct-rail-v1.json")
    parser.add_argument("--revision", default="unknown")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(build_profile(args.vector, args.revision), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
