from django.core.management.base import BaseCommand
from main.models import Problem, Category, TestCase, Example

CATEGORIES_DATA = {
    'Array': 'Massiv va array masalalari',
    'String': 'Matn va string masalalari',
    'HashTable': 'HashMap va dictionary masalalari',
    'Math': 'Matematik masalalari',
    'Stack': 'Stek masalalari',
    'Queue': 'Navbat masalalari',
    'Tree': 'Binary tree va tree masalalari',
    'Graph': 'Graf masalalari',
    'DynamicProgramming': 'Dynamic Programming masalalari',
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
        'categories': ['Array', 'HashTable'],
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
        'categories': ['Array', 'DynamicProgramming'],
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
        'categories': ['Array', 'HashTable'],
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
    # 4. Anagram Tekshirish
    {
        'title': 'Anagram Tekshirish',
        'description': 'Ikkita satrni qabul qiling va ular anagram ekanligini tekshiring. Anagram - bu bir so\'z harflarini qayta joylashtirib boshqa so\'z hosil qilish.',
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
    # 5. Majoriteta Element
    {
        'title': 'Majoriteta Element',
        'description': 'Massivda eng ko\'p qo\'llaniladigan elementni toping. Agar n/2 dan ko\'p bo\'lsa, u majoriteta element deyiladi.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3, 2, 3]',
        'output_example': '3',
        'categories': ['Array', 'HashTable'],
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
    # 7. Qavslarning To'g'riligi
    {
        'title': 'Qavslarning To\'g\'riligi',
        'description': 'Satr faqat (), {}, [] qavslardan iborat. Ularning to\'g\'ri yopilganligini tekshiring.',
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
    # 8. Palindrom Tekshirish
    {
        'title': 'Palindrom Tekshirish',
        'description': 'Berilgan satr palindrom ekanligini tekshiring. Palindrom - teskari o\'qiganda ham o\'zi bo\'lgan so\'z.',
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
    # 9. Birinchi Noquli Belgi
    {
        'title': 'Birinchi Noquli Belgi',
        'description': 'Satrdan birinchi takroriy bo\'lmagan belgini toping va uning indeksini qaytaring.',
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
    # 10. Eng Uzun Umumiy Prefix
    {
        'title': 'Eng Uzun Umumiy Prefix',
        'description': 'Satrlar massividan barcha satrlar uchun umumiy bo\'lgan eng uzun prefix topilsin.',
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
    # 11. Anagramlarni Guruhlash
    {
        'title': 'Anagramlarni Guruhlash',
        'description': 'Satrlar massivida anagramlarni guruhlang va guruhlangan natijani qaytaring.',
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
    # 12. Ikkita Massivning Kesishmasi
    {
        'title': 'Ikkita Massivning Kesishmasi',
        'description': 'Ikkita massiv berilgan. Ularning kesishmadagi elementlarni topib qaytaring. Har bir element bitta marta qaytarilsin.',
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
    # 13. So'z Naqshini Tekshirish
    {
        'title': 'So\'z Naqshini Tekshirish',
        'description': 'Naqsh va satr berilgan. Satr naqshga mos kelishini tekshiring. Har bir harf o\'z naqsh harfiga mos kelishi kerak.',
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
    # 14. Izomorf Satrlar
    {
        'title': 'Izomorf Satrlar',
        'description': 'Ikkita satr izomorf ekanligini tekshiring. Agar birinchi satrning harflari ikkinchiga o\'xshash tarzda map qilinsa, satrlar izomorf.',
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
        'description': 'Ransom note satrini magazine satridan harflardan foydalanib yozish mumkinligini tekshiring.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '"a"\n"b"',
        'output_example': 'false',
        'categories': ['String', 'HashTable'],
        'examples': [
            {'input': 'ransomNote = "a", magazine = "b"', 'output': 'false'},
            {'input': 'ransomNote = "a", magazine = "aa"', 'output': 'true'},
        ],
        'test_cases': [
            ('"a"\n"b"', 'false'),
            ('"a"\n"aa"', 'true'),
            ('"aa"\n"ab"', 'false'),
            ('"aa"\n"aab"', 'true'),
            ('"abc"\n"abc"', 'true'),
            ('"abc"\n"aabbcc"', 'true'),
        ]
    },
    # 16. Ikkining Darajasi
    {
        'title': 'Ikkining Darajasi',
        'description': 'Butun son berilgan. Uni 2 ning qaysi darajasi (shuning uchun true/false) tekshiring.',
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
    # 17. Baxtli Raqam
    {
        'title': 'Baxtli Raqam',
        'description': 'Raqam baxtli deyiladi agar unda har bir raqam bir marta qo\'l kelsa.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '123',
        'output_example': 'true',
        'categories': ['Math', 'HashTable'],
        'examples': [
            {'input': 'n = 123', 'output': 'true'},
            {'input': 'n = 1223', 'output': 'false'},
        ],
        'test_cases': [
            ('123', 'true'),
            ('1223', 'false'),
            ('1', 'true'),
            ('1023456789', 'true'),
            ('1023456780', 'false'),
            ('121', 'false'),
        ]
    },
    # 18. To'g'ri Sempurna Kvadrat
    {
        'title': 'To\'g\'ri Sempurna Kvadrat',
        'description': 'Raqam to\'g\'ri sempurna kvadrat ekanligini tekshiring (masalan, 4, 9, 16).',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '16',
        'output_example': 'true',
        'categories': ['Math'],
        'examples': [
            {'input': 'num = 16', 'output': 'true'},
            {'input': 'num = 17', 'output': 'false'},
        ],
        'test_cases': [
            ('16', 'true'),
            ('17', 'false'),
            ('1', 'true'),
            ('0', 'true'),
            ('9', 'true'),
            ('10', 'false'),
        ]
    },
    # 19. Xunuk Raqam
    {
        'title': 'Xunuk Raqam',
        'description': 'Raqam xunuk deyiladi agar uning raqamlarining kvadratlari yig\'indisi 1 ga teng bo\'lguncha siklda takrorlanmasa.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '2',
        'output_example': 'false',
        'categories': ['Math', 'DynamicProgramming'],
        'examples': [
            {'input': 'n = 2', 'output': 'false'},
            {'input': 'n = 7', 'output': 'true'},
        ],
        'test_cases': [
            ('2', 'false'),
            ('7', 'true'),
            ('10', 'false'),
            ('19', 'true'),
            ('1', 'true'),
            ('0', 'false'),
        ]
    },
    # 20. Yo'q Bo'lgan Raqam
    {
        'title': 'Yo\'q Bo\'lgan Raqam',
        'description': 'n+1 ta raqam massivida 0 dan n gacha bo\'lgan raqamlar berilgan. Yo\'q bo\'lgan raqamni toping.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3,0,1]',
        'output_example': '2',
        'categories': ['Array', 'Math'],
        'examples': [
            {'input': 'nums = [3,0,1]', 'output': '2'},
            {'input': 'nums = [0,1]', 'output': '2'},
        ],
        'test_cases': [
            ('[3,0,1]', '2'),
            ('[0,1]', '2'),
            ('[9,6,4,2,3,5,7,0,1]', '8'),
            ('[0]', '1'),
            ('[1]', '0'),
            ('[1,2,0]', '3'),
        ]
    },
    # 21. Minimal Stek
    {
        'title': 'Minimal Stek',
        'description': 'Har bir element uchun o\'ngdagi eng kichik elementni toping. Natijaviy o\'ng massivi qaytaring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[1,2,1,2,2,2,2,2,0,1,7,5,27,7,27,27,7,27,6,12,405,52,52,52,52,52,6,52,52,38,52,36,52]',
        'output_example': '[2,2,2,2,2,2,2,0,-1,1,5,5,6,7,27,27,7,27,27,27,52,52,52,52,52,6,52,52,38,36,52,-1,-1]',
        'categories': ['Stack'],
        'examples': [
            {'input': 'temps = [73,74,75,71,69,72,76,73]', 'output': '[1,1,4,2,1,1,0,0]'},
            {'input': 'temps = [30,40,50,60]', 'output': '[1,1,1,0]'},
        ],
        'test_cases': [
            ('[73,74,75,71,69,72,76,73]', '[1,1,4,2,1,1,0,0]'),
            ('[30,40,50,60]', '[1,1,1,0]'),
            ('[34,80,80,34,34,80,80,80,80,34]', '[1,0,0,0,0,0,0,0,0,0]'),
            ('[1,2,3]', '[1,1,0]'),
            ('[3,2,1]', '[0,0,0]'),
            ('[100]', '[0]'),
        ]
    },
    # 22. Reverse Polish Notation Baholash
    {
        'title': 'Reverse Polish Notation Baholash',
        'description': 'Reverse Polish Notation operatorlari massivini baholang va natija qaytaring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '["2","1","+","3","*"]',
        'output_example': '9',
        'categories': ['Array', 'Math', 'Stack'],
        'examples': [
            {'input': 'tokens = ["2","1","+","3","*"]', 'output': '9'},
            {'input': 'tokens = ["4","13","5","/","+"]', 'output': '6'},
        ],
        'test_cases': [
            ('["2","1","+","3","*"]', '9'),
            ('["4","13","5","/","+"]', '6'),
            ('["15","7","1","+","/","3","*","2","-"]', '5'),
            ('["2","3","+"]', '5'),
            ('["10"]', '10'),
            ('["2","3","*"]', '6'),
        ]
    },
    # 23. Kunlik Haroratlar
    {
        'title': 'Kunlik Haroratlar',
        'description': 'Har bir kun uchun o\'ngda isik ko\'p bo\'lgan kunni toping. Kunlar sonini qaytaring.',
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
            ('[34,80,80,34,34,80,80,80,80,34]', '[1,0,0,0,0,0,0,0,0,0]'),
            ('[1,2,3]', '[1,1,0]'),
            ('[3,2,1]', '[0,0,0]'),
            ('[100]', '[0]'),
        ]
    },
    # 24. Yo'g'un Suv
    {
        'title': 'Yo\'g\'un Suv',
        'description': 'Balandlik massivida eng ko\'p suvni qamashuvchi kontejner topilsin. Suvning hajmi qaytaring.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[1,8,6,2,5,4,8,3,7]',
        'output_example': '49',
        'categories': ['Array', 'DynamicProgramming', 'Stack'],
        'examples': [
            {'input': 'height = [1,8,6,2,5,4,8,3,7]', 'output': '49'},
            {'input': 'height = [1,1]', 'output': '1'},
        ],
        'test_cases': [
            ('[1,8,6,2,5,4,8,3,7]', '49'),
            ('[1,1]', '1'),
            ('[2,3,4,5,18,17,6]', '17'),
            ('[4,3,2,1,4]', '16'),
            ('[1,2,1]', '2'),
            ('[3,9,3,4,7,2,12,6]', '45'),
        ]
    },
    # 25. Gistogramming Eng Katta To'rtburchak
    {
        'title': 'Gistogramming Eng Katta To\'rtburchak',
        'description': 'Gistogramm ustunlarida eng katta to\'rtburchakning maydonini topilsin.',
        'difficulty': 'Hard',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,5,6,2,3]',
        'output_example': '10',
        'categories': ['Stack'],
        'examples': [
            {'input': 'heights = [2,1,5,6,2,3]', 'output': '10'},
            {'input': 'heights = [2,4]', 'output': '4'},
        ],
        'test_cases': [
            ('[2,1,5,6,2,3]', '10'),
            ('[2,4]', '4'),
            ('[1]', '1'),
            ('[1,1,1,1]', '4'),
            ('[1,2,2,1]', '4'),
            ('[0,2,0]', '2'),
        ]
    },
    # 26. Binary Daraxt Darajali Traversal
    {
        'title': 'Binary Daraxt Darajali Traversal',
        'description': 'Binary daraxtni daraj-daraj traversal qilib, natijani qaytaring.',
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
            ('[1,2,3,4,5,6,7]', '[[1],[2,3],[4,5,6,7]]'),
            ('[]', '[]'),
            ('[1,2]', '[[1],[2]]'),
            ('[1,null,2]', '[[1],[2]]'),
        ]
    },
    # 27. Yig'indi Yo'li
    {
        'title': 'Yig\'indi Yo\'li',
        'description': 'Root dan leaf gacha yo\'llar uchun eng katta yig\'indini topilsin.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[1,2,3]',
        'output_example': '6',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [1,2,3]', 'output': '6'},
            {'input': 'root = [1,2]', 'output': '3'},
        ],
        'test_cases': [
            ('[1,2,3]', '6'),
            ('[1,2]', '3'),
            ('[1]', '1'),
            ('[9,9,9]', '27'),
            ('[5,4,11,null,null,7,2]', '18'),
            ('[1,2,3,4,null,null,5]', '9'),
        ]
    },
    # 28. Binary Daraxtning Maksimal Chuqurligi
    {
        'title': 'Binary Daraxtning Maksimal Chuqurligi',
        'description': 'Binary daraxtning maksimal chuqurligi topilsin.',
        'difficulty': 'Easy',
        'function_name': 'Solution().solve',
        'input_example': '[3,9,20,null,null,15,7]',
        'output_example': '3',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [3,9,20,null,null,15,7]', 'output': '3'},
            {'input': 'root = [2,null,3]', 'output': '2'},
        ],
        'test_cases': [
            ('[3,9,20,null,null,15,7]', '3'),
            ('[2,null,3]', '2'),
            ('[]', '0'),
            ('[1]', '1'),
            ('[1,2,3,4,5,null,6]', '4'),
            ('[0]', '1'),
        ]
    },
    # 29. Binary Qidiruv Daraxti Tekshirish
    {
        'title': 'Binary Qidiruv Daraxti Tekshirish',
        'description': 'Daraxt Binary Qidiruv Daraxti ekanligini tekshiring.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[2,1,3]',
        'output_example': 'true',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [2,1,3]', 'output': 'true'},
            {'input': 'root = [5,1,4,null,null,4,6]', 'output': 'false'},
        ],
        'test_cases': [
            ('[2,1,3]', 'true'),
            ('[5,1,4,null,null,4,6]', 'false'),
            ('[1]', 'true'),
            ('[5,null,15,null,20]', 'true'),
            ('[1,null,1]', 'true'),
            ('[32,26,47,19,null,null,56,16,27,null,null,54]', 'false'),
        ]
    },
    # 30. Binary Qidiruv Daraxti ning Eng Kichik Umumiy Atasi
    {
        'title': 'Binary Qidiruv Daraxti ning Eng Kichik Umumiy Atasi',
        'description': 'Binary Qidiruv Daraxti uchun ikkita tugunning eng kichik umumiy atasi topilsin.',
        'difficulty': 'Medium',
        'function_name': 'Solution().solve',
        'input_example': '[6,2,8,0,4,7,9,null,null,3,5]',
        'output_example': '6',
        'categories': ['Tree'],
        'examples': [
            {'input': 'root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8', 'output': '6'},
            {'input': 'root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4', 'output': '2'},
        ],
        'test_cases': [
            ('[6,2,8,0,4,7,9,null,null,3,5]', '6'),
            ('[6,2,8,0,4,7,9,null,null,3,5]', '2'),
            ('[2,1]', '2'),
            ('[6,2,8,0,4,7,9]', '6'),
            ('[1,0]', '1'),
            ('[37,24,44,12,36,31,47,8,16,28,40,null,null,26,42]', '37'),
        ]
    },
]

class Command(BaseCommand):
    help = 'Load 30 Uzbek problems with English categories'

    def handle(self, *args, **options):
        self.stdout.write('🗑️  Database tozalandi!\n')
        Problem.objects.all().delete()
        Category.objects.all().delete()

        # Kategoriyalar yaratish
        categories = {}
        for cat_name, cat_desc in CATEGORIES_DATA.items():
            cat = Category.objects.create(name=cat_name, description=cat_desc)
            categories[cat_name] = cat

        self.stdout.write(f'✅ {len(categories)} ta English kategoriya yaratildi!\n')
        self.stdout.write('📚 30 ta masala qo\'shilyapti...\n')

        # Masalalar qo'shish
        for i, problem_data in enumerate(PROBLEMS_DATA, 1):
            problem = Problem.objects.create(
                title=problem_data['title'],
                description=problem_data['description'],
                difficulty=problem_data['difficulty'],
                function_name=problem_data['function_name'],
                input_example=problem_data['input_example'],
                output_example=problem_data['output_example'],
            )

            # Kategoriyalar qo'shish
            cat_names = ', '.join(problem_data['categories'])
            for cat_name in problem_data['categories']:
                problem.categories.add(categories[cat_name])

            # Misollar qo'shish
            for example in problem_data['examples']:
                Example.objects.create(
                    problem=problem,
                    ex_input=example['input'],
                    ex_output=example['output']
                )

            # Test case'lar qo'shish
            for j, (inp, out) in enumerate(problem_data['test_cases'], 1):
                TestCase.objects.create(
                    problem=problem,
                    input_data=inp,
                    expected_output=out,
                    order=j
                )

            self.stdout.write(f'✅ {i}. {problem.title} [{cat_names}]')

        self.stdout.write('\n✅ Barcha 30 ta masala qo\'shildi!')
        self.stdout.write('✅ Har bir masalada 2 ta misol bor!')
        self.stdout.write('✅ Har bir masalada 6 ta test case bor!')
        self.stdout.write('🎉 Database tayyor!')
