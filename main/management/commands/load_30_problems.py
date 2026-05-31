from django.core.management.base import BaseCommand
from main.models import Problem, Category, TestCase, Example

CATEGORIES_DATA = {
    'Array': 'Massiv va array masalalari',
    'String': 'Matn va string masalalari',
    'HashTable': 'HashMap va dictionary masalalari',
    'Math': 'Matematik masalalari',
    'Stack': 'Stack masalalari',
    'Queue': 'Queue masalalari',
    'Tree': 'Binary tree va tree masalalari',
    'Graph': 'Graph masalalari',
    'DynamicProgramming': 'Dynamic Programming masalalari',
    'Greedy': 'Greedy algorithm masalalari',
}

PROBLEMS_DATA = [
    # 1. Two Sum
    {
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target. You may assume that each input has exactly one solution, and you may not use the same element twice.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[2, 7, 11, 15]\n9',
        'output_example': '[0, 1]',
        'categories': ['Array', 'HashTable'],
        'examples': [
            {'input': '[2, 7, 11, 15], target = 9', 'output': '[0, 1]'},
            {'input': '[3, 2, 4], target = 6', 'output': '[1, 2]'},
        ],
        'test_cases': [
            ('[2, 7, 11, 15]\n9', '[0, 1]'),
            ('[3, 2, 4]\n6', '[1, 2]'),
            ('[3, 3]\n6', '[0, 1]'),
            ('[2, 5, 5, 11]\n10', '[1, 2]'),
            ('[1, 2, 3, 4]\n7', '[2, 3]'),
            ('[10, 1, 1, 0]\n0', '[2, 3]'),
        ]
    },
    # 2. Best Time to Buy and Sell Stock
    {
        'title': 'Best Time to Buy and Sell Stock',
        'description': 'Given an array prices where prices[i] is the price on day i, find the maximum profit you can make by buying and selling once. If you cannot achieve any profit, return 0.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[7, 1, 5, 3, 6, 4]',
        'output_example': '5',
        'categories': ['Array', 'DynamicProgramming'],
        'examples': [
            {'input': '[7, 1, 5, 3, 6, 4]', 'output': '5 (buy at 1, sell at 6)'},
            {'input': '[7, 6, 4, 3, 1]', 'output': '0 (no profit possible)'},
        ],
        'test_cases': [
            ('[7, 1, 5, 3, 6, 4]', '5'),
            ('[7, 6, 4, 3, 1]', '0'),
            ('[2, 4, 1]', '2'),
            ('[3, 2, 6, 5, 0, 3]', '4'),
            ('[1]', '0'),
            ('[1, 2, 3, 4, 5]', '4'),
        ]
    },
    # 3. Contains Duplicate
    {
        'title': 'Contains Duplicate',
        'description': 'Given an integer array nums, return true if any value appears at least twice in the array, and false if every element is distinct.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 3, 1]',
        'output_example': 'true',
        'categories': ['Array', 'HashTable'],
        'examples': [
            {'input': '[1, 2, 3, 1]', 'output': 'true'},
            {'input': '[1, 2, 3, 4]', 'output': 'false'},
        ],
        'test_cases': [
            ('[1, 2, 3, 1]', 'true'),
            ('[1, 2, 3, 4]', 'false'),
            ('[1, 1, 1, 1]', 'true'),
            ('[1, 2]', 'false'),
            ('[99, 99]', 'true'),
            ('[1, 2, 3, 4, 5]', 'false'),
        ]
    },
    # 4. Valid Anagram
    {
        'title': 'Valid Anagram',
        'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise. An anagram is a word formed by rearranging the letters of another word.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"anagram"\n"nagaram"',
        'output_example': 'true',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 's = "anagram", t = "nagaram"', 'output': 'true'},
            {'input': 's = "rat", t = "car"', 'output': 'false'},
        ],
        'test_cases': [
            ('"anagram"\n"nagaram"', 'true'),
            ('"rat"\n"car"', 'false'),
            ('"a"\n"b"', 'false'),
            ('"ab"\n"ba"', 'true'),
            ('"abc"\n"cab"', 'true'),
            ('"listen"\n"silent"', 'true'),
        ]
    },
    # 5. Majority Element
    {
        'title': 'Majority Element',
        'description': 'Given an array nums of size n, return the majority element. The majority element is the element that appears more than n/2 times. You may assume that the majority element always exists in the array.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3, 2, 3]',
        'output_example': '3',
        'categories': ['Array', 'HashTable'],
        'examples': [
            {'input': '[3, 2, 3]', 'output': '3'},
            {'input': '[2, 2, 1, 1, 1, 2, 2]', 'output': '2'},
        ],
        'test_cases': [
            ('[3, 2, 3]', '3'),
            ('[2, 2, 1, 1, 1, 2, 2]', '2'),
            ('[1]', '1'),
            ('[2, 2, 2, 1, 1]', '2'),
            ('[1, 1, 1, 2, 3]', '1'),
            ('[5, 5, 5, 5, 1]', '5'),
        ]
    },
    # 6. Reverse String
    {
        'title': 'Reverse String',
        'description': 'Given a string s, reverse it character by character.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"hello"',
        'output_example': '"olleh"',
        'categories': ['String'],
        'examples': [
            {'input': 's = "hello"', 'output': '"olleh"'},
            {'input': 's = "abc"', 'output': '"cba"'},
        ],
        'test_cases': [
            ('"hello"', '"olleh"'),
            ('"a"', '"a"'),
            ('"ab"', '"ba"'),
            ('"abc"', '"cba"'),
            ('"racecar"', '"racecar"'),
            ('"12345"', '"54321"'),
        ]
    },
    # 7. Valid Parentheses
    {
        'title': 'Valid Parentheses',
        'description': 'Given a string s containing just the characters "(", ")", "{", "}", "[" and "]", determine if the input string is valid. An input string is valid if brackets are closed in the correct order.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"({[]})"',
        'output_example': 'true',
        'categories': ['String', 'Stack'],
        'examples': [
            {'input': 's = "({[]})"', 'output': 'true'},
            {'input': 's = "({[}])"', 'output': 'false'},
        ],
        'test_cases': [
            ('"({[]})"', 'true'),
            ('"({[}])"', 'false'),
            ('"()"', 'true'),
            ('"(]"', 'false'),
            ('"([)]"', 'false'),
            ('"{[]}"', 'true'),
        ]
    },
    # 8. Palindrome String
    {
        'title': 'Palindrome String',
        'description': 'Given a string s, determine if it is a palindrome, considering only alphanumeric characters and ignoring cases.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"racecar"',
        'output_example': 'true',
        'categories': ['String'],
        'examples': [
            {'input': 's = "racecar"', 'output': 'true'},
            {'input': 's = "hello"', 'output': 'false'},
        ],
        'test_cases': [
            ('"racecar"', 'true'),
            ('"hello"', 'false'),
            ('"a"', 'true'),
            ('"ab"', 'false'),
            ('"aba"', 'true'),
            ('"abba"', 'true'),
        ]
    },
    # 9. First Unique Character
    {
        'title': 'First Unique Character in a String',
        'description': 'Given a string s, find the first character that appears only once in it and return its index. If such character does not exist, return -1.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"leetcode"',
        'output_example': '0',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 's = "leetcode"', 'output': '0'},
            {'input': 's = "loveleetcode"', 'output': '2'},
        ],
        'test_cases': [
            ('"leetcode"', '0'),
            ('"loveleetcode"', '2'),
            ('"aabb"', '-1'),
            ('"a"', '0'),
            ('"abc"', '0'),
            ('"aabcc"', '1'),
        ]
    },
    # 10. Longest Common Prefix
    {
        'title': 'Longest Common Prefix',
        'description': 'Given an array of strings strs, write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string "".',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '["flower","flow","flight"]',
        'output_example': '"fl"',
        'categories': ['String', 'Array'],
        'examples': [
            {'input': 'strs = ["flower","flow","flight"]', 'output': '"fl"'},
            {'input': 'strs = ["dog","racecar","car"]', 'output': '""'},
        ],
        'test_cases': [
            ('["flower","flow","flight"]', '"fl"'),
            ('["dog","racecar","car"]', '""'),
            ('["interspecies","interstellar","interstate"]', '"inters"'),
            ('["a"]', '"a"'),
            ('["ab", "a"]', '"a"'),
            ('["abc", "abc", "abc"]', '"abc"'),
        ]
    },
    # 11. Group Anagrams
    {
        'title': 'Group Anagrams',
        'description': 'Given an array of strings strs, group the anagrams together. You can return the answer in any order.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["eat","tea","tan","ate","nat","bat"]',
        'output_example': '[["bat"],["nat","tan"],["ate","eat","tea"]]',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 'strs = ["eat","tea","tan","ate","nat","bat"]', 'output': '[["bat"],["nat","tan"],["ate","eat","tea"]]'},
            {'input': 'strs = [""]', 'output': '[[""]]'},
        ],
        'test_cases': [
            ('["eat","tea","tan","ate","nat","bat"]', '[["bat"],["nat","tan"],["ate","eat","tea"]]'),
            ('[""]', '[[""]]'),
            ('["a"]', '[["a"]]'),
            ('["ab","ba","abc"]', '[["ab","ba"],["abc"]]'),
            ('["listen","silent","hello"]', '[["listen","silent"],["hello"]]'),
            ('["a","b","ab","ba"]', '[["a"],["b"],["ab","ba"]]'),
        ]
    },
    # 12. Intersection of Two Arrays
    {
        'title': 'Intersection of Two Arrays',
        'description': 'Given two integer arrays nums1 and nums2, return an array of their intersection. Each element in the result must be unique and you may return the result in any order.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1,2,2,1]\n[2,2]',
        'output_example': '[2]',
        'categories': ['Array', 'HashTable'],
        'examples': [
            {'input': 'nums1 = [1,2,2,1], nums2 = [2,2]', 'output': '[2]'},
            {'input': 'nums1 = [4,9,5], nums2 = [9,4,9,8,4]', 'output': '[4,9]'},
        ],
        'test_cases': [
            ('[1,2,2,1]\n[2,2]', '[2]'),
            ('[4,9,5]\n[9,4,9,8,4]', '[4,9]'),
            ('[1,2]\n[2,3]', '[2]'),
            ('[1,2,3]\n[2,3,4]', '[2,3]'),
            ('[]\n[1]', '[]'),
            ('[1]\n[1]', '[1]'),
        ]
    },
    # 13. Word Pattern
    {
        'title': 'Word Pattern',
        'description': 'Given a pattern and a string s, find if s follows the same pattern. Here follow means a full match, such that there is a bijection between letters in pattern and words in s.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"abba"\n"redbluebluered"',
        'output_example': 'true',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 'pattern = "abba", s = "redbluebluered"', 'output': 'true'},
            {'input': 'pattern = "abba", s = "redbluegreen"', 'output': 'false'},
        ],
        'test_cases': [
            ('"abba"\n"redbluebluered"', 'true'),
            ('"abba"\n"redbluegreen"', 'false'),
            ('"aaaa"\n"asdasdasdasd"', 'true'),
            ('"abab"\n"redblueredbluered"', 'false'),
            ('"a"\n"b"', 'true'),
            ('"ab"\n"ba"', 'true'),
        ]
    },
    # 14. Isomorphic Strings
    {
        'title': 'Isomorphic Strings',
        'description': 'Given two strings s and t, determine if they are isomorphic. Two strings s and t are isomorphic if the characters in s can be replaced to get t.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"egg"\n"add"',
        'output_example': 'true',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 's = "egg", t = "add"', 'output': 'true'},
            {'input': 's = "badc", t = "baba"', 'output': 'false'},
        ],
        'test_cases': [
            ('"egg"\n"add"', 'true'),
            ('"badc"\n"baba"', 'false'),
            ('"a"\n"b"', 'true'),
            ('"ab"\n"aa"', 'false'),
            ('"paper"\n"title"', 'true'),
            ('"foo"\n"bar"', 'false'),
        ]
    },
    # 15. Ransom Note
    {
        'title': 'Ransom Note',
        'description': 'Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine. Each letter in magazine can only be used once.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"a"\n"b"',
        'output_example': 'false',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 'ransomNote = "a", magazine = "b"', 'output': 'false'},
            {'input': 'ransomNote = "a", magazine = "a"', 'output': 'true'},
        ],
        'test_cases': [
            ('"a"\n"b"', 'false'),
            ('"a"\n"a"', 'true'),
            ('"aa"\n"ab"', 'false'),
            ('"aa"\n"aab"', 'true'),
            ('"abc"\n"abc"', 'true'),
            ('"abc"\n"xyz"', 'false'),
        ]
    },
    # 16. Power of Two
    {
        'title': 'Power of Two',
        'description': 'Given an integer n, return true if it is a power of 2. Otherwise, return false. An integer n is a power of two, if there exists an integer x such that n == 2^x.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '16',
        'output_example': 'true',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = 16', 'output': 'true'},
            {'input': 'n = 3', 'output': 'false'},
        ],
        'test_cases': [
            ('16', 'true'),
            ('3', 'false'),
            ('1', 'true'),
            ('2', 'true'),
            ('5', 'false'),
            ('1024', 'true'),
        ]
    },
    # 17. Happy Number
    {
        'title': 'Happy Number',
        'description': 'Write an algorithm to determine if a number n is happy. A happy number is defined by the following process: Starting with any positive integer, replace the number by the sum of the squares of its digits.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '19',
        'output_example': 'true',
        'categories': ['Math', 'HashTable'],
        'examples': [
            {'input': 'n = 19', 'output': 'true'},
            {'input': 'n = 2', 'output': 'false'},
        ],
        'test_cases': [
            ('19', 'true'),
            ('2', 'false'),
            ('1', 'true'),
            ('7', 'true'),
            ('10', 'true'),
            ('5', 'false'),
        ]
    },
    # 18. Valid Perfect Square
    {
        'title': 'Valid Perfect Square',
        'description': 'Given a positive integer num, write a function that returns True if num is a perfect square else False. Do not use any built-in library function like sqrt.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '16',
        'output_example': 'true',
        'categories': ['Math'],
        'examples': [
            {'input': 'num = 16', 'output': 'true'},
            {'input': 'num = 14', 'output': 'false'},
        ],
        'test_cases': [
            ('16', 'true'),
            ('14', 'false'),
            ('1', 'true'),
            ('4', 'true'),
            ('9', 'true'),
            ('25', 'true'),
        ]
    },
    # 19. Ugly Number
    {
        'title': 'Ugly Number',
        'description': 'An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5. Given an integer n, return true if n is an ugly number.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '10',
        'output_example': 'true',
        'categories': ['Math', 'DynamicProgramming'],
        'examples': [
            {'input': 'n = 10', 'output': 'true'},
            {'input': 'n = 1', 'output': 'true'},
        ],
        'test_cases': [
            ('10', 'true'),
            ('1', 'true'),
            ('6', 'true'),
            ('8', 'true'),
            ('14', 'false'),
            ('15', 'false'),
        ]
    },
    # 20. Missing Number
    {
        'title': 'Missing Number',
        'description': 'Given an array nums containing n distinct numbers in the range [0, n], return the only number in the range that is missing from the array.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[9,6,4,2,3,5,7,0,1]',
        'output_example': '8',
        'categories': ['Array', 'Math'],
        'examples': [
            {'input': 'nums = [9,6,4,2,3,5,7,0,1]', 'output': '8'},
            {'input': 'nums = [3,0,1]', 'output': '2'},
        ],
        'test_cases': [
            ('[9,6,4,2,3,5,7,0,1]', '8'),
            ('[3,0,1]', '2'),
            ('[0,1]', '2'),
            ('[0]', '1'),
            ('[1]', '0'),
            ('[0,1,2,3,4,5,6,7,9]', '8'),
        ]
    },
    # 21. Min Stack
    {
        'title': 'Min Stack',
        'description': 'Design a stack that supports push, pop, top, and retrieving the minimum element in constant time. Implement the MinStack class.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["push","push","getMin","push","getMin"]\n[[1],[0],[],[-3],[]]',
        'output_example': '[null,null,0,null,-3]',
        'categories': ['Stack'],
        'examples': [
            {'input': 'push(1), push(0), getMin() → 0', 'output': 'minimum is 0'},
            {'input': 'push(-3), getMin() → -3', 'output': 'minimum is -3'},
        ],
        'test_cases': [
            ('["push","push","getMin"]\n[[1],[0],[]]', '[null,null,0]'),
            ('["push","getMin"]\n[[0],[]]', '[null,0]'),
            ('["push","push"]\n[[1],[2]]', '[null,null]'),
            ('["push","push","getMin"]\n[[3],[1],[]]', '[null,null,1]'),
            ('["push","push","getMin"]\n[[2],[0],[]]', '[null,null,0]'),
            ('["push"]\n[[5]]', '[null]'),
        ]
    },
    # 22. Evaluate Reverse Polish Notation
    {
        'title': 'Evaluate Reverse Polish Notation',
        'description': 'Evaluate the value of an arithmetic expression in Reverse Polish Notation. Valid operators are +, -, *, and /. Each operand may be an integer or another expression.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["2","1","+","3","*"]',
        'output_example': '9',
        'categories': ['Array', 'Math', 'Stack'],
        'examples': [
            {'input': 'tokens = ["2","1","+","3","*"]', 'output': '9 (= (2 + 1) * 3)'},
            {'input': 'tokens = ["4","13","5","/","+"]', 'output': '6'},
        ],
        'test_cases': [
            ('["2","1","+","3","*"]', '9'),
            ('["4","13","5","/","+"]', '6'),
            ('["10","6","9","3","+","-11","*","/","*","17","+","5","+"]', '22'),
            ('["3","4","+"]', '7'),
            ('["5","3","-"]', '2'),
            ('["2","3","*"]', '6'),
        ]
    },
    # 23. Daily Temperatures
    {
        'title': 'Daily Temperatures',
        'description': 'Given an array of integers temperatures representing the daily temperatures, return an array answer such that answer[i] is the number of days you have to wait after the ith day to get a warmer temperature.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[73,74,75,71,69,72,76,73]',
        'output_example': '[1,1,4,2,1,1,0,0]',
        'categories': ['Array', 'Stack'],
        'examples': [
            {'input': 'temperatures = [73,74,75,71,69,72,76,73]', 'output': '[1,1,4,2,1,1,0,0]'},
            {'input': 'temperatures = [30,40,50,60]', 'output': '[1,1,1,0]'},
        ],
        'test_cases': [
            ('[73,74,75,71,69,72,76,73]', '[1,1,4,2,1,1,0,0]'),
            ('[30,40,50,60]', '[1,1,1,0]'),
            ('[30,60,90]', '[1,1,0]'),
            ('[90]', '[0]'),
            ('[45,38,20,30,40,35]', '[5,4,3,2,1,0]'),
            ('[50,45,40,35,30]', '[0,0,0,0,0]'),
        ]
    },
    # 24. Trapping Rain Water
    {
        'title': 'Trapping Rain Water',
        'description': 'Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[0,1,0,2,1,0,1,3,2,1,2,1]',
        'output_example': '6',
        'categories': ['Array', 'DynamicProgramming', 'Stack'],
        'examples': [
            {'input': 'height = [0,1,0,2,1,0,1,3,2,1,2,1]', 'output': '6'},
            {'input': 'height = [4,2,0,3,2,5]', 'output': '9'},
        ],
        'test_cases': [
            ('[0,1,0,2,1,0,1,3,2,1,2,1]', '6'),
            ('[4,2,0,3,2,5]', '9'),
            ('[0,1,2]', '0'),
            ('[5,4,3,2,1]', '0'),
            ('[3,0,2,0,4]', '7'),
            ('[2,0,2]', '2'),
        ]
    },
    # 25. Largest Rectangle in Histogram
    {
        'title': 'Largest Rectangle in Histogram',
        'description': 'Given an array of integers heights representing the histogram\'s bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,5,6,2,3]',
        'output_example': '10',
        'categories': ['Array', 'Stack'],
        'examples': [
            {'input': 'heights = [2,1,5,6,2,3]', 'output': '10'},
            {'input': 'heights = [2,4]', 'output': '4'},
        ],
        'test_cases': [
            ('[2,1,5,6,2,3]', '10'),
            ('[2,4]', '4'),
            ('[1]', '1'),
            ('[1,1]', '2'),
            ('[3,2,5,6,1,3]', '10'),
            ('[2,1,2]', '2'),
        ]
    },
    # 26. Binary Tree Level Order Traversal
    {
        'title': 'Binary Tree Level Order Traversal',
        'description': 'Given the root of a binary tree, return the level order traversal of its nodes\' values. (ie, from left to right, level by level).',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[3,9,20,null,null,15,7]',
        'output_example': '[[3],[9,20],[15,7]]',
        'categories': ['Tree', 'Queue'],
        'examples': [
            {'input': 'root = [3,9,20,null,null,15,7]', 'output': '[[3],[9,20],[15,7]]'},
            {'input': 'root = [1]', 'output': '[[1]]'},
        ],
        'test_cases': [
            ('[3,9,20,null,null,15,7]', '[[3],[9,20],[15,7]]'),
            ('[1]', '[[1]]'),
            ('[1,2,3,4,5,null,6]', '[[1],[2,3],[4,5,6]]'),
            ('[1,2,3,4,5,6]', '[[1],[2,3],[4,5,6]]'),
            ('[]', '[]'),
            ('[1,2]', '[[1],[2]]'),
        ]
    },
    # 27. Path Sum
    {
        'title': 'Path Sum',
        'description': 'Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[5,4,8,11,null,null,13,4,7,2,null,null,null,1]\n22',
        'output_example': 'true',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [5,4,8,...], targetSum = 22', 'output': 'true'},
            {'input': 'root = [1,2,3], targetSum = 5', 'output': 'false'},
        ],
        'test_cases': [
            ('[5,4,8,11,null,null,13,4,7,2,null,null,null,1]\n22', 'true'),
            ('[1,2,3]\n5', 'false'),
            ('[1,2]\n0', 'false'),
            ('[1]\n1', 'true'),
            ('[1,2,3]\n6', 'true'),
            ('[1,2,3]\n7', 'false'),
        ]
    },
    # 28. Maximum Depth of Binary Tree
    {
        'title': 'Maximum Depth of Binary Tree',
        'description': 'Given the root of a binary tree, return its maximum depth. A binary tree\'s maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3,9,20,null,null,15,7]',
        'output_example': '3',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [3,9,20,null,null,15,7]', 'output': '3'},
            {'input': 'root = [1,null,2]', 'output': '2'},
        ],
        'test_cases': [
            ('[3,9,20,null,null,15,7]', '3'),
            ('[1,null,2]', '2'),
            ('[1]', '1'),
            ('[]', '0'),
            ('[1,2,3,4,5]', '3'),
            ('[1,2,3,4,5,6]', '3'),
        ]
    },
    # 29. Validate Binary Search Tree
    {
        'title': 'Validate Binary Search Tree',
        'description': 'Given the root of a binary tree, determine if it is a valid binary search tree (BST). A valid BST is defined as follows: the left subtree of a node contains only nodes with keys less than the node\'s key.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,3]',
        'output_example': 'true',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [2,1,3]', 'output': 'true'},
            {'input': 'root = [5,1,4,null,null,3,6]', 'output': 'false'},
        ],
        'test_cases': [
            ('[2,1,3]', 'true'),
            ('[5,1,4,null,null,3,6]', 'false'),
            ('[2,2,2]', 'false'),
            ('[1]', 'true'),
            ('[0]', 'true'),
            ('[32,26,47,19,null,null,56,16,27]', 'true'),
        ]
    },
    # 30. Lowest Common Ancestor of a Binary Search Tree
    {
        'title': 'Lowest Common Ancestor of a Binary Search Tree',
        'description': 'Given a binary search tree (BST) of unique values, find the lowest common ancestor (LCA) of two given nodes in the BST.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[6,2,8,0,4,7,9,null,null,3,5]\n2\n8',
        'output_example': '6',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [6,2,8,...], p = 2, q = 8', 'output': '6'},
            {'input': 'root = [6,2,8,...], p = 2, q = 4', 'output': '2'},
        ],
        'test_cases': [
            ('[6,2,8,0,4,7,9,null,null,3,5]\n2\n8', '6'),
            ('[6,2,8,0,4,7,9,null,null,3,5]\n2\n4', '2'),
            ('[2,1]\n2\n1', '2'),
            ('[6,2,8,0,4,7,9]\n0\n4', '2'),
            ('[1]\n1\n1', '1'),
            ('[5,3,7,2,4,6,8]\n2\n4', '3'),
        ]
    },
]

