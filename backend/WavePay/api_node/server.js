const express = require('express');
const cors = require('cors');  // Importa el middleware cors
const app = express();
const port = 5001;

// Configura CORS para permitir cualquier origen (esto es ideal solo para desarrollo)
app.use(cors({ origin: 'http://localhost:3000' }));
  app.options('*', cors());  // Habilitar el manejo de todas las solicitudes preflight

app.use(express.json());  // Middleware para parsear el body como JSON

// Configurar tarifas y gastos
const positionRates = {
  'director_competicion': 189.87,
  'delegado': 143.04,
  'xefe_xuices_nacional': 176.47,
  'xefe_xuices_rexional': 143.04,
  'xuices_nacional': 117.65,
  'xuices_rexional': 94.94,
  'infraestructura': 113.92,
  'speaker': 117.65
};

const irpfRate = 0.15;

// Función para calcular tarifas
function calculateFee(hours, position) {
  if (!positionRates[position]) {
    throw new Error(`Puesto ${position} no válido.`);
  }
  const dailyRate = positionRates[position];
  const hourlyRate = dailyRate / 8;
  const feeBeforeIrpf = hourlyRate * hours;
  return feeBeforeIrpf * (1 - irpfRate);
}

// Endpoint para calcular tarifas
app.post('/calculate_fee', (req, res) => {
  try {
    const { hours, position } = req.body;
    if (hours === undefined || !position) {
      return res.status(400).json({ error: 'Parámetros "hours" y "position" son requeridos' });
    }

    const fee = calculateFee(hours, position);
    res.json({ position, hours, fee_after_irpf: fee });
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

// Iniciar el servidor
app.listen(port, () => {
  console.log(`Servidor escuchando en http://localhost:${port}`);
});
