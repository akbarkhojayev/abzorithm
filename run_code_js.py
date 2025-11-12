import sys
import json
import subprocess
import tempfile
import time
import os

def run_javascript_code(user_code: str, test_input: str, expected_output: str, timeout: int = 2):
    """
    JavaScript kodini Node.js orqali bajarish
    """
    input_lines = test_input.replace('\r', '').strip().split("\n")
    args = []
    
    for x in input_lines:
        x = x.strip()
        if not x:
            continue
        try:
            parsed = json.loads(x)
            args.append(parsed)
        except json.JSONDecodeError:
            try:
                if '.' in x:
                    args.append(float(x))
                else:
                    args.append(int(x))
            except ValueError:
                args.append(x)
    
    # JavaScript wrapper code
    code_wrapper = f"""
{user_code}

// Main execution
try {{
    const solution = new Solution();
    const args = {json.dumps(args)};
    const result = solution.solve(...args);
    console.log(JSON.stringify(result));
}} catch (error) {{
    console.error(error.message);
    process.exit(1);
}}
"""
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(code_wrapper)
            temp_path = f.name
        
        os.chmod(temp_path, 0o600)
        
        start_time = time.time()
        result = subprocess.run(
            ['node', temp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        exec_time = round(time.time() - start_time, 4)
        
        if result.returncode != 0:
            error_msg = result.stderr.replace('\n', ' ').replace('\r', ' ')[:200]
            return False, "RuntimeError", f"Runtime error: {error_msg}", exec_time
        
        output = result.stdout.strip()
        
        try:
            expected_json = json.loads(expected_output)
        except json.JSONDecodeError:
            expected_json = expected_output
        
        try:
            actual_json = json.loads(output) if output else None
        except json.JSONDecodeError:
            actual_json = output
        
        if actual_json == expected_json:
            return True, "Accepted", "Test passed", exec_time
        else:
            actual_str = json.dumps(actual_json, ensure_ascii=False) if actual_json is not None else "None"
            if len(actual_str) > 100:
                actual_str = actual_str[:97] + "..."
            return False, "Wrong Answer", actual_str, exec_time
    
    except subprocess.TimeoutExpired:
        return False, "Time Limit Exceeded", f"Execution time exceeded {timeout}s", timeout
    except Exception as e:
        exec_time = round(time.time() - start_time, 4)
        error_msg = str(e).replace('\n', ' ').replace('\r', ' ')[:200]
        return False, "RuntimeError", f"Execution error: {error_msg}", exec_time
    finally:
        try:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        except Exception:
            pass

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(json.dumps({"error": "Usage: python run_code_js.py <user_code> <test_input> <expected_output>"}))
        sys.exit(1)
    
    user_code = sys.argv[1].replace('\\n', '\n')
    test_input = sys.argv[2]
    expected_output = sys.argv[3]
    
    success, status, message, exec_time = run_javascript_code(user_code, test_input, expected_output)
    
    result = {
        "success": success,
        "status": status,
        "message": message,
        "execution_time": exec_time
    }
    
    print(json.dumps(result))
