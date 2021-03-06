from conans import ConanFile, tools, VisualStudioBuildEnvironment
from conans.tools import download, unzip
import os
import shutil
class FfmpegConan(ConanFile):
    name = "ffmpeg"
    version = "3.4"
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
        #shutil.move("ffmpeg-3.3", "ffmpeg")
        os.unlink(zip_name)
        
        #self.run("git config --global core.autocrlf false")
        #self.run("git clone --single-branch -b release/3.3 https://github.com/FFmpeg/FFmpeg.git ffmpeg") 
        if self.settings.os=="Linux":
            self.run_bash("chmod +x ffmpeg/configure")
            self.run_bash("find ffmpeg -name '*.sh' -exec chmod +x {} \;");
        
    def build(self):
        with tools.chdir("ffmpeg") :
            configure_cmd = "./configure --enable-cuda --enable-nvenc --enable-cuvid --enable-libnpp --enable-nonfree --enable-pic"
            configure_cmd += " --enable-asm --disable-yasm"
            configure_cmd += " --disable-ffserver --disable-doc"
            configure_cmd += " --disable-bzlib --disable-iconv --disable-zlib"
            configure_cmd += " --extra-cflags=\"-DWIN32_LEAN_AND_MEAN\""
            if self.settings.arch=="x86_64":
                configure_cmd += " --arch=amd64"
            if self.settings.os=="Windows":
                configure_cmd += " --toolchain=msvc"
            if self.settings.build_type == "Debug":
                configure_cmd += " --enable-debug" 
            self.run_bash(configure_cmd)
            if self.settings.os=="Windows":
                self.run_bash("make")
            else:
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
        self.copy("*.exe", dst="bin", src="ffmpeg", keep_path=False)
        self.copy("*.so", dst="lib", src="ffmpeg", keep_path=False)
        self.copy("*.so.*", dst="lib", src="ffmpeg", keep_path=False)
        self.copy("*.a", dst="lib", src="ffmpeg", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = [ "avcodec", "avfilter", "avformat",
                               "avutil", "swresample", "swscale" ]
