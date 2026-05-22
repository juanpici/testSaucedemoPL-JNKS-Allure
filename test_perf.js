import http from 'k6/http';
import { sleep } from 'k6';
import { jUnit } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

export const options = {
  duration: '5s',
  thresholds: {
    http_req_failed: ['rate<0.01'],   // Va a fallar  si hay  del 1% de errores
    http_req_duration: ['p(95)<2000'], // Va a fallar si el 95% de las peticiones tardan más de 2 segundos
  },
};

export default function () {
  http.get('https://test.k6.io');
  sleep(1);
}

// Convierte las métricas en un formato XML estándar para Jenkins
export function handleSummary(data) {
  return {
    'k6-report.xml': jUnit(data),
  };
}
