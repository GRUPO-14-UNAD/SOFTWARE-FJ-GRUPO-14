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
