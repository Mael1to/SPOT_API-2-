import React, { useState } from "react";

function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleLogin = async () => {
    const response = await fetch("http://127.0.0.1:8000/login/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    if (response.ok) {
      setMessage(`Bienvenue ${username} !`);
    } else {
      setMessage(data.error || "Échec de la connexion");
    }
  };

  return (
    <div>
      <h2>Connexion</h2>
      <input type="text" placeholder="Nom d'utilisateur" onChange={(e) => setUsername(e.target.value)} />
      <input type="password" placeholder="Mot de passe" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleLogin}>Se connecter</button>
      <p>{message}</p>
    </div>
  );
}

export default App;
