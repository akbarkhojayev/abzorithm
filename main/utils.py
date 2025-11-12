import subprocess
import tempfile
import os
import time
import json
import resource
import signal
import shutil
import stat
import uuid
from pathlib import Path
import string
import ast

import json
import ast
import subprocess
import tempfile
import time
import os


def run_python_function(user_code: str, func_name: str, test_input: str, expected_output: str, timeout: int = 2):
    """
    Bitta test case ni tekshiradi
    """
    input_lines = test_input.replace('\r', '').strip().split("\n")
    args = []

    def _parse_value(val_str: str):
        s = val_str.strip()
        try:
            return json.loads(s)
        except Exception:
            pass
        try:
            return ast.literal_eval(s)
        except Exception:
            pass
        try:
            if s.isdigit() or (s.startswith('-') and s[1:].isdigit()):
                return int(s)
            return float(s)
        except Exception:
            pass
        return s

    for raw in input_lines:
        x = raw.strip()
        if not x:
            continue
        if '=' in x:
            _, right = x.split('=', 1)
            value = _parse_value(right)
            args.append(value)
            continue
        args.append(_parse_value(x))

    def _python_literal(val):
        try:
            return json.dumps(val, ensure_ascii=False)
        except TypeError:
            return repr(val)

    input_args = ", ".join(_python_literal(a) for a in args)

    # wrapper code
    code_wrapper = f"""
{user_code}

def __resolve_callable():
    _g = globals()
    name = {json.dumps(func_name)}
    candidates = []
    if "(" in name or "." in name:
        candidates.append(name)
    else:
        candidates.extend([
            f"Solution().{{name}}",
            "Solution().solve",
        ])
    for expr in candidates:
        try:
            fn = eval(expr, _g)
            if callable(fn):
                return fn
        except Exception:
            pass
    raise NameError(f"Callable not found for any of: {{candidates}}")

if __name__ == "__main__":
    try:
        __fn = __resolve_callable()
        result = __fn({input_args})
        try:
            import json as _json
            try:
                print(_json.dumps(result, ensure_ascii=False, separators=(',', ':')))
            except TypeError:
                print(str(result))
        except Exception:
            print(str(result))
    except Exception as e:
        import sys
        sys.stderr.write(str(e))
"""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp:
        tmp.write(code_wrapper)
        tmp_path = tmp.name

    start_time = time.time()
    try:
        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        exec_time = round(time.time() - start_time, 4)

        if result.returncode != 0:
            return False, "RuntimeError", result.stderr.strip(), exec_time

        output = result.stdout.replace('\r', '').strip()
        expected_output_clean = expected_output.replace('\r', '').strip()

        def _try_json_loads(s):
            try:
                return True, json.loads(s)
            except Exception:
                return False, s

        out_is_json, out_val = _try_json_loads(output)
        exp_is_json, exp_val = _try_json_loads(expected_output_clean)

        is_equal = False
        if out_is_json and exp_is_json:
            if isinstance(out_val, (int, float)) and isinstance(exp_val, (int, float)):
                is_equal = abs(float(out_val) - float(exp_val)) <= 1e-9
            else:
                is_equal = out_val == exp_val
        else:
            is_equal = output == expected_output_clean

        if is_equal:
            return True, "Accepted", output, exec_time
        else:
            return False, "Wrong Answer", f"Output: {output}", exec_time

    except subprocess.TimeoutExpired:
        return False, "TimeLimit", "⏰ Time Limit Exceeded", timeout
    except Exception as e:
        return False, "RuntimeError", str(e), 0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def run_all_tests(user_code: str, func_name: str, tests: list, timeout: int = 2):
    """
    Bir nechta testlarni ketma-ket ishlatadi.
    tests: [{"input": "...", "expected": "..."}]
    """
    results = []
    all_passed = True

    for t in tests:
        ok, status, output, exec_time = run_python_function(
            user_code,
            func_name,
            t["input"],
            t["expected"],
            timeout=timeout
        )
        results.append({
            "input": t["input"],
            "expected": t["expected"],
            "output": output,
            "status": status,
            "exec_time": exec_time
        })
        if not ok:
            all_passed = False

    final_status = "Accepted" if all_passed else "Partially Accepted"
    return final_status, results


def create_submission_json(code: str, func_name: str, test_input: str, expected_output: str, user_id: int, problem_id: int):
    ok, status, output, exec_time = run_python_function(code, func_name, test_input, expected_output)

    submission_json = {
        "code": code,
        "language": "python",
        "status": status,
        "execution_time": exec_time,
        "memory_used": 1024,
        "user": user_id,
        "problem": problem_id
    }
    return submission_json

