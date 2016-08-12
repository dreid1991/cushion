from distutils.core import setup, Extension

incDirsPy = '/home/daniel/Documents/cushion'.split(';')

module = Extension('Cush',
        sources =  ['/home/daniel/Documents/cushion/python/Sim.cpp'],
        library_dirs = ['/home/daniel/Documents/cushion/build'],
        libraries = ['Cush'],
        include_dirs = incDirsPy,
        runtime_library_dirs = ['/usr/local/lib'],
        extra_compile_args = ' -std=c++11 -fpic '.split()
        )
setup(name='',
        version='9999',
        package_dir={'': '/home/daniel/Documents/cushion/python'},
        ext_modules=[module]
        )
