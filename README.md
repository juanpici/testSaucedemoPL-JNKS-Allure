# SauceDemo Automation & CI/CD Pipeline

Repositorio de automatización de pruebas integrales (E2E, rendimiento y seguridad) para la web SauceDemo, configurado en un pipeline de Jenkins sobre un VPS.

## Stack Tecnológico

* **E2E:** Playwright (Python) + Pytest + Allure Reports.
* **Rendimiento:** Grafana k6.
* **Seguridad (OWASP):** * Bandit (Análisis estático de código / SAST).
  * pip-audit (Escaneo de vulnerabilidades en dependencias / SCA).
  * OWASP ZAP (Escaneo dinámico pasivo / DAST mediante Docker).
* **CI/CD:** Jenkins (Pipeline declarativo).

## Estructura del Pipeline (Jenkinsfile)

El flujo se ejecuta de forma secuencial en las siguientes etapas:

1. **Checkout:** Clonado del repositorio desde GitHub.
2. **Install Environment:** Creación del entorno virtual (`venv`) e instalación de paquetes y navegadores.
3. **Code Quality (Lint):** Validación de formato de código con `flake8`.
4. **Security - Bandit:** Análisis de seguridad en el código fuente. Guarda `bandit-report.txt`.
5. **Security - pip-audit:** Revisión de librerías contra vulnerabilidades conocidas. Guarda `pip-audit-report.txt`.
6. **Security - OWASP ZAP:** Ejecución del Baseline Scan de ZAP en Docker apuntando a la aplicación. Publica el reporte HTML en Jenkins.
7. **Run Playwright Tests:** Ejecución de pruebas funcionales E2E y generación de resultados para Allure.
8. **Run Performance Tests (k6):** Ejecución del test de carga e integración de métricas en Jenkins.

## Reportes Disponibles
Al finalizar la construcción, se consolidan los siguientes artefactos en la interfaz de Jenkins:
* Tablero interactivo de Allure con los resultados E2E.
* Gráficos de tendencias de performance (k6).
* Pestaña con el reporte interactivo de OWASP ZAP.
* Logs de Bandit y pip-audit archivados para auditoría.
