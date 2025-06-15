"""
Airport Traffic Manager
Sistema de gestión de tráfico aéreo para operadores de aeropuerto

Autor: [Tu nombre]
Curso: CSE 111
Fecha: Junio 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


class AirportTrafficManager:
    """
    Clase principal para gestionar el tráfico aéreo en un aeropuerto.
    Maneja pistas de aterrizaje y terminales disponibles.
    """
    
    def __init__(self):
        self.airstrips = {
            "Runway_01": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_02": {"status": "available", "aircraft": None, "start_time": None},
            "Runway_03": {"status": "available", "aircraft": None, "start_time": None}
        }
        
        self.terminals = {
            "Terminal_A": {"status": "available", "aircraft": None, "start_time": None},
            "Terminal_B": {"status": "available", "aircraft": None, "start_time": None},
            "Terminal_C": {"status": "available", "aircraft": None, "start_time": None},
            "Terminal_D": {"status": "available", "aircraft": None, "start_time": None}
        }
        
        self.arrivals_log = []


def register_arrival(aircraft_id: str, flight_number: str, origin: str) -> Dict[str, str]:
    """
    Registra la llegada de una aeronave al sistema.
    
    Args:
        aircraft_id (str): Identificador único de la aeronave
        flight_number (str): Número de vuelo
        origin (str): Aeropuerto de origen
    
    Returns:
        Dict[str, str]: Información del registro de llegada
    
    Raises:
        ValueError: Si algún parámetro está vacío o es None
    """
    if not aircraft_id or not flight_number or not origin:
        raise ValueError("Todos los campos son obligatorios")
    
    arrival_time = datetime.now()
    
    arrival_data = {
        "aircraft_id": aircraft_id.strip().upper(),
        "flight_number": flight_number.strip().upper(),
        "origin": origin.strip().upper(),
        "arrival_time": arrival_time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "waiting_assignment"
    }
    
    return arrival_data


def assign_to(facility_dict: Dict[str, Dict], aircraft_data: Dict[str, str], facility_type: str) -> Tuple[bool, str]:
    """
    Asigna una aeronave a una instalación disponible (pista o terminal).
    
    Args:
        facility_dict (Dict): Diccionario de instalaciones disponibles
        aircraft_data (Dict): Datos de la aeronave a asignar
        facility_type (str): Tipo de instalación ("runway" o "terminal")
    
    Returns:
        Tuple[bool, str]: (éxito, mensaje/nombre_instalación)
    """
    if not facility_dict or not aircraft_data:
        return False, "Datos inválidos"
    
    # Buscar instalación disponible
    for facility_name, facility_info in facility_dict.items():
        if facility_info["status"] == "available":
            # Asignar aeronave a la instalación
            facility_info["status"] = "occupied"
            facility_info["aircraft"] = aircraft_data["aircraft_id"]
            facility_info["start_time"] = datetime.now()
            
            return True, facility_name
    
    return False, f"No hay {facility_type}s disponibles"


def check_time_used(facility_dict: Dict[str, Dict], facility_name: str) -> Optional[int]:
    """
    Calcula el tiempo que una instalación ha estado ocupada.
    
    Args:
        facility_dict (Dict): Diccionario de instalaciones
        facility_name (str): Nombre de la instalación a verificar
    
    Returns:
        Optional[int]: Minutos de uso, o None si no está ocupada o no existe
    """
    if facility_name not in facility_dict:
        return None
    
    facility = facility_dict[facility_name]
    
    if facility["status"] != "occupied" or facility["start_time"] is None:
        return None
    
    current_time = datetime.now()
    time_diff = current_time - facility["start_time"]
    
    return int(time_diff.total_seconds() / 60)


def check_available(facility_dict: Dict[str, Dict]) -> List[str]:
    """
    Devuelve una lista de instalaciones disponibles.
    
    Args:
        facility_dict (Dict): Diccionario de instalaciones
    
    Returns:
        List[str]: Lista de nombres de instalaciones disponibles
    """
    if not facility_dict:
        return []
    
    available_facilities = []
    
    for facility_name, facility_info in facility_dict.items():
        if facility_info["status"] == "available":
            available_facilities.append(facility_name)
    
    return available_facilities


def release_facility(facility_dict: Dict[str, Dict], facility_name: str) -> bool:
    """
    Libera una instalación ocupada.
    
    Args:
        facility_dict (Dict): Diccionario de instalaciones
        facility_name (str): Nombre de la instalación a liberar
    
    Returns:
        bool: True si se liberó exitosamente, False en caso contrario
    """
    if facility_name not in facility_dict:
        return False
    
    facility = facility_dict[facility_name]
    facility["status"] = "available"
    facility["aircraft"] = None
    facility["start_time"] = None
    
    return True


class AirportGUI:
    """
    Interfaz gráfica para el Airport Traffic Manager.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Airport Traffic Manager")
        self.root.geometry("800x600")
        
        self.manager = AirportTrafficManager()
        
        self.setup_gui()
        self.update_display()
    
    def setup_gui(self):
        """Configura la interfaz gráfica."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sección de registro de llegadas
        arrival_frame = ttk.LabelFrame(main_frame, text="Registro de Llegadas", padding="5")
        arrival_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(arrival_frame, text="ID Aeronave:").grid(row=0, column=0, sticky=tk.W)
        self.aircraft_id_var = tk.StringVar()
        ttk.Entry(arrival_frame, textvariable=self.aircraft_id_var).grid(row=0, column=1, padx=5)
        
        ttk.Label(arrival_frame, text="Número de Vuelo:").grid(row=0, column=2, sticky=tk.W)
        self.flight_number_var = tk.StringVar()
        ttk.Entry(arrival_frame, textvariable=self.flight_number_var).grid(row=0, column=3, padx=5)
        
        ttk.Label(arrival_frame, text="Origen:").grid(row=1, column=0, sticky=tk.W)
        self.origin_var = tk.StringVar()
        ttk.Entry(arrival_frame, textvariable=self.origin_var).grid(row=1, column=1, padx=5)
        
        ttk.Button(arrival_frame, text="Registrar Llegada", 
                  command=self.register_arrival_gui).grid(row=1, column=2, padx=5)
        
        # Sección de pistas
        runway_frame = ttk.LabelFrame(main_frame, text="Pistas de Aterrizaje", padding="5")
        runway_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(0, 5))
        
        self.runway_tree = ttk.Treeview(runway_frame, columns=("Status", "Aircraft", "Time"), show="tree headings")
        self.runway_tree.heading("#0", text="Pista")
        self.runway_tree.heading("Status", text="Estado")
        self.runway_tree.heading("Aircraft", text="Aeronave")
        self.runway_tree.heading("Time", text="Tiempo (min)")
        self.runway_tree.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(runway_frame, text="Asignar a Pista", 
                  command=self.assign_to_runway).grid(row=1, column=0, pady=5)
        ttk.Button(runway_frame, text="Liberar Pista", 
                  command=self.release_runway).grid(row=1, column=1, pady=5)
        
        # Sección de terminales
        terminal_frame = ttk.LabelFrame(main_frame, text="Terminales", padding="5")
        terminal_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.terminal_tree = ttk.Treeview(terminal_frame, columns=("Status", "Aircraft", "Time"), show="tree headings")
        self.terminal_tree.heading("#0", text="Terminal")
        self.terminal_tree.heading("Status", text="Estado")
        self.terminal_tree.heading("Aircraft", text="Aeronave")
        self.terminal_tree.heading("Time", text="Tiempo (min)")
        self.terminal_tree.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(terminal_frame, text="Asignar a Terminal", 
                  command=self.assign_to_terminal).grid(row=1, column=0, pady=5)
        ttk.Button(terminal_frame, text="Liberar Terminal", 
                  command=self.release_terminal).grid(row=1, column=1, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema listo")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Timer para actualizar display
        self.root.after(30000, self.auto_update)  # Actualizar cada 30 segundos
    
    def register_arrival_gui(self):
        """Maneja el registro de llegadas desde la GUI."""
        try:
            aircraft_id = self.aircraft_id_var.get()
            flight_number = self.flight_number_var.get()
            origin = self.origin_var.get()
            
            arrival_data = register_arrival(aircraft_id, flight_number, origin)
            self.manager.arrivals_log.append(arrival_data)
            
            # Limpiar campos
            self.aircraft_id_var.set("")
            self.flight_number_var.set("")
            self.origin_var.set("")
            
            self.status_var.set(f"Llegada registrada: {arrival_data['flight_number']}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def assign_to_runway(self):
        """Asigna aeronave a pista disponible."""
        if not self.manager.arrivals_log:
            messagebox.showwarning("Advertencia", "No hay aeronaves en espera")
            return
        
        # Usar la primera aeronave en espera
        aircraft_data = None
        for arrival in self.manager.arrivals_log:
            if arrival["status"] == "waiting_assignment":
                aircraft_data = arrival
                break
        
        if not aircraft_data:
            messagebox.showwarning("Advertencia", "No hay aeronaves esperando asignación")
            return
        
        success, result = assign_to(self.manager.airstrips, aircraft_data, "runway")
        
        if success:
            aircraft_data["status"] = "assigned_runway"
            self.status_var.set(f"Aeronave {aircraft_data['aircraft_id']} asignada a {result}")
            self.update_display()
        else:
            messagebox.showwarning("Advertencia", result)
    
    def assign_to_terminal(self):
        """Asigna aeronave a terminal disponible."""
        if not self.manager.arrivals_log:
            messagebox.showwarning("Advertencia", "No hay aeronaves en espera")
            return
        
        # Usar la primera aeronave en espera
        aircraft_data = None
        for arrival in self.manager.arrivals_log:
            if arrival["status"] == "waiting_assignment":
                aircraft_data = arrival
                break
        
        if not aircraft_data:
            messagebox.showwarning("Advertencia", "No hay aeronaves esperando asignación")
            return
        
        success, result = assign_to(self.manager.terminals, aircraft_data, "terminal")
        
        if success:
            aircraft_data["status"] = "assigned_terminal"
            self.status_var.set(f"Aeronave {aircraft_data['aircraft_id']} asignada a {result}")
            self.update_display()
        else:
            messagebox.showwarning("Advertencia", result)
    
    def release_runway(self):
        """Libera una pista seleccionada."""
        selection = self.runway_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una pista")
            return
        
        runway_name = self.runway_tree.item(selection[0])["text"]
        if release_facility(self.manager.airstrips, runway_name):
            self.status_var.set(f"Pista {runway_name} liberada")
            self.update_display()
    
    def release_terminal(self):
        """Libera un terminal seleccionado."""
        selection = self.terminal_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un terminal")
            return
        
        terminal_name = self.terminal_tree.item(selection[0])["text"]
        if release_facility(self.manager.terminals, terminal_name):
            self.status_var.set(f"Terminal {terminal_name} liberado")
            self.update_display()
    
    def update_display(self):
        """Actualiza la información mostrada en pantalla."""
        # Limpiar árboles
        for item in self.runway_tree.get_children():
            self.runway_tree.delete(item)
        
        for item in self.terminal_tree.get_children():
            self.terminal_tree.delete(item)
        
        # Actualizar pistas
        for runway_name, runway_info in self.manager.airstrips.items():
            status = "Disponible" if runway_info["status"] == "available" else "Ocupada"
            aircraft = runway_info["aircraft"] or "-"
            time_used = check_time_used(self.manager.airstrips, runway_name) or 0
            
            self.runway_tree.insert("", "end", text=runway_name, 
                                  values=(status, aircraft, time_used))
        
        # Actualizar terminales
        for terminal_name, terminal_info in self.manager.terminals.items():
            status = "Disponible" if terminal_info["status"] == "available" else "Ocupado"
            aircraft = terminal_info["aircraft"] or "-"
            time_used = check_time_used(self.manager.terminals, terminal_name) or 0
            
            self.terminal_tree.insert("", "end", text=terminal_name, 
                                    values=(status, aircraft, time_used))
    
    def auto_update(self):
        """Actualización automática del display."""
        self.update_display()
        self.root.after(30000, self.auto_update)


def main():
    """Función principal del programa."""
    root = tk.Tk()
    app = AirportGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()