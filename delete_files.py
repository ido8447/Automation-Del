# delete files from list of path's older than X days
import datetime
import os
import stat

start_time = datetime.datetime.now()

##
#one_time_log = []
#

def file_to_date(_file):
    mtime_stamp = os.path.getmtime(_file)
    modification_datetime = datetime.datetime.fromtimestamp(mtime_stamp, tz=datetime.timezone.utc)
    return modification_datetime.strftime("%d/%m/%Y")


files_size = 0
files_count = 0
links_count = 0
empty_dirs = 0
limit_time = datetime.datetime.now() - datetime.timedelta(days=60)
limit_seconds = (limit_time - datetime.datetime(1970, 1, 1)).total_seconds()
excluded_users = ['mosheb','mohammadh']
#included_users = ['idos']
users_path = '/projects/regression/users'
included_users = os.listdir(users_path)

paths = [os.path.join(users_path, d) for d in included_users]


print('Welcome')
print('This script delete all regression files bigger than 2 month')
print(f'Exclude {excluded_users} users')
print('Exclude _noclean directory in any format ')
print('And unlink the symbol files')
print("Let's Go!")

for path in paths:
    for (root, dirnames, filenames) in os.walk(path):
        username = path.split('/')[-1]
        delete = True
        for user in excluded_users:
            if user == username:
                delete = False
        if '_noclean' in str(root).lower() or not delete:
            continue

        elif len(filenames) > 0:
            absolute_files = [os.path.join(root, f) for f in filenames]
            for file in absolute_files:
                try:
                    if (os.path.islink(file)):
                        mtime = os.lstat(file).st_mtime
                        if limit_seconds > mtime:
                            modification_datetime = datetime.datetime.fromtimestamp(mtime, tz=datetime.timezone.utc)
                            link_date = modification_datetime.strftime("%d/%m/%Y")
                            print(f'({links_count}) unlinks - {link_date}: {file}')
                            #one_time_log.append(f'({links_count}) unlinks - {link_date}: {file}')
                            links_count += 1
                            os.unlink(file)
                    else:
                        file_age = os.path.getmtime(file)  # file modification to 1 1 1970 in seconds
                        if limit_seconds > file_age:
                            files_count += 1
                            files_size += os.path.getsize(file)
                            print(f'({files_count}) delete ({round(files_size / 1024 ** 3, 4)}) GB - ({file_to_date(file)}) {file}')
                            #one_time_log.append(f'({files_count}) delete ({round(files_size / 1024 ** 3, 4)}) GB - ({file_to_date(file)}) {file}')
                            os.remove(file)
                            if len(os.listdir(root)) <= 0:
                                print(f'delete empty folder - {root}')
                                #one_time_log.append(f'delete empty folder - {root}')
                                empty_dirs += 1
                                os.removedirs(root)
                        else:
                            continue
                            # print(f'stay - {file}')
                except Exception as e:
                        print(e)
                #one_time_log.append(e)
        elif len(dirnames) <= 0 and os.listdir(root) == []:
            dir_age = os.path.getmtime(root)
            if limit_seconds > dir_age:
                print(f'delete empty folder - {root}')
                #one_time_log.append(f'delete empty folder - {root}')
                empty_dirs += 1
                os.removedirs(root)
datenow = datetime.datetime.now().strftime('regression_delete_%d%m%Y_%H%M%S')
with open(f'/var/log/regression_delete_logs/{datenow}', 'w') as wr:
    wr.write(f'\n\nStart time: {start_time}\n')
    wr.write(f'End time: {datetime.datetime.now()}\n\n')
    wr.write('Excluded Users:\n')
    for ex in excluded_users:
        wr.write(f'{ex}\n')
    wr.write(f'\n{round(files_size / 1024 ** 3, 4)} GB  has been delete\n')
    wr.write(f'Delete {files_count} files\n')
    wr.write(f'Delete {links_count} links\n')
    wr.write(f'Delete {empty_dirs} empty folders')

    wr.close()

#with open('/var/log/regression_delete_logs/last_run_lines', 'w') as lines:
#    for line in one_time_log:
#        wr.write(line)
#        wr.close()
print((f'LOG: /var/log/regression_delete_logs/{datenow}')