import json
import ast
import string


def get_type(value):
    """Qiymatning tipini aniqlash (har doim aniq tip qaytaradi)."""
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "float"
    elif isinstance(value, str):
        return "str"
    elif isinstance(value, list):
        if not value:
            return "list"
        if all(isinstance(x, int) for x in value):
            return "list[int]"
        elif all(isinstance(x, str) for x in value):
            return "list[str]"
        elif all(isinstance(x, float) for x in value):
            return "list[float]"
        else:
            return "list"
    elif isinstance(value, dict):
        return "dict"
    elif value is None:
        return "None"
    else:
        return "object"


def generate_code_template(function_name: str, input_example: str, output_example: str = "", description: str = "") -> str:
    """
    LeetCode style Python template generator.
    input_example asosida parametr nomlari va ularning turlarini aniqlab beradi.
    """

    # --- Funksiya nomini tayyorlash ---
    name = function_name.strip()
    if "." in name:
        try:
            name = name.split(".")[-1]
            if name.endswith("()"):
                name = name[:-2]
        except Exception:
            pass
    if name.endswith("()"):
        name = name[:-2]
    method_name = name or "solve"

    # --- Input example tayyorlash ---
    input_example = input_example.strip().replace('\r', '')
    lines = [line.strip() for line in input_example.split("\n") if line.strip()]

    param_names = []
    param_types = []

    # --- Case 1: "name = value" format ---
    if any("=" in ln for ln in lines):
        for ln in lines:
            if "=" in ln:
                left, right = ln.split("=", 1)
                pname = left.strip()
                sanitized = ''.join(ch if ch.isalnum() or ch == '_' else '_' for ch in pname).strip('_') or 'arg'
                try:
                    val = ast.literal_eval(right.strip())
                except Exception:
                    try:
                        val = json.loads(right.strip())
                    except Exception:
                        val = right.strip()
                ptype = get_type(val)
                param_names.append(sanitized)
                param_types.append(ptype)

    # --- Case 2: JSON yoki dict ---
    elif len(lines) == 1:
        single = lines[0]
        parsed = None
        try:
            parsed = json.loads(single)
        except Exception:
            try:
                parsed = ast.literal_eval(single)
            except Exception:
                pass

        if isinstance(parsed, dict) and parsed:
            for k, v in parsed.items():
                param_names.append(k)
                param_types.append(get_type(v))
        elif isinstance(parsed, list):
            param_names = ["arr"]
            param_types = [get_type(parsed)]
        elif parsed is not None:
            param_names = ["a"]
            param_types = [get_type(parsed)]
        else:
            param_names = ["a"]
            param_types = ["object"]

    else:
        for i, ln in enumerate(lines):
            pname = string.ascii_lowercase[i]
            try:
                val = ast.literal_eval(ln)
            except Exception:
                val = ln
            param_names.append(pname)
            param_types.append(get_type(val))

    # --- Output type ---
    try:
        out_val = ast.literal_eval(output_example) if output_example else None
        return_type = get_type(out_val)
    except Exception:
        return_type = "object"

    params_str = ", ".join(
        f"{n}: {t}" for n, t in zip(param_names, param_types)
    )

    template = f'''class Solution:
    def {method_name}(self, {params_str}) -> {return_type}:
        # Kodingizni shu yerda yozing
        pass
'''
    return template




def generate_javascript_template(function_name: str, input_example: str, output_example: str = "") -> str:
    """
    JavaScript template generator - input_example'dan parametrlarni aniqlaydi
    """
    # Funksiya nomini tayyorlash
    name = function_name.strip()
    if "." in name:
        try:
            name = name.split(".")[-1]
            if name.endswith("()"):
                name = name[:-2]
        except Exception:
            pass
    if name.endswith("()"):
        name = name[:-2]
    method_name = name or "solve"

    # Input example tayyorlash
    input_example = input_example.strip().replace('\r', '')
    lines = [line.strip() for line in input_example.split("\n") if line.strip()]

    param_names = []
    
    # Case 1: "name = value" format
    if any("=" in ln for ln in lines):
        for ln in lines:
            if "=" in ln:
                left, right = ln.split("=", 1)
                pname = left.strip()
                sanitized = ''.join(ch if ch.isalnum() or ch == '_' else '_' for ch in pname).strip('_') or 'arg'
                param_names.append(sanitized)
    # Case 2: JSON yoki dict
    elif len(lines) == 1:
        single = lines[0]
        parsed = None
        try:
            parsed = json.loads(single)
        except Exception:
            try:
                parsed = ast.literal_eval(single)
            except Exception:
                pass

        if isinstance(parsed, dict) and parsed:
            param_names = list(parsed.keys())
        elif isinstance(parsed, list):
            param_names = ["arr"]
        elif parsed is not None:
            param_names = ["a"]
        else:
            param_names = ["a"]
    else:
        for i in range(len(lines)):
            param_names.append(string.ascii_lowercase[i])

    params_str = ", ".join(param_names) if param_names else "a, b"

    template = f'''class Solution {{
    {method_name}({params_str}) {{
        // Kodingizni shu yerda yozing
        return 0;
    }}
}}
'''
    return template


