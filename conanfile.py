from conans import ConanFile, CMake, tools


class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "3.3.3"
    description = "Recipe for ffmpeg library"
    license = "MIT/X Consortium license. Check file COPYING of the library"
    url = "https://github.com/vtpl1/conan-ffmpeg"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone --depth 1 --branch release/3.3 https://github.com/FFmpeg/FFmpeg.git")
        self.run("cd FFmpeg")

    def build(self):

        self.run('cmake hello %s' % cmake.command_line)
        self.run("./configure --pkg-config-flags="--static" --extra-cflags="-I$HOME/ffmpeg_build/include" 
                 --extra-ldflags="-L$HOME/ffmpeg_build/lib"
                 --bindir="$HOME/bin"
                 --enable-gpl
                 --enable-libass
                 --enable-libfdk-aac
                 --enable-libfreetype
                 --enable-libtheora                 
                 --enable-nonfree")

    def package(self):
        self.copy("*.h", dst="include", src="ffmpeg")
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ffmpeg"]
