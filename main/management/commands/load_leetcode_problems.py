from django.core.management.base import BaseCommand
from main.models import Problem, TestCase

top_leetcode_problems = [
    {
        'title': 'Valid Anagram',
        'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise.\n\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.\n\nExample 1:\nInput: s = "anagram", t = "nagaram"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().isAnagram',
        'test_cases': [
            {'input': '\"anagram\"\n\"nagaram\"', 'output': 'true'},
            {'input': '\"rat\"\n\"car\"', 'output': 'false'},
            {'input': '\"a\"\n\"a\"', 'output': 'true'},
            {'input': '\"aacc\"\n\"ccac\"', 'output': 'false'}
        ]
    },
    {
        'title': 'First Unique Character in a String',
        'description': 'Given a string s, find the first non-repeating character in it and return its index. If it does not exist, return -1.\n\nExample 1:\nInput: s = "leetcode"\nOutput: 0',
        'difficulty': 'Easy',
        'function_name': 'Solution().firstUniqChar',
        'test_cases': [
            {'input': '\"leetcode\"', 'output': '0'},
            {'input': '\"loveleetcode\"', 'output': '2'},
            {'input': '\"aabb\"', 'output': '-1'},
            {'input': '\"dddccdbba\"', 'output': '8'}
        ]
    },
    {
        'title': 'Reverse String',
        'description': 'Write a function that reverses a string. The input string is given as an array of characters s.\n\nYou must do this by modifying the input array in-place with O(1) extra memory.\n\nExample 1:\nInput: s = ["h","e","l","l","o"]\nOutput: ["o","l","l","e","h"]',
        'difficulty': 'Easy',
        'function_name': 'Solution().reverseString',
        'test_cases': [
            {'input': '["h","e","l","l","o"]', 'output': '["o","l","l","e","h"]'},
            {'input': '["H","a","n","n","a","h"]', 'output': '["h","a","n","n","a","H"]'},
            {'input': '["a"]', 'output': '["a"]'},
            {'input': '["a","b"]', 'output': '["b","a"]'}
        ]
    },
    {
        'title': 'String to Integer (atoi)',
        'description': 'Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer (similar to C/C++\'s atoi function).\n\nThe algorithm for myAtoi(string s) is as follows:\n1. Read in and ignore any leading whitespace.\n2. Check if the next character is \'+\' or \'-\'. Read this character in if it is either.\n3. Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.\n4. Convert these digits into an integer.\n5. If the integer is out of the 32-bit signed integer range [-2³¹, 2³¹ - 1], then clamp the integer.\n\nExample 1:\nInput: s = "42"\nOutput: 42',
        'difficulty': 'Medium',
        'function_name': 'Solution().myAtoi',
        'test_cases': [
            {'input': '\"42\"', 'output': '42'},
            {'input': '\"   -42\"', 'output': '-42'},
            {'input': '\"4193 with words\"', 'output': '4193'},
            {'input': '\"words and 987\"', 'output': '0'}
        ]
    },
    {
        'title': 'Count and Say',
        'description': 'The count-and-say sequence is a sequence of digit strings defined by the recursive formula:\n\ncountAndSay(1) = "1"\ncountAndSay(n) is the way you would "say" the digit string from countAndSay(n-1), which is then converted into a different digit string.\n\nExample 1:\nInput: n = 1\nOutput: "1"\nExplanation: This is the base case.',
        'difficulty': 'Easy',
        'function_name': 'Solution().countAndSay',
        'test_cases': [
            {'input': '1', 'output': '\"1\"'},
            {'input': '4', 'output': '\"1211\"'},
            {'input': '5', 'output': '\"111221\"'},
            {'input': '6', 'output': '\"312211\"'}
        ]
    },
    {
        'title': 'Add Binary',
        'description': 'Given two binary strings a and b, return their sum as a binary string.\n\nExample 1:\nInput: a = "11", b = "1"\nOutput: "100"',
        'difficulty': 'Easy',
        'function_name': 'Solution().addBinary',
        'test_cases': [
            {'input': '\"11\"\n\"1\"', 'output': '\"100\"'},
            {'input': '\"1010\"\n\"1011\"', 'output': '\"10101\"'},
            {'input': '\"0\"\n\"0\"', 'output': '\"0\"'},
            {'input': '\"1111\"\n\"1111\"', 'output': '\"11110\"'}
        ]
    },
    {
        'title': 'Happy Number',
        'description': 'Write an algorithm to determine if a number n is happy.\n\nA happy number is a number defined by the following process:\n1. Starting with any positive integer, replace the number by the sum of the squares of its digits.\n2. Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.\n3. Those numbers for which this process ends in 1 are happy.\n\nExample 1:\nInput: n = 19\nOutput: true\nExplanation:\n1² + 9² = 82\n8² + 2² = 68\n6² + 8² = 100\n1² + 0² + 0² = 1',
        'difficulty': 'Easy',
        'function_name': 'Solution().isHappy',
        'test_cases': [
            {'input': '19', 'output': 'true'},
            {'input': '2', 'output': 'false'},
            {'input': '7', 'output': 'true'},
            {'input': '1', 'output': 'true'}
        ]
    },
    {
        'title': 'Power of Two',
        'description': 'Given an integer n, return true if it is a power of two. Otherwise, return false.\n\nAn integer n is a power of two, if there exists an integer x such that n == 2ˣ.\n\nExample 1:\nInput: n = 1\nOutput: true\nExplanation: 2⁰ = 1',
        'difficulty': 'Easy',
        'function_name': 'Solution().isPowerOfTwo',
        'test_cases': [
            {'input': '1', 'output': 'true'},
            {'input': '16', 'output': 'true'},
            {'input': '3', 'output': 'false'},
            {'input': '0', 'output': 'false'}
        ]
    },
    {
        'title': 'Excel Sheet Column Title',
        'description': 'Given an integer columnNumber, return its corresponding column title as it appears in an Excel sheet.\n\nExample 1:\nInput: columnNumber = 1\nOutput: "A"\nExample 2:\nInput: columnNumber = 28\nOutput: "AB"',
        'difficulty': 'Easy',
        'function_name': 'Solution().convertToTitle',
        'test_cases': [
            {'input': '1', 'output': '\"A\"'},
            {'input': '28', 'output': '\"AB\"'},
            {'input': '701', 'output': '\"ZY\"'},
            {'input': '52', 'output': '\"AZ\"'}
        ]
    },
    {
        'title': 'Count Primes',
        'description': 'Given an integer n, return the number of prime numbers that are strictly less than n.\n\nExample 1:\nInput: n = 10\nOutput: 4\nExplanation: There are 4 prime numbers less than 10, they are 2, 3, 5, 7.',
        'difficulty': 'Easy',
        'function_name': 'Solution().countPrimes',
        'test_cases': [
            {'input': '10', 'output': '4'},
            {'input': '0', 'output': '0'},
            {'input': '1', 'output': '0'},
            {'input': '20', 'output': '8'}
        ]
    },
    {
        'title': 'Palindrome Number',
        'description': 'Given an integer x, return true if x is a palindrome, and false otherwise.\n\nExample 1:\nInput: x = 121\nOutput: true\nExplanation: 121 reads as 121 from left to right and from right to left.',
        'difficulty': 'Easy',
        'function_name': 'Solution().isPalindrome',
        'test_cases': [
            {'input': '121', 'output': 'true'},
            {'input': '-121', 'output': 'false'},
            {'input': '10', 'output': 'false'},
            {'input': '12321', 'output': 'true'}
        ]
    },
    {
        'title': 'Roman to Integer',
        'description': 'Given a roman numeral, convert it to an integer.\n\nExample 1:\nInput: s = "III"\nOutput: 3\nExplanation: III = 3.',
        'difficulty': 'Easy',
        'function_name': 'Solution().romanToInt',
        'test_cases': [
            {'input': '\"III\"', 'output': '3'},
            {'input': '\"LVIII\"', 'output': '58'},
            {'input': '\"MCMXCIV\"', 'output': '1994'},
            {'input': '\"IX\"', 'output': '9'}
        ]
    },
    {
        'title': 'Longest Common Prefix',
        'description': 'Write a function to find the longest common prefix string amongst an array of strings.\nIf there is no common prefix, return an empty string "".\n\nExample 1:\nInput: strs = ["flower","flow","flight"]\nOutput: "fl"',
        'difficulty': 'Easy',
        'function_name': 'Solution().longestCommonPrefix',
        'test_cases': [
            {'input': '["flower","flow","flight"]', 'output': '\"fl\"'},
            {'input': '["dog","racecar","car"]', 'output': '\"\"'},
            {'input': '["a"]', 'output': '\"a\"'},
            {'input': '["cir","car"]', 'output': '\"c\"'}
        ]
    },
    {
        'title': 'Valid Parentheses',
        'description': 'Given a string s containing just the characters "(", ")", "{", "}", "[" and "]", determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n\nExample 1:\nInput: s = "()"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().isValid',
        'test_cases': [
            {'input': '\"()\"', 'output': 'true'},
            {'input': '\"()[]{}\"', 'output': 'true'},
            {'input': '\"(]\"', 'output': 'false'},
            {'input': '\"{[]}\"', 'output': 'true'}
        ]
    },
    {
        'title': 'Remove Duplicates from Sorted Array',
        'description': 'Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once. The relative order of the elements should be kept the same.\n\nExample 1:\nInput: nums = [1,1,2]\nOutput: 2, nums = [1,2,_]',
        'difficulty': 'Easy',
        'function_name': 'Solution().removeDuplicates',
        'test_cases': [
            {'input': '[1,1,2]', 'output': '2'},
            {'input': '[0,0,1,1,1,2,2,3,3,4]', 'output': '5'},
            {'input': '[1,1,1,1]', 'output': '1'},
            {'input': '[]', 'output': '0'}
        ]
    },
    {
        'title': 'Remove Element',
        'description': 'Given an integer array nums and an integer val, remove all occurrences of val in nums in-place. The relative order of the elements may be changed.\n\nExample 1:\nInput: nums = [3,2,2,3], val = 3\nOutput: 2, nums = [2,2,_,_]',
        'difficulty': 'Easy',
        'function_name': 'Solution().removeElement',
        'test_cases': [
            {'input': '[3,2,2,3]\n3', 'output': '2'},
            {'input': '[0,1,2,2,3,0,4,2]\n2', 'output': '5'},
            {'input': '[1]\n1', 'output': '0'},
            {'input': '[4,5]\n5', 'output': '1'}
        ]
    },
    {
        'title': 'Search Insert Position',
        'description': 'Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.\n\nExample 1:\nInput: nums = [1,3,5,6], target = 5\nOutput: 2',
        'difficulty': 'Easy',
        'function_name': 'Solution().searchInsert',
        'test_cases': [
            {'input': '[1,3,5,6]\n5', 'output': '2'},
            {'input': '[1,3,5,6]\n2', 'output': '1'},
            {'input': '[1,3,5,6]\n7', 'output': '4'},
            {'input': '[1,3,5,6]\n0', 'output': '0'}
        ]
    },
    {
        'title': 'Length of Last Word',
        'description': 'Given a string s consisting of words and spaces, return the length of the last word in the string.\n\nA word is a maximal substring consisting of non-space characters only.\n\nExample 1:\nInput: s = "Hello World"\nOutput: 5\nExplanation: The last word is "World" with length 5.',
        'difficulty': 'Easy',
        'function_name': 'Solution().lengthOfLastWord',
        'test_cases': [
            {'input': '\"Hello World\"', 'output': '5'},
            {'input': '\"   fly me   to   the moon  \"', 'output': '4'},
            {'input': '\"luffy is still joyboy\"', 'output': '6'},
            {'input': '\"a\"', 'output': '1'}
        ]
    },
    {
        'title': 'Plus One',
        'description': 'You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading 0\'s.\n\nIncrement the large integer by one and return the resulting array of digits.\n\nExample 1:\nInput: digits = [1,2,3]\nOutput: [1,2,4]',
        'difficulty': 'Easy',
        'function_name': 'Solution().plusOne',
        'test_cases': [
            {'input': '[1,2,3]', 'output': '[1,2,4]'},
            {'input': '[4,3,2,1]', 'output': '[4,3,2,2]'},
            {'input': '[9]', 'output': '[1,0]'},
            {'input': '[9,9,9]', 'output': '[1,0,0,0]'}
        ]
    },
    {
        'title': 'Climbing Stairs',
        'description': 'You are climbing a staircase. It takes n steps to reach the top.\n\nEach time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?\n\nExample 1:\nInput: n = 2\nOutput: 2\nExplanation: There are two ways to climb to the top.\n1. 1 step + 1 step\n2. 2 steps',
        'difficulty': 'Easy',
        'function_name': 'Solution().climbStairs',
        'test_cases': [
            {'input': '2', 'output': '2'},
            {'input': '3', 'output': '3'},
            {'input': '1', 'output': '1'},
            {'input': '5', 'output': '8'}
        ]
    },
    {
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice.\n\nYou can return the answer in any order.\n\nExample 1:\nInput: nums = [2,7,11,15], target = 9\nOutput: [0,1]\nExplanation: Because nums[0] + nums[1] == 9, we return [0, 1].',
        'difficulty': 'Easy',
        'function_name': 'Solution().twoSum',
        'test_cases': [
            {'input': '[2,7,11,15]\n9', 'output': '[0, 1]'},
            {'input': '[3,2,4]\n6', 'output': '[1, 2]'},
            {'input': '[3,3]\n6', 'output': '[0, 1]'}
        ]
    },
    {
        'title': 'Add Two Numbers',
        'description': 'You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.\n\nYou may assume the two numbers do not contain any leading zero, except the number 0 itself.\n\nExample 1:\nInput: l1 = [2,4,3], l2 = [5,6,4]\nOutput: [7,0,8]\nExplanation: 342 + 465 = 807.',
        'difficulty': 'Medium',
        'function_name': 'Solution().addTwoNumbers',
        'test_cases': [
            {'input': '[2,4,3]\n[5,6,4]', 'output': '[7,0,8]'},
            {'input': '[0]\n[0]', 'output': '[0]'},
            {'input': '[9,9,9,9,9,9,9]\n[9,9,9,9]', 'output': '[8,9,9,9,0,0,0,1]'}
        ]
    },
    {
        'title': 'Longest Substring Without Repeating Characters',
        'description': 'Given a string s, find the length of the longest substring without repeating characters.\n\nExample 1:\nInput: s = "abcabcbb"\nOutput: 3\nExplanation: The answer is "abc", with the length of 3.',
        'difficulty': 'Medium',
        'function_name': 'Solution().lengthOfLongestSubstring',
        'test_cases': [
            {'input': '\"abcabcbb\"', 'output': '3'},
            {'input': '\"bbbbb\"', 'output': '1'},
            {'input': '\"pwwkew\"', 'output': '3'}
        ]
    },
    {
        'title': 'Median of Two Sorted Arrays',
        'description': 'Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.\n\nThe overall run time complexity should be O(log (m+n)).\n\nExample 1:\nInput: nums1 = [1,3], nums2 = [2]\nOutput: 2.00000\nExplanation: merged array = [1,2,3] and median is 2.',
        'difficulty': 'Hard',
        'function_name': 'Solution().findMedianSortedArrays',
        'test_cases': [
            {'input': '[1,3]\n[2]', 'output': '2.0'},
            {'input': '[1,2]\n[3,4]', 'output': '2.5'},
            {'input': '[0,0]\n[0,0]', 'output': '0.0'}
        ]
    },
    {
        'title': 'Longest Palindromic Substring',
        'description': 'Given a string s, return the longest palindromic substring in s.\n\nExample 1:\nInput: s = "babad"\nOutput: "bab"\nNote: "aba" is also a valid answer.',
        'difficulty': 'Medium',
        'function_name': 'Solution().longestPalindrome',
        'test_cases': [
            {'input': '\"babad\"', 'output': '\"bab\"'},
            {'input': '\"cbbd\"', 'output': '\"bb\"'},
            {'input': '\"a\"', 'output': '\"a\"'}
        ]
    },
    {
        'title': 'Zigzag Conversion',
        'description': 'The string "PAYPALISHIRING" is written in a zigzag pattern on a given number of rows like this: (you may want to display this pattern in a fixed font for better legibility)\n\nP   A   H   N\nA P L S I I G\nY   I   R\n\nAnd then read line by line: "PAHNAPLSIIGYIR"\n\nWrite the code that will take a string and make this conversion given a number of rows:\n\nstring convert(string s, int numRows);\n\nExample 1:\nInput: s = "PAYPALISHIRING", numRows = 3\nOutput: "PAHNAPLSIIGYIR"',
        'difficulty': 'Medium',
        'function_name': 'Solution().convert',
        'test_cases': [
            {'input': '\"PAYPALISHIRING\"\n3', 'output': '\"PAHNAPLSIIGYIR\"'},
            {'input': '\"PAYPALISHIRING\"\n4', 'output': '\"PINALSIGYAHRPI\"'},
            {'input': '\"A\"\n1', 'output': '\"A\"'}
        ]
    },
    {
        'title': 'Reverse Integer',
        'description': 'Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-2³¹, 2³¹ - 1], then return 0.\n\nAssume the environment does not allow you to store 64-bit integers (signed or unsigned).\n\nExample 1:\nInput: x = 123\nOutput: 321',
        'difficulty': 'Easy',
        'function_name': 'Solution().reverse',
        'test_cases': [
            {'input': '123', 'output': '321'},
            {'input': '-123', 'output': '-321'},
            {'input': '120', 'output': '21'}
        ]
    },
    {
        'title': 'String to Integer (atoi)',
        'description': 'Implement the myAtoi(string s) function, which converts a string to a 32-bit signed integer (similar to C/C++\'s atoi function).\n\nThe algorithm for myAtoi(string s) is as follows:\n1. Read in and ignore any leading whitespace.\n2. Check if the next character is \'+\' or \'-\'. Read this character in if it is either.\n3. Read in next the characters until the next non-digit character or the end of the input is reached. The rest of the string is ignored.\n4. Convert these digits into an integer.\n5. If the integer is out of the 32-bit signed integer range [-2³¹, 2³¹ - 1], then clamp the integer.\n6. Return the integer as the final result.\n\nExample 1:\nInput: s = "42"\nOutput: 42',
        'difficulty': 'Medium',
        'function_name': 'Solution().myAtoi',
        'test_cases': [
            {'input': '\"42\"', 'output': '42'},
            {'input': '\"   -42\"', 'output': '-42'},
            {'input': '\"4193 with words\"', 'output': '4193'}
        ]
    },
    {
        'title': 'Container With Most Water',
        'description': 'You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum amount of water a container can store.\n\nExample 1:\nInput: height = [1,8,6,2,5,4,8,3,7]\nOutput: 49\nExplanation: The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.',
        'difficulty': 'Medium',
        'function_name': 'Solution().maxArea',
        'test_cases': [
            {'input': '[1,8,6,2,5,4,8,3,7]', 'output': '49'},
            {'input': '[1,1]', 'output': '1'},
            {'input': '[4,3,2,1,4]', 'output': '16'}
        ]
    },
    {
        'title': '3Sum',
        'description': 'Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.\n\nNotice that the solution set must not contain duplicate triplets.\n\nExample 1:\nInput: nums = [-1,0,1,2,-1,-4]\nOutput: [[-1,-1,2],[-1,0,1]]',
        'difficulty': 'Medium',
        'function_name': 'Solution().threeSum',
        'test_cases': [
            {'input': '[-1,0,1,2,-1,-4]', 'output': '[[-1,-1,2],[-1,0,1]]'},
            {'input': '[]', 'output': '[]'},
            {'input': '[0]', 'output': '[]'}
        ]
    }
]

class Command(BaseCommand):
    help = 'Loads the top 10 LeetCode problems into the database'

    def handle(self, *args, **options):
        for problem_data in top_leetcode_problems:
            # Check if problem already exists
            if Problem.objects.filter(title=problem_data['title']).exists():
                self.stdout.write(self.style.WARNING(f"Problem '{problem_data['title']}' already exists. Skipping..."))
                continue
                
            # Create the problem
            problem = Problem.objects.create(
                title=problem_data['title'],
                description=problem_data['description'],
                difficulty=problem_data['difficulty'],
                function_name=problem_data['function_name'],
                input_example=problem_data['test_cases'][0]['input'],
                output_example=problem_data['test_cases'][0]['output']
            )
            
            # Add test cases
            for i, test_case in enumerate(problem_data['test_cases']):
                TestCase.objects.create(
                    problem=problem,
                    input_data=test_case['input'],
                    expected_output=test_case['output'],
                    order=i,
                    is_hidden=False
                )
            
            self.stdout.write(self.style.SUCCESS(f"Added problem: {problem_data['title']}"))
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all problems!'))
