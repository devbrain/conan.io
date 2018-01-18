from conans import ConanFile, CMake, tools
import os

class DemoConan(ConanFile):
    name = "zlib"
    version = "1.2.11"
    ZIP_FOLDER_NAME = "zlib-%s" % version
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    exports_sources = ["CMakeLists.txt"]
    license = "http://www.zlib.net/zlib_license.html"
    description = "A Massively Spiffy Yet Delicately Unobtrusive Compression Library " \
                  "(Also Free, Not to Mention Unencumbered by Patents)"

    def configure(self):
        del self.settings.compiler.libcxx
        settings = "os", "compiler", "build_type", "arch"
        options = {"shared": [True, False]}
        default_options = "shared=False"
        generators = "cmake"

    def source(self):
        source_url = "https://zlib.net/zlib-%s.tar.gz" % self.version
        tools.get(source_url)
        extracted_dir = "zlib-%s" % self.version
        os.rename(extracted_dir, "sources")
        
        tools.replace_in_file("sources/CMakeLists.txt", "project(zlib C)", '''project(zlib C)
include(${CMAKE_BINARY_DIR}/../conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = "product"
        
        cmake.configure(build_folder='build', source_folder='sources')
        cmake.build()
        cmake.install ()

    def package(self):
        product = os.path.join (os.path.join (self.build_folder,"build"), "product")

        self.copy(pattern="*", src=os.path.join (product,"include"), dst="include")
        # Extract the License/s from the header to a file
        with tools.chdir(os.path.join(self.build_folder, "sources")):
            tmp = tools.load("zlib.h")
            license_contents = tmp[2:tmp.find("*/", 1)]
            tools.save("LICENSE", license_contents)

        # Copy the license files
        self.copy("LICENSE", src="sources", dst=".")

        # Copy pc file

        # Copying static and dynamic libs
        if tools.os_info.is_windows:
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", src=os.path.join (product, "bin"), keep_path=False)

                self.copy(pattern="*zlibd.lib", dst="lib", src=os.path.join (product, "lib"), keep_path=False)
                self.copy(pattern="*zlib.lib", dst="lib", src=os.path.join (product, "lib"), keep_path=False)
                self.copy(pattern="*zlib.dll.a", dst="lib", src=os.path.join (product, "lib"), keep_path=False)
            else:
                build_dir=src=os.path.join (product, "lib");
                # MinGW
                self.copy(pattern="libzlibstaticd.a", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="libzlibstatic.a", dst="lib", src=build_dir, keep_path=False)
                # Visual Studio
                self.copy(pattern="zlibstaticd.lib", dst="lib", src=build_dir, keep_path=False)
                self.copy(pattern="zlibstatic.lib", dst="lib", src=build_dir, keep_path=False)

                lib_path = os.path.join(self.package_folder, "lib")
                suffix = "d" if self.settings.build_type == "Debug" else ""
                if self.settings.compiler == "Visual Studio":
                    current_lib = os.path.join(lib_path, "zlibstatic%s.lib" % suffix)
                    os.rename(current_lib, os.path.join(lib_path, "zlib%s.lib" % suffix))
                elif self.settings.compiler == "gcc":
                    current_lib = os.path.join(lib_path, "libzlibstatic.a")
                    os.rename(current_lib, os.path.join(lib_path, "libzlib.a"))
        else:
            build_dir=os.path.join (product, "lib")
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", src=build_dir, keep_path=False)
                else:
                    self.copy(pattern="*.so*", dst="lib", src=build_dir, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=build_dir, keep_path=False)


    def package_info(self):
        if self.settings.os == "Windows":
            self.cpp_info.libs = ['zlib']
            if self.settings.build_type == "Debug" and self.settings.compiler == "Visual Studio":
                self.cpp_info.libs[0] += "d"
        else:
            self.cpp_info.libs = ['z']
