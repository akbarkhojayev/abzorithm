from django.core.management.base import BaseCommand
from main.models import Problem, Category, TestCase, Example

PROBLEMS_DATA = [
    # EASY MASALALAR (14 ta)

    # 1. Massiv Yig'indisi
    {
        'title': 'Massiv Yig\'indisi',
        'description': 'Berilgan massivdagi barcha sonlarning yig\'indisini hisoblang.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 3, 4, 5]',
        'output_example': '15',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '15'},
            {'input': 'nums = [10, 20, 30]', 'output': '60'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '15'),
            ('[10, 20, 30]', '60'),
            ('[0]', '0'),
            ('[1]', '1'),
            ('[-1, -2, -3]', '-6'),
            ('[100, 200, 300]', '600'),
            ('[]', '0'),
        ]
    },

    # 2. Eng Katta Element
    {
        'title': 'Eng Katta Element',
        'description': 'Massivdagi eng katta sonni toping.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3, 7, 2, 9, 1]',
        'output_example': '9',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [3, 7, 2, 9, 1]', 'output': '9'},
            {'input': 'nums = [1]', 'output': '1'},
        ],
        'test_cases': [
            ('[3, 7, 2, 9, 1]', '9'),
            ('[1]', '1'),
            ('[5, 5, 5, 5]', '5'),
            ('[1, 2, 3, 4, 5]', '5'),
            ('[-5, -1, -10]', '-1'),
            ('[100, 50, 75]', '100'),
            ('[0, 0, 0]', '0'),
        ]
    },

    # 3. Eng Kichik Element
    {
        'title': 'Eng Kichik Element',
        'description': 'Massivdagi eng kichik sonni toping.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3, 7, 2, 9, 1]',
        'output_example': '1',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [3, 7, 2, 9, 1]', 'output': '1'},
            {'input': 'nums = [5, 4, 3, 2, 1]', 'output': '1'},
        ],
        'test_cases': [
            ('[3, 7, 2, 9, 1]', '1'),
            ('[5, 4, 3, 2, 1]', '1'),
            ('[10]', '10'),
            ('[5, 5, 5]', '5'),
            ('[-1, -5, -3]', '-5'),
            ('[100, 50, 75]', '50'),
            ('[0, 0, 1]', '0'),
        ]
    },

    # 4. Satr Uzunligi
    {
        'title': 'Satr Uzunligi',
        'description': 'Berilgan satrning uzunligini qaytaring (bo\'sh joylar ham sanaladdi).',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"hello"',
        'output_example': '5',
        'categories': ['String'],
        'examples': [
            {'input': 's = "hello"', 'output': '5'},
            {'input': 's = "a b c"', 'output': '5'},
        ],
        'test_cases': [
            ('"hello"', '5'),
            ('"a b c"', '5'),
            ('""', '0'),
            ('"a"', '1'),
            ('"hello world"', '11'),
            ('"12345"', '5'),
            ('"   "', '3'),
        ]
    },

    # 5. Raqam Juft yoki Toq
    {
        'title': 'Raqam Juft yoki Toq',
        'description': 'Berilgan raqam juft yoki toq ekanligini aniqlang. Juft bo\'lsa "Juft", toq bo\'lsa "Toq" qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '4',
        'output_example': '"Juft"',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = 4', 'output': '"Juft"'},
            {'input': 'n = 7', 'output': '"Toq"'},
        ],
        'test_cases': [
            ('4', '"Juft"'),
            ('7', '"Toq"'),
            ('0', '"Juft"'),
            ('1', '"Toq"'),
            ('100', '"Juft"'),
            ('999', '"Toq"'),
            ('2', '"Juft"'),
        ]
    },

    # 6. Ikkita Raqam Yig'indisi
    {
        'title': 'Ikkita Raqam Yig\'indisi',
        'description': 'Ikkita raqamni qabul qilib, ularning yig\'indisini qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '5\n3',
        'output_example': '8',
        'categories': ['Math'],
        'examples': [
            {'input': 'a = 5, b = 3', 'output': '8'},
            {'input': 'a = -1, b = 1', 'output': '0'},
        ],
        'test_cases': [
            ('5\n3', '8'),
            ('-1\n1', '0'),
            ('0\n0', '0'),
            ('10\n20', '30'),
            ('-5\n-3', '-8'),
            ('100\n1', '101'),
            ('7\n2', '9'),
        ]
    },

    # 7. Ikkita Raqam Ayirmasi
    {
        'title': 'Ikkita Raqam Ayirmasi',
        'description': 'Birinchi raqamdan ikkinchi raqamni ayiring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '10\n3',
        'output_example': '7',
        'categories': ['Math'],
        'examples': [
            {'input': 'a = 10, b = 3', 'output': '7'},
            {'input': 'a = 5, b = 5', 'output': '0'},
        ],
        'test_cases': [
            ('10\n3', '7'),
            ('5\n5', '0'),
            ('0\n0', '0'),
            ('20\n5', '15'),
            ('-5\n3', '-8'),
            ('1\n-1', '2'),
            ('100\n1', '99'),
        ]
    },

    # 8. Ikkita Raqam Ko'paytmasi
    {
        'title': 'Ikkita Raqam Ko\'paytmasi',
        'description': 'Ikkita raqamni ko\'paytiring va natijani qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '4\n5',
        'output_example': '20',
        'categories': ['Math'],
        'examples': [
            {'input': 'a = 4, b = 5', 'output': '20'},
            {'input': 'a = 0, b = 10', 'output': '0'},
        ],
        'test_cases': [
            ('4\n5', '20'),
            ('0\n10', '0'),
            ('1\n1', '1'),
            ('7\n8', '56'),
            ('-3\n4', '-12'),
            ('10\n10', '100'),
            ('2\n3', '6'),
        ]
    },

    # 9. Satrni Lotin Harflariga O'girish
    {
        'title': 'Satrni Bosh Harfga O\'girish',
        'description': 'Satrning birinchi harfini bosh harfga o\'giring. Agar satr bo\'sh bo\'lsa, bo\'sh satr qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"hello"',
        'output_example': '"Hello"',
        'categories': ['String'],
        'examples': [
            {'input': 's = "hello"', 'output': '"Hello"'},
            {'input': 's = "WORLD"', 'output': '"World"'},
        ],
        'test_cases': [
            ('"hello"', '"Hello"'),
            ('"WORLD"', '"World"'),
            ('"a"', '"A"'),
            ('"abc"', '"Abc"'),
            ('"123abc"', '"123abc"'),
            ('"HeLLo"', '"HeLLo"'),
            ('"hELLO"', '"HeLLO"'),
        ]
    },

    # 10. Massivdagi Elementlar Soni
    {
        'title': 'Massivdagi Elementlar Soni',
        'description': 'Massivning uzunligini (elementlar sonini) qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 3, 4, 5]',
        'output_example': '5',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '5'},
            {'input': 'nums = []', 'output': '0'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '5'),
            ('[]', '0'),
            ('[1]', '1'),
            ('[1, 2, 3]', '3'),
            ('[10, 20, 30, 40]', '4'),
            ('[0, 0, 0, 0, 0]', '5'),
            ('[1, 1, 1, 1, 1, 1, 1]', '7'),
        ]
    },

    # 11. Raqamni Ikki Barobar Qilish
    {
        'title': 'Raqamni Ikki Barobar Qilish',
        'description': 'Berilgan raqamni 2 ga ko\'paytiring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '5',
        'output_example': '10',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = 5', 'output': '10'},
            {'input': 'n = 0', 'output': '0'},
        ],
        'test_cases': [
            ('5', '10'),
            ('0', '0'),
            ('1', '2'),
            ('10', '20'),
            ('-3', '-6'),
            ('100', '200'),
            ('7', '14'),
        ]
    },

    # 12. Massivni Teskarisiga O'girish
    {
        'title': 'Massivni Teskarisiga O\'girish',
        'description': 'Berilgan massivni teskari tartibda qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 3, 4, 5]',
        'output_example': '[5, 4, 3, 2, 1]',
        'categories': ['Array'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '[5, 4, 3, 2, 1]'},
            {'input': 'nums = [1]', 'output': '[1]'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '[5, 4, 3, 2, 1]'),
            ('[1]', '[1]'),
            ('[]', '[]'),
            ('[1, 2, 3]', '[3, 2, 1]'),
            ('[5, 5, 5]', '[5, 5, 5]'),
            ('[1, 2]', '[2, 1]'),
            ('[10, 20, 30, 40]', '[40, 30, 20, 10]'),
        ]
    },

    # 13. Nol Bilan Tugashini Tekshiring
    {
        'title': 'Nol Bilan Tugashini Tekshiring',
        'description': 'Raqamning oxirgi raqami nol bilan tugashini tekshiring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '120',
        'output_example': 'true',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = 120', 'output': 'true'},
            {'input': 'n = 123', 'output': 'false'},
        ],
        'test_cases': [
            ('120', 'true'),
            ('123', 'false'),
            ('0', 'true'),
            ('10', 'true'),
            ('100', 'true'),
            ('999', 'false'),
            ('50', 'true'),
        ]
    },

    # 14. Raqamning Mutloq Qiymati
    {
        'title': 'Raqamning Mutloq Qiymati',
        'description': 'Berilgan raqamning mutloq qiymatini (absolute value) qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '-5',
        'output_example': '5',
        'categories': ['Math'],
        'examples': [
            {'input': 'n = -5', 'output': '5'},
            {'input': 'n = 10', 'output': '10'},
        ],
        'test_cases': [
            ('-5', '5'),
            ('10', '10'),
            ('0', '0'),
            ('-100', '100'),
            ('1', '1'),
            ('-1', '1'),
            ('-999', '999'),
        ]
    },

    # MEDIUM MASALALAR (3 ta)

    # 15. Berilgan Target Yig'indining Soni
    {
        'title': 'Berilgan Target Yig\'indining Soni',
        'description': 'Massivda target songa teng yig\'indining necha xil juftlik bor, uni hisoblang.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[1, 5, 7, -1, 5]\n5',
        'output_example': '2',
        'categories': ['Array', 'HashTable'],
        'examples': [
            {'input': 'nums = [1, 5, 7, -1, 5], target = 5', 'output': '2'},
            {'input': 'nums = [1, 1, 1, 1], target = 2', 'output': '6'},
        ],
        'test_cases': [
            ('[1, 5, 7, -1, 5]\n5', '2'),
            ('[1, 1, 1, 1]\n2', '6'),
            ('[0, 0]\n0', '1'),
            ('[1, 2, 3]\n5', '2'),
            ('[1]\n1', '0'),
            ('[1, 1, 1, 1, 1]\n2', '10'),
            ('[2, 3, 4]\n6', '1'),
        ]
    },

    # 16. 3 ta Sonning Yig'indisi
    {
        'title': '3 ta Sonning Yig\'indisi Nolga Teng',
        'description': 'Massivda 3 ta sonni topingki, ularning yig\'indisi 0 ga teng bo\'lsin. Takroriy bo\'lmagan juftliklarni qaytaring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[-1, 0, 1, 2, -1, -4]',
        'output_example': '[[-1, -1, 2], [-1, 0, 1]]',
        'categories': ['Array', 'HashTable'],
        'examples': [
            {'input': 'nums = [-1, 0, 1, 2, -1, -4]', 'output': '[[-1, -1, 2], [-1, 0, 1]]'},
            {'input': 'nums = [0, 0, 0, 0]', 'output': '[[0, 0, 0]]'},
        ],
        'test_cases': [
            ('[-1, 0, 1, 2, -1, -4]', '[[-1, -1, 2], [-1, 0, 1]]'),
            ('[0, 0, 0, 0]', '[[0, 0, 0]]'),
            ('[-2, 0, 1, 1, 2]', '[[-2, 0, 2], [-2, 1, 1]]'),
            ('[-1, -1, -1, 0, 1, 2]', '[[-1, -1, 2], [-1, 0, 1]]'),
            ('[0]', '[]'),
            ('[-1, 0, 1]', '[[-1, 0, 1]]'),
            ('[1, -2, -1, 0, 2]', '[[-2, 0, 2], [-1, 0, 1]]'),
        ]
    },

    # 17. Massivda Takroriy Qismiy Massiv Topish
    {
        'title': 'Massivning O\'rtacha Qiymati',
        'description': 'Massivning o\'rtacha (average) qiymatini hisoblang. Agar massiv bo\'sh bo\'lsa, 0 qaytaring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 3, 4, 5]',
        'output_example': '3.0',
        'categories': ['Array', 'Math'],
        'examples': [
            {'input': 'nums = [1, 2, 3, 4, 5]', 'output': '3.0'},
            {'input': 'nums = [10, 20, 30]', 'output': '20.0'},
        ],
        'test_cases': [
            ('[1, 2, 3, 4, 5]', '3.0'),
            ('[10, 20, 30]', '20.0'),
            ('[5]', '5.0'),
            ('[0]', '0.0'),
            ('[1, 1, 1, 1]', '1.0'),
            ('[2, 4, 6, 8]', '5.0'),
            ('[1, 2, 3]', '2.0'),
        ]
    },

    # HARD MASALALAR (3 ta)

    # 18. Massivda Eng Katta Kvadrat
    {
        'title': 'Massivda Eng Katta Qo\'shni Yig\'indisining Farqi',
        'description': 'Massivda eng katta qo\'shni (ketma-ket) ikkita elementning yig\'indisining farqini toping.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[1, 3, -1, -3, 5, 3, 4, -2]',
        'output_example': '8',
        'categories': ['Array', 'DynamicProgramming'],
        'examples': [
            {'input': 'nums = [1, 3, -1, -3, 5, 3, 4, -2]', 'output': '8'},
            {'input': 'nums = [1, 2, 3, 4]', 'output': '3'},
        ],
        'test_cases': [
            ('[1, 3, -1, -3, 5, 3, 4, -2]', '8'),
            ('[1, 2, 3, 4]', '3'),
            ('[1, 1, 1, 1]', '0'),
            ('[5, -3, 4, -1, 2]', '6'),
            ('[1, -1, 1, -1]', '2'),
            ('[-5, -2, -3, -1]', '4'),
            ('[10, 5, 8, 3, 2]', '7'),
        ]
    },

    # 19. Eng Katta Subarray Yig'indisi (Kadane Algoritm)
    {
        'title': 'Eng Katta Subarray Yig\'indisi',
        'description': 'Massivning ketma-ket qismi (subarray) ning eng katta yig\'indisini toping.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[-2, 1, -3, 4, -1, 2, 1, -5, 4]',
        'output_example': '6',
        'categories': ['Array', 'DynamicProgramming'],
        'examples': [
            {'input': 'nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]', 'output': '6'},
            {'input': 'nums = [1]', 'output': '1'},
        ],
        'test_cases': [
            ('[-2, 1, -3, 4, -1, 2, 1, -5, 4]', '6'),
            ('[1]', '1'),
            ('[-1]', '-1'),
            ('[5, -3, 5]', '7'),
            ('[-2, -1, -3, -4]', '-1'),
            ('[2, -1, 2, -1, 4, -5]', '6'),
            ('[1, 2, 3, 4, 5]', '15'),
        ]
    },

    # 20. Massiv Rotaciyasi
    {
        'title': 'Massivda Maksimal Profit',
        'description': 'Massiv narxlardan eng katta foydani topish uchun bir marta sotib, bir marta sotish orqali maksimal profit hisoblang.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[3, 2, 6, 5, 0, 3]',
        'output_example': '4',
        'categories': ['Array', 'DynamicProgramming'],
        'examples': [
            {'input': 'prices = [3, 2, 6, 5, 0, 3]', 'output': '4'},
            {'input': 'prices = [7, 6, 4, 3, 1]', 'output': '0'},
        ],
        'test_cases': [
            ('[3, 2, 6, 5, 0, 3]', '4'),
            ('[7, 6, 4, 3, 1]', '0'),
            ('[2, 4, 1]', '2'),
            ('[1, 2, 3, 4, 5]', '4'),
            ('[5, 4, 3, 2, 1]', '0'),
            ('[1, 5, 2, 3, 4]', '4'),
            ('[3, 3, 5, 0, 0, 3, 1, 4]', '4'),
        ]
    },
]

