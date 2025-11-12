import subprocess
import json
import tempfile
import os
from typing import Tuple

def run_python_function_docker(user_code: str, func_name: str, test_input: str, expected_output: str, timeout: int = 2, language: str = 'python') -> Tuple[bool, str, str, float]:
    """
    Docker container orqali xavfsiz kod ishga tushirish
    """
    # Til bo'yicha executor tanlash
    executor_map = {
        'python': 'run_code.py',
        'javascript': 'run_code_js.py',
        'dart': 'run_code_dart.py',
    }
    
    executor_script = executor_map.get(language, 'run_code.py')
    
    try:
        # Docker container ishga tushirish
        result = subprocess.run([
            'docker', 'run', 
            '--rm',  # Container'ni avtomatik o'chirish
            '--memory=200m',  # 200MB RAM cheklash
            '--cpus=2',  # CPU cheklash
            'abzorithm_code_executor',  # Image nomi
            'python3', executor_script,  # Executor script ishga tushirish
            user_code,
            test_input,
            expected_output
        ], capture_output=True, text=True, timeout=timeout + 10)
        
        if result.returncode != 0:
            return False, "DockerError", f"Docker execution failed: {result.stderr}", 0
        
        # JSON natijani parse qilish
        try:
            result_data = json.loads(result.stdout)
            return (
                result_data.get('success', False),
                result_data.get('status', 'Unknown'),
                result_data.get('message', ''),
                result_data.get('execution_time', 0)
            )
        except json.JSONDecodeError:
            return False, "ParseError", f"Failed to parse result: {result.stdout}", 0
            
    except subprocess.TimeoutExpired:
        return False, "Time Limit Exceeded", f"Docker execution exceeded {timeout + 5}s", timeout + 5

        return False, "DockerError", f"Docker execution error: {str(e)}", 0

def build_docker_image():
    """
    Docker image yaratish
    """
    try:
        result = subprocess.run([
            'docker', 'build', 
            '-t', 'abzorithm_code_executor',
            '-f', 'Dockerfile.executor',
            '.'
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Docker build failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Docker build error: {str(e)}")
        return False
