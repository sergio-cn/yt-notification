# YouTube → Telegram Notifier

Bot que avisa en tu canal de Telegram cada vez que subes un video a YouTube.

## Configuración

### 1. Crea el bot de Telegram
1. Abre [@BotFather](https://t.me/BotFather) en Telegram
2. Escribe `/newbot` y sigue los pasos
3. Copia el **token** que te da

### 2. Añade el bot a tu canal
1. Ve a tu canal @en_solitario
2. Ajustes → Administradores → Añadir administrador
3. Busca tu bot y dale permiso para **publicar mensajes**

### 3. Guarda el token en GitHub
1. Ve a tu repo → Settings → Secrets and variables → Actions
2. Clic en **New repository secret**
3. Nombre: `TELEGRAM_TOKEN`
4. Valor: el token que te dio BotFather

### 4. Activa GitHub Actions
1. Ve a la pestaña **Actions** de tu repo
2. Si te pide activarla, acéptalo
3. Listo, se ejecutará automáticamente cada 15 minutos

## Seguridad
- El token **nunca** está en el código, solo en los Secrets de GitHub
- El canal de YouTube está hardcodeado: solo puede publicar videos de tu canal
- Nadie externo tiene acceso a tus credenciales
