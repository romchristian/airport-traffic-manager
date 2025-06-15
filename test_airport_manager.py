"""
Test Suite para Airport Traffic Manager
Sistema de pruebas unitarias usando pytest

Autor: [Tu nombre]
Curso: CSE 111
Fecha: Junio 2025

Para ejecutar las pruebas:
    pytest test_airport_manager.py -v
"""

import pytest
from datetime import datetime, timedelta
import sys
import os

# Agregar el directorio padre al path para importar el módulo principal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from airport_manager import (
    register_arrival,
    assign_to,
    check_time_used,
    check_available,
    release_facility
)


class TestRegisterArrival:
    """Tests para la función register_arrival()"""
    
    def test_register_arrival_valid_data(self):
        """Prueba registro de llegada con datos válidos"""
        result = register_arrival("ABC123", "UA100", "JFK")
        
        assert result["aircraft_id"] == "ABC123"
        assert result["flight_number"] == "UA100"
        assert result["origin"] == "JFK"
        assert result["status"] == "waiting_assignment"
        assert "arrival_time" in result
        
        # Verificar que el tiempo de llegada es reciente (últimos 5 segundos)
        arrival_time = datetime.strptime(result["arrival_time"], "%Y-%m-%d %H:%M:%S")
        time_diff = datetime.now() - arrival_time
        assert time_diff.total_seconds() < 5
    
    def test_register_arrival_with_spaces(self):
        """Prueba que se eliminen espacios extra y se conviertan a mayúsculas"""
        result = register_arrival("  abc123  ", "  ua100  ", "  jfk  ")
        
        assert result["aircraft_id"] == "ABC123"
        assert result["flight_number"] == "UA100"
        assert result["origin"] == "JFK"
    
    def test_register_arrival_empty_aircraft_id(self):
        """Prueba error con aircraft_id vacío"""
        with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
            register_arrival("", "UA100", "JFK")
    
    def test_register_arrival_empty_flight_number(self):
        """Prueba error con flight_number vacío"""
        with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
            register_arrival("ABC123", "", "JFK")
    
    def test_register_arrival_empty_origin(self):
        """Prueba error con origin vacío"""
        with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
            register_arrival("ABC123", "UA100", "")
    
    def test_register_arrival_none_values(self):
        """Prueba error con valores None"""
        with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
            register_arrival(None, "UA100", "JFK")
        
        with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
            register_arrival("ABC123", None, "JFK")
        
        with pytest.raises(ValueError, match="Todos los campos son obligatorios"):
            register_arrival("ABC123", "UA100", None)


class TestAssignTo:
    """Tests para la función assign_to()"""
    
    @pytest.fixture
    def sample_facilities(self):
        """Fixture con instalaciones de prueba"""
        return {
            "Runway_01": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_02": {"status": "occupied", "aircraft": "XYZ789", "start_time": datetime.now()},
            "Runway_03": {"status": "available", "aircraft": None, "start_time": None}
        }
    
    @pytest.fixture
    def sample_aircraft(self):
        """Fixture con datos de aeronave de prueba"""
        return {
            "aircraft_id": "ABC123",
            "flight_number": "UA100",
            "origin": "JFK",
            "arrival_time": "2025-06-15 10:30:00",
            "status": "waiting_assignment"
        }
    
    def test_assign_to_available_facility(self, sample_facilities, sample_aircraft):
        """Prueba asignación exitosa a instalación disponible"""
        success, facility_name = assign_to(sample_facilities, sample_aircraft, "runway")
        
        assert success is True
        assert facility_name in ["Runway_01", "Runway_03"]  # Cualquiera de las disponibles
        
        # Verificar que la instalación ahora está ocupada
        assert sample_facilities[facility_name]["status"] == "occupied"
        assert sample_facilities[facility_name]["aircraft"] == "ABC123"
        assert sample_facilities[facility_name]["start_time"] is not None
    
    def test_assign_to_no_available_facilities(self, sample_aircraft):
        """Prueba cuando no hay instalaciones disponibles"""
        occupied_facilities = {
            "Runway_01": {"status": "occupied", "aircraft": "XYZ789", "start_time": datetime.now()},
            "Runway_02": {"status": "occupied", "aircraft": "DEF456", "start_time": datetime.now()}
        }
        
        success, message = assign_to(occupied_facilities, sample_aircraft, "runway")
        
        assert success is False
        assert "No hay runways disponibles" in message
    
    def test_assign_to_empty_facilities(self, sample_aircraft):
        """Prueba con diccionario de instalaciones vacío"""
        success, message = assign_to({}, sample_aircraft, "runway")
        
        assert success is False
        assert message == "Datos inválidos"
    
    def test_assign_to_invalid_aircraft_data(self, sample_facilities):
        """Prueba con datos de aeronave inválidos"""
        success, message = assign_to(sample_facilities, {}, "runway")
        
        assert success is False
        assert message == "Datos inválidos"
        
        success, message = assign_to(sample_facilities, None, "runway")
        
        assert success is False
        assert message == "Datos inválidos"


