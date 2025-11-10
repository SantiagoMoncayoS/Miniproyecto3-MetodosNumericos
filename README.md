# Miniproyecto 3 – Métodos Numéricos para Ecuaciones en Derivadas Parciales

Repositorio de entrega del **Miniproyecto 3** para la materia *Métodos Numéricos para Ecuaciones en Derivadas Parciales* (2025-2).  
Profesor: **José Hernán Ortiz Ocampo**

---

## 📄 Descripción general

Este proyecto implementa la **solución numérica de la ecuación de Poisson** mediante el **Método de Elementos Finitos (FEM)** en dos configuraciones:

1. **FEM 1D** sobre una malla no uniforme generada aleatoriamente.  
2. **FEM 2D** sobre un dominio **hexagonal regular** con condiciones de frontera Dirichlet homogéneas (u = 0).

El trabajo incluye:
- Ensamble matricial y resolución del problema 1D por elementos lineales.  
- Implementación de un mallado 2D automático mediante triangulación de Delaunay.  
- Resolución del problema estacionario en 2D con carga variable.  
- Análisis **Monte Carlo** y **paramétrico** para estudiar la influencia estadística de los parámetros geométricos y de carga.  
- Graficación de soluciones, mallas y distribuciones de u_max.

---

## 📂 Contenido del repositorio

- `src/` → Código fuente principal del proyecto  
  - `main.py` → Script principal con interfaz por línea de comandos (CLI) que permite elegir el modo de ejecución:  
    - `fem1d` → problema 1D.  
    - `det2d` → simulación 2D determinística.  
    - `mc` → simulación Monte Carlo.  
    - `param` → estudio paramétrico.  
  - `mesh1d.py` → Generación de malla aleatoria en [0, 1].  
  - `fem1d.py` → Ensamble y resolución del sistema 1D.  
  - `mesh2d_hex.py` → Generación de puntos y polígono hexagonal.  
  - `fem2d.py` → Ensamble y resolución FEM P1 en el hexágono.  
  - `loads.py` → Definición de las funciones de carga 1D y 2D.  
  - `plotting.py` → Rutinas de graficación y visualización de resultados.

- `figures/` → Figuras generadas automáticamente:  
  - `fem1d_solution.png` – Solución 1D.  
  - `det_potential.png` – Campo de potencial 2D.  
  - `det_load.png` – Distribución de carga 2D.  
  - `mc_hist.png` – Histograma de u_max (Monte Carlo).  
  - `param_scatter.png` – u_max vs parámetro (barrido paramétrico).

- `outputs/` → Resultados en formato `.npz` con los vectores y parámetros de cada simulación.

- `tests/` → Pruebas básicas para verificar el correcto ensamble y tamaño de los vectores.

- `requirements.txt` → Dependencias necesarias (`numpy`, `matplotlib`, `scipy`).

- `LICENSE`, `.gitignore`, `README.md` → Metadatos y documentación del proyecto.

---

## ⚙️ Configuración del entorno de ejecución

Se recomienda **Python 3.10 o superior**.

### 🔹 Opción A – Manual por terminal (Windows)
```bash
python -m venv env1
.\env1\Scripts\activate
pip install -r requirements.txt
```

### 🔹 Opción B – Linux / Mac
```bash
python3 -m venv env1
source env1/bin/activate
pip install -r requirements.txt
```

---

## 🧮 Ejemplos de ejecución

### 1️⃣ FEM 1D – Malla aleatoria
```bash
python -m src.main fem1d --nint 40 --seed 0 --plot
```
Genera las gráficas `fem1d_solution.png` y `fem1d_mesh.png`.

### 2️⃣ FEM 2D – Simulación determinística
```bash
python -m src.main det2d --nx 45 --ny 45 --save-prefix det_hex
```
Genera las figuras `det_potential.png` y `det_load.png`.

### 3️⃣ FEM 2D – Análisis Monte Carlo
```bash
python -m src.main mc --N 100 --nx 40 --ny 40 --save-prefix mc_hex
```
Produce el histograma `mc_hist.png` y el archivo `outputs/mc_hex.npz` con los resultados estadísticos (media, desviación, intervalo 95 %).

### 4️⃣ FEM 2D – Estudio paramétrico
```bash
python -m src.main param --param gamma --N 100 --nx 40 --ny 40 --save-prefix par_hex
```
Genera el gráfico `param_scatter.png` de u_max vs γ.

---

## 📊 Resultados esperados

- En 1D: comportamiento suave y continuo de la solución con nodos aleatorios.  
- En 2D: campo de potencial simétrico dentro del hexágono y u = 0 en el borde.  
- Monte Carlo: distribución aproximadamente normal de u_max con dispersión moderada.  
- Barrido paramétrico: fuerte correlación positiva de u_max con α y β; efecto secundario de R; influencia mínima de γ y θ.
