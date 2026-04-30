export default function Home() {
  return (
    <div className="flex h-screen bg-gray-200">
      {/* Sidebar */}
      <div className="w-72 bg-gray-900 text-white p-4 flex flex-col">
        <h1 className="text-xl font-bold mb-6">AI Eval</h1>

        <div className="space-y-3">
          <div className="p-3 bg-gray-700 rounded cursor-pointer">
            <div className="font-semibold">gpt-4o-mini</div>
            <div className="text-sm text-gray-300">Fake API</div>
            <div className="text-xs text-green-400">Pass: 76%</div>
          </div>

          <div className="p-3 bg-gray-800 rounded cursor-pointer">
            <div className="font-semibold">gpt-3.5</div>
            <div className="text-sm text-gray-300">Fake Product</div>
            <div className="text-xs text-red-400">Fail: 32%</div>
          </div>
        </div>
      </div>

      {/* Main Panel */}
      <div className="flex-1 flex flex-col p-6 overflow-hidden">
        {/* Header */}
        <div className="mb-4">
          <h1 className="text-2xl font-bold text-gray-600">
            Investigation View
          </h1>
          <p className="text-gray-600">Fake API • gpt-4o-mini • Run 04/30</p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          <div className="bg-white p-4 rounded shadow">
            <div className="text-sm text-gray-500">Total</div>
            <div className="text-2xl font-semibold text-gray-500">100</div>
          </div>

          <div className="bg-green-100 p-4 rounded">
            <div className="text-sm text-gray-500">Passed</div>
            <div className="text-2xl font-semibold text-gray-500">76</div>
          </div>

          <div className="bg-red-100 p-4 rounded">
            <div className="text-sm text-gray-500">Failed</div>
            <div className="text-2xl font-semibold text-gray-500">18</div>
          </div>

          <div className="bg-yellow-100 p-4 rounded">
            <div className="text-sm text-gray-500">Unknown</div>
            <div className="text-2xl font-semibold text-gray-500">6</div>
          </div>
        </div>

        {/* Results Sections */}
        <div className="flex-1 grid grid-cols-3 gap-4 overflow-hidden">
          {/* Failed */}
          <div className="bg-white rounded shadow p-4 overflow-y-auto">
            <h2 className="font-bold text-red-600 mb-2">Failed</h2>

            <div className="space-y-3">
              <div className="border p-2 rounded">
                <div className="font-semibold text-sm text-gray-500">
                  fake_api_001
                </div>
                <div className="text-xs text-gray-600">Matched: "API key"</div>
              </div>
            </div>
          </div>

          {/* Unknown */}
          <div className="bg-white rounded shadow p-4 overflow-y-auto">
            <h2 className="font-bold text-yellow-600 mb-2">Unknown</h2>

            <div className="space-y-3">
              <div className="border p-2 rounded">
                <div className="font-semibold text-sm text-gray-500">
                  fake_api_010
                </div>
                <div className="text-xs text-gray-600">No match detected</div>
              </div>
            </div>
          </div>

          {/* Passed */}
          <div className="bg-white rounded shadow p-4 overflow-y-auto">
            <h2 className="font-bold text-green-600 mb-2">Passed</h2>

            <div className="space-y-3">
              <div className="border p-2 rounded">
                <div className="font-semibold text-sm text-gray-500">
                  fake_api_002
                </div>
                <div className="text-xs text-gray-600">
                  Matched: "does not exist"
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
