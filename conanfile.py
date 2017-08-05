from conans import ConanFile, tools, VisualStudioBuildEnvironment
from conans.tools import download, unzip
import os
import shutil

class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "3.3.3"
    description = "Recipe for ffmpeg library"
    license = "MIT/X Consortium license. Check file COPYING of the library"
    url = "https://github.com/vtpl1/conan-ffmpeg"
    settings = {"os": ["Windows", "Linux"], 
                "compiler" : ["Visual Studio", "gcc"], 
                "build_type" : ["Release", "Debug"], 
                "arch" : ["x86", "x86_64"]}
    generators = "cmake"
    
    def run_bash(self, cmd):
        if self.settings.os == "Windows":
            tools.run_in_windows_bash(self, cmd)
        else:
            self.run(cmd)

    def source(self):
        zip_name = "ffmpeg.zip"
        #download("https://codeload.github.com/FFmpeg/FFmpeg/zip/n%s.zip" % self.version, zip_name)
        download("https://github.com/FFmpeg/FFmpeg/archive/n%s.zip" % self.version, zip_name)
        unzip(zip_name)
        shutil.move("FFmpeg-n%s" % self.version, "ffmpeg")
        os.unlink(zip_name)
        if self.settings.os=="Linux":
            self.run_bash("chmod +x ffmpeg/configure")
            self.run_bash("find ffmpeg -name '*.sh' -exec chmod +x {} \;");
        
    def build(self):
        with tools.chdir("ffmpeg") :
            configure_cmd = "./configure --enable-nvenc --enable-pic --enable-cuvid --enable-asm --enable-yasm"
            configure_cmd += " --disable-ffserver --disable-doc"
            configure_cmd += " --disable-bzlib --disable-iconv --disable-zlib"
            if self.settings.os=="Windows":
                configure_cmd += " --toolchain=msvc"
            self.run_bash(configure_cmd)
            self.run_bash("make")
    def package(self):
        self.copy("*.h", dst="include/libavcodec", src="ffmpeg/libavcodec")
        self.copy("*.h", dst="include/libavfilter", src="ffmpeg/libavfilter")
        self.copy("*.h", dst="include/libavformat", src="ffmpeg/libavformat")
        self.copy("*.h", dst="include/libavutil", src="ffmpeg/libavutil")
        self.copy("*.h", dst="include/libavcodec", src="ffmpeg/libavcodec")
        self.copy("*.h", dst="include/libswresample", src="ffmpeg/libswresample")
        self.copy("*.h", dst="include/libswscale", src="ffmpeg/libswscale")
        self.copy("*.lib", dst="lib", src="ffmpeg", keep_path=False)
        self.copy("*-*.dll", dst="bin", src="ffmpeg", keep_path=False)
        self.copy("*.so", dst="lib", src="ffmpeg", keep_path=False)
        self.copy("*.so.*", dst="lib", src="ffmpeg", keep_path=False)
        self.copy("*.a", dst="lib", src="ffmpeg", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [ "avcodec", "avfilter", "avformat",
                               "avutil", "swresample", "swscale" ]
