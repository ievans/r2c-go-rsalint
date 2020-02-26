#!/usr/bin/env python3

import json
import os
import sys


def make_results(json, base_path):
    output = []
    print(json, file=sys.stderr)
    for directory, results in json.items():

        results = results["rsalint"]
        for result in results:
            path = result["posn"].split(":")[0]

            path = os.path.relpath(path, base_path)
            if path.startswith("./"):
                path = path[2:]

            line = int(result["posn"].split(":")[1])
            col = int(result["posn"].split(":")[2])
            obj = {
                "check_id": result["message"],
                "path": path,
                "start": {"line": line, "col": col},
                "end": {},
            }
            # if element["line_number"]:
            #    obj["start"]["line"] = element["line_number"]
            # if element["line_range"]:
            #     obj["start"]["col"] = element["line_range"][0]
            #     if len(element["line_range"]) > 1:
            #         obj["end"]["line"] = element["line_number"]
            #         obj["end"]["col"] = element["line_range"][-1]

            if "end" in obj and not "line" in obj["end"]:
                obj["end"]["line"] = obj["start"]["line"]
            output.append(obj)
    return output


def format_json(json_output, stream, base):
    results = make_results(json_output, base)
    obj = {"results": results}
    json.dump(obj, stream, indent=4, separators=(",", ": "))


if __name__ == "__main__":
    base = sys.argv[1]
    json_output = json.loads(sys.stdin.read())
    format_json(json_output, sys.stdout, base)
