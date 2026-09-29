# Justificacion

| Principio | Archivo | Decision concreta |
| --- | --- | --- |
| SRP | `RegistrarPrestamo.py` | Valida y registra prestamos; la persistencia y notificacion estan en puertos. |
| SRP | `RegistrarDevolucion.py` | Coordina devolucion, multa, estado y notificacion mediante dependencias. |
| OCP | `RepositorioEquipoSQLite.py` | Crea equipos mediante un registro de constructores inyectado desde `main.py`. |
| LSP | `RepositorioPrestamoSQLite.py` / `RepositorioPrestamoLocal.py` | Ambos implementan el mismo puerto y pueden sustituirse. |
| ISP | `RepositorioEstudiante.py`, `RepositorioEquipo.py`, `RepositorioPrestamo.py`, `RepositorioMulta.py` | Cada puerto representa una responsabilidad de persistencia. |
| DIP | `RegistrarPrestamo.py` y `RegistrarDevolucion.py` | Los casos de uso dependen de puertos, no de SQLite ni adaptadores concretos. |
| Clean Architecture | `dominio/` | El dominio no importa aplicacion, infraestructura ni sqlite3. |
| Clean Architecture | `aplicacion/` | La aplicacion importa entidades y puertos, no infraestructura. |
| Composicion | `main.py` | El programa ensambla repositorios, fecha, notificador y categorias concretas. |

## Revisión de imports

- `dominio/` no importa `sqlite3`, `aplicacion` ni `infraestructura`.
- `aplicacion/` no importa `sqlite3` ni `infraestructura`.
- `infraestructura/` implementa los puertos y concentra SQLite.
- `main.py` ensambla las clases concretas de infraestructura.

## Declaración

La declaración de autoría y los nombres de la pareja deben ser completados y firmados por los integrantes según las reglas del taller.

"Declaramos que el diseño, el código y los diagramas son de nuestra autoría y que no usamos IA generativa para producirlos"

Nombres: ____________________________________
