""" Test data """


test_data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""
test_data_to_list = test_data.strip().split('\n')
test_result = 95437


test_dir1 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d"""

test_dir1_to_list = test_dir1.strip().split('\n')

test_dir3 = """$ cd /
$ ls
14848514 b.txt
8504156 c.dat
$ cd a"""

test_dir3_to_list = test_dir3.strip().split('\n')
test_dir3_size = 23352670

test_dir4 = """$ cd lpswsp
$ ls
173180 dcqnblb"""
test_dir4_to_list = test_dir4.strip().split('\n')

test_dir5 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
29116 f
2557 g
62596 h.lst"""

test_dir5_to_list = test_dir5.strip().split('\n')

""" End of test data"""



""" define classes """

from collections import Counter

class File():

    filetype = 'file'

    def __init__(self, path, size = 0):
        self.size = size
        self.path = path
        self.name = self.path.split('/')[-1]

    def __str__(self):
        indent = '  '*self.layers()
        return indent + f"- {self.path}, ({self.filetype},{self.size})"
    
    def __eq__(self, other):
        return self.path == other.path
    
    def __lt__(self, other):
        return self.path < other.path
    
    def __hash__(self) -> int:
        return hash(self.path)

    def layers(self):
        c = Counter(self.path)
        return c['/']
    
    def bottom_level_directory(self):
        dir = self.path.split('/')[-2]
        return '/' if dir == '' else dir
    



class Directory(File):

    """ Directories are defined as a type of file that can contain other files """

    directories = []
    filetype = 'dir'

    def __init__(self, path, files = []):
        super().__init__(path)
        self.name = self.path.split('/')[-2] 
        self.files = files
        for file in self.files:
            self.size += file.size

    def layers(self):
        c = Counter(self.path)
        return c['/']-1

    
    def add_file(self,*args):
        for arg in args:
            self.files.append(arg)
            self.size += arg.size

    def delete_file(self, *args):
        for arg in args:
            if arg not in self.files:
                print('File does not exist')
            else:
                self.files.remove(arg)
                self.size -= arg.size
                print('File deleted')

    
    def large(self):
        if self.size() > 100000:
            return True
        else:
            return False
        

        

    

class ParentDirectory(Directory):

    """ Parent directories are defined as a directory that can contain other directories """

    def __init__(self, name, files=[], directories=[]):
        super().__init__(name,files)
        if self.name == '':
            self.name = '/'
        self.directories = directories
        for directory in directories:
            self.size += directory.size

    def add_directory(self,*args):
        for arg in args:
            self.directories.append(arg)
            self.size += arg.size

    def delete_directory(self, *args):
        for arg in args:
            if arg not in self.directories:
                print('Directory does not exist')
            else:
                self.directoryies.remove(arg)
                self.size -= arg.size
                print('Directory deleted')

    def add_file(self,*args):
        for arg in args:
            added = False
            for directory in self.directories:
                if arg.bottom_level_directory() == directory.name:
                    directory.add(arg)
                    added = True
                    break
                else:
                    continue
            if not added:
                self.files.append(arg)
                self.size += arg.size

    
    

        

class FileSystem():

    """ Top level file system. Contains list of all files in a system  """

    def __init__(self, files=[], max_size = 70000000, total_size = 0):
        self.files = sorted(set(files))
        self.directories = [ file for file in files 
                             if isinstance(file, Directory)
                             or isinstance(file, ParentDirectory) ]
        self.max_size = max_size
        self.size = total_size
        for file in self.files:
            self.size += file.size

    def __str__(self):
        return '\n'.join(str(file) for file in self.files)
    
    def unused_space(self):
        return self.max_size - self.size
    
    def small_dirs(self, max_size = 100000):
        small_directories = []
        size = 0
        for directory in self.directories:
            print(directory)
            if directory.size > max_size:
                pass
            else:
                small_directories.append(directory.name)
                size += directory.size
        return small_directories, size
    



""" end of class definition """








""" with classes defined  """

def listing(lines, directory):
    """ takes in lines from terminal output and finds the location of the directory's listing"""
 
    for line_number, line in enumerate(lines):
        if line == f'$ cd {directory.name}':
            start = line_number
            break
        else:
            continue
    for line_number, line in enumerate(lines[start+1:]):
        if line[0] == '$ cd':
            end = line_number+start+1
            break
        elif line_number == len(lines[start+1:])-1:
            end = line_number+start+2
            break
        
    return (start, end)
    
