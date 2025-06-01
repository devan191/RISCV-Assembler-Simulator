import React from "react";

function Stepper({ stepIdx, setStepIdx, steps }) {
  return (
    <div className="flex items-center gap-2 mb-4">
      <button
        className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 transition disabled:opacity-50"
        onClick={() => setStepIdx((i) => Math.max(0, i - 1))}
        disabled={stepIdx === 0}
      >
        &#8592; Prev
      </button>
      <span className="font-mono text-sm text-gray-700">
        Step <span className="font-bold">{stepIdx + 1}</span> / {steps.length}
      </span>
      <button
        className="px-3 py-1 bg-gray-200 rounded hover:bg-gray-300 transition disabled:opacity-50"
        onClick={() => setStepIdx((i) => Math.min(steps.length - 1, i + 1))}
        disabled={stepIdx === steps.length - 1}
      >
        Next &#8594;
      </button>
    </div>
  );
}

export default Stepper;
