from django.core.management.base import BaseCommand
from main.models import Problem, Category, TestCase, Example

PROBLEMS_DATA = [
    # EASY MASALALAR (14 ta) - Oddiy masalalar
    {
        'title': 'Ikkita Raqamni Qo\'shish',
        'description': 'Ikkita raqamni qabul qilib, ularning yig\'indisini qaytaring.',
        'difficulty': 'Easy',
        'categories': ['Math'],
        'examples': [
            {'input': 'a = 5, b = 3', 'output': '8'},
            {'input': 'a = -1, b = 1', 'output': '0'},
        ],
        'test_cases': [
            ('5\n3', '8', False),
            ('10\n20', '30', False),
            ('-5\n5', '0', False),
            ('0\n0', '0', True),
            ('100\n50', '150', True),
            ('7\n8', '15', True),
            ('-10\n-5', '-15', True),
        ]
    },
    {
        'title': 'Ikkita Raqamni Ayirish',
        'description': 'Birinchi raqamdan ikkinchi raqamni ayiring.',
        'difficulty': 'Easy',
        'categories': ['Math'],
        'examples': [
            {'input': 'a = 10, b = 3', 'output': '7'},
            {'input': 'a = 5, b = 5', 'output': '0'},
        ],
        'test_cases': [
            ('10\n3', '7', False),
            ('20\n5', '15', False),
            ('0\n0', '0', False),
            ('50\n30', '20', True),
            ('5\n10', '-5', True),
            ('100\n1', '99', True),
            ('-5\n3', '-8', True),
        ]
    },
    {
        'title': 'Raqamni Ikki Barobar Qilish',
        'description': 'Berilgan raqamni 2 ga ko\'paytiring.',
        'difficulty': 'Easy',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = 5', 'output': '10'},
            {'input': 'n = 0', 'output': '0'},
        ],
        'test_cases': [
            ('5', '10', False),
            ('10', '20', False),
            ('0', '0', False),
            ('7', '14', True),
            ('-3', '-6', True),
            ('100', '200', True),
            ('1', '2', True),
        ]
    },
    {
        'title': 'Massiv Yig\'indisi',
        'description': 'Berilgan massivdagi barcha sonlarning yig\'indisini hisoblang.',
        'difficulty': 'Easy',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '15'},
            {'input': 'nums = [10, 20, 30]', 'output': '60'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '15', False),
            ('[10, 20, 30]', '60', False),
            ('[0]', '0', False),
            ('[1]', '1', True),
            ('[-1, -2, -3]', '-6', True),
            ('[100, 200, 300]', '600', True),
            ('[]', '0', True),
        ]
    },
    {
        'title': 'Eng Katta Element',
        'description': 'Massivdagi eng katta sonni toping.',
        'difficulty': 'Easy',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [3, 7, 2, 9, 1]', 'output': '9'},
            {'input': 'nums = [1]', 'output': '1'},
        ],
        'test_cases': [
            ('[3, 7, 2, 9, 1]', '9', False),
            ('[1]', '1', False),
            ('[5, 5, 5, 5]', '5', False),
            ('[1, 2, 3, 4, 5]', '5', True),
            ('[-5, -1, -10]', '-1', True),
            ('[100, 50, 75]', '100', True),
            ('[0, 0, 0]', '0', True),
        ]
    },
    {
        'title': 'Eng Kichik Element',
        'description': 'Massivdagi eng kichik sonni toping.',
        'difficulty': 'Easy',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [3, 7, 2, 9, 1]', 'output': '1'},
            {'input': 'nums = [5, 4, 3, 2, 1]', 'output': '1'},
        ],
        'test_cases': [
            ('[3, 7, 2, 9, 1]', '1', False),
            ('[5, 4, 3, 2, 1]', '1', False),
            ('[10]', '10', False),
            ('[5, 5, 5]', '5', True),
            ('[-1, -5, -3]', '-5', True),
            ('[100, 50, 75]', '50', True),
            ('[0, 0, 1]', '0', True),
        ]
    },
    {
        'title': 'Satr Uzunligi',
        'description': 'Berilgan satrning uzunligini qaytaring.',
        'difficulty': 'Easy',
        'categories': ['String'],
        'examples': [
            {'input': 's = "hello"', 'output': '5'},
            {'input': 's = "a b c"', 'output': '5'},
        ],
        'test_cases': [
            ('"hello"', '5', False),
            ('"a b c"', '5', False),
            ('""', '0', False),
            ('"a"', '1', True),
            ('"hello world"', '11', True),
            ('"12345"', '5', True),
            ('"   "', '3', True),
        ]
    },
    {
        'title': 'Raqam Juft yoki Toq',
        'description': 'Berilgan raqam juft yoki toq ekanligini aniqlang. Juft bo\'lsa "Juft", toq bo\'lsa "Toq" qaytaring.',
        'difficulty': 'Easy',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = 4', 'output': '"Juft"'},
            {'input': 'n = 7', 'output': '"Toq"'},
        ],
        'test_cases': [
            ('4', '"Juft"', False),
            ('7', '"Toq"', False),
            ('0', '"Juft"', False),
            ('1', '"Toq"', True),
            ('100', '"Juft"', True),
            ('999', '"Toq"', True),
            ('2', '"Juft"', True),
        ]
    },
    {
        'title': 'Satrni Bosh Harfga O\'girish',
        'description': 'Satrning birinchi harfini bosh harfga o\'giring.',
        'difficulty': 'Easy',
        'categories': ['String'],
        'examples': [
            {'input': 's = "hello"', 'output': '"Hello"'},
            {'input': 's = "WORLD"', 'output': '"World"'},
        ],
        'test_cases': [
            ('"hello"', '"Hello"', False),
            ('"WORLD"', '"World"', False),
            ('"a"', '"A"', False),
            ('"abc"', '"Abc"', True),
            ('"123abc"', '"123abc"', True),
            ('"HeLLo"', '"HeLLo"', True),
            ('"hELLO"', '"HeLLO"', True),
        ]
    },
    {
        'title': 'Massiv Uzunligi',
        'description': 'Massivning uzunligini (elementlar sonini) qaytaring.',
        'difficulty': 'Easy',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '5'},
            {'input': 'nums = []', 'output': '0'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '5', False),
            ('[]', '0', False),
            ('[1]', '1', False),
            ('[1, 2, 3]', '3', True),
            ('[10, 20, 30, 40]', '4', True),
            ('[0, 0, 0, 0, 0]', '5', True),
            ('[1, 1, 1, 1, 1, 1, 1]', '7', True),
        ]
    },
    {
        'title': 'Massivni Teskari Qilish',
        'description': 'Berilgan massivni teskari tartibda qaytaring.',
        'difficulty': 'Easy',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '[5, 4, 3, 2, 1]'},
            {'input': 'nums = [1]', 'output': '[1]'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '[5, 4, 3, 2, 1]', False),
            ('[1]', '[1]', False),
            ('[]', '[]', False),
            ('[1, 2, 3]', '[3, 2, 1]', True),
            ('[5, 5, 5]', '[5, 5, 5]', True),
            ('[1, 2]', '[2, 1]', True),
            ('[10, 20, 30, 40]', '[40, 30, 20, 10]', True),
        ]
    },
    {
        'title': 'Nol Bilan Tugashini Tekshiring',
        'description': 'Raqamning oxirgi raqami nol bilan tugashini tekshiring.',
        'difficulty': 'Easy',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = 120', 'output': 'true'},
            {'input': 'n = 123', 'output': 'false'},
        ],
        'test_cases': [
            ('120', 'true', False),
            ('123', 'false', False),
            ('0', 'true', False),
            ('10', 'true', True),
            ('100', 'true', True),
            ('999', 'false', True),
            ('50', 'true', True),
        ]
    },
    {
        'title': 'Raqamning Mutloq Qiymati',
        'description': 'Berilgan raqamning mutloq qiymatini (absolute value) qaytaring.',
        'difficulty': 'Easy',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = -5', 'output': '5'},
            {'input': 'n = 10', 'output': '10'},
        ],
        'test_cases': [
            ('-5', '5', False),
            ('10', '10', False),
            ('0', '0', False),
            ('-100', '100', True),
            ('1', '1', True),
            ('-1', '1', True),
            ('-999', '999', True),
        ]
    },
    {
        'title': 'Palindrom Tekshirish',
        'description': 'Berilgan satr palindrom ekanligini tekshiring. Palindrom - teskari o\'qiganda ham o\'zi bo\'lgan so\'z.',
        'difficulty': 'Easy',
        'categories': ['String'],
        'examples': [
            {'input': 's = "racecar"', 'output': 'true'},
            {'input': 's = "hello"', 'output': 'false'},
        ],
        'test_cases': [
            ('"racecar"', 'true', False),
            ('"hello"', 'false', False),
            ('"a"', 'true', False),
            ('"ab"', 'false', True),
            ('"aba"', 'true', True),
            ('"abba"', 'true', True),
            ('"madam"', 'true', True),
        ]
    },

    # MEDIUM MASALALAR (3 ta)
    {
        'title': 'Ikkita Sonning Yig\'indisining Soni',
        'description': 'Massivda berilgan target songa teng yig\'indining necha xil juftlik bor, uni hisoblang.',
        'difficulty': 'Medium',
        'categories': ['Array', 'HashTable'],
        'examples': [
            {'input': 'nums = [1, 5, 7, -1, 5], target = 5', 'output': '2'},
            {'input': 'nums = [1, 1, 1, 1], target = 2', 'output': '6'},
        ],
        'test_cases': [
            ('[1, 5, 7, -1, 5]\n5', '2', False),
            ('[1, 1, 1, 1]\n2', '6', False),
            ('[0, 0]\n0', '1', False),
            ('[1, 2, 3]\n5', '2', True),
            ('[1]\n1', '0', True),
            ('[1, 1, 1, 1, 1]\n2', '10', True),
            ('[2, 3, 4]\n6', '1', True),
        ]
    },
    {
        'title': 'Massivning O\'rtacha Qiymati',
        'description': 'Massivning o\'rtacha (average) qiymatini hisoblang.',
        'difficulty': 'Medium',
        'categories': ['Array', 'Math'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '3.0'},
            {'input': 'nums = [10, 20, 30]', 'output': '20.0'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '3.0', False),
            ('[10, 20, 30]', '20.0', False),
            ('[5]', '5.0', False),
            ('[0]', '0.0', True),
            ('[1, 1, 1, 1]', '1.0', True),
            ('[2, 4, 6, 8]', '5.0', True),
            ('[1, 2, 3]', '2.0', True),
        ]
    },
    {
        'title': 'Satrlar Orasida Umumiy Harflarni Topish',
        'description': 'Ikkita satrda umumiy bo\'lgan barcha harflarni toping va natijaviy satrni qaytaring.',
        'difficulty': 'Medium',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 's1 = "hello", s2 = "world"', 'output': '"lo"'},
            {'input': 's1 = "abc", s2 = "def"', 'output': '""'},
        ],
        'test_cases': [
            ('"hello"\n"world"', '"lo"', False),
            ('"abc"\n"def"', '""', False),
            ('"a"\n"a"', '"a"', False),
            ('"aab"\n"ab"', '"a"', True),
            ('"ab"\n"ba"', '"ab"', True),
            ('"abc"\n"cba"', '"abc"', True),
            ('"xyz"\n"abc"', '""', True),
        ]
    },

    # HARD MASALALAR (3 ta)
    {
        'title': 'Eng Katta Subarray Yig\'indisi',
        'description': 'Massivning ketma-ket qismi (subarray) ning eng katta yig\'indisini toping.',
        'difficulty': 'Hard',
        'categories': ['Array', 'DynamicProgramming'],
        'examples': [
            {'input': 'nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]', 'output': '6'},
            {'input': 'nums = [1]', 'output': '1'},
        ],
        'test_cases': [
            ('[-2, 1, -3, 4, -1, 2, 1, -5, 4]', '6', False),
            ('[1]', '1', False),
            ('[-1]', '-1', False),
            ('[5, -3, 5]', '7', True),
            ('[-2, -1, -3, -4]', '-1', True),
            ('[2, -1, 2, -1, 4, -5]', '6', True),
            ('[1, 2, 3, 4, 5]', '15', True),
        ]
    },
    {
        'title': 'Yo\'g\'un Suv',
        'description': 'Balandlik massivida eng ko\'p suvni qamashuvchi kontejner topilsin. Suvning hajmi qaytaring.',
        'difficulty': 'Hard',
        'categories': ['Array', 'TwoPointers'],
        'examples': [
            {'input': 'height = [1,8,6,2,5,4,8,3,7]', 'output': '49'},
            {'input': 'height = [1,1]', 'output': '1'},
        ],
        'test_cases': [
            ('[1,8,6,2,5,4,8,3,7]', '49', False),
            ('[1,1]', '1', False),
            ('[2,3,4,5,18,17,6]', '17', False),
            ('[4,3,2,1,4]', '16', True),
            ('[1,2,1]', '2', True),
            ('[3,9,3,4,7,2,12,6]', '45', True),
            ('[2,3,10,5,7,8,9]', '36', True),
        ]
    },
    {
        'title': 'Massivda Maksimal Profit',
        'description': 'Massiv narxlardan eng katta foydani topish uchun bir marta sotib, bir marta sotish orqali maksimal profit hisoblang.',
        'difficulty': 'Hard',
        'categories': ['Array', 'DynamicProgramming'],
        'examples': [
            {'input': 'prices = [3, 2, 6, 5, 0, 3]', 'output': '4'},
            {'input': 'prices = [7, 6, 4, 3, 1]', 'output': '0'},
        ],
        'test_cases': [
            ('[3, 2, 6, 5, 0, 3]', '4', False),
            ('[7, 6, 4, 3, 1]', '0', False),
            ('[2, 4, 1]', '2', False),
            ('[1, 2, 3, 4, 5]', '4', True),
            ('[5, 4, 3, 2, 1]', '0', True),
            ('[1, 5, 2, 3, 4]', '4', True),
            ('[3, 3, 5, 0, 0, 3, 1, 4]', '4', True),
        ]
    },
]