def is_parent_directory(lines, directory):
    """ checks if other directories in the listing, and returns ParentDirecctory if True"""
    if any('dir' in line for line in lines):
        return ParentDirectory(directory.path, directory.files, directory.directories)
    else:
        return directory
    
def populate_directory(lines, directory): # NEEDS WORK, CURRENTLY PUTTING ALL FILES UNDER EVERYTHING
    start, end = listing(lines, directory)
    directory = is_parent_directory(lines[start+2:end], directory)
    for line_number, line in enumerate(lines[start+2:end]):
        if line[:3] == 'dir':
            path = directory.path.removesuffix('.') + line[4:] + '/.'
            inner_directory = populate_directory(lines[line_number+1:], Directory(path))
            directory.add_directory(inner_directory)
            break
        elif line[0] != '$':
            path = directory.path.removesuffix('.') + line.split()[1]
            directory.add_file(File(path,int(line.split()[0])))
            continue

    return directory


directory =  populate_directory(test_dir5_to_list, Directory('/a/.'))
filenames = [file.name for file in directory.files]
assert filenames == ['f','g','h.lst']
assert directory.size == 94269


def parse_terminal_output(lines):

    """ takes in lines from terminal output and converts into a filesystem"""
    
    current_directory = ''
    directories = []
    files = []
    
    for line_index, line in enumerate(lines):
        words = line.strip().split()
        if words[0] == '$':
            if words[1] == 'cd': 
                if words[2] == '..':
                    current_directory,_,_ = current_directory.rpartition('/')
                elif words[2] != '/':
                    current_directory += '/' + words[2]
            continue
        elif words[0] == 'dir':
            path = current_directory + '/' + words[1] + '/.'
            new_lines = lines[line_index:]
            directory = populate_directory(new_lines, Directory(path))
            directories.append(directory)
            
        else:
            path = current_directory + '/' + words[1]
            files.append(File(path,int(words[0])))
    
    for directory in directories:
        print(f'{directory.name}:',  [str(file) for file in directory.files])
    all_files = files + directories

    return FileSystem(all_files)
            


test_filesystem = parse_terminal_output(test_data_to_list)

#assert test_filesystem.small_dirs()[1] == test_result
   






    


test_files = {'abc': 123, 'j': 10, 'k': 30}
test_dir_xyz_listing = ['j','k']
#test_dir_xyz = Directory('xyz',test_dir_xyz_listing)
#test_dir_xyz.get_file_sizes(test_files)
#print(test_dir_xyz.sizes)


test_dir_mno = ['dir xyz', 'abc']
#test_dir_mno = convert_to_directories('mno',test_dir_mno)
#test_dir_mno.get_file_sizes(test_files)




def filesystem_class(lines):
    """ extract filesystem from given terminal output """
    directories = []
    file_sizes = {}

    listings = find_listings(lines)
    for directory, linelist in listings.items():

        lines = lines[linelist[0]:linelist[1]]
        listing, files = extract_listing(lines)

        directory = convert_to_directories(directory, listing)

        file_sizes.update(files)
        directory.get_file_sizes(file_sizes)
        directories.append(directory)
        
    
    return directories, files




#filesystem(test_dir1_to_list)
#assert filesystem(test_dir3_to_list) == (['/'], {'b.txt':14848514, 'c.dat': 8504156})


#assert filesystem(test_dir1_to_list)[1] == ({'b.txt':14848514, 'c.dat': 8504156})



""" find possible files for deletion """


  
def small_directories_class(directories):
    """ given a  list of directories, create a list of the small directories """
    small_directories = []
    for directory in directories:
        if directory.large():
            pass
        else:
            small_directories.append(directory)
    return small_directories

def sum_of_sizes_class(directories):
    sum_of_sizes = 0
    for directory in directories:
        sum_of_sizes += directory.size()
    return sum_of_sizes

def possible_deletions_class(lines):
    directories, files = filesystem_class(lines)
    small = small_directories(directories)
    return sum_of_sizes(small)



#assert possible_deletions(test_dir3_to_list) == 0

