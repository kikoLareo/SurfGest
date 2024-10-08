import React, { useState } from 'react';

function App() {
  const [hours, setHours] = useState('');
  const [position, setPosition] = useState('');
  const [response, setResponse] = useState(null);

  const positions = [
    "director_competicion",
    "delegado",
    "xefe_xuices_nacional",
    "xefe_xuices_rexional",
    "xuices_nacional",
    "xuices_rexional",
    "infraestructura",
    "speaker"
  ];

  const handleCalculateFee = async () => {
    try {
      const res = await fetch('http://localhost:5001/calculate_fee', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          hours: parseInt(hours),
          position: position,
        }),
      });

      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error al hacer la solicitud:', error);
    }
  };

  return (
    <div className="App">
      <h1>Calculadora de Tarifas de Surf</h1>
      <div>
        <label>
          Horas trabajadas:
          <input
            type="number"
            value={hours}
            onChange={(e) => setHours(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          Puesto:
          <select value={position} onChange={(e) => setPosition(e.target.value)}>
            <option value="">Seleccione un puesto</option>
            {positions.map((pos) => (
              <option key={pos} value={pos}>
                {pos}
              </option>
            ))}
          </select>
        </label>
      </div>
      <button onClick={handleCalculateFee}>Calcular Tarifa</button>
      {response && (
        <div>
          <h2>Resultado:</h2>
          <p>Puesto: {response.position}</p>
          <p>Horas: {response.hours}</p>
          <p>Tarifa después de IRPF: {response.fee_after_irpf} €</p>
        </div>
      )}
    </div>
  );
}

export default App;
