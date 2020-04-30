# conan.io
conan remote add <REMOTE> https://api.bintray.com/conan/devbrain/devbrain

# conan package creation

mkdir mypkg && cd mypkg
conan new hello/0.1 -t

conan create . devbrain/stable --profile gcc

conan upload SDL2/2.0.12@sdl2/stable -r=devbrain

https://bintray.com/devbrain
