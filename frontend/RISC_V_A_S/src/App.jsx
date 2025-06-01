import { useState, useEffect } from "react";
import "./index.css";
import RegistersTable from "./components/RegistersTable";
import MemoryTable from "./components/MemoryTable";
import Stepper from "./components/Stepper";
import About from "./components/About";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:5000";

function parseSteps(simOutput) {
  // Split output into steps by Program Counter
  const stepBlocks = simOutput.split(/Program Counter:- /g).slice(1);
  // Find all memory stats blocks
  const memBlocks = simOutput.split("Data Memory stats :-");
  // The last block is the final memory, others (if any) are per step
  let memStatsPerStep = [];
  if (memBlocks.length > 1) {
    // Try to match memory stats after each register print
    // This assumes that if memory stats are printed after each instruction, they appear in order
    memStatsPerStep = memBlocks
      .slice(1, stepBlocks.length + 1)
      .map((memBlock) => {
        return memBlock
          .trim()
          .split(/\r?\n/)
          .filter(Boolean)
          .map((line) => {
            const [address, value] = line.split(":");
            return { address: address?.trim(), value: value?.trim() };
          });
      });
  }
  return stepBlocks.map((block, idx) => {
    const [pcLine, ...rest] = block.split("\n");
    const pc = pcLine.trim();
    const regBlock = block.match(/Register values:: \[([^\]]*)\]/);
    let registers = [];
    if (regBlock) {
      const regPairs = regBlock[1]
        .trim()
        .split(/\}\s*\{/)
        .map((s) => s.replace(/[\{\}]/g, "").trim());
      registers = regPairs.filter(Boolean).map((pair) => {
        const [name, value] = pair.split(":");
        return { name: name?.trim(), value: value?.trim() };
      });
    }
    // Attach memory stats for this step if available
    const memory = memStatsPerStep[idx] || [];
    return { pc, registers, memory, raw: block };
  });
}

function parseMemory(simOutput) {
  // Extract memory stats from simOutput (final state)
  const memBlock = simOutput.split("Data Memory stats :-")[1];
  if (!memBlock) return [];
  return memBlock
    .trim()
    .split(/\r?\n/)
    .filter(Boolean)
    .map((line) => {
      const [address, value] = line.split(":");
      return { address: address?.trim(), value: value?.trim() };
    });
}

