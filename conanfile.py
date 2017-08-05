from conans import ConanFile, CMake, tools


class ExpatConan(ConanFile):
    name = "Expat"
    version = "2.2.1"
    description = "Recipe for Expat library"
    license = "MIT/X Consortium license. Check file COPYING of the library"
    url = "https://github.com/vtpl1/conan-expat"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    exports = ['FindExpat.cmake']

    def source(self):
        self.run("git clone --depth 1 --branch R_2_2_1 https://github.com/libexpat/libexpat")
        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("libexpat/expat/CMakeLists.txt", "project(expat)",
            '''project(expat)
            include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
            conan_basic_setup()''')

    def build(self):
        cmake = CMake(self, parallel=True)

        cmake_args = { "CMAKE_INSTALL_PREFIX" : self.package_folder,
                       "BUILD_doc" : "OFF",
                       "BUILD_examples" : "OFF",
                       "BUILD_shared" : self.options.shared,
                       "BUILD_tests" : "OFF",
                       "BUILD_tools" : "OFF",
                       #"CMAKE_CXX_FLAGS" : "${CMAKE_CXX_FLAGS} -DXML_POOR_ENTROPY"
                     }

        cmake.configure(source_dir="../libexpat/expat", build_dir="build", defs=cmake_args)
        cmake.build(target="install")

    def package(self):
        self.copy("FindExpat.cmake", ".", ".")

    def package_info(self):
        self.cpp_info.debug.libs = ["expatd"]
        self.cpp_info.release.libs = ["expat"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        if not self.options.shared:
            self.cpp_info.defines = ["XML_STATIC"]

    def configure(self):
        del self.settings.compiler.libcxx
