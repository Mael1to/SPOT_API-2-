import React, { useEffect, useState } from "react";

function Personality() {
  const [personality, setPersonality] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/personality/", {
      headers: { Authorization: "Bearer TON_ACCESS_TOKEN" },
    })
      .then((res) => res.json())
      .then((data) => setPersonality(data));
  }, []);

  return (
    <div>
      <h2>Votre Personnalité Musicale</h2>
      {personality ? (
        <p>Popularité Moyenne : {personality.average_popularity} | Durée Moyenne : {personality.average_duration} sec</p>
      ) : (
        <p>Chargement...</p>
      )}
    </div>
  );
}

export default Personality;