class Command(BaseCommand):
    help = 'Load 20 more problems (14 Easy, 3 Medium, 3 Hard)'

    def handle(self, *args, **options):
        # Get existing categories
        categories_map = {}
        for cat in Category.objects.all():
            categories_map[cat.name] = cat

        self.stdout.write('📚 20 ta yangi masala qo\'shilyapti...\n')

        # Add problems
        for i, problem_data in enumerate(PROBLEMS_DATA, 1):
            problem = Problem.objects.create(
                title=problem_data['title'],
                description=problem_data['description'],
                difficulty=problem_data['difficulty'],
                function_name=problem_data['function_name'],
                input_example=problem_data['input_example'],
                output_example=problem_data['output_example'],
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

            # Add test cases
            for j, (inp, out) in enumerate(problem_data['test_cases'], 1):
                TestCase.objects.create(
                    problem=problem,
                    input_data=inp,
                    expected_output=out,
                    order=j
                )

            difficulty_emoji = '🟢' if problem_data['difficulty'] == 'Easy' else '🟡' if problem_data['difficulty'] == 'Medium' else '🔴'
            self.stdout.write(f'{difficulty_emoji} {i}. {problem.title} ({problem_data["difficulty"]}) [{cat_names}] - {len(problem_data["test_cases"])} test case')

        self.stdout.write('\n✅ Barcha 20 ta masala qo\'shildi!')
        self.stdout.write('✅ 14 ta Easy masala')
        self.stdout.write('✅ 3 ta Medium masala')
        self.stdout.write('✅ 3 ta Hard masala')
        self.stdout.write('✅ Har biri uchun kamida 7 ta test case')
        self.stdout.write('✅ Barcha tavsiflar UZBEK tilida')
        self.stdout.write('✅ Kategoriyalar ENGLISH tilida')
        self.stdout.write('🎉 Database yangilantirildi!')
