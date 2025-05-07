import React from "react";

interface ChatPanelProps {
  resumeIa: string;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ resumeIa }) => {
  if (!resumeIa) return null;

  const lines = resumeIa.split("\n").filter((line) => line.trim() !== "");

  return (
    <div
      style={{
        marginTop: 30,
        padding: "20px",
        backgroundColor: "#fefefe",
        border: "1px solid #ccc",
        borderRadius: "8px",
        maxHeight: "400px",
        overflowY: "auto",
        boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
      }}
    >
      <h4 style={{ color: "#0d4e32", marginBottom: "16px" }}>
        🧠 Résumé d’audit IA
      </h4>

      <div style={{ lineHeight: 1.6, fontSize: "0.95rem", color: "#333" }}>
        {lines.map((line, idx) => (
          <p key={idx} style={{ margin: "8px 0" }}>
            {line.startsWith("1.") ||
            line.startsWith("2.") ||
            line.startsWith("3.") ||
            line.startsWith("4.") ? (
              <strong>{line}</strong>
            ) : (
              line
            )}
          </p>
        ))}
      </div>
    </div>
  );
};

export default ChatPanel;
