# C++ Development with MSYS2 on Windows

## Overview

This skill provides instructions for C++ development on Windows using MSYS2 and the MinGW-w64 toolchain. Use this when the user requests C++ development, compilation, or when a project requires native C++ build tools.

## Environment Setup

### Launching the MinGW64 Shell

To compile C++ code or run C++ build tools, you MUST launch the proper shell environment:

```powershell
# From PowerShell/CMD, launch MSYS2 MinGW64 shell
msys2_shell.cmd -mingw64
```

**Important:** All C++ compilation commands (g++, gcc, make, cmake) must run inside this shell environment.

### Installing the Toolchain

Inside the MSYS2 shell, install the required packages:

```bash
# Update package database
pacman -Syu

# Install the full MinGW-w64 toolchain
pacman -S mingw-w64-x86_64-toolchain

# Install CMake and Ninja
pacman -S mingw-w64-x86_64-cmake mingw-w64-x86_64-ninja

# Install additional common libraries (as needed)
pacman -S mingw-w64-x86_64-gtest      # Google Test
pacman -S mingw-w64-x86_64-boost      # Boost libraries
pacman -S mingw-w64-x86_64-gflags     # Command-line flags
pacman -S mingw-w64-x86_64-glog       # Google Logging
```

### Verifying Installation

```bash
# Check compiler version
g++ --version

# Check CMake version
cmake --version

# Check make version
make --version
```

## Compilation Workflows

### Single File Compilation

```bash
# Compile a single C++ file
g++ -std=c++17 -O2 -o program.exe source.cpp

# With debugging symbols
g++ -std=c++17 -g -o program.exe source.cpp

# With all warnings enabled
g++ -std=c++17 -Wall -Wextra -pedantic -o program.exe source.cpp
```

### Multi-File Projects

```bash
# Compile multiple source files
g++ -std=c++17 -O2 -o program.exe main.cpp utils.cpp helpers.cpp

# Compile separately and link
g++ -std=c++17 -c main.cpp -o main.o
g++ -std=c++17 -c utils.cpp -o utils.o
g++ -std=c++17 -o program.exe main.o utils.o
```

### Using CMake

For projects with CMakeLists.txt:

```bash
# Create build directory
mkdir build && cd build

# Configure with Ninja generator
cmake -G Ninja -DCMAKE_BUILD_TYPE=Release ..

# Build
cmake --build .

# Or use Ninja directly
ninja
```

### Using Make

For projects with Makefile:

```bash
# Build the project
make

# Build with specific target
make target_name

# Clean build
make clean

# Install (if Makefile has install target)
make install
```

## Common Compiler Flags

| Flag | Description |
|------|-------------|
| `-std=c++11/14/17/20` | C++ standard version |
| `-O0, -O1, -O2, -O3` | Optimization level |
| `-g` | Debugging symbols |
| `-Wall -Wextra` | Enable warnings |
| `-Werror` | Treat warnings as errors |
| `-I/path` | Add include directory |
| `-L/path` | Add library directory |
| `-lname` | Link library (e.g., `-lpthread`) |
| `-o output` | Output filename |
| `-c` | Compile only (no linking) |
| `-DDEFINE` | Define preprocessor macro |

## Running Compiled Programs

```bash
# Run the compiled program
./program.exe

# Or directly
program.exe
```

## Debugging with GDB

```bash
# Compile with debug symbols
g++ -std=c++17 -g -o program.exe source.cpp

# Start debugger
gdb program.exe

# Common GDB commands:
#   break main      - Set breakpoint at main
#   run             - Start program
#   next / step     - Step over / into
#   print var       - Print variable value
#   continue        - Continue execution
#   quit            - Exit debugger
```

## Project Structure Example

```
myproject/
├── src/
│   ├── main.cpp
│   ├── utils.cpp
│   └── utils.h
├── include/
│   └── mylib.h
├── tests/
│   └── test_main.cpp
├── CMakeLists.txt
└── Makefile
```

## Integration with VS Code

When working in VS Code:

1. Ensure MSYS2 is in PATH or configure the terminal
2. Use tasks.json to automate builds
3. Use launch.json for debugging

Example tasks.json:
```json
{
    "version": "2.0.0",
    "tasks": [{
        "label": "C++ Build",
        "type": "shell",
        "command": "g++",
        "args": [
            "-std=c++17",
            "-g",
            "${file}",
            "-o",
            "${fileDirname}/${fileBasenameNoExtension}.exe"
        ],
        "group": "build"
    }]
}
```

## Common Issues

### "g++ is not recognized"
- Ensure you launched `msys2_shell.cmd -mingw64`
- Check that `C:\msys64\mingw64\bin` is in PATH

### "DLL not found" when running exe
- The executable needs mingw DLLs in PATH
- Option 1: Add `C:\msys64\mingw64\bin` to PATH
- Option 2: Use `-static` flag: `g++ -static -o program.exe source.cpp`

### Header not found
- Use `-I` flag to specify include paths
- Example: `g++ -I./include -I./src -o program.exe source.cpp`

### Linker errors
- Ensure all object files are linked
- Link libraries with `-l` flag after source files
- Example: `g++ -o program.exe main.cpp utils.cpp -lpthread`

## When to Use This Skill

Use this skill when:
- User requests C++ compilation or project setup
- A Python package requires building C extensions from source
- Working with native dependencies that need compilation
- Debugging C++ code or analyzing native crashes
- User explicitly mentions C++, MSYS2, MinGW, or g++

Do NOT use this skill for:
- Pure Python projects (use `uv` instead)
- VectorBT or other Python libraries that handle compilation internally
- Numba-jitted code (no manual compilation needed)
