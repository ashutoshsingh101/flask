string = 'this is my dog'

string_list = string.split(' ')
if len(string_list) > 1:
    for i in range(1,len(string_list)):
        print('yes')
        string_list[i] = string_list[i].title()
    camel_case_string = ''
    for item in string_list:
        camel_case_string = camel_case_string+str(item)
    return camel_case_string
else:
    return string