class Command(BaseCommand):
    help = 'Load 20 problems (14 Easy + 3 Medium + 3 Hard) with 7 test cases each (3 visible, 4 hidden)'

    def handle(self, *args, **options):
        # Get existing categories, create if not exist
        categories_map = {}
        for cat_name in ['Array', 'String', 'Math', 'HashTable', 'DynamicProgramming', 'TwoPointers']:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories_map[cat_name] = cat

        self.stdout.write('📚 20 ta masala qo\'shilyapti...\n')

        for i, problem_data in enumerate(PROBLEMS_DATA, 1):
            problem = Problem.objects.create(
                title=problem_data['title'],
                description=problem_data['description'],
                difficulty=problem_data['difficulty'],
                function_name='Solution().solve',
                input_example=problem_data['examples'][0]['input'],
                output_example=problem_data['examples'][0]['output'],
            )

            # Add categories
            cat_names = ', '.join(problem_data['categories'])
            for cat_name in problem_data['categories']:
                if cat_name in categories_map:
                    problem.categories.add(categories_map[cat_name])

            # Add examples
            for example in problem_data['examples']:
                Example.objects.create(
                    problem=problem,
                    ex_input=example['input'],
                    ex_output=example['output']
                )

            # Add test cases (3 visible + 4+ hidden)
            for j, (inp, out, is_visible) in enumerate(problem_data['test_cases'], 1):
                TestCase.objects.create(
                    problem=problem,
                    input_data=inp,
                    expected_output=out,
                    order=j,
                    is_hidden=not is_visible
                )

            difficulty_emoji = '🟢' if problem_data['difficulty'] == 'Easy' else '🟡' if problem_data['difficulty'] == 'Medium' else '🔴'
            self.stdout.write(f'{difficulty_emoji} {i}. {problem.title} ({problem_data["difficulty"]}) [{cat_names}]')

        self.stdout.write('\n✅ HAMMASINI TAYYORLANDI!')
        self.stdout.write('✅ Jami: 20 ta masala')
        self.stdout.write('✅ 14 ta Easy (oddiy)')
        self.stdout.write('✅ 3 ta Medium')
        self.stdout.write('✅ 3 ta Hard')
        self.stdout.write('✅ Har biri uchun 7 ta test case (3 visible, 4 hidden)')
        self.stdout.write('✅ Barcha tavsiflar UZBEK tilida')
        self.stdout.write('✅ Kategoriyalar ENGLISH tilida')
        self.stdout.write('🎉 Database tayyor!')
