import database_manager

while True:
    cmd = input()
    # print(cmd)
    if cmd == 'drop':
        database_manager.drop_tables()

    elif cmd == 'init':
        database_manager.init()

    elif cmd.lower().startswith('addst'):
        params = cmd[5:].replace(' ', '').split(',')
        if database_manager.add_student(params[0], params[1], params[2]) == 0:
            print('student added.')
        else:
            print('student with id ' + params[0] + ' already exist.')

    elif cmd.lower().startswith('addct'):
        params = cmd[5:].replace(' ', '').split(',')
        if database_manager.add_course(params[0].upper(), params[1], params[2]) == 0:
            print('course added.')
        else:
            print('course with id ' + params[0].upper() + ' already exist.')

    elif cmd.lower().startswith('addpr'):
        params = cmd[5:].replace(' ', '').split(',')
        if database_manager.add_prof(params[0].upper(), params[1], params[2]) == 0:
            print('professor added.')
        else:
            print('professor with id ' + params[0].upper() + ' already exist.')

    elif cmd.lower() == 'getst':
        database_manager.get_students()

    elif cmd.lower() == 'getct':
        database_manager.get_courses()

    elif cmd.lower() == 'getpr':
        database_manager.get_profs()

    elif cmd.lower().startswith('searchst'):
        name = cmd[8:].replace(' ', '').lower()
        database_manager.search_student(name)

    else:
        print('unknown command')
