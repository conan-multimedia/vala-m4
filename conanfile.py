from conans import ConanFile, CMake, tools
import os

class Valam4Conan(ConanFile):
    name = "vala-m4"
    version = "0.35.2"
    description = "Vala is a programming language using modern high level abstractions without imposing additional"
    " runtime requirements and without using a different ABI compared to applications and libraries written in C"
    url = "https://github.com/conan-multimedia/vala-m4"
    homepage = "https://wiki.gnome.org/Projects/Vala/"
    m4_wiki = "http://www.gnu.org/software/m4/m4.html"
    license = "LGPLv2_1Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"

    source_subfolder = "source_subfolder"

    def source(self):
        maj_ver = '.'.join(self.version.split('.')[0:2])
        tarball_name = 'vala-{version}.tar'.format(version=self.version)
        archive_name = '%s.xz' % tarball_name
        url_ = 'http://ftp.gnome.org/pub/GNOME/sources/vala/{0}/{1}'.format(maj_ver, archive_name)
        tools.download(url_, archive_name)
        
        if self.settings.os == 'Windows':
            self.run('7z x %s' % archive_name)
            self.run('7z x %s' % tarball_name)
            os.unlink(tarball_name)
        else:
            self.run('tar -xJf %s' % archive_name)
        os.rename('vala-%s'%(self.version) , self.source_subfolder)
        os.unlink(archive_name)

    def build(self):
        pass

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("vapigen.m4", src="%s/vapigen"%(os.getcwd()), dst="share/aclocal")
                self.copy("vala.m4", src="%s"%(os.getcwd()), dst="share/aclocal")
                self.copy("Makefile.vapigen", src="%s/vapigen"%(os.getcwd()), dst="share/vala")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

