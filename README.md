# Airport Traffic Manager

**Curso:** CSE 111 - Programming with Functions  
**Proyecto:** Student Chosen Program  
**Autor:** [Tu Nombre]  
**Fecha:** Junio 2025

## Descripción del Proyecto

Airport Traffic Manager es un sistema de gestión de tráfico aéreo diseñado para ayudar a los operadores de aeropuerto a administrar las pistas de aterrizaje y terminales disponibles. El programa cuenta con una interfaz gráfica intuitiva desarrollada con tkinter.

## Problema que Resuelve

El sistema aborda la necesidad real de los operadores de tráfico aéreo de:
- Gestionar eficientemente las pistas de aterrizaje disponibles
- Controlar la ocupación de terminales
- Registrar llegadas de aeronaves
- Monitorear tiempos de uso de instalaciones
- Optimizar la asignación de recursos aeroportuarios

## Características Principales

### Funcionalidades Core
- **Registro de Llegadas**: Registra aeronaves que llegan al aeropuerto
- **Asignación Automática**: Asigna aeronaves a pistas y terminales disponibles
- **Monitoreo de Tiempo**: Calcula tiempo de uso de instalaciones
- **Gestión de Disponibilidad**: Controla qué instalaciones están libres u ocupadas
- **Liberación de Instalaciones**: Permite liberar pistas y terminales

### Interfaz Gráfica
- Interfaz intuitiva desarrollada con tkinter
- Visualización en tiempo real del estado de instalaciones
- Formularios para registro de llegadas
- Botones para asignación y liberación de recursos
- Actualización automática cada 30 segundos

## Estructura del Proyecto

```
airport-traffic-manager/
│
├── airport_manager.py          # Programa principal
├── test_airport_manager.py     # Suite de pruebas
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación
└── docs/                       # Documentación adicional
```

## Módulos de Python Utilizados

- **tkinter**: Interfaz gráfica de usuario
- **datetime**: Manejo de fechas y tiempos
- **pytest**: Framework de pruebas unitarias
- **typing**: Type hints para mejor documentación del código

## Funciones Principales

### Funciones Core (Reutilizables)
- `register_arrival(aircraft_id, flight_number, origin)`: Registra llegada de aeronave
- `assign_to(facility_dict, aircraft_data, facility_type)`: Asigna aeronave a instalación
- `check_time_used(facility_dict, facility_name)`: Calcula tiempo de uso
- `check_available(facility_dict)`: Lista instalaciones disponibles
- `release_facility(facility_dict, facility_name)`: Libera instalación ocupada

### Funciones de Interfaz
- `AirportGUI`: Clase principal de la interfaz gráfica
- `main()`: Función principal del programa

## Instalación y Ejecución

### Requisitos del Sistema
- Python 3.7 o superior
- tkinter (incluido con Python)
- pytest (para ejecutar pruebas)

### Instalación
```bash
# Clonar o descargar el proyecto
git clone <repository-url>
cd airport-traffic-manager

# Instalar dependencias (opcional, para pruebas)
pip install -r requirements.txt
```

### Ejecución del Programa
```bash
python airport_manager.py
```

### Ejecución de Pruebas
```bash
# Ejecutar todas las pruebas
pytest test_airport_manager.py -v

# Ejecutar con reporte de cobertura
pytest test_airport_manager.py --cov=airport_manager --cov-report=html
```

## Uso del Sistema

### 1. Registro de Llegadas
1. Completar los campos: ID Aeronave, Número de Vuelo, Origen
2. Hacer clic en "Registrar Llegada"
3. La aeronave quedará en estado "esperando asignación"

### 2. Asignación a Pistas
1. Hacer clic en "Asignar a Pista"
2. El sistema asignará automáticamente la primera aeronave en espera a una pista disponible
3. La pista cambiará a estado "Ocupada"

### 3. Asignación a Terminales
1. Hacer clic en "Asignar a Terminal"
2. Similar al proceso de pistas, pero para terminales

### 4. Liberación de Instalaciones
1. Seleccionar la instalación ocupada en la lista
2. Hacer clic en "Liberar Pista" o "Liberar Terminal"
3. La instalación volverá a estar disponible

## Arquitectura del Sistema

### Diseño de Clases
- **AirportTrafficManager**: Gestiona el estado del aeropuerto
- **AirportGUI**: Interfaz gráfica de usuario

### Estructura de Datos
- **Instalaciones**: Diccionarios con estado, aeronave asignada y tiempo de inicio
- **Registros de Llegada**: Lista de aeronaves registradas con su información

### Patrones de Diseño
- **Separación de Responsabilidades**: Lógica de negocio separada de la interfaz
- **Funciones Puras**: Las funciones core no dependen de estado global
- **Manejo de Errores**: Validación de entrada y manejo de excepciones

## Pruebas Unitarias

### Cobertura de Pruebas
- **TestRegisterArrival**: Pruebas para registro de llegadas
- **TestAssignTo**: Pruebas para asignación de instalaciones
- **TestCheckTimeUsed**: Pruebas para cálculo de tiempo de uso
- **TestCheckAvailable**: Pruebas para verificación de disponibilidad
- **TestReleaseFacility**: Pruebas para liberación de instalaciones
- **TestIntegration**: Pruebas de integración del flujo completo

### Casos de Prueba
- Casos válidos con datos correctos
- Casos inválidos con datos erróneos
- Casos límite y edge cases
- Pruebas de integración del flujo completo

## Aprendizajes del Proyecto

### Objetivos Logrados
1. **Interfaz Gráfica**: Dominio de tkinter para crear GUIs funcionales
2. **Arquitectura de Software**: Separación de lógica de negocio y presentación
3. **Pruebas Unitarias**: Desarrollo de suite completa de pruebas con pytest
4. **Manejo de Tiempo**: Uso de datetime para cálculos temporales
5. **Validación de Datos**: Implementación de validaciones robustas

### Habilidades Desarrolladas
- Diseño de interfaces de usuario intuitivas
- Programación orientada a objetos
- Testing y desarrollo guiado por pruebas (TDD)
- Documentación técnica
- Control de versiones y organización de proyectos

## Posibles Mejoras Futuras

- Persistencia de datos en base de datos
- Reportes y estadísticas de uso
- Integración con sistemas de radar
- Notificaciones automáticas
- Soporte para múltiples aeropuertos
- API REST para integración externa
- Autenticación y autorización de usuarios

## Conclusión

Airport Traffic Manager demuestra la aplicación práctica de conceptos de programación en Python para resolver problemas reales del mundo de la aviación. El proyecto integra múltiples aspectos de la programación moderna incluyendo interfaces gráficas, pruebas unitarias, manejo de tiempo y validación de datos.

---

*Proyecto desarrollado como parte del curso CSE 111 - Programming with Functions*