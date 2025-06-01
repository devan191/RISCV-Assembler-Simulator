import React from "react";

function About() {
  return (
    <div className="max-w-3xl mx-auto bg-white rounded-2xl shadow-xl p-8 mt-10 mb-16">
      {/* --- Project Title & Overview --- */}
      <h1 className="text-3xl font-extrabold text-blue-800 mb-4">
        About This Project
      </h1>
      <p className="mb-4 text-gray-700 text-lg">
        <b>RISC-V Assembler & Simulator</b> is an educational tool designed to
        help students and enthusiasts understand the RISC-V instruction set
        architecture (ISA) at a low level. This project allows you to write
        RISC-V assembly code, assemble it into machine code, and simulate its
        execution step-by-step, visualizing how registers and memory change
        after each instruction.
      </p>

      {/* --- Key Features --- */}
      <h2 className="text-xl font-bold text-green-700 mt-6 mb-2">
        Key Features
      </h2>
      <ul className="list-disc ml-8 text-gray-700 mb-4">
        <li>
          Interactive web interface for writing, assembling, and simulating
          RISC-V code
        </li>
        <li>
          Step-by-step visualization of register and memory state after each
          instruction
        </li>
        <li>Support for R, I, S, B, U, and J type instructions</li>
        <li>
          Robust error handling for invalid syntax, registers, and immediates
        </li>
        <li>Label support for branching and jumping</li>
        <li>Realistic simulation of stack and data memory</li>
        <li>Modern, responsive UI built with React, Vite, and Tailwind CSS</li>
      </ul>

      {/* --- How It Works --- */}
      <h2 className="text-xl font-bold text-green-700 mt-6 mb-2">
        How It Works
      </h2>
      <ol className="list-decimal ml-8 text-gray-700 mb-4">
        <li>Write your RISC-V assembly code in the editor.</li>
        <li>
          Click <b>Assemble</b> to convert your code into 32-bit machine code.
        </li>
        <li>
          Click <b>Simulate</b> to execute the code and step through each
          instruction, observing changes in registers and memory.
        </li>
      </ol>

      {/* --- Educational Value --- */}
      <h2 className="text-xl font-bold text-green-700 mt-6 mb-2">
        Educational Value
      </h2>
      <p className="mb-4 text-gray-700">
        This project is inspired by academic coursework focused on hands-on
        learning of computer architecture concepts. By visualizing the effects
        of each instruction, users gain a deeper understanding of how assembly
        code is executed at the hardware level.
      </p>

      {/* --- Project Structure --- */}
      <h2 className="text-xl font-bold text-green-700 mt-6 mb-2">
        Project Structure
      </h2>
      <ul className="list-disc ml-8 text-gray-700 mb-4">
        <li>
          <b>Assembler.py</b>: Converts assembly code to machine code
        </li>
        <li>
          <b>Simulator.py</b>: Simulates execution, updating registers and
          memory
        </li>
        <li>
          <b>Web UI</b>: Modern frontend for code editing, output, and step
          navigation
        </li>
        <li>
          <b>Backend</b>: Python Flask server connecting the UI to the assembler
          and simulator
        </li>
      </ul>

      {/* --- Why Use This Tool? --- */}
      <h2 className="text-xl font-bold text-green-700 mt-6 mb-2">
        Why Use This Tool?
      </h2>
      <ul className="list-disc ml-8 text-gray-700 mb-4">
        <li>
          Perfect for students, educators, and anyone learning RISC-V or
          computer architecture
        </li>
        <li>
          Immediate feedback and visualization of low-level code execution
        </li>
        <li>
          Open source and easily extensible for new instructions or features
        </li>
      </ul>

      {/* --- Register Encoding Section --- */}
      <h2 className="text-xl font-bold text-green-700 mt-8 mb-3">
        Register Encoding
      </h2>
      <p className="mb-4 text-gray-700">
        Below is the standard RISC-V register encoding table, showing addresses,
        register names (x0–x31), their ABI names, and a brief description of
        each register’s purpose. Use this as a reference when writing assembly
        or interpreting machine code.
      </p>
      <div className="flex justify-center mb-6">
        {/* 
          Assuming you place the image file in your public folder as:
          public/register_encoding.png
          Then reference it via "/register_encoding.png" 
        */}
        <img
          src="/register_encoding.png"
          alt="RISC-V Register Encoding Table"
          className="rounded-lg shadow-md max-w-full h-auto"
        />
      </div>
      <p className="text-sm text-gray-500 italic mb-8">
        * Table shows x0–x31, ABI names, and whether the register is caller‐ or
        callee‐saved.
      </p>

      {/* --- Memory Size & Addressing Section --- */}
      <h2 className="text-xl font-bold text-green-700 mt-8 mb-3">
        Memory Size & Addressing
      </h2>
      <p className="mb-4 text-gray-700">
        Our simulator uses fixed-size memory regions. Each location is 32 bits
        wide (4 bytes). Below are the details for Program Memory, Stack Memory,
        and Data Memory:
      </p>
      <div className="space-y-4 ml-4">
        {/* Program Memory */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-1">
            (a) Program Memory
          </h3>
          <ul className="list-disc ml-6 text-gray-700 mb-2">
            <li>
              <b>Size:</b> 256 bytes total (64 words × 4 bytes per word)
            </li>
            <li>
              <b>Address Range:</b> <code>0x0000 0000</code> to{" "}
              <code>0x0000 00FF</code>
            </li>
            <li>
              <b>Description:</b> This space holds up to 64 instructions. Each
              instruction is 32 bits (4 bytes).{" "}
            </li>
          </ul>
        </div>

        {/* Stack Memory */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-1">
            (b) Stack Memory
          </h3>
          <ul className="list-disc ml-6 text-gray-700 mb-2">
            <li>
              <b>Size:</b> 128 bytes total (32 words × 4 bytes per word)
            </li>
            <li>
              <b>Address Range:</b> <code>0x0000 0100</code> to{" "}
              <code>0x0000 017F</code>
            </li>
            <li>
              <b>Description:</b> The stack grows downward. You must decrement
              the stack pointer before storing any register value. This region
              is used for saving registers, function call overhead, and local
              variables.
            </li>
          </ul>
        </div>

        {/* Data Memory */}
        <div>
          <h3 className="text-lg font-semibold text-gray-800 mb-1">
            (c) Data Memory
          </h3>
          <ul className="list-disc ml-6 text-gray-700">
            <li>
              <b>Size:</b> 128 bytes total (32 words × 4 bytes per word)
            </li>
            <li>
              <b>Address Range:</b> <code>0x0001 0000</code> to{" "}
              <code>0x0001 007F</code>
            </li>
            <li>
              <b>Description:</b> Used for static data, global variables, and
              any heap-like usage if needed. Each word is 32 bits wide.
            </li>
          </ul>
        </div>
      </div>

      {/* --- Footer / Attribution --- */}
      <div className="mt-8 text-gray-500 text-sm">
        <b />
        Developed for academic and educational use. Inspired by university‐
        level computer architecture coursework.
      </div>
    </div>
  );
}

export default About;
