
# Compiler
CXX = g++

# Specify the path for the header files
INCLUDE_PATH = include

# Specify the path for the source files
SRC_PATH = src

# Specify the path for the object files
OBJ_PATH = obj

# Specify the flags for the compiler
CXXFLAGS = -I$(INCLUDE_PATH) -Wall

# Find all the .cpp files in the SRC_PATH
SRCS = $(wildcard $(SRC_PATH)/*.cpp)

# Replace .cpp with .o for all source files
OBJS = $(patsubst $(SRC_PATH)/%.cpp,$(OBJ_PATH)/%.o,$(SRCS))

# Specify the output file
TARGET = myrpal

all: $(TARGET)

# Link the object files to create the binary
$(TARGET): $(OBJS) 
	$(CXX) $^ -o $@

# Compile the source files into object files
$(OBJ_PATH)/%.o: $(SRC_PATH)/%.cpp 
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean the object and binary files
clean: 
	rm -f $(OBJ_PATH)/*.o myrpal

.PHONY: all clean