#assert possible_deletions(test_data_to_list) == test_result





    

""" without classes defined """


""" convert terminal output into filesystem """

def find_listings(lines):
    """ takes in lines from terminal output and finds the start of a listing,
     returns the lines of that listing and the name of the outer directory """
    listings = {}
    listing = False
    for line_number, line in enumerate(lines):
        while not listing: 
            if line == '$ ls':
                directory = lines[line_number-1][5:] 
                listings[directory] = line_number+1
                listing = True
            break
        while listing:
            if line[:4] == '$ cd':
                listings[directory] = [listings[directory],line_number]
                listing = False
            elif line_number == len(lines)-1:
                listings[directory] = [listings[directory],line_number+1]
                listing = False
            break

    return listings


assert find_listings(test_dir1_to_list) == {'/':[2,6]}

 


def extract_listing(lines):
    """ takes in lines of a listing and extracts directory/filenames; 
    saves file sizes to a files dictionary"""

   
    files = {}
    listing = []
 
    for file in lines:
        if file[:3] == 'dir':
            listing.append(file)
        else:
            size, filename = file.split(' ')
            files[filename] = int(size)
            listing.append(filename)
    
    return listing, files



test_dir2 = ['dir xyz', '123 abc']

assert extract_listing(test_dir2) == (['dir xyz', 'abc'], {'abc': 123})

def filesystem(lines):
    """ extract filesystem from given terminal output """
    directories = {}
    file_sizes = {}

    listings = find_listings(lines)
    for directory, linelist in listings.items():
        list_lines = lines[linelist[0]:linelist[1]]
        listing, files = extract_listing(list_lines)
        directories[directory] = listing
        file_sizes.update(files)
   
    return directories, file_sizes


assert filesystem(test_dir1_to_list) == ({'/':['dir a', 'b.txt', 'c.dat', 'dir d']}, {'b.txt':14848514, 'c.dat': 8504156})
assert filesystem(test_data_to_list)[0] ==  {'/':['dir a', 'b.txt', 'c.dat', 'dir d'],
                                             'a':['dir e', 'f', 'g', 'h.lst'],
                                             'e':['i'],
                                             'd':['j', 'd.log', 'd.ext', 'k']}



""" find directory sizes """

def directory_size(listing, files):
        size = 0
        for file in listing:
            size += files[file]
        return size

def parent_directory_size(directories, listing, files, size = 0): #NEEDS EDITING
    files_listing = [file for file in listing if 'dir' not in file]
    dir_listing = [file[4:] for file in listing if 'dir' in file]
    size += directory_size(files_listing,files)
    #print(f'I have added the files {files_listing}. Size is now {size}')
    if dir_listing == []:
        #print(f'Nothing further to add in this directory, size is {size}')
        return size
    else:
        for dir in dir_listing:
            listing = directories[dir]
            size = parent_directory_size(directories, listing, files, size)    
    return size


def get_sizes(directories,files):
    directory_sizes = {}
    for directory, listing in directories.items():
        #print(f"INITIATING DIRECTORY {directory}")
        directory_sizes[directory] = parent_directory_size(directories, listing, files)
        #print(f"DIRECTORY {directory} IS COMPLETE")
    return directory_sizes


""" find possible deletions """

def small_directories(directories, files):
    """ given a  list of directories, create a list of the small directories """
    small_directories = {}
    directory_sizes = get_sizes(directories,files)
    for directory in directories.keys():
        if directory_sizes[directory] > 100000:
            pass
        else:
            small_directories[directory] = directory_sizes[directory]

    return small_directories
          
    
def sum_of_sizes(directory_sizes):
    return sum(directory_sizes.values())


def possible_deletions(lines):
    directories, files = filesystem(lines)
    small = small_directories(directories,files)
    return sum_of_sizes(small)



assert possible_deletions(test_dir3_to_list) == 0

assert possible_deletions(test_data_to_list) == test_result

directories_4, files_4 = filesystem(test_dir4_to_list)
assert get_sizes(directories_4,files_4) == {'lpswsp': 173180}



with open('../input_data/07_No_Space_Left_On_Device.txt', 'r', encoding="utf-8") as file:
    input = file.read().strip().split('\n')

#answer_1 = possible_deletions(input)   

#print(answer_1)


    

