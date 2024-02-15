# RPAL Project

The objective of this project is to implement a lexical analyzer and a parser for the RPAL language. The lexical analyzer and the parser are implemented in C++.

## Setup 
You can download the source code by running the following command:

```bash
git clone https://github.com/rajivaPavan/rpal-project.git
```

navigate to the project directory by running the following command:

```bash
cd rpal-project
```

## Pre-requisites
### Ubuntu
To run this project on Ubuntu, you will need to have `g++` and `make` installed. (if you already have them installed, you can skip to [Usage](#usage)).

You can install them by following these steps:

1. Open a terminal.

2. Update the package list by running the following command:

```bash
sudo apt update
```
3. Install `g++` and `make` by running the following command:

```bash
sudo apt install g++ make
```

## Usage

To run the project, you will need to navigate to the project directory and run the following commands:

run the following command to create the required directories:
```bash
make clean
mkdir -p obj
```

run the following command to compile the project:
```bash
make
```

This will compile the project and create an executable file called `myrpal`. You can run the executable by running the following command:

```bash
./myrpal
```

## Files and Directories

The project directory contains the following files and directories:

- `myrpal.cpp`: The main file that contains the entry point of the program.
- `lexer.cpp`: The file that contains the implementation of the lexical analyzer.
- `lexer.h`: The header file that contains the declaration of the lexical analyzer.
- `parser.cpp`: The file that contains the implementation of the parser.
- `parser.h`: The header file that contains the declaration of the parser.
- `source.rpal`: The file that contains the source code of the RPAL language.
- `Makefile`: The file that contains the instructions for compiling the project.
