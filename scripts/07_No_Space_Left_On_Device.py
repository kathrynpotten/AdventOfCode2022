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




""" define directory classes """
class Directory():

    def __init__(self, name, files=[]):
        self.name = name
        self.files = files

    def __str__(self):
        return f'{self.name}:  {self.files}'
    
    def get_file_sizes(self, files):
        """ grabs file sizes from supplied dictionary """
        self.sizes = {}
        for file in self.files:
            self.sizes[file] = files[file]
        return self.sizes

    def file_size(self,file):
        return self.sizes[file]
    
    def size(self):
        size = 0
        for file in self.files:
            size += self.sizes[file]
        return size
    
    def large(self):
        if self.size() > 100000:
            return True
        else:
            return False


    

class ParentDirectory(Directory):

    def __init__(self,name,files=[]):
        super().__init__(name,files)
    
    def get_file_sizes(self, files):
        """ grabs file sizes from supplied dictionary """
        self.sizes = {}
        for file in self.files:
            if file[:3] == 'dir':
                print("I'm a directory")
                file = file[4:]
                self.sizes[file] = super().size()
            else:
                self.sizes[file] = files[file]
        return self.sizes
    
    def size(self):
        size = 0
        for file in self.files:
            if file[:3] == 'dir':
                size += super().size()
            else:
                size += self.sizes[file]
        return size
                
""" end of class definition """




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
                listings[directory] = [listings[directory],line_number]
                listing = False
            break

    return listings



test_dir1 = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a"""

test_dir1_to_list = test_dir1.strip().split('\n')

assert find_listings(test_dir1_to_list) == {'/':[2,6]}

 


def extract_listing(lines):
    """ takes in lines of a listing and extracts directory/filenames; 
    saves file sizes to a files dictionary"""

    #initiate dictionary which contains list of files and their sizes
    files = {}
    listing = []
 
    for object in lines:
        if object[:3] == 'dir':
            listing.append(object)
        else:
            size, filename = object.split(' ')
            files[filename] = int(size)
            listing.append(filename)
    
    return listing, files



test_dir2 = ['dir xyz', '123 abc']

assert extract_listing(test_dir2) == (['dir xyz', 'abc'], {'abc': 123})




""" with classes defined  """

def convert_to_directories(directory, listing):
    """ given a directory name and list of files, convert into directory objects.
    If a directory contains other directories, make it a parent directory"""
    
    if any('dir' in object for object in listing):
        directory = ParentDirectory(directory, listing)    
    else:
        directory = Directory(directory, listing)
        
    return directory
    


test_files = {'abc': 123, 'j': 10, 'k': 30}
test_dir_xyz_listing = ['j','k']
test_dir_xyz = Directory('xyz',test_dir_xyz_listing)
test_dir_xyz.get_file_sizes(test_files)
#print(test_dir_xyz.sizes)


test_dir_mno = ['dir xyz', 'abc']
test_dir_mno = convert_to_directories('mno',test_dir_mno)
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


test_dir3 = """$ cd /
$ ls
14848514 b.txt
8504156 c.dat
$ cd a"""

test_dir3_to_list = test_dir3.strip().split('\n')



#filesystem(test_dir1_to_list)
#assert filesystem(test_dir3_to_list) == (['/'], {'b.txt':14848514, 'c.dat': 8504156})


#assert filesystem(test_dir1_to_list)[1] == ({'b.txt':14848514, 'c.dat': 8504156})



""" find possible files for deletion """


  
def small_directories(directories):
    """ given a  list of directories, create a list of the small directories """
    small_directories = []
    for directory in directories:
        if directory.large():
            pass
        else:
            small_directories.append(directory)
    return small_directories

def sum_of_sizes(directories):
    sum_of_sizes = 0
    for directory in directories:
        sum_of_sizes += directory.size()
    return sum_of_sizes

def possible_deletions(lines):
    directories, files = filesystem_class(lines)
    small = small_directories(directories)
    return sum_of_sizes(small)



#assert possible_deletions(test_dir3_to_list) == 0

#assert possible_deletions(test_data_to_list) == test_result





    

""" without classes defined """

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




""" find possible files for deletion """

def directory_size(listing, files):
        size = 0
        for file in listing:
            size += files[file]
        return size

def parent_directory_size(directories, listing, files): #NEEDS EDITING TO PROCESS INNER LOOP MULTIPLE TIMES
    size = 0
    files_listing = [file for file in listing if 'dir' not in file]
    dir_listing = [file[4:] for file in listing if 'dir' in file]
    if dir_listing == []:
        return directory_size(files_listing,files)
    else:
        for dir in dir_listing:
            listing = directories[dir]
            size += parent_directory_size(directories, listing, files)      
    return size


def get_sizes(directories,listing,files):
    directory_sizes = {}
    for directory in directories.keys():
        directory_sizes[directory] = parent_directory_size(directories, listing, files)
    return directory_sizes



def small_directories(directories, files):
    """ given a  list of directories, create a list of the small directories """
    small_directories = {}
    for directory,listing in directories.items():
        directory_sizes = get_sizes(directories,listing,files)
        print(directory_sizes)
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


print(possible_deletions(test_data_to_list))


#assert possible_deletions(test_data_to_list) == test_result




with open('../input_data/07_No_Space_Left_On_Device.txt', 'r', encoding="utf-8") as file:
    input = file.read().strip().split('\n')

#answer_1 = possible_deletions(input)   

#print(answer_1)


    

