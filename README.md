# Laboratory 4 - Regular Expression and Finite Automata

This repository contains the solution to Laboratory 4 of the "Ingeniería en Ciencia de la Computación y Tecnologías de la Información" course at Universidad del Valle de Guatemala.

## Overview

This laboratory focuses on implementing a solution for regular expression handling and finite automata using the concepts of Thompson's construction algorithm. The solution consists of two main exercises:

1. **Exercise 1:** Construction of a Non-deterministic Finite Automaton (NFA) using Thompson's algorithm and simulating its operation to recognize strings belonging to the regular expression's language.
2. **Exercise 2:** Demonstrating that a given language is not regular using the Pumping Lemma.

## Project Structure

- **`main.py`:** The main entry point of the application, where the program processes input regular expressions and strings, constructs the corresponding NFA, and simulates the NFA to determine if the strings are part of the language.
- **`input.txt`:** A text file containing the list of regular expressions to be processed by the program.
- **`README.md`:** This file, containing instructions and information about the repository.
- **`astnode.py`:** A Python file that contains the class definitions for AstNode.
- **`main.py`:** Entry file in Python.
- **`nfa_results/`:** A directory containing the graphical representation of the NFA for each regular expression.

## Running the Program

1. **Run the program:**

   ```bash
   python main.py
