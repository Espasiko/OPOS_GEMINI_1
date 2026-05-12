---
description: Compila el fork BMO Chandra Edition y despliega main.js + styles.css al vault de Obsidian con backup previo. Hay que recargar el plugin en Obsidian (Settings → Community plugins → disable/enable BMO) para que cargue el nuevo código.
---

1. Build de producción del fork:
// turbo
```bash
cd /home/spas/obsidian-bmo-chatbot-plus && npm run build
```

2. Backup del main.js actual del vault (con timestamp):
// turbo
```bash
cp /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/.obsidian/plugins/bmo-chatbot/main.js \
   /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/.obsidian/plugins/bmo-chatbot/main.js.backup-$(date +%Y%m%d-%H%M%S)
```

3. Copiar main.js y styles.css al plugin instalado:
// turbo
```bash
cp /home/spas/obsidian-bmo-chatbot-plus/main.js \
   /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/.obsidian/plugins/bmo-chatbot/main.js && \
cp /home/spas/obsidian-bmo-chatbot-plus/styles.css \
   /mnt/d/BOVEDA_OPOS/BOVEDA_OPOS/.obsidian/plugins/bmo-chatbot/styles.css
```

4. Recargar en Obsidian (manual): Settings → Community plugins → desactivar **BMO Chatbot** → activarlo de nuevo. O `Ctrl+P` → `Reload app without saving`.

5. Verificar en consola Obsidian (`Ctrl+Shift+I`):
   - Logs `[BMO Chandra]` indican actividad del módulo multi-chat.
   - Nueva carpeta en el vault: `BMO/Chats/Chandra_Opos/<fecha>__<slug>__<id>.md`.
   - Tras un mensaje user + respuesta bot → archivo renombrado automáticamente con título generado.
