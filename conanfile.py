from conans import ConanFile, AutoToolsBuildEnvironment, tools


class Exceptions4cConan(ConanFile):
    name = 'exceptions4c'
    version = 'master'
    license = 'LGPL3'
    author = 'Jakub Pieńkowski <jakub@jakski.name>'
    url = 'https://github.com/Jakski/conan-exceptions4c'
    description = 'An exception handling framework for C'
    topics = ('c', 'exceptions')
    settings = 'os', 'compiler', 'build_type', 'arch'
    options = {
        'repo_url': "ANY",
        'thread_safe': [True, False],
    }
    default_options = {
        'repo_url': 'https://github.com/guillermocalvo/exceptions4c.git',
        'thread_safe': True
    }
    _source_subfolder = '.'

    def configure(self):
        del self.settings.compiler.libcxx
        del self.settings.compiler.cppstd

    def source(self):
        self.run(f'git clone --depth 1 --branch {self.version} {self.options.repo_url} {self._source_subfolder}')

    def build(self):
        self.run('autoreconf --install', cwd=self._source_subfolder)
        autotools = AutoToolsBuildEnvironment(self)
        if self.options.thread_safe:
            autotools.defines.append('E4C_THREADSAFE')
        autotools.configure(configure_dir=self._source_subfolder)
        autotools.make()

    def package(self):
        self.copy('*.h', dst='include', src='src')
        self.copy('*.dll', dst='bin', keep_path=False)
        self.copy('*.so', dst='lib', keep_path=False)
        self.copy('*.dylib', dst='lib', keep_path=False)
        self.copy('*.a', dst='lib', keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs = ["pthread"]
        if self.options.thread_safe:
            self.cpp_info.defines = ['E4C_THREADSAFE']
