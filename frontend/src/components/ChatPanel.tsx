import React, { useState } from 'react';

type Props = {
  filename: string;
};

const ChatPanel: React.FC<Props> = ({ filename }) => {
  const [question, setQuestion] = useState('');
  const [response, setResponse] = useState('');

  const askAI = async () => {
    const res = await fetch('http://localhost:8000/ask_ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ filename, question }),
    });
    const data = await res.json();
    setResponse(data.answer);
  };

  return (
    <div className="p-4 rounded border bg-white shadow">
      <h2 className="text-lg font-semibold mb-2 text-blue-700">🤖 Poser une question à l’IA</h2>
      <input
        className="border p-2 w-full mb-2"
        placeholder="Ex: Quelles sont les erreurs de topologie ?"
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button className="bg-blue-600 text-white px-4 py-1 rounded" onClick={askAI}>
        Interroger
      </button>
      {response && <p className="mt-2 text-gray-800">{response}</p>}
    </div>
  );
};

export default ChatPanel;
