interface Props {
  sentiment: { label: string; score: number };
  summary: string;
}

export default function ResultCard({ result }: { result: any }) {
  return (
    <div className="mt-6 bg-gray-50 p-6 rounded-lg border border-gray-200 shadow-md">
      <h2 className="text-2xl font-bold text-indigo-700 mb-2">Analysis Result</h2>
      <p className="text-gray-600">
        <strong>Sentiment:</strong> {result.sentiment?.label} (
        {Number(result.sentiment?.score).toFixed(2)})
      </p>
      <p className="mt-4 text-gray-700 leading-relaxed">
        <strong>Summary:</strong> {result.summary}
      </p>
    </div>
  );
}