class Command(BaseCommand):
    help = 'Loads 30 complete problems with categories and examples'

    def handle(self, *args, **options):
        # Clear existing data
        Problem.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('🗑️  Database cleared!'))

        # Create categories
        categories = {}
        for cat_name, cat_desc in CATEGORIES_DATA.items():
            cat = Category.objects.create(name=cat_name, description=cat_desc)
            categories[cat_name] = cat

        self.stdout.write(self.style.SUCCESS('✅ 10 categories created!\n'))
        self.stdout.write(self.style.WARNING('📚 Adding 30 problems...\n'))

        created_count = 0
        for problem_data in PROBLEMS_DATA:
            try:
                problem = Problem.objects.create(
                    title=problem_data['title'],
                    description=problem_data['description'],
                    difficulty=problem_data['difficulty'],
                    function_name=problem_data['function_name'],
                    input_example=problem_data['input_example'],
                    output_example=problem_data['output_example'],
                )

                # Add categories
                for cat_name in problem_data['categories']:
                    problem.categories.add(categories[cat_name])

                # Add examples
                for example_data in problem_data['examples']:
                    Example.objects.create(
                        problem=problem,
                        ex_input=example_data['input'],
                        ex_output=example_data['output']
                    )

                # Add test cases
                for i, (input_data, expected_output) in enumerate(problem_data['test_cases']):
                    TestCase.objects.create(
                        problem=problem,
                        input_data=input_data,
                        expected_output=expected_output,
                        order=i,
                        is_hidden=(i >= 2)
                    )

                created_count += 1
                cats_str = ', '.join(problem_data['categories'])
                self.stdout.write(
                    self.style.SUCCESS(f'✅ {created_count}. {problem_data["title"]} [{cats_str}]')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error: {problem_data["title"]} - {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully added {created_count} problems!'))
        self.stdout.write(self.style.SUCCESS('✅ Each problem has 2 examples!'))
        self.stdout.write(self.style.SUCCESS('✅ Each problem has 6 test cases!'))
        self.stdout.write(self.style.SUCCESS('🎉 Database fully populated!'))
