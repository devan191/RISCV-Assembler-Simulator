import React from "react";

function RegistersTable({ registers, darkMode }) {
  if (!registers || registers.length === 0) {
    return (
      <div
        className={`mt-4 p-4 rounded-lg ${
          darkMode ? "bg-slate-800" : "bg-slate-50"
        } shadow-inner`}
      >
        <p
          className={`${
            darkMode ? "text-slate-400" : "text-slate-500"
          } text-sm text-center`}
        >
          No register data to display.
        </p>
      </div>
    );
  }
  return (
    <div className="mt-4">
      <h3
        className={`text-md font-semibold ${
          darkMode ? "text-emerald-400" : "text-emerald-600"
        } mb-2`}
      >
        Registers:
      </h3>
      <div
        className={`overflow-x-auto rounded-lg shadow-md ${
          darkMode ? "bg-slate-800" : "bg-white"
        } max-h-72 custom-scrollbar`}
      >
        <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-700">
          <thead className={`${darkMode ? "bg-slate-700" : "bg-slate-100"}`}>
            <tr>
              <th
                scope="col"
                className={`px-4 py-2.5 text-left text-xs font-medium ${
                  darkMode ? "text-slate-300" : "text-slate-500"
                } uppercase tracking-wider`}
              >
                Register
              </th>
              <th
                scope="col"
                className={`px-4 py-2.5 text-left text-xs font-medium ${
                  darkMode ? "text-slate-300" : "text-slate-500"
                } uppercase tracking-wider`}
              >
                Value (Decimal)
              </th>
            </tr>
          </thead>
          <tbody
            className={`${
              darkMode
                ? "bg-slate-800 divide-slate-700"
                : "bg-white divide-slate-200"
            }`}
          >
            {registers.map(({ name, value }, index) => (
              <tr
                key={index}
                className={`${
                  darkMode ? "hover:bg-slate-700" : "hover:bg-slate-50"
                } transition-colors`}
              >
                <td
                  className={`px-4 py-2 whitespace-nowrap text-xs font-mono ${
                    darkMode ? "text-sky-300" : "text-sky-700"
                  }`}
                >
                  {name}
                </td>
                <td
                  className={`px-4 py-2 whitespace-nowrap text-xs font-mono ${
                    darkMode ? "text-slate-300" : "text-slate-700"
                  }`}
                >
                  {value}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default RegistersTable;
