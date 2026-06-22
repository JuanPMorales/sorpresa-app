# App Cita Sorpresa

Una aplicación Streamlit interactiva para planificar citas sorpresa.

## Instalación

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/app_cita_sorpresa.git
   cd app_cita_sorpresa
   ```

2. **Crea un ambiente virtual**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows
   source venv/bin/activate  # En Mac/Linux
   ```

3. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configura las variables de entorno**
   - Copia el archivo `.env.example` a `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edita el archivo `.env` y reemplaza los valores:
     ```
     TOKEN_TELEGRAM=tu_token_del_bot
     CHAT_ID=tu_chat_id
     NOMBRES_VALIDOS= "nombre que quieras"
     ```

## Ejecución

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

## Seguridad

- El archivo `.env` **NO** debe ser commiteado en Git (está en `.gitignore`)
- Mantén tus credenciales de Telegram privadas
- Usa solo en repositorios privados

## Características

- Login con nombre personalizado
- Ruleta de planes (en casa y de salida)
- Selector de fecha y hora
- Notificaciones por Telegram
- Diseño neón futurista

## Notas

Este proyecto desarrollado con asistencia de herramientas de IA (GitHub Copilot, Chatgpt, Gemini),con personalizaciones y ajustes específicos para la experiencia deseada.