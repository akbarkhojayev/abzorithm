#!/usr/bin/env python3
"""
Docker yechimini test qilish uchun script
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main.utils_docker import run_python_function_docker

def test_docker_execution():
    """Docker execution test"""
    
    # Test 1: Two Sum
    print("🧪 Testing Two Sum...")
    code1 = '''class Solution:
    def solve(self, nums, target):
        lookup = {}
        for i, num in enumerate(nums):
            diff = target - num
            if diff in lookup:
                return [lookup[diff], i]
            lookup[num] = i
        return []'''
    
    result1 = run_python_function_docker(
        code1, 
        'solve', 
        'nums = [2,7,11,15], target = 9', 
        '[0,1]'
    )
    print(f"Two Sum: {result1}")
    
    # Test 2: Valid Parentheses
    print("\n🧪 Testing Valid Parentheses...")
    code2 = '''class Solution:
    def solve(self, s):
        stack = []
        mapping = {")": "(", "}": "{", "]": "["}
        for char in s:
            if char in mapping:
                if not stack or stack.pop() != mapping[char]:
                    return False
            else:
                stack.append(char)
        return not stack'''
    
    result2 = run_python_function_docker(
        code2, 
        'solve', 
        's = "()"', 
        'True'
    )
    print(f"Valid Parentheses: {result2}")
    
    # Test 3: Maximum Subarray
    print("\n🧪 Testing Maximum Subarray...")
    code3 = '''class Solution:
    def solve(self, nums):
        current_sum = nums[0]
        max_sum = nums[0]
        for num in nums[1:]:
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)
        return max_sum'''
    
    result3 = run_python_function_docker(
        code3, 
        'solve', 
        'nums = [-2,1,-3,4,-1,2,1,-5,4]', 
        '6'
    )
    print(f"Maximum Subarray: {result3}")

if __name__ == "__main__":
    print("🐳 Docker Code Execution Test")
    print("=" * 50)
    
    try:
        test_docker_execution()
        print("\n✅ All tests completed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
