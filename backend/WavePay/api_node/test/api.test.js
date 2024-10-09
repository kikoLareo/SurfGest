import chai from 'chai';
import chaiHttp from 'chai-http';
import { app } from '../server.js'; // Asegúrate de que la ruta sea correcta
const expect = chai.expect;

chai.use(chaiHttp);

// Configuración de logs
const log = (message) => {
  const timestamp = new Date().toISOString();
  console.log(`[${timestamp}] - ${message}`);
};

describe('SurfFeeCalculator API', () => {
  before(() => {
    log('Iniciando pruebas para SurfFeeCalculator API');
  });

  after(() => {
    log('Finalizando pruebas para SurfFeeCalculator API');
  });

  it('Debería calcular la tarifa para un director de competición', (done) => {
    log('Enviando solicitud para calcular la tarifa para un director de competición');
    chai.request(app)
      .post('/calculate_fee')
      .send({ hours: 5, position: 'director_competicion' })
      .end((_, res) => {
        log('Recibida respuesta del servidor para calcular tarifa');
        expect(res).to.have.status(200);
        expect(res.body).to.have.property('position').eql('director_competicion');
        expect(res.body).to.have.property('fee_after_irpf');
        expect(res.body.fee_after_irpf).to.be.a('number');
        log(`Tarifa calculada correctamente: ${res.body.fee_after_irpf}`);
        done();
      });
  });

  it('Debería devolver un error si falta algún parámetro', (done) => {
    log('Enviando solicitud con parámetro faltante para verificar manejo de errores');
    chai.request(app)
      .post('/calculate_fee')
      .send({ hours: 5 }) // Falta el parámetro 'position'
      .end((err, res) => {
        log('Recibida respuesta del servidor para solicitud con error');
        expect(res).to.have.status(400);
        expect(res.body).to.have.property('error');
        log(`Error devuelto correctamente: ${res.body.error}`);
        done();
      });
  });
});