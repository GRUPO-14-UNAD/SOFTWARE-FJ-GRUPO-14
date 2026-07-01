"""
SOFTWARE-FJ-GRUPO-14
Sistema Integral de Gestión de Clientes, Servicios y  Reservas
CREADORES: Juan David Crespo Carpio
Liseth Camila Pastusan Valdes
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

# 4. CLASE CLIENTE

class Cliente(Entidad):
    """Representa un cliente con validaciones robustas."""
    
    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente, nombre)
        self._email = self._validar_email(email)
        self._telefono = self._validar_telefono(telefono)
        self._fecha_registro = datetime.datetime.now()
        self._activo = True
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, valor: str) -> None:
        self._email = self._validar_email(valor)
    
    @property
    def telefono(self) -> str:
        return self._telefono
    
    @telefono.setter
    def telefono(self, valor: str) -> None:
        self._telefono = self._validar_telefono(valor)
    
    @property
    def activo(self) -> bool:
        return self._activo
    
    def activar(self) -> None:
        self._activo = True
        LoggerSistema.registrar_evento(f"Cliente {self._id} activado.")
    
    def desactivar(self) -> None:
        self._activo = False
        LoggerSistema.registrar_evento(f"Cliente {self._id} desactivado.")
    
    def _validar_email(self, email: str) -> str:
        patron = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(patron, email):
            raise DatoInvalidoError(f"Email invalido: {email}")
        return email
    
    def _validar_telefono(self, telefono: str) -> str:
        if not telefono.isdigit() or len(telefono) < 7:
            raise DatoInvalidoError(f"Telefono invalido: {telefono}")
        return telefono
    
    def mostrar_info(self) -> str:
        estado = "Activo" if self._activo else "Inactivo"
        return f"Cliente {self._id}: {self._nombre} | Email: {self._email} | Tel: {self._telefono} | Estado: {estado}"
    
    def actualizar_datos(self, nombre: Optional[str] = None, email: Optional[str] = None, telefono: Optional[str] = None) -> None:
        try:
            if nombre is not None:
                self._nombre = nombre
            if email is not None:
                self.email = email
            if telefono is not None:
                self.telefono = telefono
            LoggerSistema.registrar_evento(f"Datos actualizados para cliente {self._id}")
        except DatoInvalidoError as e:
            LoggerSistema.registrar_error(f"Error al actualizar cliente {self._id}", e)
            raise
            
# 5. CLASE ABSTRACTA SERVICIO

class Servicio(ABC):
    """Clase abstracta que representa un servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, disponible: bool = True):
        self._id_servicio = self._validar_id(id_servicio)
        self._nombre = self._validar_nombre(nombre)
        self._disponible = disponible

    @property
    def id_servicio(self) -> str:
        return self._id_servicio

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool) -> None:
        self._disponible = estado
        LoggerSistema.registrar_evento(
            f"Servicio {self._id_servicio} disponibilidad cambiada a {estado}"
        )

    def _validar_id(self, id_servicio: str) -> str:
        if not id_servicio:
            raise ParametroFaltanteError("El ID del servicio es obligatorio")
        return id_servicio

    def _validar_nombre(self, nombre: str) -> str:
        if not nombre or len(nombre.strip()) < 3:
            raise DatoInvalidoError("Nombre del servicio invalido")
        return nombre

    def validar_disponibilidad(self) -> None:
        if not self._disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self._nombre} no esta disponible")

    @abstractmethod
    def calcular_costo(self, cantidad: int = 1, descuento: float = 0) -> float:
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        pass


# 6. SERVICIO DE RESERVA DE SALAS

class ReservaSala(Servicio):
    """Servicio especializado para reservar salas."""

    def __init__(self, id_servicio: str, nombre: str, capacidad: int, precio_hora: float):
        super().__init__(id_servicio, nombre)
        if capacidad <= 0:
            raise DatoInvalidoError("Capacidad invalida")
        
        self._capacidad = capacidad
        self._precio_hora = precio_hora


    def calcular_costo(self, horas: int = 1, descuento: float = 0) -> float:
        self.validar_disponibilidad()

        costo = self._precio_hora * horas

        if descuento > 0:
            costo -= costo * (descuento / 100)

        return costo

    def describir_servicio(self) -> str:
        return (
            f"Sala: {self._nombre} | "
            f"Capacidad: {self._capacidad} personas")

# 7. SERVICIO DE ALQUILER DE EQUIPOS

class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, equipo: str, precio_dia: float):
        super().__init__(id_servicio, nombre)

        if precio_dia <= 0:
            raise DatoInvalidoError("Precio invalido")

        self._equipo = equipo
        self._precio_dia = precio_dia


    def calcular_costo(self, dias: int = 1, descuento: float = 0) -> float:
        self.validar_disponibilidad()

        costo = self._precio_dia * dias

        if descuento:
            costo -= costo * (descuento / 100)

        return costo

    def describir_servicio(self) -> str:
        return (
            f"Equipo: {self._equipo} | "
            f"Servicio: {self._nombre}")       

# 8. SERVICIO DE ASESORIA ESPECIALIZADA

class AsesoriaEspecializada(Servicio):
    """Servicio especializado de asesorias."""

    def __init__(self, id_servicio: str, nombre: str, especialista: str, tarifa: float):
        super().__init__(id_servicio, nombre)

        if tarifa <= 0:
            raise DatoInvalidoError("Tarifa invalida")

        self._especialista = especialista
        self._tarifa = tarifa


    def calcular_costo(self, horas: int = 1, descuento: float = 0) -> float:
        self.validar_disponibilidad()

        costo = self._tarifa * horas

        if descuento:
            costo -= costo * (descuento / 100)

        return costo

    def describir_servicio(self) -> str:
        return (
            f"Asesoria con {self._especialista} | "
            f"Servicio: {self._nombre}" )
