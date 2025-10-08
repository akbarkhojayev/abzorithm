from django.core.management.base import BaseCommand
from main.models import Problem, TestCase

problems = [
    {
        'title': 'Detect Capital',
        'description': 'We define the usage of capitals in a word to be right when one of the following cases holds:\n1. All letters in this word are capitals, like "USA".\n2. All letters in this word are not capitals, like "leetcode".\n3. Only the first letter in this word is capital, like "Google".\n\nGiven a string word, return true if the usage of capitals in it is right.\n\nExample 1:\nInput: word = "USA"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().detectCapitalUse',
        'test_cases': [
            {'input': '\"USA\"', 'output': 'true'},
            {'input': '\"FlaG\"', 'output': 'false'},
            {'input': '\"Google\"', 'output': 'true'},
            {'input': '\"leetcode\"', 'output': 'true'}
        ]
    },
    {
        'title': 'Student Attendance Record I',
        'description': 'You are given a string s representing an attendance record for a student. The record only contains the following three characters:\n- \'A\': Absent.\n- \'L\': Late.\n- \'P\': Present.\n\nThe student is eligible for an attendance award if they meet both of the following criteria:\n1. The student was absent (\'A\') for fewer than 2 days total.\n2. The student was never late (\'L\') for 3 or more consecutive days.\n\nReturn true if the student is eligible for an attendance award, or false otherwise.\n\nExample 1:\nInput: s = "PPALLP"\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().checkRecord',
        'test_cases': [
            {'input': '\"PPALLP\"', 'output': 'true'},
            {'input': '\"PPALLL\"', 'output': 'false'},
            {'input': '\"AAAA\"', 'output': 'false'},
            {'input': '\"LLPLLPLPPLLPL"', 'output': 'true'}
        ]
    },
    {
        'title': 'Reverse String II',
        'description': 'Given a string s and an integer k, reverse the first k characters for every 2k characters counting from the start of the string.\n\nIf there are fewer than k characters left, reverse all of them. If there are less than 2k but greater than or equal to k characters, then reverse the first k characters and leave the other as original.\n\nExample 1:\nInput: s = "abcdefg", k = 2\nOutput: "bacdfeg"',
        'difficulty': 'Easy',
        'function_name': 'Solution().reverseStr',
        'test_cases': [
            {'input': '\"abcdefg\"\n2', 'output': '\"bacdfeg\"'},
            {'input': '\"abcd\"\n2', 'output': '\"bacd\"'},
            {'input': '\"a\"\n2', 'output': '\"a\"'},
            {'input': '\"abcdefg\"\n8', 'output': '\"gfedcba\"'}
        ]
    },
    {
        'title': 'Count Binary Substrings',
        'description': 'Given a binary string s, return the number of non-empty substrings that have the same number of 0\'s and 1\'s, and all the 0\'s and all the 1\'s in these substrings are grouped consecutively.\n\nSubstrings that occur multiple times are counted the number of times they occur.\n\nExample 1:\nInput: s = "00110011"\nOutput: 6\nExplanation: There are 6 substrings that have equal number of consecutive 1\'s and 0\'s: "0011", "01", "1100", "10", "0011", and "01".',
        'difficulty': 'Easy',
        'function_name': 'Solution().countBinarySubstrings',
        'test_cases': [
            {'input': '\"00110011\"', 'output': '6'},
            {'input': '\"10101\"', 'output': '4'},
            {'input': '\"1\"', 'output': '0'},
            {'input': '\"000111000\"', 'output': '6'}
        ]
    },
    {
        'title': 'Robot Return to Origin',
        'description': 'There is a robot starting at the position (0, 0), the origin, on a 2D plane. Given a sequence of its moves, judge if this robot ends up at (0, 0) after it completes its moves.\n\nYou are given a string moves that represents the move sequence of the robot where moves[i] represents its ith move. Valid moves are \'R\' (right), \'L\' (left), \'U\' (up), and \'D\' (down).\n\nReturn true if the robot returns to the origin after it finishes all of its moves, or false otherwise.\n\nNote: The way that the robot is "facing" is irrelevant. \'R\' will always make the robot move to the right once, \'L\' will always make it move left, etc.\n\nExample 1:\nInput: moves = "UD"\nOutput: true\nExplanation: The robot moves up once, and then down once. All moves have the same magnitude, so it ended up at the origin where it started. Therefore, we return true.',
        'difficulty': 'Easy',
        'function_name': 'Solution().judgeCircle',
        'test_cases': [
            {'input': '\"UD\"', 'output': 'true'},
            {'input': '\"LL\"', 'output': 'false'},
            {'input': '\"LDRRLRUULR\"', 'output': 'false'},
            {'input': '\"UDDU\"', 'output': 'true'}
        ]
    },
    {
        'title': 'Valid Perfect Square',
        'description': 'Given a positive integer num, write a function which returns True if num is a perfect square else False.\n\nFollow up: Do not use any built-in library function such as sqrt.\n\nExample 1:\nInput: num = 16\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().isPerfectSquare',
        'test_cases': [
            {'input': '16', 'output': 'true'},
            {'input': '14', 'output': 'false'},
            {'input': '1', 'output': 'true'},
            {'input': '2147483647', 'output': 'false'}
        ]
    },
    {
        'title': 'Sum of Two Integers',
        'description': 'Given two integers a and b, return the sum of the two integers without using the operators + and -.\n\nExample 1:\nInput: a = 1, b = 2\nOutput: 3',
        'difficulty': 'Medium',
        'function_name': 'Solution().getSum',
        'test_cases': [
            {'input': '1\n2', 'output': '3'},
            {'input': '2\n3', 'output': '5'},
            {'input': '-1\n1', 'output': '0'},
            {'input': '20\n30', 'output': '50'}
        ]
    },
    {
        'title': 'Power of Three',
        'description': 'Given an integer n, return true if it is a power of three. Otherwise, return false.\n\nAn integer n is a power of three, if there exists an integer x such that n == 3ˣ.\n\nExample 1:\nInput: n = 27\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().isPowerOfThree',
        'test_cases': [
            {'input': '27', 'output': 'true'},
            {'input': '0', 'output': 'false'},
            {'input': '9', 'output': 'true'},
            {'input': '45', 'output': 'false'}
        ]
    },
    {
        'title': 'Power of Four',
        'description': 'Given an integer n, return true if it is a power of four. Otherwise, return false.\n\nAn integer n is a power of four, if there exists an integer x such that n == 4ˣ.\n\nExample 1:\nInput: n = 16\nOutput: true',
        'difficulty': 'Easy',
        'function_name': 'Solution().isPowerOfFour',
        'test_cases': [
            {'input': '16', 'output': 'true'},
            {'input': '5', 'output': 'false'},
            {'input': '1', 'output': 'true'},
            {'input': '64', 'output': 'true'}
        ]
    },
    {
        'title': 'Add Strings',
        'description': 'Given two non-negative integers, num1 and num2 represented as string, return the sum of num1 and num2 as a string.\n\nYou must solve the problem without using any built-in library for handling large integers (such as BigInteger). You must also not convert the inputs to integers directly.\n\nExample 1:\nInput: num1 = "11", num2 = "123"\nOutput: "134"',
        'difficulty': 'Easy',
        'function_name': 'Solution().addStrings',
        'test_cases': [
            {'input': '\"11\"\n\"123\"', 'output': '\"134\"'},
            {'input': '\"456\"\n\"77\"', 'output': '\"533\"'},
            {'input': '\"0\"\n\"0\"', 'output': '\"0\"'},
            {'input': '\"999\"\n\"1\"', 'output': '\"1000\"'}
        ]
    },
    {
        'title': 'Number of Segments in a String',
        'description': 'Given a string s, return the number of segments in the string.\n\nA segment is defined to be a contiguous sequence of non-space characters.\n\nExample 1:\nInput: s = "Hello, my name is John"\nOutput: 5\nExplanation: The five segments are ["Hello,", "my", "name", "is", "John"]',
        'difficulty': 'Easy',
        'function_name': 'Solution().countSegments',
        'test_cases': [
            {'input': '\"Hello, my name is John\"', 'output': '5'},
            {'input': '\"Hello\"', 'output': '1'},
            {'input': '\"\"', 'output': '0'},
            {'input': '\"                \"', 'output': '0'}
        ]
    },
    {
        'title': 'Arranging Coins',
        'description': 'You have n coins and you want to build a staircase with these coins. The staircase consists of k rows where the iᵗʰ row has exactly i coins. The last row of the staircase may be incomplete.\n\nGiven the integer n, return the number of complete rows of the staircase you will build.\n\nExample 1:\nInput: n = 5\nOutput: 2\nExplanation: Because the 3ʳᵈ row is incomplete, we return 2.',
        'difficulty': 'Easy',
        'function_name': 'Solution().arrangeCoins',
        'test_cases': [
            {'input': '5', 'output': '2'},
            {'input': '8', 'output': '3'},
            {'input': '1', 'output': '1'},
            {'input': '0', 'output': '0'}
        ]
    },
    {
        'title': 'Binary Number with Alternating Bits',
        'description': 'Given a positive integer, check whether it has alternating bits: namely, if two adjacent bits will always have different values.\n\nExample 1:\nInput: n = 5\nOutput: true\nExplanation: The binary representation of 5 is: 101',
        'difficulty': 'Easy',
        'function_name': 'Solution().hasAlternatingBits',
        'test_cases': [
            {'input': '5', 'output': 'true'},
            {'input': '7', 'output': 'false'},
            {'input': '11', 'output': 'false'},
            {'input': '10', 'output': 'true'}
        ]
    },
    {
        'title': 'Binary Gap',
        'description': 'Given a positive integer n, find and return the longest distance between any two adjacent 1\'s in the binary representation of n. If there are no two adjacent 1\'s, return 0.\n\nTwo 1\'s are adjacent if there are only 0\'s separating them (possibly no 0\'s). The distance between two 1\'s is the absolute difference between their bit positions.\n\nExample 1:\nInput: n = 22\nOutput: 2\nExplanation: 22 in binary is "10110".',
        'difficulty': 'Easy',
        'function_name': 'Solution().binaryGap',
        'test_cases': [
            {'input': '22', 'output': '2'},
            {'input': '8', 'output': '0'},
            {'input': '5', 'output': '2'},
            {'input': '1', 'output': '0'}
        ]
    }
]

class Command(BaseCommand):
    help = 'Loads additional string and math problems into the database'

    def handle(self, *args, **options):
        for problem_data in problems:
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
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all additional problems!'))
