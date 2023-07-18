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

test_result = 95437




def find_listings(lines):
    """ takes in lines from terminal output and finds the start of a listing,
     returns the lines of that listing and the name of the outer directory """
    listings = {}
    listing = False
    for line_number, line in enumerate(lines):
        while not listing: 
            if line == '$ ls':
                directory = lines[line_number-1][-1:]
                listings[directory] = line_number+1
                listing = True
            break
        while listing:
            if line[:4] == '$ cd':
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




def filesystem(lines):
    """ extract filesystem from given terminal output """
    directories = {}
    file_sizes = {}

    listings = find_listings(lines)
    for directory, linelist in listings.items():

        lines = lines[linelist[0]:linelist[1]]
        listing, files = extract_listing(lines)

        directories[directory] = listing
        file_sizes.update(files)

    return directories, files
    

assert filesystem(test_dir1_to_list) == ({'/':['dir a', 'b.txt', 'c.dat', 'dir d']}, {'b.txt':14848514, 'c.dat': 8504156})



def directory_sizes(directories, files):
    pass

