import sys
import json
import ast
import resource
import time
import tempfile
import os
from typing import Any, Tuple

def safe_eval(expr: str) -> Any:
    """
    Xavfsiz eval - faqat literal qiymatlarni qabul qiladi
    """
    try:
        return ast.literal_eval(expr)
    except (ValueError, SyntaxError):
        raise ValueError(f"Invalid literal: {expr}")

def run_user_code(user_code: str, test_input: str, expected_output: str, timeout: int = 2) -> Tuple[bool, str, str, float]:
    """
    Foydalanuvchi kodini xavfsiz ishga tushirish
    """
    # Resource cheklovlari
    try:
        resource.setrlimit(resource.RLIMIT_CPU, (timeout, timeout))
        resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))  # 100MB RAM
        resource.setrlimit(resource.RLIMIT_FSIZE, (5 * 1024 * 1024, 5 * 1024 * 1024))  # 5MB file size
        resource.setrlimit(resource.RLIMIT_NPROC, (20, 20))  # 20 process
    except (OSError, ValueError):
        pass

    input_lines = test_input.replace('\r', '').strip().split("\n")
    args = []
    
    for x in input_lines:
        x = x.strip()
        if not x:
            continue

        if "[" in x and "]" in x:
            try:
                if " = [" in x:
                    list_part = x.split(" = ")[1]
                    nums = safe_eval(list_part)
                elif x.startswith("[") and x.endswith("]"):
                    nums = safe_eval(x)
                else:
                    nums = safe_eval(x)
                
                if isinstance(nums, list):
                    args.append(nums)
                    continue
            except:
                pass

        if "," in x and not "=" in x and not "[" in x and not "]" in x:
            try:
                nums = [int(item.strip()) for item in x.split(",")]
                args.append(nums)
                continue
            except:
                pass

        if "," in x and "=" in x and "[" in x and "]" in x:
            try:
                parts = x.split(", ")
                for part in parts:
                    if " = [" in part:
                        list_part = part.split(" = ")[1]
                        nums = safe_eval(list_part)
                        args.append(nums)
                    elif " = " in part and not "[" in part:
                        value = part.split(" = ")[1]
                        try:
                            args.append(int(value))
                        except:
                            args.append(value)
                continue
            except:
                pass

        try:
            parsed = json.loads(x)
            if isinstance(parsed, (str, int, float, bool, type(None), list, dict)):
                args.append(parsed)
            else:
                raise ValueError(f"Unsupported type: {type(parsed)}")
        except (json.JSONDecodeError, ValueError):
            try:
                if '.' in x:
                    args.append(float(x))
                else:
                    args.append(int(x))
            except ValueError:
                args.append(x)

    def _safe_literal(val):
        if isinstance(val, str):
            return json.dumps(val, ensure_ascii=False)
        elif isinstance(val, (int, float, bool, type(None))):
            return str(val)
        elif isinstance(val, (list, dict)):
            return json.dumps(val, ensure_ascii=False)
        else:
            raise ValueError(f"Unsupported type: {type(val)}")
    
    try:
        input_args = ", ".join(_safe_literal(a) for a in args)
    except ValueError as e:
        return False, "InvalidInput", f"Invalid argument: {str(e)}", 0


    code_wrapper = f"""
import sys
import json
import resource

# Import cheklash
forbidden_modules = ['os', 'subprocess', 'socket', 'urllib', 'requests', 'shutil', 'glob', 'pathlib', 'importlib', 'sys']
for module in forbidden_modules:
    if module in sys.modules:
        sys.modules[module] = None

{user_code}

def __resolve_callable():
    try:
        solution = Solution()
        return getattr(solution, 'solve')
    except AttributeError:
        raise NameError("Method 'solve' not found in Solution class")

if __name__ == "__main__":
    try:
        # Resurs cheklovlari
        try:
            resource.setrlimit(resource.RLIMIT_CPU, ({timeout}, {timeout}))
            resource.setrlimit(resource.RLIMIT_AS, (100 * 1024 * 1024, 100 * 1024 * 1024))
        except (OSError, ValueError):
            pass
        
        __fn = __resolve_callable()
        result = __fn({input_args})
        
        # Natijani JSON formatda chiqarish
        try:
            print(json.dumps(result, ensure_ascii=False, separators=(',', ':')))
        except (TypeError, ValueError):
            print(json.dumps(str(result), ensure_ascii=False))
    except Exception as e:
        error_msg = str(e).replace('\\n', ' ').replace('\\r', ' ')[:200]
        sys.stderr.write(f"Error: {{error_msg}}")
"""

    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code_wrapper)
            temp_path = f.name
        
        os.chmod(temp_path, 0o600)
        
    except Exception as e:
        return False, "FileError", f"Failed to create temp file: {str(e)}", 0

    start_time = time.time()
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir(),
            env={'PATH': '/usr/local/bin:/usr/bin:/bin', 'PYTHONPATH': ''}
        )
        exec_time = round(time.time() - start_time, 4)

        if result.returncode != 0:
            error_msg = result.stderr.replace('\n', ' ').replace('\r', ' ')[:200]
            return False, "RuntimeError", f"Runtime error: {error_msg}", exec_time

        output = result.stdout.strip()
        if len(output) > 1000:
            return False, "OutputError", "Output too large", exec_time

        try:
            expected_json = json.loads(expected_output)
        except json.JSONDecodeError:
            # Boolean string'lar uchun
            if expected_output.lower() in ['true', 'false']:
                expected_json = expected_output.lower() == 'true'
            else:
                expected_json = expected_output

        # Actual output parsing
        try:
            actual_json = json.loads(output) if output else None
        except json.JSONDecodeError:
            # Boolean string'lar uchun
            if output.lower() in ['true', 'false']:
                actual_json = output.lower() == 'true'
            else:
                actual_json = output

        # Comparison
        if actual_json == expected_json:
            return True, "Accepted", "Test passed", exec_time
        else:
            expected_str = json.dumps(expected_json, ensure_ascii=False) if expected_json is not None else "None"
            actual_str = json.dumps(actual_json, ensure_ascii=False) if actual_json is not None else "None"
            
            if len(expected_str) > 100:
                expected_str = expected_str[:97] + "..."
            if len(actual_str) > 100:
                actual_str = actual_str[:97] + "..."
                
            return False, "Wrong Answer", f"Got: {actual_str}, Expected: {expected_str}", exec_time

    except subprocess.TimeoutExpired:
        return False, "Time Limit Exceeded", f"Execution time exceeded {timeout}s", timeout
    except Exception as e:
        exec_time = round(time.time() - start_time, 4)
        error_msg = str(e).replace('\n', ' ').replace('\r', ' ')[:200]
        return False, "RuntimeError", f"Execution error: {error_msg}", exec_time
    finally:
        # Cleanup
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except Exception:
            pass

if __name__ == "__main__":
    # Command line arguments
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Usage: python run_code.py <user_code> <test_input> <expected_output>"}))
        sys.exit(1)
    
    user_code = sys.argv[1].replace('\\n', '\n')
    test_input = sys.argv[2]
    expected_output = sys.argv[3]
    
    success, status, message, exec_time = run_user_code(user_code, test_input, expected_output)
    
    result = {
        "success": success,
        "status": status,
        "message": message,
        "execution_time": exec_time
    }
    
    print(json.dumps(result))
