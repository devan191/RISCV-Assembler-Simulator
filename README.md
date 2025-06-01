# RISC-V Assembler & Simulator

## Overview

This project is a custom-built RISC-V assembler and simulator, designed to translate RISC-V assembly code into machine code and simulate its execution. It provides a hands-on, educational tool for understanding the RISC-V instruction set architecture (ISA). Running live at https://riscv-assembler-simulator.vercel.app/

## Features

- **Assembler**: Converts RISC-V assembly instructions into 32-bit binary machine code, supporting a wide range of instruction types (R, I, S, B, U, J).
- **Simulator**: Executes the generated machine code, emulating register and memory operations, and outputs the state of registers and memory after each instruction.
- **Label Handling**: Supports labels for branching and jumping, with error checking for redefinitions and syntax.
- **Immediate and Register Validation**: Robust error handling for invalid immediates, register names, and instruction formats.
- **Memory Management**: Simulates a stack and data memory, with checks for memory overflows and invalid accesses.
- **Extensible Design**: Modular code structure with clear separation between constants, helpers, error handling, and main logic.
- **Input/Output**: Reads assembly code from `backend/input.txt`, outputs machine code to `backend/output.txt`, and simulates execution from `backend/siminput.txt` to `backend/simoutput.txt`.
- **Modern Web Frontend**: Interactive React-based UI for writing, assembling, and simulating RISC-V code, with step-by-step visualization of registers and memory.

## Project Structure

- `backend/` — All backend logic (Python/Flask):
  - `Assembler.py`: Main assembler logic. Reads assembly, encodes instructions, handles labels, and writes machine code.
  - `Simulator.py`: Main simulator logic. Reads machine code, simulates execution, and prints register/memory state.
  - `constants.py`, `helpers.py`, `errors.py`, `simconstants.py`, `simhelpers.py`: Utility modules for encoding, validation, and simulation.
  - `input.txt`, `output.txt`, `siminput.txt`, `simoutput.txt`: Sample input/output files for assembler and simulator.
- `frontend/` — All frontend logic (React/Vite):
  - `RISC_V_A_S/`: Main React app, with all source, assets, and config files.
    - `src/`: React components, styles, and assets.
    - `public/`: Static assets for the frontend.

## Example Backend Workflow

1. **Write Assembly**: Edit `backend/input.txt` with your RISC-V assembly code.
2. **Assemble**: Run `python backend/Assembler.py` to generate `backend/output.txt` (machine code).
3. **Simulate**: Copy `backend/output.txt` to `backend/siminput.txt` and run `python backend/Simulator.py` to see the execution results in `backend/simoutput.txt`.

## Example Input/Output

**backend/input.txt**

```
addi a0,a1,10
sub a3,a4,a5
addi t0,t1,10
beq a0,t0,label
jal ra,label
label:  beq zero,zero,0
```

**backend/output.txt** (machine code)

```
00000000101001011000010100010011
01000000111101110000011010110011
... (etc)
```

**backend/simoutput.txt** (register/memory state)

```
Program Counter:- 0x00000000
Register values:: [ {zero:0} {ra:0} ... {a0:10} ... ]
... (etc)
```

## Frontend (Web UI)

- The React-based frontend is located in `frontend/RISC_V_A_S/`.
- To run the frontend locally:
  1. Open a terminal in `frontend/RISC_V_A_S/`.
  2. Install dependencies:
     ```
     npm install
     ```
  3. Start the development server:
     ```
     npm run dev
     ```
  4. Open the provided local URL in your browser.
- The web UI allows you to write, assemble, and simulate RISC-V code interactively, with step-by-step visualization of registers and memory.

## Why This Project Stands Out

- **Educational Value**: Demonstrates a deep understanding of computer architecture, binary encoding, and low-level programming.
- **Error Handling**: Proactively checks for common assembly errors, making it robust and user-friendly.
- **Readable and Modular Code**: Clean separation of concerns, making it easy to extend or adapt for new instructions or features.
- **Realistic Simulation**: Mimics actual RISC-V hardware behavior, including stack pointer initialization and memory layout.
- **Modern UI**: Clean, responsive, and interactive web interface for hands-on learning.

## How to Run (Backend)

1. Ensure you have Python 3 installed.
2. Place your assembly code in `backend/input.txt`.
3. Run the assembler:
   ```
   python backend/Assembler.py
   ```
4. Copy `backend/output.txt` to `backend/siminput.txt` (or automate this step).
5. Run the simulator:
   ```
   python backend/Simulator.py
   ```
6. View the results in `backend/simoutput.txt`.

## How to Run (Frontend)

1. Ensure you have Node.js and npm installed.
2. In `frontend/RISC_V_A_S/`, run:
   ```
   npm install
   npm run dev
   ```
3. Open the local URL provided by Vite (usually http://localhost:5173).

## Customization & Extension

- Add new instructions by updating `backend/constants.py` and the relevant encoder/decoder logic.
- Enhance the simulator to support more advanced features (e.g., system calls, more memory operations).
- The frontend is easily extensible for new features, instructions, or UI improvements.

---

For more details, see the code and comments in each module and do check ProbPDF.pdf in backend folder, which contains all the assumptions, encodings and syntax on which this project is built upon. Contributions and suggestions are welcome!
