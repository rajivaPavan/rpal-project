#include <iostream>
#include "lexer.h"
#include "parser.h"

using namespace std;

int main(int argc, const char** argv) {

    // Create a Lexer instance
    Lexer lexer;

    // Call the tokenize method
    lexer.tokenize(/* parameters */);

    // Create a Parser instance
    Parser parser;

    // Call the parse method
    parser.parse(/* parameters */);

    return 0;
}