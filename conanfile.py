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

