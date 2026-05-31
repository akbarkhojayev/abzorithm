from django.core.management.base import BaseCommand
from main.models import Problem, TestCase

basic_math_problems = [
    {
        'title': 'Sum of Two Numbers',
        'description': 'Given two integers a and b, return their sum.\n\nExample 1:\nInput: a = 5, b = 3\nOutput: 8\n\nExample 2:\nInput: a = -1, b = 1\nOutput: 0',
        'difficulty': 'Easy',
        'function_name': 'Solution().addNumbers',
        'test_cases': [
            {'input': '5\n3', 'output': '8'},
            {'input': '-1\n1', 'output': '0'},
            {'input': '10\n20', 'output': '30'},
            {'input': '-5\n-3', 'output': '-8'},
            {'input': '0\n0', 'output': '0'},
            {'input': '100\n-50', 'output': '50'}
        ]
    },
    {
        'title': 'Difference of Two Numbers',
        'description': 'Given two integers a and b, return their difference (a - b).\n\nExample 1:\nInput: a = 10, b = 3\nOutput: 7\n\nExample 2:\nInput: a = 5, b = 8\nOutput: -3',
        'difficulty': 'Easy',
        'function_name': 'Solution().subtractNumbers',
        'test_cases': [
            {'input': '10\n3', 'output': '7'},
            {'input': '5\n8', 'output': '-3'},
            {'input': '0\n5', 'output': '-5'},
            {'input': '-10\n-5', 'output': '-5'},
            {'input': '15\n15', 'output': '0'},
            {'input': '-3\n-8', 'output': '5'}
        ]
    },
    {
        'title': 'Product of Two Numbers',
        'description': 'Given two integers a and b, return their product (a * b).\n\nExample 1:\nInput: a = 4, b = 5\nOutput: 20\n\nExample 2:\nInput: a = -3, b = 7\nOutput: -21',
        'difficulty': 'Easy',
        'function_name': 'Solution().multiplyNumbers',
        'test_cases': [
            {'input': '4\n5', 'output': '20'},
            {'input': '-3\n7', 'output': '-21'},
            {'input': '0\n100', 'output': '0'},
            {'input': '-2\n-3', 'output': '6'},
            {'input': '1\n1', 'output': '1'},
            {'input': '10\n-10', 'output': '-100'}
        ]
    },
    {
        'title': 'Division of Two Numbers',
        'description': 'Given two integers a and b, return the quotient of a divided by b (a / b). Truncate the result towards zero.\n\nExample 1:\nInput: a = 10, b = 3\nOutput: 3\n\nExample 2:\nInput: a = -7, b = 3\nOutput: -2',
        'difficulty': 'Easy',
        'function_name': 'Solution().divideNumbers',
        'test_cases': [
            {'input': '10\n3', 'output': '3'},
            {'input': '-7\n3', 'output': '-2'},
            {'input': '20\n5', 'output': '4'},
            {'input': '-10\n-3', 'output': '3'},
            {'input': '1\n1', 'output': '1'},
            {'input': '0\n5', 'output': '0'}
        ]
    },
    {
        'title': 'Remainder of Two Numbers',
        'description': 'Given two integers a and b, return the remainder when a is divided by b (a % b).\n\nExample 1:\nInput: a = 10, b = 3\nOutput: 1\n\nExample 2:\nInput: a = -7, b = 3\nOutput: -1',
        'difficulty': 'Easy',
        'function_name': 'Solution().remainderNumbers',
        'test_cases': [
            {'input': '10\n3', 'output': '1'},
            {'input': '-7\n3', 'output': '-1'},
            {'input': '20\n5', 'output': '0'},
            {'input': '15\n4', 'output': '3'},
            {'input': '7\n7', 'output': '0'},
            {'input': '5\n2', 'output': '1'}
        ]
    },
    {
        'title': 'Absolute Value',
        'description': 'Given an integer n, return its absolute value.\n\nExample 1:\nInput: n = -5\nOutput: 5\n\nExample 2:\nInput: n = 10\nOutput: 10',
        'difficulty': 'Easy',
        'function_name': 'Solution().absoluteValue',
        'test_cases': [
            {'input': '-5', 'output': '5'},
            {'input': '10', 'output': '10'},
            {'input': '0', 'output': '0'},
            {'input': '-100', 'output': '100'},
            {'input': '1', 'output': '1'},
            {'input': '-1', 'output': '1'}
        ]
    },
    {
        'title': 'Maximum of Two Numbers',
        'description': 'Given two integers a and b, return the maximum of the two.\n\nExample 1:\nInput: a = 5, b = 3\nOutput: 5\n\nExample 2:\nInput: a = -10, b = -20\nOutput: -10',
        'difficulty': 'Easy',
        'function_name': 'Solution().maxOfTwo',
        'test_cases': [
            {'input': '5\n3', 'output': '5'},
            {'input': '-10\n-20', 'output': '-10'},
            {'input': '0\n0', 'output': '0'},
            {'input': '100\n50', 'output': '100'},
            {'input': '-5\n5', 'output': '5'},
            {'input': '1\n1', 'output': '1'}
        ]
    },
    {
        'title': 'Minimum of Two Numbers',
        'description': 'Given two integers a and b, return the minimum of the two.\n\nExample 1:\nInput: a = 5, b = 3\nOutput: 3\n\nExample 2:\nInput: a = -10, b = -20\nOutput: -20',
        'difficulty': 'Easy',
        'function_name': 'Solution().minOfTwo',
        'test_cases': [
            {'input': '5\n3', 'output': '3'},
            {'input': '-10\n-20', 'output': '-20'},
            {'input': '0\n0', 'output': '0'},
            {'input': '100\n50', 'output': '50'},
            {'input': '-5\n5', 'output': '-5'},
            {'input': '1\n1', 'output': '1'}
        ]
    },
    {
        'title': 'Average of Two Numbers',
        'description': 'Given two integers a and b, return their average (rounded down).\n\nExample 1:\nInput: a = 5, b = 3\nOutput: 4\n\nExample 2:\nInput: a = 10, b = 20\nOutput: 15',
        'difficulty': 'Easy',
        'function_name': 'Solution().averageOfTwo',
        'test_cases': [
            {'input': '5\n3', 'output': '4'},
            {'input': '10\n20', 'output': '15'},
            {'input': '1\n2', 'output': '1'},
            {'input': '0\n0', 'output': '0'},
            {'input': '-5\n5', 'output': '0'},
            {'input': '7\n8', 'output': '7'}
        ]
    },
    {
        'title': 'Sum of Three Numbers',
        'description': 'Given three integers a, b, and c, return their sum.\n\nExample 1:\nInput: a = 1, b = 2, c = 3\nOutput: 6\n\nExample 2:\nInput: a = -1, b = 0, c = 1\nOutput: 0',
        'difficulty': 'Easy',
        'function_name': 'Solution().sumOfThree',
        'test_cases': [
            {'input': '1\n2\n3', 'output': '6'},
            {'input': '-1\n0\n1', 'output': '0'},
            {'input': '10\n20\n30', 'output': '60'},
            {'input': '-5\n-5\n-5', 'output': '-15'},
            {'input': '0\n0\n0', 'output': '0'},
            {'input': '100\n-50\n25', 'output': '75'}
        ]
    },
    {
        'title': 'Square of a Number',
        'description': 'Given an integer n, return its square (n * n).\n\nExample 1:\nInput: n = 5\nOutput: 25\n\nExample 2:\nInput: n = -3\nOutput: 9',
        'difficulty': 'Easy',
        'function_name': 'Solution().squareOfNumber',
        'test_cases': [
            {'input': '5', 'output': '25'},
            {'input': '-3', 'output': '9'},
            {'input': '0', 'output': '0'},
            {'input': '10', 'output': '100'},
            {'input': '-1', 'output': '1'},
            {'input': '7', 'output': '49'}
        ]
    },
    {
        'title': 'Cube of a Number',
        'description': 'Given an integer n, return its cube (n * n * n).\n\nExample 1:\nInput: n = 3\nOutput: 27\n\nExample 2:\nInput: n = -2\nOutput: -8',
        'difficulty': 'Easy',
        'function_name': 'Solution().cubeOfNumber',
        'test_cases': [
            {'input': '3', 'output': '27'},
            {'input': '-2', 'output': '-8'},
            {'input': '0', 'output': '0'},
            {'input': '5', 'output': '125'},
            {'input': '-1', 'output': '-1'},
            {'input': '2', 'output': '8'}
        ]
    },
    {
        'title': 'Check if Number is Even',
        'description': 'Given an integer n, return true if n is even, false otherwise.\n\nExample 1:\nInput: n = 4\nOutput: true\n\nExample 2:\nInput: n = 7\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().isEven',
        'test_cases': [
            {'input': '4', 'output': 'true'},
            {'input': '7', 'output': 'false'},
            {'input': '0', 'output': 'true'},
            {'input': '-2', 'output': 'true'},
            {'input': '-3', 'output': 'false'},
            {'input': '100', 'output': 'true'}
        ]
    },
    {
        'title': 'Check if Number is Odd',
        'description': 'Given an integer n, return true if n is odd, false otherwise.\n\nExample 1:\nInput: n = 3\nOutput: true\n\nExample 2:\nInput: n = 4\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().isOdd',
        'test_cases': [
            {'input': '3', 'output': 'true'},
            {'input': '4', 'output': 'false'},
            {'input': '0', 'output': 'false'},
            {'input': '-1', 'output': 'true'},
            {'input': '-2', 'output': 'false'},
            {'input': '99', 'output': 'true'}
        ]
    },
    {
        'title': 'Check if Number is Positive',
        'description': 'Given an integer n, return true if n is positive (greater than 0), false otherwise.\n\nExample 1:\nInput: n = 5\nOutput: true\n\nExample 2:\nInput: n = -3\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().isPositive',
        'test_cases': [
            {'input': '5', 'output': 'true'},
            {'input': '-3', 'output': 'false'},
            {'input': '0', 'output': 'false'},
            {'input': '1', 'output': 'true'},
            {'input': '-1', 'output': 'false'},
            {'input': '100', 'output': 'true'}
        ]
    },
    {
        'title': 'Check if Number is Negative',
        'description': 'Given an integer n, return true if n is negative (less than 0), false otherwise.\n\nExample 1:\nInput: n = -5\nOutput: true\n\nExample 2:\nInput: n = 3\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().isNegative',
        'test_cases': [
            {'input': '-5', 'output': 'true'},
            {'input': '3', 'output': 'false'},
            {'input': '0', 'output': 'false'},
            {'input': '-1', 'output': 'true'},
            {'input': '1', 'output': 'false'},
            {'input': '-100', 'output': 'true'}
        ]
    },
    {
        'title': 'Check if Number is Zero',
        'description': 'Given an integer n, return true if n is zero, false otherwise.\n\nExample 1:\nInput: n = 0\nOutput: true\n\nExample 2:\nInput: n = 5\nOutput: false',
        'difficulty': 'Easy',
        'function_name': 'Solution().isZero',
        'test_cases': [
            {'input': '0', 'output': 'true'},
            {'input': '5', 'output': 'false'},
            {'input': '-1', 'output': 'false'},
            {'input': '1', 'output': 'false'},
            {'input': '-0', 'output': 'true'},
            {'input': '100', 'output': 'false'}
        ]
    }
]

class Command(BaseCommand):
    help = 'Loads basic math problems (addition, subtraction, multiplication, etc.)'

    def handle(self, *args, **options):
        for problem_data in basic_math_problems:
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
        
        self.stdout.write(self.style.SUCCESS('Successfully loaded all basic math problems!'))
