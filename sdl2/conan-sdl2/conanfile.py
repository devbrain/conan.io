from conans import ConanFile, CMake, tools
import os


class Sdl2Conan(ConanFile):
    name = "SDL2"
    version = "2.0.12-1"
    libversion = "2.0.12"
    url = ""
    description = "Simple DirectMedia Layer is a cross-platform development library designed to provide low level " \
                  "access to audio, keyboard, mouse, joystick, and graphics hardware via OpenGL and Direct3D"
    license = "https://hg.libsdl.org/SDL/file/5c8fc26757d7/COPYING.txt"
    exports_sources = ["CMakeLists.txt", "LICENSE"]
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False],
               "pic":   [True, False],
               "with3dnow": [True, False],
               "alsa": [True, False],
               "alsa_shared": [True, False],
               "altivec": [True, False],
               "arts": [True, False],
               "arts_shared": [True, False],
               "assembly": [True, False],
               "assertions": ["auto", "disabled", "release", "enabled", "paranoid" ],
               "clock_gettime": [True, False],
               "directfb_shared": [True, False],
               "directx": [True, False],
               "diskaudio": [True, False],
               "dummyaudio": [True, False],
               "esd": [True, False],
               "esd_shared": [True, False],
               "fusionsound": [True, False],
               "fusionsound_shared": [True, False],
               "gcc_atomics": [True, False],
               "input_tslib": [True, False],
               "jack": [True, False],
               "jack_shared": [True, False],
               "kmsdrm_shared": [True, False],
               "libc": [True, False],
               "libsamplerate": [True, False],
               "libsamplerate_shared": [True, False],
               "mir_shared": [True, False],
               "mmx": [True, False],
               "nas": [True, False],
               "nas_shared": [True, False],
               "oss": [True, False],
               "pthreads": [True, False],
               "pthreads_sem": [True, False],
               "pulseaudio": [True, False],
               "pulseaudio_shared": [True, False],
               "render_d3d": [True, False],
               "rpath": [True, False],
               "sdl_dlopen": [True, False],
               "sdl_static_pic": [True, False],
               "sndio": [True, False],
               "sse": [True, False],
               "sse2": [True, False],
               "sse3": [True, False],
               "ssemath": [True, False],
               "video_cocoa": [True, False],
               "video_directfb": [True, False],
               "video_dummy": [True, False],
               "video_kmsdrm": [True, False],
               "video_mir": [True, False],
               "video_opengl": [True, False],
               "video_opengles": [True, False],
               "video_rpi": [True, False],
               "video_vivante": [True, False],
               "video_vulkan": [True, False],
               "video_wayland": [True, False],
               "video_wayland_qt_touch": [True, False],
               "video_x11": [True, False],
               "video_x11_xcursor": [True, False],
               "video_x11_xinerama": [True, False],
               "video_x11_xinput": [True, False],
               "video_x11_xrandr": [True, False],
               "video_x11_xscrnsaver": [True, False],
               "video_x11_xshape": [True, False],
               "video_x11_xvm": [True, False],
               "wayland_shared": [True, False],
               "x11_shared": [True, False]}
    default_options = ("shared=False",
                       "pic=False",
                       "with3dnow=True",
                       "alsa=True",
                       "alsa_shared=True",
                       "altivec=False",
                       "arts=False",
                       "arts_shared=False",
                       "assembly=True",
                       "assertions=auto",
                       "clock_gettime=False",
                       "directfb_shared=False",
                       "directx=False",
                       "diskaudio=True",
                       "dummyaudio=True",
                       "esd=False",
                       "esd_shared=False",
                       "fusionsound=False",
                       "fusionsound_shared=False",
                       "gcc_atomics=True",
                       "input_tslib=False",
                       "jack=False",
                       "jack_shared=False",
                       "kmsdrm_shared=False",
                       "libc=True",
                       "libsamplerate=False",
                       "libsamplerate_shared=False",
                       "mir_shared=False",
                       "mmx=True",
                       "nas=False",
                       "nas_shared=False",
                       "oss=True",
                       "pthreads=True",
                       "pthreads_sem=True",
                       "pulseaudio=True",
                       "pulseaudio_shared=True",
                       "render_d3d=False",
                       "rpath=True",
                       "sdl_dlopen=True",
                       "sdl_static_pic=False",
                       "sndio=False",
                       "sse=True",
                       "sse2=True",
                       "sse3=True",
                       "ssemath=False",
                       "video_cocoa=False",
                       "video_directfb=False",
                       "video_dummy=True",
                       "video_kmsdrm=False",
                       "video_mir=False",
                       "video_opengl=True",
                       "video_opengles=True",
                       "video_rpi=False",
                       "video_vivante=False",
                       "video_vulkan=False",
                       "video_wayland=False",
                       "video_wayland_qt_touch=False",
                       "video_x11=True",
                       "video_x11_xcursor=True",
                       "video_x11_xinerama=True",
                       "video_x11_xinput=True",
                       "video_x11_xrandr=True",
                       "video_x11_xscrnsaver=True",
                       "video_x11_xshape=True",
                       "video_x11_xvm=True",
                       "wayland_shared=False",
                       "x11_shared=True")
    generators = "cmake"

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://www.libsdl.org/release/SDL2-%s.tar.gz" % self.libversion
        tools.get(source_url)
        extracted_dir = "SDL2-" + self.libversion
        os.rename(extracted_dir, "sources")

    def map_value (self, val) :
        if val == True:
            return "ON"
        return "OFF"

    def build(self):
        tools.replace_in_file(os.path.join('sources', 'CMakeLists.txt'),
                              'install(FILES ${SDL2_BINARY_DIR}/libSDL2${SOPOSTFIX}${SOEXT} DESTINATION "lib${LIB_SUFFIX}")', '')
        cmake = CMake(self)
        env = dict()
        
        if self.options.shared:
            cmake.definitions["SDL_SHARED"] = True;
            cmake.definitions["SDL_STATIC"] = False;
        else:
            cmake.definitions["SDL_SHARED"] = False;
            cmake.definitions["SDL_STATIC"] = True;
            cmake.definitions["FORCE_STATIC_VCRT"] = True;
            cmake.definitions["SDL_STATIC_PIC"] = self.options.pic;
            

        cmake.definitions["3DNOW"] = self.map_value(self.options.with3dnow)
        cmake.definitions["ALSA"] = self.map_value(self.options.alsa)
        cmake.definitions["ALSA_SHARED"] = self.map_value(self.options.alsa_shared)
        cmake.definitions["ALTIVEC"] = self.map_value(self.options.altivec)
        cmake.definitions["ARTS"] = self.map_value(self.options.arts)
        cmake.definitions["ARTS_SHARED"] = self.map_value(self.options.arts_shared)
        cmake.definitions["ASSEMBLY"] = self.map_value(self.options.assembly)
        cmake.definitions["ASSERTIONS"] = self.options.assertions
        cmake.definitions["CLOCK_GETTIME"] = self.map_value(self.options.clock_gettime)
        cmake.definitions["DIRECTFB_SHARED"] = self.map_value(self.options.directfb_shared)
        cmake.definitions["DIRECTX"] = self.map_value(self.options.directx)
        cmake.definitions["DISKAUDIO"] = self.map_value(self.options.diskaudio)
        cmake.definitions["DUMMYAUDIO"] = self.map_value(self.options.dummyaudio)
        cmake.definitions["ESD"] = self.map_value(self.options.esd)
        cmake.definitions["ESD_SHARED"] = self.map_value(self.options.esd_shared)
        cmake.definitions["FUSIONSOUND"] = self.map_value(self.options.fusionsound)
        cmake.definitions["FUSIONSOUND_SHARED"] = self.map_value(self.options.fusionsound_shared)
        cmake.definitions["GCC_ATOMICS"] = self.map_value(self.options.gcc_atomics)
        cmake.definitions["INPUT_TSLIB"] = self.map_value(self.options.input_tslib)
        cmake.definitions["JACK"] = self.map_value(self.options.jack)
        cmake.definitions["JACK_SHARED"] = self.map_value(self.options.jack_shared)
        cmake.definitions["KMSDRM_SHARED"] = self.map_value(self.options.kmsdrm_shared)
        cmake.definitions["LIBC"] = self.map_value(self.options.libc)
        cmake.definitions["LIBSAMPLERATE"] = self.map_value(self.options.libsamplerate)
        cmake.definitions["LIBSAMPLERATE_SHARED"] = self.map_value(self.options.libsamplerate_shared)
        cmake.definitions["MIR_SHARED"] = self.map_value(self.options.mir_shared)
        cmake.definitions["MMX"] = self.map_value(self.options.mmx)
        cmake.definitions["NAS"] = self.map_value(self.options.nas)
        cmake.definitions["NAS_SHARED"] = self.map_value(self.options.nas_shared)
        cmake.definitions["OSS"] = self.map_value(self.options.oss)
        cmake.definitions["PTHREADS"] = self.map_value(self.options.pthreads)
        cmake.definitions["PTHREADS_SEM"] = self.map_value(self.options.pthreads_sem)
        cmake.definitions["PULSEAUDIO"] = self.map_value(self.options.pulseaudio)
        cmake.definitions["PULSEAUDIO_SHARED"] = self.map_value(self.options.pulseaudio_shared)
        cmake.definitions["RENDER_D3D"] = self.map_value(self.options.render_d3d)
        cmake.definitions["RPATH"] = self.map_value(self.options.rpath)
        cmake.definitions["SDL_DLOPEN"] = self.map_value(self.options.sdl_dlopen)
        cmake.definitions["SDL_STATIC_PIC"] = self.map_value(self.options.sdl_static_pic)
        cmake.definitions["SNDIO"] = self.map_value(self.options.sndio)
        cmake.definitions["SSE"] = self.map_value(self.options.sse)
        cmake.definitions["SSE2"] = self.map_value(self.options.sse2)
        cmake.definitions["SSE3"] = self.map_value(self.options.sse3)
        cmake.definitions["SSEMATH"] = self.map_value(self.options.ssemath)
        cmake.definitions["VIDEO_COCOA"] = self.map_value(self.options.video_cocoa)
        cmake.definitions["VIDEO_DIRECTFB"] = self.map_value(self.options.video_directfb)
        cmake.definitions["VIDEO_DUMMY"] = self.map_value(self.options.video_dummy)
        cmake.definitions["VIDEO_KMSDRM"] = self.map_value(self.options.video_kmsdrm)
        cmake.definitions["VIDEO_MIR"] = self.map_value(self.options.video_mir)
        cmake.definitions["VIDEO_OPENGL"] = self.map_value(self.options.video_opengl)
        cmake.definitions["VIDEO_OPENGLES"] = self.map_value(self.options.video_opengles)
        cmake.definitions["VIDEO_RPI"] = self.map_value(self.options.video_rpi)
        cmake.definitions["VIDEO_VIVANTE"] = self.map_value(self.options.video_vivante)
        cmake.definitions["VIDEO_VULKAN"] = self.map_value(self.options.video_vulkan)
        cmake.definitions["VIDEO_WAYLAND"] = self.map_value(self.options.video_wayland)
        cmake.definitions["VIDEO_WAYLAND_QT_TOUCH"] = self.map_value(self.options.video_wayland_qt_touch)
        cmake.definitions["VIDEO_X11"] = self.map_value(self.options.video_x11)
        cmake.definitions["VIDEO_X11_XCURSOR"] = self.map_value(self.options.video_x11_xcursor)
        cmake.definitions["VIDEO_X11_XINERAMA"] = self.map_value(self.options.video_x11_xinerama)
        cmake.definitions["VIDEO_X11_XINPUT"] = self.map_value(self.options.video_x11_xinput)
        cmake.definitions["VIDEO_X11_XRANDR"] = self.map_value(self.options.video_x11_xrandr)
        cmake.definitions["VIDEO_X11_XSCRNSAVER"] = self.map_value(self.options.video_x11_xscrnsaver)
        cmake.definitions["VIDEO_X11_XSHAPE"] = self.map_value(self.options.video_x11_xshape)
        cmake.definitions["VIDEO_X11_XVM"] = self.map_value(self.options.video_x11_xvm)
        cmake.definitions["WAYLAND_SHARED"] = self.map_value(self.options.wayland_shared)
        cmake.definitions["X11_SHARED"] = self.map_value(self.options.x11_shared)

        

        with tools.environment_append(env):
            cmake.configure(build_folder='build', source_folder='sources')
            cmake.build()
            cmake.install()

    def package(self):
        self.copy(pattern="*", src=os.path.join ("build", "lib"),     dst="lib")
        self.copy(pattern="*", src=os.path.join ("build","include"), dst="include")
        self.copy(pattern="*", src=os.path.join ("build","bin"),     dst="bin")
        if self.settings.os == "Windows":
            self.copy (pattern="*.pdb", src=os.path.join ("build", "lib"), dst="lib") 			
        self.copy(pattern="COPYING.txt", src="sources")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.includedirs.append(os.path.join('include', 'SDL2'))
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['dl', 'rt', 'pthread', 'sndio', 'm'])
            if self.options.alsa:
                self.cpp_info.libs.append('asound')
            if self.options.jack:
                self.cpp_info.libs.append('jack')
            if self.options.pulseaudio:
                self.cpp_info.libs.append('pulse')
            if self.options.nas:
                self.cpp_info.libs.append('audio')
            if self.options.esd:
                self.cpp_info.libs.append('esd')
        elif self.settings.os == "Macos":
            frameworks = ['Cocoa', 'Carbon', 'IOKit', 'CoreVideo', 'CoreAudio', 'AudioToolbox', 'ForceFeedback']
            for framework in frameworks:
                self.cpp_info.exelinkflags.append("-framework %s" % framework)
                self.cpp_info.sharedlinkflags = self.cpp_info.exelinkflags
        elif self.settings.os == "Windows":
            self.cpp_info.libs.extend(['imm32', 'winmm', 'version'])