def generate_dart_template(function_name: str, input_example: str, output_example: str = "") -> str:
    """
    Dart template generator - input_example'dan parametrlarni aniqlaydi
    """
    # Funksiya nomini tayyorlash
    name = function_name.strip()
    if "." in name:
        try:
            name = name.split(".")[-1]
            if name.endswith("()"):
                name = name[:-2]
        except Exception:
            pass
    if name.endswith("()"):
        name = name[:-2]
    method_name = name or "solve"

    # Input example tayyorlash
    input_example = input_example.strip().replace('\r', '')
    lines = [line.strip() for line in input_example.split("\n") if line.strip()]

    param_names = []
    param_types = []
    
    # Case 1: "name = value" format
    if any("=" in ln for ln in lines):
        for ln in lines:
            if "=" in ln:
                left, right = ln.split("=", 1)
                pname = left.strip()
                sanitized = ''.join(ch if ch.isalnum() or ch == '_' else '_' for ch in pname).strip('_') or 'arg'
                try:
                    val = ast.literal_eval(right.strip())
                except Exception:
                    try:
                        val = json.loads(right.strip())
                    except Exception:
                        val = right.strip()
                
                # Dart type mapping
                dart_type = "dynamic"
                if isinstance(val, bool):
                    dart_type = "bool"
                elif isinstance(val, int):
                    dart_type = "int"
                elif isinstance(val, float):
                    dart_type = "double"
                elif isinstance(val, str):
                    dart_type = "String"
                elif isinstance(val, list):
                    if val and all(isinstance(x, int) for x in val):
                        dart_type = "List<int>"
                    elif val and all(isinstance(x, str) for x in val):
                        dart_type = "List<String>"
                    else:
                        dart_type = "List<dynamic>"
                
                param_names.append(sanitized)
                param_types.append(dart_type)
    # Case 2: JSON yoki dict
    elif len(lines) == 1:
        single = lines[0]
        parsed = None
        try:
            parsed = json.loads(single)
        except Exception:
            try:
                parsed = ast.literal_eval(single)
            except Exception:
                pass

        if isinstance(parsed, dict) and parsed:
            for k, v in parsed.items():
                dart_type = "dynamic"
                if isinstance(v, bool):
                    dart_type = "bool"
                elif isinstance(v, int):
                    dart_type = "int"
                elif isinstance(v, float):
                    dart_type = "double"
                elif isinstance(v, str):
                    dart_type = "String"
                elif isinstance(v, list):
                    dart_type = "List<dynamic>"
                param_names.append(k)
                param_types.append(dart_type)
        elif isinstance(parsed, list):
            param_names = ["arr"]
            param_types = ["List<dynamic>"]
        elif parsed is not None:
            param_names = ["a"]
            param_types = ["dynamic"]
        else:
            param_names = ["a"]
            param_types = ["dynamic"]
    else:
        for i in range(len(lines)):
            param_names.append(string.ascii_lowercase[i])
            param_types.append("dynamic")

    if not param_names:
        param_names = ["a", "b"]
        param_types = ["dynamic", "dynamic"]

    params_str = ", ".join(
        f"{t} {n}" for n, t in zip(param_names, param_types)
    )

    # Output type
    try:
        out_val = ast.literal_eval(output_example) if output_example else None
        if isinstance(out_val, bool):
            return_type = "bool"
        elif isinstance(out_val, int):
            return_type = "int"
        elif isinstance(out_val, float):
            return_type = "double"
        elif isinstance(out_val, str):
            return_type = "String"
        elif isinstance(out_val, list):
            return_type = "List<dynamic>"
        else:
            return_type = "dynamic"
    except Exception:
        return_type = "dynamic"

    template = f'''class Solution {{
  {return_type} {method_name}({params_str}) {{
    // Kodingizni shu yerda yozing
    return null;
  }}
}}
'''
    return template
