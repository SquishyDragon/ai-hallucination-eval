"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [run, setRun] = useState<any>(null);

  useEffect(() => {
    fetch("/latest_results.json")
      .then((res) => res.json())
      .then((data) => setRun(data))
      .catch((err) => console.error("Failed to load results:", err));
  }, []);

  if (!run) {
    return <div className="p-6">Loading results...</div>;
  }

  const normalizedResults = run.results.map((r: any, i: number) => ({
    id: i + 1,
    status: r.Status,
    prompt: r.Prompt,
    response: r.Response,
    passingMatch: r["Passing Match"] || [],
    failingMatch: r["Failing Match"] || [],
    message: r.Message,
  }));


  const passed = normalizedResults.filter((r: any) => r.status === "Pass");
  const failed = normalizedResults.filter((r: any) => r.status === "Fail");
  const unknown = normalizedResults.filter((r: any) => r.status === "Unknown");

  const getMatchText = (r: any) => {
    if (r["Passing Match"]) return r["Passing Match"].join(", ");
    if (r["Failing Match"]) return r["Failing Match"].join(", ");
    return "No match detected";
  };

  return (
    <div className="flex h-screen bg-gray-200">
      <div className="w-72 bg-gray-900 text-white p-4 flex flex-col">
        <h1 className="text-xl font-bold mb-6">AI Eval</h1>

        <div className="space-y-3">
          <div className="p-3 bg-gray-700 rounded cursor-pointer">
            <div className="font-semibold">{run.model}</div>
            {/* <div className="text-sm text-gray-300">{run.category}</div> */}
            <div className="text-xs text-green-400">
              Pass: {run.pass_rate.toFixed(1)}%
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 flex flex-col p-6 overflow-hidden">
        <div className="mb-4">
          <h1 className="text-2xl font-bold text-gray-600">
            Investigation View
          </h1>
          <p className="text-gray-600">
            {/* {run.category} •  */}
            {run.model} • {run.run_id}
          </p>
        </div>

        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded shadow">
            <div className="text-sm text-gray-500">Total</div>
            <div className="text-2xl font-semibold text-gray-500">
              {run.total_tests}
            </div>
          </div>

          <div className="bg-green-100 p-4 rounded">
            <div className="text-sm text-gray-500">Passed</div>
            <div className="text-2xl font-semibold text-gray-500">
              {run.passed}
            </div>
          </div>

          <div className="bg-red-100 p-4 rounded">
            <div className="text-sm text-gray-500">Failed</div>
            <div className="text-2xl font-semibold text-gray-500">
              {run.failed}
            </div>
          </div>

          <div className="bg-yellow-100 p-4 rounded">
            <div className="text-sm text-gray-500">Unknown</div>
            <div className="text-2xl font-semibold text-gray-500">
              {run.unknown}
            </div>
          </div>
        </div>

        <div className="flex-1 grid grid-cols-3 gap-4 overflow-hidden">
          <ResultColumn
            title="Failed"
            titleClass="text-red-600"
            results={failed}
            getMatchText={getMatchText}
            emptyText="No failed tests"
          />

          <ResultColumn
            title="Unknown"
            titleClass="text-yellow-600"
            results={unknown}
            getMatchText={getMatchText}
            emptyText="No unknown tests"
          />

          <ResultColumn
            title="Passed"
            titleClass="text-green-600"
            results={passed}
            getMatchText={getMatchText}
            emptyText="No passed tests"
          />
        </div>
      </div>
    </div>
  );
}

function ResultColumn({
  title,
  titleClass,
  results,
  getMatchText,
  emptyText,
}: any) {
  return (
    <div className="bg-white rounded shadow p-4 overflow-y-auto">
      <h2 className={`font-bold mb-2 ${titleClass}`}>{title}</h2>

      <div className="space-y-3">
        {results.length === 0 && (
          <div className="text-sm text-gray-400">{emptyText}</div>
        )}

        {results.map((r: any, index: number) => (
          <div key={index} className="border p-2 rounded">
            {/* Backend does not currently output test_id */}
            {/* <div className="font-semibold text-sm text-gray-500">{r.id}</div> */}

            <div className="font-semibold text-sm text-gray-500">
              Test {index + 1}
            </div>

            <div className="text-xs text-gray-600">
              Matched: "{getMatchText(r)}"
            </div>

            <div className="text-xs text-gray-400 mt-1 line-clamp-2">
              {r.Prompt}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
