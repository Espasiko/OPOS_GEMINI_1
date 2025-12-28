
# 🖥️ Guía: Monitorear Entrenamiento desde VS Code (Opcional)

Has pedido usar la extensión `googlecolab.colab`. Como soy un agente de terminal, **no puedo hacer clic en el botón de "Login" de tu VS Code** ni instalar extensiones gráficas por ti.

Pero aquí tienes los pasos exactos para hacerlo tú:

## 1. Instalación
1.  En VS Code, ve a **Extensiones** (`Ctrl+Shift+X`).
2.  Busca: `Google Colab`.
3.  Instala la oficial de Google (`googlecolab.colab`).

## 2. Conexión
1.  Abre el notebook `fine_tuning_v9_supreme.ipynb` en tu VS Code local.
2.  Arriba a la derecha, verás "Select Kernel" o "Jupyter Server: Local". Házle clic.
3.  Selecciona **"Connect to Google Colab"**.
4.  Te pedirá autenticación: Sigue los pasos en el navegador.

## 3. Ejecución
*   Una vez conectado, puedes ejecutar las celdas desde VS Code y ver el output en tiempo real.
*   **⚠️ ADVERTENCIA DE RIESGO:** Si tu ordenador se suspende, se desconecta el WiFi o cierras VS Code, **el entrenamiento podría detenerse** o perderías la conexión con los logs.

## 🏁 Recomendación "Modo Nocturno"
Para un entrenamiento de 3-4 horas por la noche, **es más seguro usar el Navegador (Chrome/Edge)** directamente en la web de Colab.
*   Motivo: La conexión es más estable y menos dependiente de tu PC local.
*   Si usas el navegador, asegúrate de dejar la pestaña abierta (puedes usar una extensión de "Auto Refresh" o reproducir un video de YouTube en bucle para que no entre en suspensión).

**Resumen:**
El notebook `fine_tuning_v9_supreme.ipynb` funciona en ambos sitios. Tú eliges.
