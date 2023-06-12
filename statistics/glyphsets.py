import string

languages = {
    "english": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "french": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZéàèùçâêîôûëïü",
    "italian": "abcdefghilmnopqrstuvzABCDEFGHILMNOPQRSTUVZ",
    "german": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZßäöüÄÜÖ",
    "spanish": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZñÑ",
    "portugal": "abcdefghijlmnopqrstuvxzABCDEFGHIJLMNOPQRSTUVXZ",
    "turkish": "abcdefghijklmnoprstuvyzABCDEFGHİJKLMNOPRSTUVYZçğıöüşÇĞIÖÜŞ",
    "russian": "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЁ",
    "polish": "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZąćęłńóśźżĄĆĘŁŃÓŚŹŻ",
}
additional_glyphs = {
    "digits": "0123456789",
    "punctuation": ";:,.?!…",
    "math": "#&|()[]{}+-×/√<≤=≠≥>^%",
    "programming": "$*@\\_~`\"'",
}
union = set()
for language, alphabet in sorted(languages.items(), key=lambda item: -len(item[1])):
    print(len(alphabet), language)
    union |= set(alphabet)
print(len(union), "".join(sorted(union)))
union.update(*additional_glyphs.values())
print(len(union), "".join(sorted(set().union(*additional_glyphs.values()))))
assert all(char in union for char in string.printable[:-6])


text = ""
text = string.printable[:-6]
for char in text:
    if char not in union:
        print(ord(char), char)
