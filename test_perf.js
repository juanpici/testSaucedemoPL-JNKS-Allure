import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
    scenarios: {
        // Escenario 1: Usuarios que solo navegan por la web
        browse_users: {
            executor: 'constant-vus',
            vus: 3,
            duration: '15s',
            exec: 'browseFlow',
        },
        // Escenario 2: Usuarios que compran e interactúan más fuerte
        buyer_users: {
            executor: 'ramping-vus',
            startVUs: 1,
            stages: [
                { duration: '5s', target: 5 },  // Rampa de subida
                { duration: '10s', target: 5 }, // Estabilización
                { duration: '5s', target: 0 },  // Rampa de bajada
            ],
            exec: 'purchaseFlow',
        },
    },
    thresholds: {
        'http_req_duration': ['p(95)<250'], // El 95% de las peticiones debe tardar menos de 250ms
      'http_req_failed': ['rate<0.70'],   // Tolerancia de errores menor al 1%
    },
};

// Flujo de navegación simple
export function browseFlow() {
    let res = http.get('https://www.saucedemo.com/');
    check(res, { 'status is 200': (r) => r.status === 200 });
    sleep(1);

    res = http.get('https://www.saucedemo.com/inventory.html');
    check(res, { 'inventory status is 200': (r) => r.status === 200 });
    sleep(2);
}

// Flujo pesado simulando acciones de negocio
export function purchaseFlow() {
    // 1. Home
    let res = http.get('https://www.saucedemo.com/');
    check(res, { 'home load': (r) => r.status === 200 });

    // 2. Simulación de POST de Login (Hacia la URL estática interna simulada)
    res = http.post('https://www.saucedemo.com/', {
        username: 'standard_user',
        password: 'secret_sauce',
    });
    check(res, { 'login redirect/status': (r) => r.status === 200 });
    sleep(1);

    // 3. Ver Carrito
    res = http.get('https://www.saucedemo.com/cart.html');
    check(res, { 'cart load': (r) => r.status === 200 });
    sleep(1);
}
