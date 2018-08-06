
import clang.cindex

def print_tree(cursor, indent):
    #print(cursor.displayname)
    print(" " * indent + cursor.displayname + "(" + str(cursor.kind) + ")(" + str(cursor.type.get_size()) + ")")
    for x in cursor.get_children():
        print_tree(x, indent + 1)

def convert_header(header, includes):
    index = clang.cindex.Index.create()
    print(header)
    tu = index.parse(header, ["-x", "c++"])
    print(tu)
    print_tree(tu.cursor, 0)
