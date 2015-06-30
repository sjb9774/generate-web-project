#!/usr/local/bin/python3

if __name__ == "__main__":
    from argparse import ArgumentParser
    import os
    import sys
    parser = ArgumentParser(description='Make a new project.')
    parser.add_argument('name',
                        help='Name to use for the project.',
                        action='store')
    parser.add_argument('--dir',
                        default=os.path.abspath(os.path.curdir) ,
                        help='The directory in which to initialize the project.',
                        action='store')
    parser.add_argument('--flask',
                        required=False,
                        default=True,
                        help='Create a flask app?',
                        action='store_true')
    parser.add_argument('--bootstrap',
                        required=False,
                        default=False,
                        help='Include bootstrap css & js?',
                        action='store_true')

    args = parser.parse_args()
    name = args.name
    given_dir = args.dir
    real_dir = os.path.expanduser(given_dir)

    bootstrap = {'js': '',
                 'css': ''}

    static = {'js': [], 'css': []}

    if args.bootstrap:
        bs_js = 'bootstrap.js'
        bs_css = 'bootstrap.css'
        static_js_libs = {'libs': [bs_js]}
        static_css_libs = {'libs': [bs_css]}
        static['js'].append(static_js_libs)
        static['css'].append(static_css_libs)

    structure = [
                    {
                        name:
                        [
                            {
                                name.replace(' ', '_').replace('-', '_').lower():
                                [
                                    '__init__.py',
                                    'db.py',
                                    'config.py',
                                    'views.py',
                                    'models',
                                    'templates',
                                    {
                                        'static': [static]
                                    }
                                ],
                            },
                            'runserver.py',
                            'README.md',
                            'conf.cfg'
                        ]
                    }
                ]

    def create_dir(dir_struct, path):
        this_path = os.path.dirname(__file__)
        for node in dir_struct:
            if type(node) == str:
                if os.path.exists(path + '/' + node):
                    print('File {fullpath} already exists. Skipping...'.format(fullpath=path+'/'+node))
                    continue

                # has an extension
                if node.split('/')[-1].find('.') != -1:
                    if 'libs' in path.split('/'):
                        # library file
                        with open('{0}/libs/{1}'.format(this_path, node), 'r') as lib_file:
                            with open(path + '/' + node, 'w+') as write_file:
                                write_file.write(''.join(lib_file.readlines()))
                    else:
                        with open('{0}/templates/{1}'.format(this_path, node), 'r') as template:
                            subbed_text = ''.join(template.readlines()).replace('{$name}', name.replace(' ', '_').replace('-', '_').lower())
                        with open(path + '/' + node, 'w+') as write_file:
                            write_file.write(subbed_text)
                else:
                    # it's an empty folder
                    if os.path.exists(path + '/' + node):
                        print('Folder {folder} already exists. Using it...'.format(folder=path+'/'+sub_node))
                    else:
                        os.mkdir(path + '/' + node)
            else:
                # node is a dict
                for sub_node in node:
                    if os.path.exists(path + '/' + sub_node):
                        print('Folder {folder} already exists. Using it...'.format(folder=path+'/'+sub_node))
                    else:
                        os.mkdir(path + '/' + sub_node)
                    create_dir(node[sub_node], path + '/' + sub_node)
    create_dir(structure, real_dir)

class DirNode:

    def __init__(self, node_name, is_dir=False, parent=None, children=None):
        self.name = node_name
        self.is_dir = is_dir
        self.parent = parent
        if children:
            for child in children:
                self.add_child(child)
                child.parent = self

    def add_child(self, node):
        if self.is_dir:
            self.children.append(node)
        else:
            raise ValueError("{} is not a directory".format(self.get_path()))

    def is_root(self):
        return self.parent == None

    def get_path(self):
        path = self.name
        node = self
        while node.parent != None:
            path = node.parent.name + '/' + path
            node = node.parent
        return '/' + path

import os
import sys

class FileThing(DirNode):

    def __init__(self, name, is_dir,
                 parent=None, children=None, rfile=None, wfile=None, content_callback=None):
        super(FileThing, self).__init__(name, is_dir=is_dir, parent=parent, children=children)
        if rfile:
            self.rfile = open(rfile, 'r')
            self.content = self.rfile.readlines()
            self.rfile.close()
            if content_callback:
                self.content = content_callback(self.content)
        else:
            self.rfile = None

        if wfile:
            self.wfile = open(wfile, 'w+')
        else:
            self.wfile = None

    def create(self, overwrite=False):

        if os.path.exists(path) and not overwrite:
            raise IOError('Cannot overwrite existing file "{path}".'.format(path=path))
        else:
            if self.is_dir:
                os.mkdir(path)
            else:
                if self.content:
                    self.wfile.write(content)
