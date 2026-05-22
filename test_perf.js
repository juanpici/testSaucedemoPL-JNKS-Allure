import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  scenarios: {
    constant_load: {
      executor: 'constant-vus',
      vus: 3,
      duration: '5s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.01'],    // Falla si hay más del 1% de errores
    http_req_duration: ['p(95)<2000'], // Falla si el percentil 95 supera los 2 segundos
  },
};

export default function () {
  // Apuntamos a SauceDemo de forma consistente con tu pipeline
  http.get('https://www.saucedemo.com');
  sleep(1);
}

// Custom summary para inyectar métricas reales en el plugin de Jenkins
export function handleSummary(data) {
  // Convertimos los milisegundos de k6 a segundos para el estándar JUnit
  const avgSeconds = (data.metrics.http_req_duration.values.avg / 1000).toFixed(4);
  const p95Seconds = (data.metrics.http_req_duration.values['p(95)'] / 1000).toFixed(4);
  const totalRequests = data.metrics.http_reqs.values.count;
  const failedRequests = data.metrics.http_req_failed.values.passes;

  // Construcción manual del XML que el Performance Plugin de Jenkins sí puede parsear con datos fluctuantes
  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<testsuites>\n`;
  xml += `  <testsuite name="k6-performance" tests="2" failures="${failedRequests}" time="${avgSeconds}">\n`;
  xml += `    <testcase classname="SauceDemo.Performance" name="HTTPReqDuration_Avg" time="${avgSeconds}" />\n`;
  xml += `    <testcase classname="SauceDemo.Performance" name="HTTPReqDuration_P95" time="${p95Seconds}" />\n`;
  
  if (failedRequests > 0) {
    xml += `    <testcase classname="SauceDemo.Errors" name="Requests_Failed" time="0">\n`;
    xml += `      <failure message="Total de peticiones fallidas: ${failedRequests}" type="KPI_Failure" />\n`;
    xml += `    </testcase>\n`;
  }
  
  xml += `  </testsuite>\n</testsuites>`;

  return {
    'k6-report.xml': xml,
  };
}
