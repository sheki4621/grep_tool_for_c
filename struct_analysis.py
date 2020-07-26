import re

def get_file_list():

    return ['struct.c', 'struct.h']

def line_generator(file):
    with open(file) as f:
        lines = f.readlines()
        for l in lines:
            yield l

def search_rematch4line(line, rex):
    m = re.search(rex, line)
    if m == None:
        return ''
    return m.group()


def get_dict_struct_instance(file, structs):
    print(file)
    # print(structs)
    result = {}
    gen = line_generator(file)
    for line in gen:
        for struct in structs:
            search_result = search_rematch4line(line, '{}\s[\*?\w*\,?\s?]*;'.format(struct))
            search_result = search_result.strip(' ;')
            words = search_result.split()
            if len(words) >= 2:
                struct_name = words[0]
                for i in range(len(words) -1):
                    result[words[i+1].strip('* ,')] = struct_name
    return result

def search_var(file, member):
    result = {}
    gen = line_generator(file)
    for i, line in enumerate(gen):
        searched_line = search_rematch4line(line.strip(), '^.*{}.*$'.format(member)).strip()
        if len(searched_line) > 0:
            result[i+1] = searched_line
    return result


def write_csv(filename, target_file, lines, struct_name='', val_name=''):
    with open(filename, mode='a') as f:
        if val_name == '':
            f.write('{}:{}\n'.format(target_file, struct_name))
        else:
            f.write('{}:{}:{}\n'.format(target_file, struct_name, val_name))

        for key, value in lines.items():
            f.write('{},{}\n'.format(key, value))
        f.write('\n\n')

def main():
    filelist = get_file_list()
    result_filename = 'analysis_result.csv'

    ###### CHANGE ######
    structs = ['PERSON', 'BODY']
    # True: only struct name, False: include struct's val name
    only_struct = True
    #only_struct = False
    ###### CHANGE ######


    for file in filelist:
        print("Filename:{}".format(file))
        # {'PERSON':person, 'BODY':body}
        # {'tanaka':PERSON, 'kobayashi':PERSON, 'BODY':BODY}
        # {'PERSON':[tanaka, kobayashi], 'BODY':[kobayasinokarada]}

        struct_instance = get_dict_struct_instance(file, structs)
        print(struct_instance)

        if only_struct:
            for struct in structs:
              file_search_result = search_var(file, struct)
              write_csv(result_filename, file, file_search_result, struct)

        else:
            for instance, struct in struct_instance.items():

                file_search_result = search_var(file, instance)
                write_csv(result_filename, file, file_search_result, struct, instance)

    # print(result)

    # for file in filelist:
    #     print(file)
        #result = analyze(file)
        #output(result)

if __name__ == "__main__":
    main()


    print('test')
    line = ' if(!init(persons, 30)){'
    rex = '^.*persons.*$'
    m = re.search(rex, line)
    if m == None:
        print('naiyooooo')
    print(m.group())