class TestCheckTimeUsed:
    """Tests para la función check_time_used()"""
    
    @pytest.fixture
    def facilities_with_time(self):
        """Fixture con instalaciones que tienen tiempo de uso"""
        past_time = datetime.now() - timedelta(minutes=30)
        return {
            "Runway_01": {"status": "occupied", "aircraft": "ABC123", "start_time": past_time},
            "Runway_02": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_03": {"status": "occupied", "aircraft": "XYZ789", "start_time": datetime.now()}
        }
    
    def test_check_time_used_occupied_facility(self, facilities_with_time):
        """Prueba cálculo de tiempo para instalación ocupada"""
        time_used = check_time_used(facilities_with_time, "Runway_01")
        
        # Debería ser aproximadamente 30 minutos (±1 minuto de tolerancia)
        assert time_used is not None
        assert 29 <= time_used <= 31
    
    def test_check_time_used_recently_occupied(self, facilities_with_time):
        """Prueba con instalación ocupada recientemente"""
        time_used = check_time_used(facilities_with_time, "Runway_03")
        
        # Debería ser 0 o muy poco tiempo
        assert time_used is not None
        assert 0 <= time_used <= 1
    
    def test_check_time_used_available_facility(self, facilities_with_time):
        """Prueba con instalación disponible"""
        time_used = check_time_used(facilities_with_time, "Runway_02")
        
        assert time_used is None
    
    def test_check_time_used_nonexistent_facility(self, facilities_with_time):
        """Prueba con instalación que no existe"""
        time_used = check_time_used(facilities_with_time, "Runway_99")
        
        assert time_used is None
    
    def test_check_time_used_empty_dict(self):
        """Prueba con diccionario vacío"""
        time_used = check_time_used({}, "Runway_01")
        
        assert time_used is None


class TestCheckAvailable:
    """Tests para la función check_available()"""
    
    @pytest.fixture
    def mixed_facilities(self):
        """Fixture con instalaciones mixtas (disponibles y ocupadas)"""
        return {
            "Runway_01": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_02": {"status": "occupied", "aircraft": "ABC123", "start_time": datetime.now()},
            "Runway_03": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_04": {"status": "occupied", "aircraft": "XYZ789", "start_time": datetime.now()}
        }
    
    def test_check_available_mixed_facilities(self, mixed_facilities):
        """Prueba con instalaciones mixtas"""
        available = check_available(mixed_facilities)
        
        assert len(available) == 2
        assert "Runway_01" in available
        assert "Runway_03" in available
        assert "Runway_02" not in available
        assert "Runway_04" not in available
    
    def test_check_available_all_available(self):
        """Prueba con todas las instalaciones disponibles"""
        all_available = {
            "Runway_01": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_02": {"status": "available", "aircraft": None, "start_time": None}
        }
        
        available = check_available(all_available)
        
        assert len(available) == 2
        assert "Runway_01" in available
        assert "Runway_02" in available
    
    def test_check_available_all_occupied(self):
        """Prueba con todas las instalaciones ocupadas"""
        all_occupied = {
            "Runway_01": {"status": "occupied", "aircraft": "ABC123", "start_time": datetime.now()},
            "Runway_02": {"status": "occupied", "aircraft": "XYZ789", "start_time": datetime.now()}
        }
        
        available = check_available(all_occupied)
        
        assert len(available) == 0
        assert available == []
    
    def test_check_available_empty_dict(self):
        """Prueba con diccionario vacío"""
        available = check_available({})
        
        assert available == []
    
    def test_check_available_none_input(self):
        """Prueba con entrada None"""
        available = check_available(None)
        
        assert available == []


