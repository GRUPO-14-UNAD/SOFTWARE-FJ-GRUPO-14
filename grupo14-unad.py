"""
SOFTWARE-FJ-GRUPO-14
Sistema Integral de Gestión de Clientes, Servicios y  Reservas
CREADDORES: Juan David Crespo Carpio
fecha de inicio: 19 de junio 2026
"""
import re
import datetime
import os
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

# 1. EXCEPCIONES PERSONALIZADAS

class SistemaError(Exception):
    """Excepcion base del sistema."""
    pass

class DatoInvalidoError(SistemaError):
    """Lanzada cuando un dato no supera la validacion."""
    pass

class ServicioNoDisponibleError(SistemaError):
    """Lanzada cuando un servicio no esta disponible."""
    pass

class ClienteInactivoError(SistemaError):
    """Lanzada cuando se intenta operar con un cliente inactivo."""
    pass

class ReservaInvalidaError(SistemaError):
    """Lanzada cuando una operacion sobre reserva no es valida."""
    pass

class ParametroFaltanteError(SistemaError):
    """Lanzada cuando faltan parametros obligatorios."""
    pass



# 2. LOGGER (REGISTRO DE EVENTOS Y ERRORES)


class LoggerSistema:
    """Maneja el registro de eventos y errores en archivos de texto."""
    
    @staticmethod
    def _escribir(archivo: str, mensaje: str) -> None:
        """Escribe un mensaje con timestamp en el archivo especificado."""
        try:
            with open(archivo, "a", encoding="utf-8") as f:
                timestamp = datetime.datetime.now().isoformat()
                f.write(f"{timestamp} - {mensaje}\n")
        except Exception as e:
            print(f"Error critico al escribir en log: {e}")
    
    @staticmethod
    def registrar_evento(mensaje: str) -> None:
        LoggerSistema._escribir("eventos.log", f"[EVENTO] {mensaje}")
    
    @staticmethod
    def registrar_error(mensaje: str, exc_info: Optional[Exception] = None) -> None:
        if exc_info:
            mensaje = f"{mensaje} - {type(exc_info).__name__}: {exc_info}"
        LoggerSistema._escribir("errores.log", f"[ERROR] {mensaje}")

       # 3. CLASE ABSTRACTA ENTIDAD

class Entidad(ABC):
    """Clase base abstracta para todas las entidades."""
    
    def __init__(self, id_entidad: str, nombre: str):
        self._id = id_entidad
        self._nombre = nombre
    
    @property
    def id(self) -> str:
        return self._id
    
    @property
    def nombre(self) -> str:
        return self._nombre
    
    @abstractmethod
    def mostrar_info(self) -> str:
        pass 