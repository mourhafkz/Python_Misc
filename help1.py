# any type of search and replace is easier with dictionary
# check the temp_list result and tell me what your desired input is 


word = input('write your word here:')
replacement_dict = {'a': '1', 'e': '2', 'i': '3', 'o': '4', 'u': '5'}
temp_list = []

for letter in word:
    if letter in replacement_dict:
        word.replace(letter, replacement_dict[letter])
        temp_list.append(replacement_dict[letter])
    else:
        word.replace(letter, letter+'a')
        temp_list.append(letter)

print(''.join(temp_list))
print(word)