class TestReleaseFacility:
    """Tests para la función release_facility()"""
    
    @pytest.fixture
    def occupied_facilities(self):
        """Fixture con instalaciones ocupadas"""
        return {
            "Runway_01": {"status": "occupied", "aircraft": "ABC123", "start_time": datetime.now()},
            "Runway_02": {"status": "available", "aircraft": None, "start_time": None}
        }
    
    def test_release_occupied_facility(self, occupied_facilities):
        """Prueba liberación de instalación ocupada"""
        result = release_facility(occupied_facilities, "Runway_01")
        
        assert result is True
        assert occupied_facilities["Runway_01"]["status"] == "available"
        assert occupied_facilities["Runway_01"]["aircraft"] is None
        assert occupied_facilities["Runway_01"]["start_time"] is None
    
    def test_release_already_available_facility(self, occupied_facilities):
        """Prueba liberación de instalación ya disponible"""
        result = release_facility(occupied_facilities, "Runway_02")
        
        assert result is True
        assert occupied_facilities["Runway_02"]["status"] == "available"
    
    def test_release_nonexistent_facility(self, occupied_facilities):
        """Prueba liberación de instalación inexistente"""
        result = release_facility(occupied_facilities, "Runway_99")
        
        assert result is False


class TestIntegration:
    """Tests de integración del sistema completo"""
    
    def test_complete_workflow(self):
        """Prueba el flujo completo del sistema"""
        # 1. Crear instalaciones
        facilities = {
            "Runway_01": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_02": {"status": "available", "aircraft": None, "start_time": None}
        }
        
        # 2. Registrar llegada
        aircraft_data = register_arrival("ABC123", "UA100", "JFK")
        assert aircraft_data["status"] == "waiting_assignment"
        
        # 3. Verificar instalaciones disponibles
        available = check_available(facilities)
        assert len(available) == 2
        
        # 4. Asignar aeronave
        success, facility_name = assign_to(facilities, aircraft_data, "runway")
        assert success is True
        
        # 5. Verificar que se redujo disponibilidad
        available_after = check_available(facilities)
        assert len(available_after) == 1
        
        # 6. Verificar tiempo de uso
        time_used = check_time_used(facilities, facility_name)
        assert time_used is not None
        assert time_used >= 0
        
        # 7. Liberar instalación
        release_result = release_facility(facilities, facility_name)
        assert release_result is True
        
        # 8. Verificar que volvió a estar disponible
        final_available = check_available(facilities)
        assert len(final_available) == 2
        
        # 9. Verificar que no hay tiempo de uso después de liberar
        time_after_release = check_time_used(facilities, facility_name)
        assert time_after_release is None


def test_edge_cases():
    """Prueba casos límite del sistema"""
    
    def test_multiple_assignments_same_aircraft():
        """Prueba múltiples asignaciones con la misma aeronave"""
        facilities = {
            "Runway_01": {"status": "available", "aircraft": None, "start_time": None}
        }
        
        aircraft_data = register_arrival("ABC123", "UA100", "JFK")
        
        # Primera asignación
        success1, facility1 = assign_to(facilities, aircraft_data, "runway")
        assert success1 is True
        
        # Segunda asignación (debería fallar - no hay más instalaciones)
        success2, message2 = assign_to(facilities, aircraft_data, "runway")
        assert success2 is False
        assert "No hay runways disponibles" in message2
    
    def test_facility_status_consistency():
        """Prueba consistencia del estado de las instalaciones"""
        facilities = {
            "Terminal_A": {"status": "available", "aircraft": None, "start_time": None}
        }
        
        aircraft_data = register_arrival("XYZ789", "DL200", "LAX")
        
        # Asignar
        assign_to(facilities, aircraft_data, "terminal")
        
        # Verificar estados
        available_before = check_available(facilities)
        assert len(available_before) == 0
        
        time_used = check_time_used(facilities, "Terminal_A")
        assert time_used is not None
        
        # Liberar
        release_facility(facilities, "Terminal_A")
        
        # Verificar estados después de liberar
        available_after = check_available(facilities)
        assert len(available_after) == 1
        
        time_after = check_time_used(facilities, "Terminal_A")
        assert time_after is None


if __name__ == "__main__":
    # Ejecutar todas las pruebas
    pytest.main([__file__, "-v", "--tb=short"])