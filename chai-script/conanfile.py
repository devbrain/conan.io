# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools

class ChaiscriptConan(ConanFile):
    name = 'chaiscript'
    version = '6.1.0'
    description = 'ChaiScript is a scripting language designed specifically for integration with C++. It provides seamless integration with C++ on all levels, including shared_ptr objects, functors and exceptions.'
    url = 'https://github.com/birsoyo/conan-chaiscript'
    homepage = 'http://chaiscript.com'
    author = 'Orhun Birsoy <orhunbirsoy@gmail.com>'

    license = 'BSD-3-Clause License'

    no_copy_source = True

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"

    settings = "os"

    def source(self):
        source_url = 'https://github.com/ChaiScript/ChaiScript'
        tools.get(f'{source_url}/archive/v{self.version}.tar.gz')
        extracted_dir = "ChaiScript" + '-' + self.version
        
        #Rename to "source_folder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def package(self):
        include_folder = os.path.join(self.source_subfolder, 'include')
        self.copy(pattern='LICENSE', dst='license', src=self.source_subfolder)
        self.copy(pattern='*', dst='include', src=include_folder)

    def package_info(self):
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'pthread'])
            self.cpp_info.system_libs.extend(['dl', 'pthread'])
            
    def package_id(self):
        self.info.header_only()
        
