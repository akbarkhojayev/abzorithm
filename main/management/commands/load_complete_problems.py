from django.core.management.base import BaseCommand
from main.models import Problem, TestCase

problems_data = [
    # EASY - Mathematical Operations (1-10)
    {
        'title': 'Multiply Two Numbers',
        'description': 'Given two integers a and b, return their product (a * b).\n\nExample 1:\nInput: a = 4, b = 5\nOutput: 20\n\nExample 2:\nInput: a = -3, b = 7\nOutput: -21',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '4\n5',
        'output_example': '20',
        'test_cases': [
            ('4\n5', '20'),
            ('-3\n7', '-21'),
            ('0\n100', '0'),
            ('-2\n-3', '6'),
            ('1\n1', '1'),
            ('10\n-10', '-100'),
        ]
    },
    {
        'title': 'Sum of Two Numbers',
        'description': 'Given two integers a and b, return their sum.\n\nExample 1:\nInput: a = 5, b = 3\nOutput: 8\n\nExample 2:\nInput: a = -1, b = 1\nOutput: 0',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '5\n3',
        'output_example': '8',
        'test_cases': [
            ('5\n3', '8'),
            ('-1\n1', '0'),
            ('10\n20', '30'),
            ('-5\n-3', '-8'),
            ('0\n0', '0'),
            ('100\n-50', '50'),
        ]
    },
    {
        'title': 'Subtract Two Numbers',
        'description': 'Given two integers a and b, return their difference (a - b).\n\nExample 1:\nInput: a = 10, b = 3\nOutput: 7\n\nExample 2:\nInput: a = 5, b = 8\nOutput: -3',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '10\n3',
        'output_example': '7',
        'test_cases': [
            ('10\n3', '7'),
            ('5\n8', '-3'),
            ('0\n5', '-5'),
            ('-10\n-5', '-5'),
            ('15\n15', '0'),
            ('-3\n-8', '5'),
        ]
    },
    {
        'title': 'Absolute Value',
        'description': 'Given an integer n, return its absolute value (distance from 0).\n\nExample 1:\nInput: n = -5\nOutput: 5\n\nExample 2:\nInput: n = 10\nOutput: 10',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '-5',
        'output_example': '5',
        'test_cases': [
            ('-5', '5'),
            ('10', '10'),
            ('0', '0'),
            ('-100', '100'),
            ('1', '1'),
            ('-1', '1'),
        ]
    },
    {
        'title': 'Check if Positive',
        'description': 'Given an integer n, return true if n is positive (greater than 0), false otherwise.\n\nExample 1:\nInput: n = 5\nOutput: true\n\nExample 2:\nInput: n = -3\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '5',
        'output_example': 'true',
        'test_cases': [
            ('5', 'true'),
            ('-3', 'false'),
            ('0', 'false'),
            ('1', 'true'),
            ('-1', 'false'),
            ('100', 'true'),
        ]
    },
    {
        'title': 'Check if Negative',
        'description': 'Given an integer n, return true if n is negative (less than 0), false otherwise.\n\nExample 1:\nInput: n = -5\nOutput: true\n\nExample 2:\nInput: n = 3\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '-5',
        'output_example': 'true',
        'test_cases': [
            ('-5', 'true'),
            ('3', 'false'),
            ('0', 'false'),
            ('-1', 'true'),
            ('1', 'false'),
            ('-100', 'true'),
        ]
    },
    {
        'title': 'Check if Even',
        'description': 'Given an integer n, return true if n is even, false if odd.\n\nExample 1:\nInput: n = 4\nOutput: true\n\nExample 2:\nInput: n = 7\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '4',
        'output_example': 'true',
        'test_cases': [
            ('4', 'true'),
            ('7', 'false'),
            ('0', 'true'),
            ('-2', 'true'),
            ('-3', 'false'),
            ('100', 'true'),
        ]
    },
    {
        'title': 'Check if Odd',
        'description': 'Given an integer n, return true if n is odd, false if even.\n\nExample 1:\nInput: n = 3\nOutput: true\n\nExample 2:\nInput: n = 4\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '3',
        'output_example': 'true',
        'test_cases': [
            ('3', 'true'),
            ('4', 'false'),
            ('0', 'false'),
            ('-1', 'true'),
            ('-2', 'false'),
            ('99', 'true'),
        ]
    },
    {
        'title': 'Maximum of Two',
        'description': 'Given two integers a and b, return the maximum (larger) value.\n\nExample 1:\nInput: a = 5, b = 3\nOutput: 5\n\nExample 2:\nInput: a = -10, b = -20\nOutput: -10',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '5\n3',
        'output_example': '5',
        'test_cases': [
            ('5\n3', '5'),
            ('-10\n-20', '-10'),
            ('0\n0', '0'),
            ('100\n50', '100'),
            ('-5\n5', '5'),
            ('1\n1', '1'),
        ]
    },
    {
        'title': 'Minimum of Two',
        'description': 'Given two integers a and b, return the minimum (smaller) value.\n\nExample 1:\nInput: a = 5, b = 3\nOutput: 3\n\nExample 2:\nInput: a = -10, b = -20\nOutput: -20',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '5\n3',
        'output_example': '3',
        'test_cases': [
            ('5\n3', '3'),
            ('-10\n-20', '-20'),
            ('0\n0', '0'),
            ('100\n50', '50'),
            ('-5\n5', '-5'),
            ('1\n1', '1'),
        ]
    },

    # MEDIUM - More Complex (11-20)
    {
        'title': 'Reverse an Integer',
        'description': 'Given an integer n, return the integer with digits reversed.\n\nExample 1:\nInput: n = 123\nOutput: 321\n\nExample 2:\nInput: n = -456\nOutput: -654',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '123',
        'output_example': '321',
        'test_cases': [
            ('123', '321'),
            ('-456', '-654'),
            ('1000', '1'),
            ('0', '0'),
            ('100', '1'),
            ('999', '999'),
        ]
    },
    {
        'title': 'Sum of Digits',
        'description': 'Given an integer n, return the sum of its digits.\n\nExample 1:\nInput: n = 123\nOutput: 6\n\nExample 2:\nInput: n = 456\nOutput: 15',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '123',
        'output_example': '6',
        'test_cases': [
            ('123', '6'),
            ('456', '15'),
            ('0', '0'),
            ('1000', '1'),
            ('999', '27'),
            ('1', '1'),
        ]
    },
    {
        'title': 'Count Digits',
        'description': 'Given an integer n, return the number of digits.\n\nExample 1:\nInput: n = 123\nOutput: 3\n\nExample 2:\nInput: n = 1000\nOutput: 4',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '123',
        'output_example': '3',
        'test_cases': [
            ('123', '3'),
            ('1000', '4'),
            ('0', '1'),
            ('1', '1'),
            ('999999', '6'),
            ('-456', '3'),
        ]
    },
    {
        'title': 'Check if Prime',
        'description': 'Given an integer n, return true if it is a prime number, false otherwise.\n\nExample 1:\nInput: n = 7\nOutput: true\n\nExample 2:\nInput: n = 4\nOutput: false',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '7',
        'output_example': 'true',
        'test_cases': [
            ('7', 'true'),
            ('4', 'false'),
            ('2', 'true'),
            ('1', 'false'),
            ('17', 'true'),
            ('20', 'false'),
        ]
    },
    {
        'title': 'Factorial',
        'description': 'Given a non-negative integer n, return n! (factorial).\n\nExample 1:\nInput: n = 5\nOutput: 120\n\nExample 2:\nInput: n = 0\nOutput: 1',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '5',
        'output_example': '120',
        'test_cases': [
            ('5', '120'),
            ('0', '1'),
            ('1', '1'),
            ('3', '6'),
            ('4', '24'),
            ('6', '720'),
        ]
    },
    {
        'title': 'Power Function',
        'description': 'Given integers a and b, return a^b (a raised to power b).\n\nExample 1:\nInput: a = 2, b = 3\nOutput: 8\n\nExample 2:\nInput: a = 5, b = 2\nOutput: 25',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '2\n3',
        'output_example': '8',
        'test_cases': [
            ('2\n3', '8'),
            ('5\n2', '25'),
            ('10\n0', '1'),
            ('2\n0', '1'),
            ('3\n3', '27'),
            ('2\n5', '32'),
        ]
    },
    {
        'title': 'GCD (Greatest Common Divisor)',
        'description': 'Given two integers a and b, return their GCD.\n\nExample 1:\nInput: a = 48, b = 18\nOutput: 6\n\nExample 2:\nInput: a = 12, b = 8\nOutput: 4',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '48\n18',
        'output_example': '6',
        'test_cases': [
            ('48\n18', '6'),
            ('12\n8', '4'),
            ('10\n5', '5'),
            ('7\n3', '1'),
            ('100\n50', '50'),
            ('21\n14', '7'),
        ]
    },
    {
        'title': 'LCM (Least Common Multiple)',
        'description': 'Given two integers a and b, return their LCM.\n\nExample 1:\nInput: a = 12, b = 18\nOutput: 36\n\nExample 2:\nInput: a = 4, b = 6\nOutput: 12',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '12\n18',
        'output_example': '36',
        'test_cases': [
            ('12\n18', '36'),
            ('4\n6', '12'),
            ('5\n7', '35'),
            ('10\n15', '30'),
            ('3\n5', '15'),
            ('6\n8', '24'),
        ]
    },
    {
        'title': 'Check if Palindrome Number',
        'description': 'Given an integer n, return true if it is a palindrome number, false otherwise.\n\nExample 1:\nInput: n = 121\nOutput: true\n\nExample 2:\nInput: n = 123\nOutput: false',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '121',
        'output_example': 'true',
        'test_cases': [
            ('121', 'true'),
            ('123', 'false'),
            ('0', 'true'),
            ('10', 'false'),
            ('1001', 'true'),
            ('1221', 'true'),
        ]
    },

    # HARD - Challenging (21-30)
    {
        'title': 'Fibonacci Number',
        'description': 'Given an integer n, return the n-th Fibonacci number.\n\nExample 1:\nInput: n = 4\nOutput: 3\n\nExample 2:\nInput: n = 6\nOutput: 8',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '4',
        'output_example': '3',
        'test_cases': [
            ('4', '3'),
            ('6', '8'),
            ('0', '0'),
            ('1', '1'),
            ('5', '5'),
            ('7', '13'),
        ]
    },
    {
        'title': 'Longest Common Substring',
        'description': 'Given two strings s1 and s2, return the length of their longest common substring.\n\nExample 1:\nInput: s1 = "hello", s2 = "ello"\nOutput: 4\n\nExample 2:\nInput: s1 = "abc", s2 = "def"\nOutput: 0',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '"hello"\n"ello"',
        'output_example': '4',
        'test_cases': [
            ('"hello"\n"ello"', '4'),
            ('"abc"\n"def"', '0'),
            ('"programming"\n"gaming"', '6'),
            ('"test"\n"test"', '4'),
            ('"a"\n"b"', '0'),
            ('"xyz"\n"yza"', '2'),
        ]
    },
    {
        'title': 'Edit Distance',
        'description': 'Given two strings word1 and word2, return the minimum number of operations to convert word1 to word2.\n\nExample 1:\nInput: word1 = "horse", word2 = "ros"\nOutput: 3\n\nExample 2:\nInput: word1 = "intention", word2 = "execution"\nOutput: 5',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '"horse"\n"ros"',
        'output_example': '3',
        'test_cases': [
            ('"horse"\n"ros"', '3'),
            ('"intention"\n"execution"', '5'),
            ('"a"\n"b"', '1'),
            ('"cat"\n"cat"', '0'),
            ('"abc"\n""', '3'),
            ('""\n"abc"', '3'),
        ]
    },
    {
        'title': 'Maximum Subarray Sum',
        'description': 'Given an array of integers, return the maximum sum of a contiguous subarray.\n\nExample 1:\nInput: [-2, 1, -3, 4, -1, 2, 1, -5, 4]\nOutput: 6\n\nExample 2:\nInput: [5, 4, -1, 7, 8]\nOutput: 23',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[-2, 1, -3, 4, -1, 2, 1, -5, 4]',
        'output_example': '6',
        'test_cases': [
            ('[-2, 1, -3, 4, -1, 2, 1, -5, 4]', '6'),
            ('[5, 4, -1, 7, 8]', '23'),
            ('[-1]', '-1'),
            ('[1, 2, 3, 4, 5]', '15'),
            ('[-5, -3, -2]', '-2'),
            ('[1, -3, 2, -2, 5]', '5'),
        ]
    },
    {
        'title': 'Longest Palindromic Substring',
        'description': 'Given a string s, return the longest palindromic substring.\n\nExample 1:\nInput: s = "babad"\nOutput: "bab" or "aba"\n\nExample 2:\nInput: s = "cbbd"\nOutput: "bb"',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '"babad"',
        'output_example': '"bab"',
        'test_cases': [
            ('"babad"', '"bab"'),
            ('"cbbd"', '"bb"'),
            ('"a"', '"a"'),
            ('"ac"', '"a"'),
            ('"abacabad"', '"abacaba"'),
            ('"racecar"', '"racecar"'),
        ]
    },
    {
        'title': 'Coin Change',
        'description': 'Given coins of different denominations and an amount, return the minimum number of coins needed to make that amount.\n\nExample 1:\nInput: coins = [1, 2, 5], amount = 5\nOutput: 1\n\nExample 2:\nInput: coins = [2], amount = 3\nOutput: -1',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 5]\n5',
        'output_example': '1',
        'test_cases': [
            ('[1, 2, 5]\n5', '1'),
            ('[2]\n3', '-1'),
            ('[10]\n10', '1'),
            ('[1]\n1', '1'),
            ('[2, 5, 10]\n27', '4'),
            ('[1, 3, 4]\n6', '2'),
        ]
    },
    {
        'title': 'Word Ladder',
        'description': 'Given two words and a list of words, find if we can go from the first word to the second word by changing one letter at a time.\n\nExample 1:\nInput: beginWord = "hit", endWord = "cog", wordList = ["hot", "dot", "dog", "lot", "log", "cog"]\nOutput: true\n\nExample 2:\nInput: beginWord = "hit", endWord = "cog", wordList = ["hot", "dot", "dog", "lot", "log"]\nOutput: false',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '"hit"\n"cog"\n["hot", "dot", "dog", "lot", "log", "cog"]',
        'output_example': 'true',
        'test_cases': [
            ('"hit"\n"cog"\n["hot", "dot", "dog", "lot", "log", "cog"]', 'true'),
            ('"hit"\n"cog"\n["hot", "dot", "dog", "lot", "log"]', 'false'),
            ('"a"\n"c"\n["a", "b", "c"]', 'true'),
            ('"cat"\n"bat"\n["bat"]', 'true'),
            ('"a"\n"b"\n[]', 'false'),
            ('"cold"\n"warm"\n["cold", "cord", "card", "ward", "warm"]', 'true'),
        ]
    },
    {
        'title': 'Regular Expression Matching',
        'description': 'Given a string s and a pattern p, implement regular expression matching with support for \'.\'(any character) and \'*\'(zero or more of the preceding element).\n\nExample 1:\nInput: s = "aa", p = "a"\nOutput: false\n\nExample 2:\nInput: s = "aa", p = "a*"\nOutput: true',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '"aa"\n"a"',
        'output_example': 'false',
        'test_cases': [
            ('"aa"\n"a"', 'false'),
            ('"aa"\n"a*"', 'true'),
            ('"ab"\n".*"', 'true'),
            ('"aab"\n"c*a*b"', 'true'),
            ('"mississippi"\n"m*iss*p*.."', 'false'),
            ('"ab"\n".*c"', 'false'),
        ]
    },
    {
        'title': 'Merge K Sorted Lists',
        'description': 'Given an array of k sorted linked lists, merge them into a single sorted list.\n\nExample 1:\nInput: lists = [[1, 4, 5], [1, 3, 4], [2, 6]]\nOutput: [1, 1, 2, 3, 4, 4, 5, 6]\n\nExample 2:\nInput: lists = []\nOutput: []',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[[1, 4, 5], [1, 3, 4], [2, 6]]',
        'output_example': '[1, 1, 2, 3, 4, 4, 5, 6]',
        'test_cases': [
            ('[[1, 4, 5], [1, 3, 4], [2, 6]]', '[1, 1, 2, 3, 4, 4, 5, 6]'),
            ('[]', '[]'),
            ('[[]]', '[]'),
            ('[[1]]', '[1]'),
            ('[[1, 2], [3, 4]]', '[1, 2, 3, 4]'),
            ('[[5], [1], [1, 2, 3]]', '[1, 1, 2, 3, 5]'),
        ]
    },
    {
        'title': 'Median of Two Sorted Arrays',
        'description': 'Given two sorted arrays, find the median of the combined sorted array.\n\nExample 1:\nInput: nums1 = [1, 3], nums2 = [2]\nOutput: 2.0\n\nExample 2:\nInput: nums1 = [1, 2], nums2 = [3, 4]\nOutput: 2.5',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[1, 3]\n[2]',
        'output_example': '2.0',
        'test_cases': [
            ('[1, 3]\n[2]', '2.0'),
            ('[1, 2]\n[3, 4]', '2.5'),
            ('[0, 0]\n[0, 0]', '0.0'),
            ('[]\\n[1]', '1.0'),
            ('[2]\n[]', '2.0'),
            ('[1, 3, 5]\n[2, 4, 6]', '3.5'),
        ]
    },
    {
        'title': 'Wildcard Matching',
        'description': 'Implement wildcard pattern matching with support for \'?\'(single character) and \'*\'(any sequence of characters).\n\nExample 1:\nInput: s = "aa", p = "a"\nOutput: false\n\nExample 2:\nInput: s = "aa", p = "*"\nOutput: true',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '"aa"\n"a"',
        'output_example': 'false',
        'test_cases': [
            ('"aa"\n"a"', 'false'),
            ('"aa"\n"*"', 'true'),
            ('"cb"\n"?a"', 'false'),
            ('"adceb"\n"*a*b"', 'true'),
            ('"acdcb"\n"a*c?b"', 'false'),
            ('"aa"\n"*"', 'true'),
        ]
    },
]

class Command(BaseCommand):
    help = 'Loads 30 complete problems with all difficulty levels'

    def handle(self, *args, **options):
        # Clear existing problems
        Problem.objects.all().delete()
        self.stdout.write(self.style.WARNING('Database cleared!'))

        created_count = 0

        for problem_data in problems_data:
            try:
                problem = Problem.objects.create(
                    title=problem_data['title'],
                    description=problem_data['description'],
                    difficulty=problem_data['difficulty'],
                    function_name=problem_data['function_name'],
                    input_example=problem_data['input_example'],
                    output_example=problem_data['output_example'],
                    tags='algorithm,coding'
                )

                # Add test cases
                for i, (input_data, expected_output) in enumerate(problem_data['test_cases']):
                    TestCase.objects.create(
                        problem=problem,
                        input_data=input_data,
                        expected_output=expected_output,
                        order=i,
                        is_hidden=(i >= 2)  # First 2 are public, rest are hidden
                    )

                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Added: {problem_data["title"]} ({problem_data["difficulty"]})')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error: {problem_data["title"]} - {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully added {created_count} problems!'))
        self.stdout.write(self.style.SUCCESS('Database ready to use!'))
