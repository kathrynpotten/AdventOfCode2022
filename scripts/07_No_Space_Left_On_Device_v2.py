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
""".strip().split('\n')

test_result = 95437


""" define classes """

from collections import Counter

class File():


    def __init__(self, path, size = 0):
        self.size = size
        self.path = path
        self.filetype = 'dir' if path.endswith('.') else 'file'

    def __repr__(self):
        return f'File({self.path!r}, {self.size!r})'

    def __str__(self):
        indent = '  '*self.layers()
        size_descr = f', {self.size}' if self.filetype == 'file' else ''
        return indent + f"- {self.path}, ({self.filetype}{size_descr})"
    
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
    
    def name(self):
        if self.path == '/.':
            return '/'
        name = self.path.removesuffix('/.') if self.filetype == 'dir' else self.path
        _,_,name = name.rpartition('/')
        return name
        

    def layers(self):
        c = Counter(self.path)
        return c['/']-1 if self.filetype == 'dir' else c['/']
    
    def bottom_level_directory(self):
        if self.path == '/.':
            return '/'
        dir = self.path.removesuffix(self.name()+'/.') if self.filetype == 'dir' else self.path.removesuffix(self.name())
        _,_,dir = dir.rpartition('/')
        return dir
    



    

        

class FileSystem():

    """ Top level file system. Contains list of all files in a system  """

    def __init__(self, files=[], max_size = 70000000):
        self.files = sorted(set(files))
        self.max_size = max_size
        self.directories = [file for file in self.files
                            if file.filetype == 'dir']
        
    def __repr__(self):
        return f'FileSystem([{self.files}])'

    def __str__(self):
        return '\n'.join(str(file) for file in self.files)
    
    def __iter__(self):
        return iter(self.files)
    
    def __eq__(self, other):
        return self.files == other.files

    def file_size(self, file):
        if file.filetype == 'file':
            return file.size
        elif file.filetype == 'dir':
            dir = file.path.removesuffix('/.')
            inner_files = [f for f in self.files if f.filetype == 'file' and dir in f.path]
            return sum(self.file_size(file) for file in inner_files)
        
        

    def unused_space(self):
        return self.max_size - self.total_size()
    


    def small_dirs(self, max_size = 100000):
        small_dirs = []
        total_size = 0
        for dir in self.directories:
            size = self.file_size(dir)
            if size > max_size:
                pass
            else:
                small_dirs.append(dir.path.removesuffix('/.'))
                total_size += size
        
        return small_dirs, total_size
    




""" end of class definition """









def parse_terminal_output(lines):

    """ takes in lines from terminal output and converts into a filesystem"""
    
    current_directory = ''
    files = [File('/.')]
    
    for line in lines:
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
            files.append(File(path))
        elif words[0] != 'dir':
            path = current_directory + '/' + words[1]
            files.append(File(path,int(words[0])))


    return FileSystem(files)
            

test_files = FileSystem(
    [
        File("/."),
        File("/a/."),
        File("/a/e/."),
        File("/a/e/i", 584),
        File("/a/f", 29116),
        File("/a/g", 2557),
        File("/a/h.lst", 62596),
        File("/b.txt", 14848514),
        File("/c.dat", 8504156),
        File("/d/."),
        File("/d/j", 4060174),
        File("/d/d.log", 8033020),
        File("/d/d.ext", 5626152),
        File("/d/k", 7214296),
    ]
)

test_filesystem = parse_terminal_output(test_data)

assert test_filesystem == test_files
assert str(test_filesystem) == str(test_files) 


assert test_filesystem.small_dirs() == (['/a', '/a/e'], 95437)
assert test_filesystem.small_dirs()[1] == test_result
   



with open('../input_data/07_No_Space_Left_On_Device.txt', 'r', encoding="utf-8") as file:
    input = file.read().strip().split('\n')

answer_filesystem = parse_terminal_output(input)

answer_1 = answer_filesystem.small_dirs()[1]
print(answer_1)


    

