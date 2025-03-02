# 🧬 Proyecto: "Misión vida" (nombre en proceso de decidirse)

## 🎮 Descripción
"Misión Vida" es un videojuego educativo desarrollado en **Python + Pygame** que enseña el proceso de formación del cuerpo humano desde la fecundación hasta el desarrollo celular. El jugador asume el rol de **Cristóbal**, un valiente espermatozoide cuya misión es llegar al óvulo y fusionarse con él para dar inicio a la vida (pronto contara con todo el proceso en general, siendo un total de 5 niveles).

Este juego está diseñado para ser compatible con **teclado y controles arcade**, ofreciendo una experiencia educativa e interactiva para todo público.

---

## 🏗 Arquitectura del Proyecto

El proyecto sigue una **arquitectura en capas** basada en los principios de **arquitectura limpia**, asegurando modularidad, escalabilidad y facilidad de mantenimiento.

```
/game_project
│── /core             # ⚙️ Lógica del juego (mecánicas, colisiones, etc.)
│── /entities         # 🧩 Clases de personajes, enemigos y obstáculos
│── /scenes           # 🎬 Escenas y niveles del juego
│── /services         # 🌐 Conexión con API (SQLite para persistencia de datos(solo en caso de ser requerido una API))
│── /config           # ⚙️ Configuraciones globales (pantalla, FPS, colores)
│── /inputs           # 🎮 Manejo de controles (teclado y arcade)
│── /assets           # 🎨 Sprites, sonidos y fuentes
│── main.py           # 🚀 Punto de entrada del juego
│── settings.py       # 🛠️ Configuraciones generales
│── README.md         # 📄 Documentación
```

---

## ⚙️ Instalación y Configuración
### 🔹 **Requisitos Previos**
- Python 3.8+
- Pygame (`pip install pygame`)

### 🚀 **Ejecución del Juego**
```sh
python main.py
```

---

## 🎮 Controles
(En proceso de decidirse)

| Acción  | Teclado  | Arcade |
|---------|---------|--------|
| Mover izquierda | ← | Botón 0 |
| Mover derecha | → | Botón 1 |
| Saltar | Espacio | Botón 2 |
| Atacar | X | Botón 3 |

---

## 🔧 Modificación de Niveles
Los niveles están definidos en la carpeta `/scenes/` y pueden modificarse fácilmente agregando nuevos enemigos, obstáculos o mecánicas.

---

## 🛠️ Expansión Futura
- Agregar más niveles (fase de desarrollo celular, órganos, etc.)
- Implementar más mecánicas de juego
- Mejorar las cinemáticas y la narrativa
- Integración con más APIs educativas

---

## 🤝 Contribuciones
Si deseas contribuir, por favor sigue estos pasos:
1. **Fork** el repositorio
2. Crea una rama (`git checkout -b feature-nombre`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`)
4. Haz push a la rama (`git push origin feature-nombre`)
5. Abre un Pull Request 🚀

---

## 📜 Licencia
Este proyecto está bajo la licencia **VIXEL**. ¡Siéntete libre de usarlo y mejorarlo! 🎉
