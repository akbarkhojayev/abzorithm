from django.core.management.base import BaseCommand
from main.models import Problem, Category, TestCase

# Category va problems data
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
    # ARRAY Problems (1-5)
    {
        'title': 'Two Sum',
        'description': 'Given an array of integers nums and an integer target, return the indices of the two numbers that add up to target.\n\nExample 1:\nInput: nums = [2, 7, 11, 15], target = 9\nOutput: [0, 1] (because nums[0] + nums[1] = 9)',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[2, 7, 11, 15]\n9',
        'output_example': '[0, 1]',
        'categories': ['Array', 'HashTable'],
        'test_cases': [
            ('[2, 7, 11, 15]\n9', '[0, 1]'),
            ('[3, 2, 4]\n6', '[1, 2]'),
            ('[3, 3]\n6', '[0, 1]'),
            ('[2, 5, 5, 11]\n10', '[1, 2]'),
            ('[1, 2, 3, 4]\n7', '[2, 3]'),
            ('[10, 1, 1, 0]\n0', '[2, 3]'),
        ]
    },
    {
        'title': 'Best Time to Buy and Sell Stock',
        'description': 'Given an array prices where prices[i] is the price on day i, find the maximum profit you can make by buying and selling once.\n\nExample:\nInput: prices = [7, 1, 5, 3, 6, 4]\nOutput: 5 (buy at 1, sell at 6)',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[7, 1, 5, 3, 6, 4]',
        'output_example': '5',
        'categories': ['Array', 'DynamicProgramming'],
        'test_cases': [
            ('[7, 1, 5, 3, 6, 4]', '5'),
            ('[7, 6, 4, 3, 1]', '0'),
            ('[2, 4, 1]', '2'),
            ('[3, 2, 6, 5, 0, 3]', '4'),
            ('[1]', '0'),
            ('[1, 2, 3, 4, 5]', '4'),
        ]
    },
    {
        'title': 'Contains Duplicate',
        'description': 'Given an integer array nums, return true if any value appears at least twice in the array, and false if every element is distinct.\n\nExample:\nInput: nums = [1, 2, 3, 1]\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 3, 1]',
        'output_example': 'true',
        'categories': ['Array', 'HashTable'],
        'test_cases': [
            ('[1, 2, 3, 1]', 'true'),
            ('[1, 2, 3, 4]', 'false'),
            ('[1, 1, 1, 1]', 'true'),
            ('[1, 2]', 'false'),
            ('[99, 99]', 'true'),
            ('[1, 2, 3, 4, 5]', 'false'),
        ]
    },
    {
        'title': 'Valid Anagram',
        'description': 'Given two strings s and t, return true if t is an anagram of s, and false otherwise.\n\nExample:\nInput: s = "anagram", t = "nagaram"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"anagram"\n"nagaram"',
        'output_example': 'true',
        'categories': ['String', 'HashTable'],
        'test_cases': [
            ('"anagram"\n"nagaram"', 'true'),
            ('"rat"\n"car"', 'false'),
            ('"a"\n"b"', 'false'),
            ('"ab"\n"ba"', 'true'),
            ('"abc"\n"cab"', 'true'),
            ('"listen"\n"silent"', 'true'),
        ]
    },
    {
        'title': 'Majority Element',
        'description': 'Given an array nums of size n, return the majority element. The majority element is the element that appears more than n/2 times.\n\nExample:\nInput: nums = [3, 2, 3]\nOutput: 3',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3, 2, 3]',
        'output_example': '3',
        'categories': ['Array', 'HashTable'],
        'test_cases': [
            ('[3, 2, 3]', '3'),
            ('[2, 2, 1, 1, 1, 2, 2]', '2'),
            ('[1]', '1'),
            ('[2, 2, 2, 1, 1]', '2'),
            ('[1, 1, 1, 2, 3]', '1'),
            ('[5, 5, 5, 5, 1]', '5'),
        ]
    },

    # STRING Problems (6-10)
    {
        'title': 'Reverse String',
        'description': 'Given a string s, reverse it character by character.\n\nExample:\nInput: s = "hello"\nOutput: "olleh"',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"hello"',
        'output_example': '"olleh"',
        'categories': ['String'],
        'test_cases': [
            ('"hello"', '"olleh"'),
            ('"a"', '"a"'),
            ('"ab"', '"ba"'),
            ('"abc"', '"cba"'),
            ('"racecar"', '"racecar"'),
            ('"12345"', '"54321"'),
        ]
    },
    {
        'title': 'Valid Parentheses',
        'description': 'Given a string s containing only (), {}, and [], determine if the input string is valid.\n\nExample:\nInput: s = "({[]}"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"({[]})"',
        'output_example': 'true',
        'categories': ['String', 'Stack'],
        'test_cases': [
            ('"({[]})"', 'true'),
            ('"({[}])"', 'false'),
            ('"()"', 'true'),
            ('"(]"', 'false'),
            ('"([)]"', 'false'),
            ('"{[]}"', 'true'),
        ]
    },
    {
        'title': 'Palindrome String',
        'description': 'Given a string s, determine if it is a palindrome, considering only alphanumeric characters.\n\nExample:\nInput: s = "A man, a plan, a canal: Panama"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"racecar"',
        'output_example': 'true',
        'categories': ['String'],
        'test_cases': [
            ('"racecar"', 'true'),
            ('"hello"', 'false'),
            ('"a"', 'true'),
            ('"ab"', 'false'),
            ('"aba"', 'true'),
            ('"abba"', 'true'),
        ]
    },
    {
        'title': 'First Unique Character',
        'description': 'Given a string s, find the first character that appears only once in it and return its index.\n\nExample:\nInput: s = "leetcode"\nOutput: 0',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"leetcode"',
        'output_example': '0',
        'categories': ['String', 'HashTable'],
        'test_cases': [
            ('"leetcode"', '0'),
            ('"loveleetcode"', '2'),
            ('"aabb"', '-1'),
            ('"a"', '0'),
            ('"abc"', '0'),
            ('"aabcc"', '1'),
        ]
    },
    {
        'title': 'Longest Common Prefix',
        'description': 'Given an array of strings strs, write a function to find the longest common prefix string amongst an array of strings.\n\nExample:\nInput: strs = ["flower","flow","flight"]\nOutput: "fl"',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '["flower","flow","flight"]',
        'output_example': '"fl"',
        'categories': ['String', 'Array'],
        'test_cases': [
            ('["flower","flow","flight"]', '"fl"'),
            ('["dog","racecar","car"]', '""'),
            ('["interspecies","interstellar","interstate"]', '"inters"'),
            ('["a"]', '"a"'),
            ('["ab", "a"]', '"a"'),
            ('["abc", "abc", "abc"]', '"abc"'),
        ]
    },

    # HASHMAP/DICTIONARY Problems (11-15)
    {
        'title': 'Group Anagrams',
        'description': 'Given an array of strings strs, group the anagrams together.\n\nExample:\nInput: strs = ["eat","tea","tan","ate","nat","bat"]\nOutput: [["bat"],["nat","tan"],["ate","eat","tea"]]',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["eat","tea","tan","ate","nat","bat"]',
        'output_example': '[["bat"],["nat","tan"],["ate","eat","tea"]]',
        'categories': ['String', 'HashTable'],
        'test_cases': [
            ('["eat","tea","tan","ate","nat","bat"]', '[["bat"],["nat","tan"],["ate","eat","tea"]]'),
            ('[""]', '[[""]]'),
            ('["a"]', '[["a"]]'),
            ('["ab","ba","abc"]', '[["ab","ba"],["abc"]]'),
            ('["listen","silent","hello"]', '[["listen","silent"],["hello"]]'),
            ('["a","b","ab","ba"]', '[["a"],["b"],["ab","ba"]]'),
        ]
    },
    {
        'title': 'Intersection of Two Arrays',
        'description': 'Given two integer arrays nums1 and nums2, return an array of their intersection.\n\nExample:\nInput: nums1 = [1,2,2,1], nums2 = [2,2]\nOutput: [2]',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1,2,2,1]\n[2,2]',
        'output_example': '[2]',
        'categories': ['Array', 'HashTable'],
        'test_cases': [
            ('[1,2,2,1]\n[2,2]', '[2]'),
            ('[4,9,5]\n[9,4,9,8,4]', '[4,9]'),
            ('[1,2]\n[2,3]', '[2]'),
            ('[1,2,3]\n[2,3,4]', '[2,3]'),
            ('[]\n[1]', '[]'),
            ('[1]\n[1]', '[1]'),
        ]
    },
    {
        'title': 'Word Pattern',
        'description': 'Given a pattern and a string s, find if s follows the same pattern.\n\nExample:\nInput: pattern = "abba", s = "redbluebluered"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"abba"\n"redbluebluered"',
        'output_example': 'true',
        'categories': ['String', 'HashTable'],
        'test_cases': [
            ('"abba"\n"redbluebluered"', 'true'),
            ('"abba"\n"redbluegreen"', 'false'),
            ('"aaaa"\n"asdasdasdasd"', 'true'),
            ('"abab"\n"redblueredbluered"', 'false'),
            ('"a"\n"b"', 'true'),
            ('"ab"\n"ba"', 'true'),
        ]
    },
    {
        'title': 'Isomorphic Strings',
        'description': 'Given two strings s and t, determine if they are isomorphic.\n\nExample:\nInput: s = "egg", t = "add"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"egg"\n"add"',
        'output_example': 'true',
        'categories': ['String', 'HashTable'],
        'test_cases': [
            ('"egg"\n"add"', 'true'),
            ('"badc"\n"baba"', 'false'),
            ('"a"\n"b"', 'true'),
            ('"ab"\n"aa"', 'false'),
            ('"paper"\n"title"', 'true'),
            ('"foo"\n"bar"', 'false'),
        ]
    },
    {
        'title': 'Ransom Note',
        'description': 'Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine.\n\nExample:\nInput: ransomNote = "a", magazine = "b"\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"a"\n"b"',
        'output_example': 'false',
        'categories': ['String', 'HashTable'],
        'test_cases': [
            ('"a"\n"b"', 'false'),
            ('"a"\n"a"', 'true'),
            ('"aa"\n"ab"', 'false'),
            ('"aa"\n"aab"', 'true'),
            ('"abc"\n"abc"', 'true'),
            ('"abc"\n"xyz"', 'false'),
        ]
    },

    # MATH Problems (16-20)
    {
        'title': 'Power of Two',
        'description': 'Given an integer n, return true if it is a power of 2. Otherwise, return false.\n\nExample:\nInput: n = 16\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '16',
        'output_example': 'true',
        'categories': ['Math'],
        'test_cases': [
            ('16', 'true'),
            ('3', 'false'),
            ('1', 'true'),
            ('2', 'true'),
            ('5', 'false'),
            ('1024', 'true'),
        ]
    },
    {
        'title': 'Happy Number',
        'description': 'Write an algorithm to determine if a number n is happy.\n\nExample:\nInput: n = 19\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '19',
        'output_example': 'true',
        'categories': ['Math', 'HashTable'],
        'test_cases': [
            ('19', 'true'),
            ('2', 'false'),
            ('1', 'true'),
            ('7', 'true'),
            ('10', 'true'),
            ('5', 'false'),
        ]
    },
    {
        'title': 'Valid Perfect Square',
        'description': 'Given a positive integer num, write a function that returns True if num is a perfect square else False.\n\nExample:\nInput: num = 16\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '16',
        'output_example': 'true',
        'categories': ['Math'],
        'test_cases': [
            ('16', 'true'),
            ('14', 'false'),
            ('1', 'true'),
            ('4', 'true'),
            ('9', 'true'),
            ('25', 'true'),
        ]
    },
    {
        'title': 'Ugly Number',
        'description': 'An ugly number is a positive integer whose prime factors are limited to 2, 3, and 5.\n\nExample:\nInput: n = 10\nOutput: true (10 = 2 × 5)',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '10',
        'output_example': 'true',
        'categories': ['Math', 'DynamicProgramming'],
        'test_cases': [
            ('10', 'true'),
            ('1', 'true'),
            ('6', 'true'),
            ('8', 'true'),
            ('14', 'false'),
            ('15', 'false'),
        ]
    },
    {
        'title': 'Missing Number',
        'description': 'Given an array nums containing n distinct numbers in the range [0, n], return the only number that is missing from the array.\n\nExample:\nInput: nums = [9,6,4,2,3,5,7,0,1]\nOutput: 8',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[9,6,4,2,3,5,7,0,1]',
        'output_example': '8',
        'categories': ['Array', 'Math'],
        'test_cases': [
            ('[9,6,4,2,3,5,7,0,1]', '8'),
            ('[3,0,1]', '2'),
            ('[0,1]', '2'),
            ('[0]', '1'),
            ('[1]', '0'),
            ('[0,1,2,3,4,5,6,7,9]', '8'),
        ]
    },

    # STACK Problems (21-25)
    {
        'title': 'Min Stack',
        'description': 'Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.\n\nExample:\nInput: push(1), push(0), getMin() → 0, push(-3), getMin() → -3, pop()',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["push","push","getMin","push","getMin"]\n[[1],[0],[],[-3],[]]',
        'output_example': '[null,null,0,null,-3]',
        'categories': ['Stack'],
        'test_cases': [
            ('["push","push","getMin"]\n[[1],[0],[]]', '[null,null,0]'),
            ('["push","getMin"]\n[[0],[]]', '[null,0]'),
            ('["push","push"]\n[[1],[2]]', '[null,null]'),
            ('["push","push","getMin"]\n[[3],[1],[]]', '[null,null,1]'),
            ('["push","push","getMin"]\n[[2],[0],[]]', '[null,null,0]'),
            ('["push"]\n[[5]]', '[null]'),
        ]
    },
    {
        'title': 'Evaluate Reverse Polish Notation',
        'description': 'Evaluate the value of an arithmetic expression in Reverse Polish Notation.\n\nExample:\nInput: tokens = ["2","1","+","3","*"]\nOutput: 9 (= ((2 + 1) × 3) = 9)',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["2","1","+","3","*"]',
        'output_example': '9',
        'categories': ['Array', 'Math', 'Stack'],
        'test_cases': [
            ('["2","1","+","3","*"]', '9'),
            ('["4","13","5","/","+"]', '6'),
            ('["10","6","9","3","+","-11","*","/","*","17","+","5","+"]', '22'),
            ('["3","4","+"]', '7'),
            ('["5","3","-"]', '2'),
            ('["2","3","*"]', '6'),
        ]
    },
    {
        'title': 'Daily Temperatures',
        'description': 'Given an array of integers temperatures and the daily temperatures, return an array answer where answer[i] is the number of days you have to wait until a warmer temperature.\n\nExample:\nInput: temperatures = [73,74,75,71,69,72,76,73]\nOutput: [1,1,4,2,1,1,0,0]',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[73,74,75,71,69,72,76,73]',
        'output_example': '[1,1,4,2,1,1,0,0]',
        'categories': ['Array', 'Stack'],
        'test_cases': [
            ('[73,74,75,71,69,72,76,73]', '[1,1,4,2,1,1,0,0]'),
            ('[30,40,50,60]', '[1,1,1,0]'),
            ('[30,60,90]', '[1,1,0]'),
            ('[90]', '[0]'),
            ('[45,38,20,30,40,35]', '[5,4,3,2,1,0]'),
            ('[50,45,40,35,30]', '[0,0,0,0,0]'),
        ]
    },
    {
        'title': 'Trapping Rain Water',
        'description': 'Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.\n\nExample:\nInput: height = [0,1,0,2,1,0,1,3,2,1,2,1]\nOutput: 6',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[0,1,0,2,1,0,1,3,2,1,2,1]',
        'output_example': '6',
        'categories': ['Array', 'DynamicProgramming', 'Stack'],
        'test_cases': [
            ('[0,1,0,2,1,0,1,3,2,1,2,1]', '6'),
            ('[4,2,0,3,2,5]', '9'),
            ('[0,1,2]', '0'),
            ('[5,4,3,2,1]', '0'),
            ('[3,0,2,0,4]', '7'),
            ('[2,0,2]', '2'),
        ]
    },
    {
        'title': 'Largest Rectangle in Histogram',
        'description': 'Given an array of integers heights representing the histogram\'s bar height where the width of each bar is 1, return the area of the largest rectangle in the histogram.\n\nExample:\nInput: heights = [2,1,5,6,2,3]\nOutput: 10',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,5,6,2,3]',
        'output_example': '10',
        'categories': ['Array', 'Stack'],
        'test_cases': [
            ('[2,1,5,6,2,3]', '10'),
            ('[2,4]', '4'),
            ('[1]', '1'),
            ('[1,1]', '2'),
            ('[3,2,5,6,1,3]', '10'),
            ('[2,1,2]', '2'),
        ]
    },

    # TREE Problems (26-30)
    {
        'title': 'Binary Tree Level Order Traversal',
        'description': 'Given the root of a binary tree, return the level order traversal of its nodes\' values (left to right, level by level).\n\nExample:\nInput: root = [3,9,20,null,null,15,7]\nOutput: [[3],[9,20],[15,7]]',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[3,9,20,null,null,15,7]',
        'output_example': '[[3],[9,20],[15,7]]',
        'categories': ['Tree', 'Queue'],
        'test_cases': [
            ('[3,9,20,null,null,15,7]', '[[3],[9,20],[15,7]]'),
            ('[1]', '[[1]]'),
            ('[1,2,3,4,5,null,6]', '[[1],[2,3],[4,5,6]]'),
            ('[1,2,3,4,5,6]', '[[1],[2,3],[4,5,6]]'),
            ('[]', '[]'),
            ('[1,2]', '[[1],[2]]'),
        ]
    },
    {
        'title': 'Path Sum',
        'description': 'Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.\n\nExample:\nInput: root = [5,4,8,11,null,13,4,7,2,null,null,null,1], targetSum = 22\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[5,4,8,11,null,null,13,4,7,2,null,null,null,1]\n22',
        'output_example': 'true',
        'categories': ['Tree'],
        'test_cases': [
            ('[5,4,8,11,null,null,13,4,7,2,null,null,null,1]\n22', 'true'),
            ('[1,2,3]\n5', 'false'),
            ('[1,2]\n0', 'false'),
            ('[1]\n1', 'true'),
            ('[1,2,3]\n6', 'true'),
            ('[1,2,3]\n7', 'false'),
        ]
    },
    {
        'title': 'Maximum Depth of Binary Tree',
        'description': 'Given the root of a binary tree, return its maximum depth.\n\nExample:\nInput: root = [3,9,20,null,null,15,7]\nOutput: 3',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3,9,20,null,null,15,7]',
        'output_example': '3',
        'categories': ['Tree'],
        'test_cases': [
            ('[3,9,20,null,null,15,7]', '3'),
            ('[1,null,2]', '2'),
            ('[1]', '1'),
            ('[]', '0'),
            ('[1,2,3,4,5]', '3'),
            ('[1,2,3,4,5,6]', '3'),
        ]
    },
    {
        'title': 'Validate Binary Search Tree',
        'description': 'Given the root of a binary tree, determine if it is a valid binary search tree (BST).\n\nExample:\nInput: root = [2,1,3]\nOutput: true',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,3]',
        'output_example': 'true',
        'categories': ['Tree'],
        'test_cases': [
            ('[2,1,3]', 'true'),
            ('[5,1,4,null,null,3,6]', 'false'),
            ('[2,2,2]', 'false'),
            ('[1]', 'true'),
            ('[0]', 'true'),
            ('[32,26,47,19,null,null,56,16,27]', 'true'),
        ]
    },
    {
        'title': 'Lowest Common Ancestor of a Binary Search Tree',
        'description': 'Given a binary search tree (BST) of unique values, find the lowest common ancestor (LCA) of two given nodes in the BST.\n\nExample:\nInput: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8\nOutput: 6',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[6,2,8,0,4,7,9,null,null,3,5]\n2\n8',
        'output_example': '6',
        'categories': ['Tree'],
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
    help = 'Loads 30 problems with categories'

    def handle(self, *args, **options):
        # Clear existing data
        Problem.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('🗑️  Database cleared!'))

        # Create categories first
        categories = {}
        for cat_name, cat_desc in CATEGORIES_DATA.items():
            cat = Category.objects.create(name=cat_name, description=cat_desc)
            categories[cat_name] = cat
            self.stdout.write(self.style.SUCCESS(f'✅ Created category: {cat_name}'))

        self.stdout.write(self.style.WARNING('\n📚 Adding problems...\n'))

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

                # Add categories to problem
                for cat_name in problem_data['categories']:
                    problem.categories.add(categories[cat_name])

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
                    self.style.SUCCESS(f'✅ {problem_data["title"]} [{cats_str}]')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error: {problem_data["title"]} - {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully added {created_count} problems!'))
        self.stdout.write(self.style.SUCCESS(f'✅ {len(categories)} categories created!'))
        self.stdout.write(self.style.SUCCESS('🎉 Database ready with categories!'))
