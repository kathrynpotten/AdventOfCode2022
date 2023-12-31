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


#test_dir1 = """$ cd /
#$ ls
#dir a
#14848514 b.txt
#8504156 c.dat
#dir d"""

#test_dir1_to_list = test_dir1.strip().split('\n')

#test_dir3 = """$ cd /
#$ ls
#14848514 b.txt
#8504156 c.dat
#$ cd a"""

#test_dir3_to_list = test_dir3.strip().split('\n')
#test_dir3_size = 23352670

#test_dir4 = """$ cd lpswsp
#$ ls
#173180 dcqnblb"""
#test_dir4_to_list = test_dir4.strip().split('\n')

#test_dir5 = """$ cd /
#$ ls
#dir a
#14848514 b.txt
#8504156 c.dat
#dir d
#$ cd a
#$ ls
#29116 f
#2557 g
#62596 h.lst""".strip().split('\n')

#test_dir6 = """$ cd /
#$ ls
#dir a
#14848514 b.txt
#8504156 c.dat
#dir d
#$ cd a
#$ ls
#dir e
#29116 f
#2557 g
#62596 h.lst
#$ cd e
#$ ls
#584 i
#$ cd ..""".strip().split('\n')"""



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

    def __del__(self):
        return 'File deleted'
    
    def __len__(self):
        return len(self.path)

    def layers(self):
        c = Counter(self.path)
        return c['/']
    
    def bottom_level_directory(self):
        dir = self.path.split('/')[-2]
        return '/' if dir == '' else dir
    



class Directory(File):

    """ Directories are defined as a type of file that can contain other files """

    filetype = 'dir'

    def __init__(self, path, files = []):
        super().__init__(path)
        self.name = self.path.split('/')[-2] 
        self.files = files
        for file in self.files:
            self.size += file.size
        self.directories = [file for file in self.files
                            if isinstance(file, Directory)]

    def contents(self):
        contents = self.files
        for dir in self.directories:
            for file in dir.files:
                contents.append(file)
        contents = sorted(set(contents))
        print('\n'.join(str(file) for file in contents))
        return contents


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
        
    def bottom_level_directory(self):
        dir = self.path.split('/')[-3]
        return '/' if dir == '' else dir

    

        

class FileSystem():

    """ Top level file system. Contains list of all files in a system  """

    def __init__(self, files=[], max_size = 70000000):
        self.files = sorted(set(files))
        self.max_size = max_size
        self.size = (sum([file.size for file in self.files]))
        self.directories = [file for file in self.files
                            if isinstance(file, Directory)]
        

    def __str__(self):
        return '\n'.join(str(file) for file in self.all_files())
    

    def all_files(self):
        all_files = self.files
        for dir in self.directories:
            for file in dir.files:
                all_files.append(file)
        return sorted(set(all_files))


    def unused_space(self):
        return self.max_size - self.size
    
    def small_dirs(self, max_size = 100000):
        small_directories = []
        total_size = 0
        for dir in self.directories:
            if dir.size > max_size:
                pass
            else:
                small_directories.append(dir.name)
                total_size += dir.size
        
        return small_directories, total_size
    




""" end of class definition """








""" with classes defined  """


def populate_directory(directory, files):
    added = []
    for file in files:
        if file.bottom_level_directory() == directory.name:
            directory.add_file(file)
            added.append(file)

    return directory, added


def parse_terminal_output(lines):

    """ takes in lines from terminal output and converts into a filesystem"""
    
    current_directory = ''
    files = []
    
    #parse lines to output all files in system
    for line in lines:
        words = line.strip().split()
        if words[0] == '$':
            if words[1] == 'cd': 
                if words[2] == '..':
                    current_directory,_,_ = current_directory.rpartition('/')
                elif words[2] != '/':
                    current_directory += '/' + words[2]
                    path = current_directory + '/.'
                    files.append(Directory(path))
            continue
        elif words[0] != 'dir':
            path = current_directory + '/' + words[1]
            files.append(File(path,int(words[0])))

    # separate directories from non-directories
    dirs = [file for file  in files if isinstance(file, Directory)]
    # remove top-level directories from files
    for dir in dirs:
        if dir.bottom_level_directory() == '/':
            files.remove(dir)
    dirs.sort(key=len, reverse=True)
    
    
    #populate directories and remove files added to directories from the files list
    for dir in dirs:
        dir, added_files = populate_directory(dir, files)
        files = [file for file in files if file not in added_files]

    all_files = files + dirs


    return FileSystem(all_files)
            


test_filesystem = parse_terminal_output(test_data_to_list)
#print(test_filesystem)

#assert test_filesystem.small_dirs()[1] == test_result
   

"""
with open('../input_data/07_No_Space_Left_On_Device.txt', 'r', encoding="utf-8") as file:
    input = file.read().strip().split('\n')

answer_filesystem = parse_terminal_output(input)

answer_1 = answer_filesystem.small_dirs()[1]
print(answer_1) """


    
















    

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


#assert find_listings(test_dir1_to_list) == {'/':[2,6]}

 


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


#assert filesystem(test_dir1_to_list) == ({'/':['dir a', 'b.txt', 'c.dat', 'dir d']}, {'b.txt':14848514, 'c.dat': 8504156})
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



#assert possible_deletions(test_dir3_to_list) == 0

assert possible_deletions(test_data_to_list) == test_result

#directories_4, files_4 = filesystem(test_dir4_to_list)
#assert get_sizes(directories_4,files_4) == {'lpswsp': 173180}




"""
with open('../input_data/07_No_Space_Left_On_Device.txt', 'r', encoding="utf-8") as file:
    input = file.read().strip().split('\n')

answer_1 = possible_deletions(input)  
print(answer_1) """


    

