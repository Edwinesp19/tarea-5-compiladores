# Ejecutables - Analizador Sintáctico - Edwin Espinal

## 📱 **Ejecutables Disponibles**

En la carpeta `dist/` encontrarás los siguientes ejecutables listos para usar:

### 🖥️ **AnalizadorSintactico-GUI**
- **Archivo**: `AnalizadorSintactico-GUI` (macOS)
- **Archivo**: `AnalizadorSintactico-GUI.app` (Aplicación macOS)
- **Descripción**: Interfaz gráfica completa del analizador sintáctico
- **Uso**: Doble clic para ejecutar
- **Características**:
  - Interfaz gráfica amigable
  - Editor de código integrado
  - Resultados en tiempo real
  - Operaciones de archivo (cargar, guardar, nuevo)
  - Código de ejemplo incluido
  - Ayuda integrada

### 💻 **AnalizadorSintactico-CLI**
- **Archivo**: `AnalizadorSintactico-CLI` (macOS)
- **Descripción**: Versión de línea de comandos
- **Uso**: `./AnalizadorSintactico-CLI <archivo_fuente>`
- **Ejemplo**: `./AnalizadorSintactico-CLI test_with_errors.txt`
- **Características**:
  - Análisis rápido por línea de comandos
  - Salida detallada de errores
  - Reporte de tabla de símbolos
  - Perfecto para scripts y automatización

## 🚀 **Cómo Ejecutar**

### **Interfaz Gráfica:**
```bash
# Opción 1: Ejecutable directo
./dist/AnalizadorSintactico-GUI

# Opción 2: Aplicación macOS
open dist/AnalizadorSintactico-GUI.app
```

### **Línea de Comandos:**
```bash
# Analizar archivo con errores
./dist/AnalizadorSintactico-CLI test_with_errors.txt

# Analizar archivo sin errores
./dist/AnalizadorSintactico-CLI test_no_errors.txt
```

## 📊 **Ejemplo de Salida**

### **Con Errores Sintácticos:**
```
Tokenizando...
Se encontraron 259 tokens

Realizando análisis sintáctico...

============================================================
ANALIZADOR SINTÁCTICO - EDWIN ESPINAL
RESULTADOS DEL ANÁLISIS SINTÁCTICO
============================================================

Se encontraron 6 errores sintácticos:
----------------------------------------
  Error at line 8, column 18: Type mismatch: cannot assign string to int
  Error at line 11, column 1: Undefined variable 'undefinedVar'
  Error at line 18, column 15: Variable 'x' already declared in current scope
  Error at line 33, column 1: Undefined variable 'localVar'
  Error at line 46, column 8: Type mismatch: cannot assign int to string
  Error at line 49, column 1: Undefined variable 'result'

Reporte de Tabla de Símbolos:
==================================================
Nombre: x
  Tipo: int
  Línea: 2, Columna: 9
  Inicializado: Sí
------------------------------
```

### **Sin Errores Sintácticos:**
```
Tokenizando...
Se encontraron 306 tokens

Realizando análisis sintáctico...

============================================================
ANALIZADOR SINTÁCTICO - EDWIN ESPINAL
RESULTADOS DEL ANÁLISIS SINTÁCTICO
============================================================

¡No se encontraron errores sintácticos!
```

## 🔧 **Requisitos del Sistema**

### **macOS:**
- ✅ **AnalizadorSintactico-GUI**: Funciona sin dependencias
- ✅ **AnalizadorSintactico-CLI**: Funciona sin dependencias
- macOS 10.13 o superior
- No requiere Python instalado

### **Windows:**
- Para crear ejecutables de Windows, usar PyInstaller en Windows:
```bash
pip install pyinstaller
pyinstaller --onefile --name "AnalizadorSintactico-CLI" semantic_analyzer.py
pyinstaller --onefile --windowed --name "AnalizadorSintactico-GUI" semantic_analyzer_gui.py
```

## 📁 **Archivos de Prueba Incluidos**

- **test_with_errors.txt**: Archivo con 6 errores sintácticos intencionados
- **test_no_errors.txt**: Archivo con código sintácticamente correcto

## 🎯 **Características del Analizador**

### **Análisis Léxico:**
- Tokenización completa del código fuente
- Reconocimiento de palabras clave, operadores, literales
- Manejo de comentarios y espacios en blanco

### **Análisis Sintáctico:**
- Verificación de tipos y compatibilidad
- Análisis de alcance de variables
- Detección de variables no definidas
- Detección de redeclaraciones
- Validación de declaraciones de funciones

### **Reporte de Errores:**
- Mensajes de error precisos con línea y columna
- Descripción clara del problema
- Tabla de símbolos detallada

## 👨‍💻 **Autor**

**Edwin Espinal**  
Curso: Compiladores  
Institución: UTESA  
Año: 2024

---

**¡El Analizador Sintáctico está listo para usar! 🎉**