function App() {
  const [code, setCode] = useState("");
  const [machineCode, setMachineCode] = useState("");
  const [simOutput, setSimOutput] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [stepIdx, setStepIdx] = useState(0);
  const [showAbout, setShowAbout] = useState(false);
  const [darkMode, setDarkMode] = useState(
    () => localStorage.getItem("rvasm_darkmode") === "true"
  );

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("rvasm_darkmode", darkMode);
  }, [darkMode]);

  const assemble = async () => {
    setError("");
    setMachineCode("");
    setSimOutput("");
    setStepIdx(0);
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/assemble`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await res.json();
      if (res.ok) setMachineCode(data.machine_code);
      else setError(data.error || "Assembly failed");
    } catch (e) {
      setError("Could not connect to backend.");
    }
    setLoading(false);
  };

  const simulate = async () => {
    setError("");
    setSimOutput("");
    setStepIdx(0);
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/simulate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ machine_code: machineCode }),
      });
      const data = await res.json();
      if (res.ok) setSimOutput(data.sim_output);
      else setError(data.error || "Simulation failed");
    } catch (e) {
      setError("Could not connect to backend.");
    }
    setLoading(false);
  };

  const steps = simOutput ? parseSteps(simOutput) : [];
  const memory = simOutput ? parseMemory(simOutput) : [];
  const currentStep = steps[stepIdx] || null;

  return (
    <div
      className={`min-h-screen flex flex-col items-center py-8 px-4 transition-colors duration-300 ${
        darkMode ? "bg-slate-900" : "bg-gradient-to-br from-sky-100 to-cyan-100"
      }`}
    >
      <nav className="w-full max-w-7xl flex justify-between items-center mb-8 px-4">
        <h1
          className={`text-3xl font-bold tracking-tight ${
            darkMode ? "text-sky-400" : "text-sky-700"
          } drop-shadow-sm`}
        >
          RISC-V Assembler & Simulator
        </h1>
        <div className="flex items-center gap-3">
          <button
            className={`font-semibold px-4 py-2 rounded-lg transition-all duration-200 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 ${
              darkMode
                ? "bg-sky-600 hover:bg-sky-500 text-white focus:ring-sky-400"
                : "bg-white hover:bg-sky-50 text-sky-700 focus:ring-sky-600 border border-sky-200"
            }`}
            onClick={() => setShowAbout((a) => !a)}
          >
            {showAbout ? "Back to Simulator" : "About"}
          </button>
          <button
            className={`p-2 rounded-full transition-all duration-200 ease-in-out shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-offset-2 ${
              darkMode
                ? "bg-slate-700 hover:bg-slate-600 text-yellow-400 focus:ring-yellow-400"
                : "bg-white hover:bg-slate-100 text-slate-700 focus:ring-slate-600"
            }`}
            onClick={() => setDarkMode((d) => !d)}
            title="Toggle dark mode"
          >
            {darkMode ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 3v1m0 16v1m8.66-15.66l-.707.707M4.04 19.96l-.707.707M21 12h-1M4 12H3m15.66 8.66l-.707-.707M4.04 4.04l-.707-.707"
                />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
                />
              </svg>
            )}
          </button>
        </div>
      </nav>

      {showAbout ? (
        <About />
      ) : (
        <>
          <div
            className={`w-full max-w-5xl ${
              darkMode ? "bg-slate-800" : "bg-white"
            } rounded-xl shadow-2xl p-8 mb-10 flex flex-col gap-6 transition-colors duration-300`}
          >
            <label
              htmlFor="editor"
              className={`block font-semibold mb-1 text-lg ${
                darkMode ? "text-sky-300" : "text-slate-700"
              }`}
            >
              Assembly Code Editor:
            </label>
            <div className="relative group">
              <textarea
                id="editor"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                rows={12}
                className={`w-full font-mono text-sm p-4 border ${
                  darkMode
                    ? "border-slate-700 bg-slate-900 text-slate-200 focus:ring-sky-500 placeholder-slate-500"
                    : "border-slate-300 bg-slate-50 text-slate-800 focus:ring-sky-500 placeholder-slate-400"
                } rounded-lg focus:outline-none focus:ring-2 resize-y transition-colors duration-300 shadow-inner`}
                placeholder={`Enter your RISC-V assembly code here...
Example:
  addi x1, x0, 5
  add x2, x1, x1

Note: Assembly code must end with 'beq zero, zero, 0' (virtual halt).`}
              />
              <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <button
                  onClick={() => setCode("")}
                  className={`px-2 py-1 text-xs ${
                    darkMode
                      ? "bg-slate-700 hover:bg-slate-600 text-slate-300"
                      : "bg-slate-200 hover:bg-slate-300 text-slate-700"
                  } rounded`}
                >
                  Clear
                </button>
              </div>
            </div>
            <div className="flex flex-wrap gap-4 items-center">
              <button
                onClick={assemble}
                className={`font-bold py-2.5 px-8 rounded-lg shadow-md hover:shadow-lg disabled:opacity-60 transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                  darkMode
                    ? "bg-sky-600 hover:bg-sky-500 text-white focus:ring-sky-400"
                    : "bg-sky-600 hover:bg-sky-700 text-white focus:ring-sky-500"
                }`}
                disabled={loading || !code}
              >
                {loading ? "Assembling..." : "Assemble"}
              </button>
              <button
                onClick={simulate}
                className={`font-bold py-2.5 px-8 rounded-lg shadow-md hover:shadow-lg disabled:opacity-60 transition-all duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-offset-2 ${
                  darkMode
                    ? "bg-emerald-600 hover:bg-emerald-500 text-white focus:ring-emerald-400"
                    : "bg-emerald-500 hover:bg-emerald-600 text-white focus:ring-emerald-500"
                }`}
                disabled={!machineCode || loading}
              >
                {loading ? "Simulating..." : "Simulate"}
              </button>
              {error && (
                <div
                  className={`w-full flex items-center gap-2 mt-4 p-3 rounded-lg border text-sm font-semibold shadow-md bg-gradient-to-r from-red-100 to-red-50 border-red-300 text-red-700 dark:from-red-900 dark:to-slate-900 dark:border-red-700 dark:text-red-300`}
                  role="alert"
                  style={{ minHeight: "48px" }}
                >
                  <svg
                    className="w-5 h-5 flex-shrink-0 mr-2"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M12 9v2m0 4h.01M21 12A9 9 0 113 12a9 9 0 0118 0z"
                    />
                  </svg>
                  <span>{error}</span>
                </div>
              )}
            </div>
          </div>

          <div className="w-full max-w-7xl grid grid-cols-1 lg:grid-cols-2 gap-8 px-4">
            <div
              className={`${
                darkMode ? "bg-slate-800" : "bg-white"
              } rounded-xl shadow-xl p-6 flex flex-col transition-colors duration-300`}
            >
              <h2
                className={`text-xl font-semibold ${
                  darkMode ? "text-sky-400" : "text-sky-700"
                } mb-4 border-b ${
                  darkMode ? "border-slate-700" : "border-slate-200"
                } pb-2`}
              >
                Machine Code Output
              </h2>
              <pre
                className={`${
                  darkMode
                    ? "bg-slate-900 text-slate-300"
                    : "bg-slate-100 text-slate-700"
                } rounded-lg p-4 min-h-[150px] overflow-x-auto whitespace-pre-wrap text-xs font-mono shadow-inner flex-grow`}
              >
                {machineCode || "Machine code will appear here after assembly."}
              </pre>
            </div>

            <div
              className={`${
                darkMode ? "bg-slate-800" : "bg-white"
              } rounded-xl shadow-xl p-6 flex flex-col transition-colors duration-300`}
            >
              <h2
                className={`text-xl font-semibold ${
                  darkMode ? "text-emerald-400" : "text-emerald-700"
                } mb-4 border-b ${
                  darkMode ? "border-slate-700" : "border-slate-200"
                } pb-2`}
              >
                Simulation Output
              </h2>
              {steps.length > 0 && currentStep ? (
                <>
                  <Stepper
                    stepIdx={stepIdx}
                    setStepIdx={setStepIdx}
                    steps={steps}
                    darkMode={darkMode}
                  />
                  <div className="mt-4">
                    <div
                      className={`mb-3 flex items-center justify-between p-2 rounded-md ${
                        darkMode ? "bg-slate-700" : "bg-slate-100"
                      } shadow-sm`}
                    >
                      <span
                        className={`font-semibold ${
                          darkMode ? "text-slate-300" : "text-slate-600"
                        } text-sm`}
                      >
                        Program Counter:
                      </span>
                      <span
                        className={`ml-2 ${
                          darkMode
                            ? "bg-sky-700 text-sky-200"
                            : "bg-sky-100 text-sky-800"
                        } px-2.5 py-1 rounded-md text-xs font-mono shadow-inner`}
                      >
                        {currentStep.pc}
                      </span>
                    </div>
                    <RegistersTable
                      registers={currentStep.registers}
                      darkMode={darkMode}
                    />
                    {currentStep.memory && currentStep.memory.length > 0 && (
                      <MemoryTable
                        memory={currentStep.memory}
                        title="Memory (Current Step):"
                        darkMode={darkMode}
                      />
                    )}
                  </div>
                </>
              ) : (
                <pre
                  className={`${
                    darkMode
                      ? "bg-slate-900 text-slate-400"
                      : "bg-slate-100 text-slate-500"
                  } rounded-lg p-4 min-h-[150px] overflow-x-auto whitespace-pre-wrap text-sm font-mono shadow-inner flex-grow flex items-center justify-center`}
                >
                  {simOutput === ""
                    ? "Simulation output will appear here."
                    : "No steps to display. Assemble and simulate code."}
                </pre>
              )}
            </div>
          </div>

          {memory.length > 0 && (
            <div
              className={`w-full max-w-7xl mt-8 px-4 ${
                steps.length > 0 && currentStep ? "" : "hidden"
              }`}
            >
              <MemoryTable
                memory={memory}
                title="Memory (Final State):"
                darkMode={darkMode}
              />
            </div>
          )}
        </>
      )}
      <footer
        className={`mt-16 text-xs ${
          darkMode ? "text-slate-500" : "text-slate-400"
        }`}
      >
        &copy; {new Date().getFullYear()} RISC-V Assembler & Simulator. Crafted
        with ❤️ by Devan.
        <a
          href="https://github.com/devan191/RISCV-Assembler-Simulator"
          target="_blank"
          rel="noopener noreferrer"
          className={`ml-2 ${
            darkMode ? "hover:text-sky-400" : "hover:text-sky-600"
          }`}
        >
          View on GitHub
        </a>
      </footer>
    </div>
  );
}

export default App;
