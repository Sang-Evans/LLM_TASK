"use client";
import { useEffect, useState } from "react";
import { checkHealth, askGemini } from "../lib/api";

export default function Home() {
  const [status, setStatus] = useState("Checking...");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    checkHealth()
      .then((res) => setStatus(res.status))
      .catch(() => setStatus("Backend unavailable"));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setAnswer("");
    try {
      const res = await askGemini(question);
      setAnswer(res.answer);
    } catch (err) {
      setAnswer("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-4">Gemini Q&A</h1>
      <p className="mb-6 text-sm text-gray-600">
        Backend status: <span className="font-semibold">{status}</span>
      </p>
      <form onSubmit={handleSubmit} className="space-y-3 mb-6">
        <textarea
          className="w-full border rounded p-3"
          rows="3"
          placeholder="Ask your question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:bg-gray-400"
        >
          {loading ? "Asking Gemini..." : "Ask"}
        </button>
      </form>
      {answer && (
        <div className="border rounded p-4 bg-gray-50">
          <h2 className="text-lg font-semibold mb-2">Answer:</h2>
          <pre className="whitespace-pre-wrap">{answer}</pre>
        </div>
      )}
    </main>
  );
}
