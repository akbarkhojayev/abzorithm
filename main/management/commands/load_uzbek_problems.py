from django.core.management.base import BaseCommand
from main.models import Problem, Category, TestCase, Example

CATEGORIES_DATA = {
    'Massiv': 'Massiv va array masalalari',
    'Matn': 'Matn va string masalalari',
    'Xesh Jadval': 'HashMap va dictionary masalalari',
    'Matematika': 'Matematik masalalari',
    'Stek': 'Stek masalalari',
    'Navbat': 'Navbat masalalari',
    'Daraxti': 'Binary tree va tree masalalari',
    'Graf': 'Graf masalalari',
    'Dinamik Dasturlash': 'Dynamic Programming masalalari',
    'Greedy': 'Greedy algorithm masalalari',
}

PROBLEMS_DATA = [
    # 1. Ikkita Sonning Yig'indisi
    {
        'title': 'Ikkita Sonning Yig\'indisi',
        'description': 'Butun sonlardan tuzilgan massiv va target son berilgan. Massivdan shunday ikkita sonni toping, ularning yig\'indisi target songa teng bo\'lsin. Javobda ularning indekslarini qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[2, 7, 11, 15]\n9',
        'output_example': '[0, 1]',
        'categories': ['Massiv', 'Xesh Jadval'],
        'examples': [
            {'input': 'massiv = [2, 7, 11, 15], target = 9', 'output': '[0, 1]'},
            {'input': 'massiv = [3, 2, 4], target = 6', 'output': '[1, 2]'},
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
    # 2. Aktsiyalar Bilan Eng Katta Foyda
    {
        'title': 'Aktsiyalar Bilan Eng Katta Foyda',
        'description': 'Aktsiya narxlari massivi berilgan. Bir marta sotib, bir marta sot qila olasiz. Eng katta foydani hisoblang.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[7, 1, 5, 3, 6, 4]',
        'output_example': '5',
        'categories': ['Massiv', 'Dinamik Dasturlash'],
        'examples': [
            {'input': 'narxlar = [7, 1, 5, 3, 6, 4]', 'output': '5 (1 da sotib, 6 da sot)'},
            {'input': 'narxlar = [7, 6, 4, 3, 1]', 'output': '0 (foyda yo\'q)'},
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
    # 3. Takroriy Elementni Topish
    {
        'title': 'Takroriy Elementni Topish',
        'description': 'Butun sonlar massivida takroriy element borligini tekshiring. Agar bir element ikki marta yoki undan ko\'p qo\'llanilib bo\'lsa, True qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1, 2, 3, 1]',
        'output_example': 'true',
        'categories': ['Massiv', 'Xesh Jadval'],
        'examples': [
            {'input': 'massiv = [1, 2, 3, 1]', 'output': 'true'},
            {'input': 'massiv = [1, 2, 3, 4]', 'output': 'false'},
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
    # 4. Grammatical Tekshirish
    {
        'title': 'Grammatik Anagram Tekshirish',
        'description': 'Ikkita satrni qabul qiling va ular anagram ekanligini tekshiring. Anagram - bu bir so\'z harflarini qayta joylashtirib boshqa so\'z hosil qilish.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"anagram"\n"nagaram"',
        'output_example': 'true',
        'categories': ['Matn', 'Xesh Jadval'],
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
    # 5. Eng Ko'p Qo'llaniladigan Element
    {
        'title': 'Eng Ko\'p Qo\'llaniladigan Element',
        'description': 'Massivda eng ko\'p qo\'llaniladigan elementni toping. Agar n/2 dan ko\'p bo\'lsa, u majorite element deyiladi.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3, 2, 3]',
        'output_example': '3',
        'categories': ['Massiv', 'Xesh Jadval'],
        'examples': [
            {'input': 'massiv = [3, 2, 3]', 'output': '3'},
            {'input': 'massiv = [2, 2, 1, 1, 1, 2, 2]', 'output': '2'},
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
    # 6. Satrni Teskari Qilish
    {
        'title': 'Satrni Teskari Qilish',
        'description': 'Berilgan satrni teskari qilib, aksariy version qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"hello"',
        'output_example': '"olleh"',
        'categories': ['Matn'],
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
    # 7. Qavslarning To'g'riligi
    {
        'title': 'Qavslarning To\'g\'riligi',
        'description': 'Satr faqat (), {}, [] qavslardan iborat. Ularning to\'g\'ri yopilganligini tekshiring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"({[]})"',
        'output_example': 'true',
        'categories': ['Matn', 'Stek'],
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
    # 8. Palindrom Tekshirish
    {
        'title': 'Palindrom Tekshirish',
        'description': 'Berilgan satr palindrom ekanligini tekshiring. Palindrom - teskari o\'qiganda ham o\'zi bo\'lgan so\'z.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"racecar"',
        'output_example': 'true',
        'categories': ['Matn'],
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
    # 9. Birinchi Takroriy Bo'lmagan Belgi
    {
        'title': 'Birinchi Takroriy Bo\'lmagan Belgi',
        'description': 'Satrdan birinchi takroriy bo\'lmagan belgini toping va uning indeksini qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"leetcode"',
        'output_example': '0',
        'categories': ['Matn', 'Xesh Jadval'],
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
    # 10. Eng Uzun Umumiy Prefix
    {
        'title': 'Eng Uzun Umumiy Prefix',
        'description': 'Satrlar massividan barcha satrlar uchun umumiy bo\'lgan eng uzun prefix topilsin.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '["flower","flow","flight"]',
        'output_example': '"fl"',
        'categories': ['Matn', 'Massiv'],
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
    # 11. Anagramlarni Guruhlash
    {
        'title': 'Anagramlarni Guruhlash',
        'description': 'Satrlar massivida anagramlarni guruhlang va guruhlangan natijani qaytaring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["eat","tea","tan","ate","nat","bat"]',
        'output_example': '[["bat"],["nat","tan"],["ate","eat","tea"]]',
        'categories': ['Matn', 'Xesh Jadval'],
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
    # 12. Ikkita Massivning Kesishmasi
    {
        'title': 'Ikkita Massivning Kesishmasi',
        'description': 'Ikkita massiv berilgan. Ularning kesishmadagi elementlarni topib qaytaring. Har bir element bitta marta qaytarilsin.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1,2,2,1]\n[2,2]',
        'output_example': '[2]',
        'categories': ['Massiv', 'Xesh Jadval'],
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
    # 13. So'z Naqshini Tekshirish
    {
        'title': 'So\'z Naqshini Tekshirish',
        'description': 'Naqsh va satr berilgan. Satr naqshga mos kelishini tekshiring. Har bir harf o\'z naqsh harfiga mos kelishi kerak.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"abba"\n"redbluebluered"',
        'output_example': 'true',
        'categories': ['Matn', 'Xesh Jadval'],
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
    # 14. Izomorf Satrlar
    {
        'title': 'Izomorf Satrlar',
        'description': 'Ikkita satr izomorf ekanligini tekshiring. Agar birinchi satrning harflari ikkinchiga o\'xshash tarzda map qilinsa, satrlar izomorf.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"egg"\n"add"',
        'output_example': 'true',
        'categories': ['Matn', 'Xesh Jadval'],
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
        'description': 'Ransom note va magazine satrlari berilgan. Ransom note magazine\'s harflaridan yasalishi mumkinmi?',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"a"\n"b"',
        'output_example': 'false',
        'categories': ['Matn', 'Xesh Jadval'],
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
    # 16. Ikkining Darajasi
    {
        'title': 'Ikkining Darajasi',
        'description': 'Butun son n berilgan. Agar u 2 ning darajasi bo\'lsa, true qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '16',
        'output_example': 'true',
        'categories': ['Matematika'],
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
    # 17. Baxtli Raqam
    {
        'title': 'Baxtli Raqam',
        'description': 'Musbat butun son n berilgan. Baxtli raqam ekanligini tekshiring. Raqamning raqamlarini kvadratiga ko\'taring va jarayonni takrorlang.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '19',
        'output_example': 'true',
        'categories': ['Matematika', 'Xesh Jadval'],
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
    # 18. To'g'ri Sempurna Kvadrat
    {
        'title': 'To\'g\'ri Sempurna Kvadrat',
        'description': 'Musbat butun son berilgan. Agar u sempurna kvadrat bo\'lsa, true qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '16',
        'output_example': 'true',
        'categories': ['Matematika'],
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
    # 19. Xunuk Raqam
    {
        'title': 'Xunuk Raqam',
        'description': 'Xunuk raqam asosiy faktorlari 2, 3 va 5 ga cheklanadi. n xunuk raqam ekanligini tekshiring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '10',
        'output_example': 'true',
        'categories': ['Matematika', 'Dinamik Dasturlash'],
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
    # 20. Yo'q Bo'lgan Raqam
    {
        'title': 'Yo\'q Bo\'lgan Raqam',
        'description': 'Massiv [0, n] diapazondan n ta turli raqamni o\'z ichiga oladi. Yo\'q bo\'lgan raqamni toping.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[9,6,4,2,3,5,7,0,1]',
        'output_example': '8',
        'categories': ['Massiv', 'Matematika'],
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
    # 21. Minimal Stek
    {
        'title': 'Minimal Stek',
        'description': 'push, pop, top va minimal element ishlarini qo\'laydigan stek yarating. Barcha amallar O(1) vaqtda bo\'lishi kerak.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["push","push","getMin","push","getMin"]\n[[1],[0],[],[-3],[]]',
        'output_example': '[null,null,0,null,-3]',
        'categories': ['Stek'],
        'examples': [
            {'input': '["push","push","getMin"]\n[[1],[0],[]]', 'output': '[null,null,0]'},
            {'input': '["push","getMin"]\n[[0],[]]', 'output': '[null,0]'},
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
    # 22. Reverse Polish Notation Baholash
    {
        'title': 'Reverse Polish Notation Baholash',
        'description': 'Reverse Polish Notation da arithmetic ifodani baholang. Operandlar va +, -, *, / operatorlari beriladi.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["2","1","+","3","*"]',
        'output_example': '9',
        'categories': ['Massiv', 'Matematika', 'Stek'],
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
    # 23. Kunlik Haroratlar
    {
        'title': 'Kunlik Haroratlar',
        'description': 'Kunlik haroratlar massivi berilgan. Har bir kun uchun keyingi isitroq kun qachon ekanligini topib, kunlar sonini qaytaring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[73,74,75,71,69,72,76,73]',
        'output_example': '[1,1,4,2,1,1,0,0]',
        'categories': ['Massiv', 'Stek'],
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
    # 24. Yog'un Suv
    {
        'title': 'Yo\'g\'un Suv',
        'description': 'Balandlik massivi berilgan. Yog\'un suv qancha bo\'lishi mumkinligini hisoblang. Bar kengligi 1 ga teng.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[0,1,0,2,1,0,1,3,2,1,2,1]',
        'output_example': '6',
        'categories': ['Massiv', 'Dinamik Dasturlash', 'Stek'],
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
    # 25. Gistogramming eng katta to'rtburchak
    {
        'title': 'Gistogramming Eng Katta To\'rtburchak',
        'description': 'Balandlik massivi berilgan. Gistogramada eng katta to\'rtburchak maydonini toping.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,5,6,2,3]',
        'output_example': '10',
        'categories': ['Massiv', 'Stek'],
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
    # 26. Binary Daraxt Darajali Traversal
    {
        'title': 'Binary Daraxt Darajali Traversal',
        'description': 'Binary daraxt berilgan. Darajali tartibi bilan traversal qiling (chap dan o\'ng, qat qat).',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[3,9,20,null,null,15,7]',
        'output_example': '[[3],[9,20],[15,7]]',
        'categories': ['Daraxti', 'Navbat'],
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
    # 27. Yig'indi Yo'li
    {
        'title': 'Yig\'indi Yo\'li',
        'description': 'Binary daraxt va target sum berilgan. Ildizdan bargacha yo\'lning yig\'indisi target ga teng bo\'lsa, true qaytaring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[5,4,8,11,null,null,13,4,7,2,null,null,null,1]\n22',
        'output_example': 'true',
        'categories': ['Daraxti'],
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
    # 28. Binary Daraxtning Maksimal Chuqurligi
    {
        'title': 'Binary Daraxtning Maksimal Chuqurligi',
        'description': 'Binary daraxt berilgan. Maksimal chuqurligi toping (ildizdan eng uzoq bargachagacha).',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3,9,20,null,null,15,7]',
        'output_example': '3',
        'categories': ['Daraxti'],
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
    # 29. Binary Qidiruv Daraxti Tekshirish
    {
        'title': 'Binary Qidiruv Daraxti Tekshirish',
        'description': 'Binary daraxt berilgan. Uning binary qidiruv daraxti ekanligini tekshiring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,3]',
        'output_example': 'true',
        'categories': ['Daraxti'],
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
    # 30. Binary Qidiruv Daraxti ning Eng Kichik Umumiy Atasi
    {
        'title': 'Binary Qidiruv Daraxti ning Eng Kichik Umumiy Atasi',
        'description': 'Binary qidiruv daraxti va ikkita node berilgan. Ularning eng kichik umumiy atasi (LCA) ni toping.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[6,2,8,0,4,7,9,null,null,3,5]\n2\n8',
        'output_example': '6',
        'categories': ['Daraxti'],
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
    help = 'Uzbek tilida 30 ta masalani qo\'shadi'

    def handle(self, *args, **options):
        # Clear existing data
        Problem.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.WARNING('🗑️  Database tozalandi!'))

        # Create categories
        categories = {}
        for cat_name, cat_desc in CATEGORIES_DATA.items():
            cat = Category.objects.create(name=cat_name, description=cat_desc)
            categories[cat_name] = cat
            self.stdout.write(self.style.SUCCESS(f'✅ Kategoriya yaratildi: {cat_name}'))

        self.stdout.write(self.style.SUCCESS('✅ 10 ta kategoriya yaratildi!\n'))
        self.stdout.write(self.style.WARNING('📚 30 ta masala qo\'shilyapti...\n'))

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
                    self.style.ERROR(f'❌ Xato: {problem_data["title"]} - {str(e)}')
                )

        self.stdout.write(self.style.SUCCESS(f'\n✅ Barcha {created_count} ta masala qo\'shildi!'))
        self.stdout.write(self.style.SUCCESS('✅ Har bir masalada 2 ta misol bor!'))
        self.stdout.write(self.style.SUCCESS('✅ Har bir masalada 6 ta test case bor!'))
        self.stdout.write(self.style.SUCCESS('🎉 Database UZBEK TILIDA tayyor!'))
