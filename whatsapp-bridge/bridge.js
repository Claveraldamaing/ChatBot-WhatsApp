const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');

const FASTAPI_URL = 'http://127.0.0.1:8000/webhook-local';
let client = null;
let reconnectAttempts = 0;
const MAX_RECONNECT_ATTEMPTS = 10;
const BASE_RECONNECT_DELAY = 5000;

function crearClient() {
    const c = new Client({
        authStrategy: new LocalAuth(),
        puppeteer: {
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
        }
    });

    c.on('loading_screen', (percent, message) => {
        console.log(`Cargando WhatsApp Web: ${percent}% - ${message}`);
    });

    c.on('qr', qr => {
        qrcode.generate(qr, { small: true });
        console.log('Escanea el QR con tu WhatsApp');
    });

    c.on('authenticated', () => {
        console.log('Autenticado correctamente');
    });

    c.on('auth_failure', msg => {
        console.error('Error de autenticacion:', msg);
    });

    c.on('ready', () => {
        console.log('WhatsApp conectado!');
        reconnectAttempts = 0;
    });

    c.on('disconnected', reason => {
        console.log(`[BRIDGE] Desconectado: ${reason}`);
        reconectar();
    });

    c.on('error', err => {
        console.error('Error en el bridge:', err.message);
        if (err.message.includes('Execution context was destroyed') ||
            err.message.includes('Target closed') ||
            err.message.includes('Session closed')) {
            console.log('[BRIDGE] Error de Puppeteer detectado, reconectando...');
            reconectar();
        }
    });

    registrarHandlerMensajes(c);

    return c;
}

function reconectar() {
    if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
        console.error(`[BRIDGE] Maximo de reconexiones alcanzado (${MAX_RECONNECT_ATTEMPTS}). Deteniendo.`);
        process.exit(1);
    }
    reconnectAttempts++;
    const delay = BASE_RECONNECT_DELAY * Math.pow(1.5, reconnectAttempts - 1);
    console.log(`[BRIDGE] Reconectando en ${Math.round(delay / 1000)}s (intento ${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})...`);
    setTimeout(() => {
        try {
            if (client) {
                client.destroy().catch(() => {});
            }
        } catch (e) {}
        client = crearClient();
        client.initialize().catch(err => {
            console.error('[BRIDGE] Error al inicializar:', err.message);
            reconectar();
        });
    }, delay);
}

function normalizarTelefono(num) {
    return num.replace('@c.us', '').replace('@lid', '').replace('@g.us', '').replace(/[^0-9]/g, '');
}

function extraerTelefono(msg, contact) {
    const fuentes = [
        { nombre: 'msg.from', valor: msg.from },
        { nombre: 'msg.author', valor: msg.author },
        { nombre: 'contact.number', valor: contact.number },
    ];

    for (const fuente of fuentes) {
        if (!fuente.valor) continue;
        if (fuente.valor.includes('@lid')) continue;
        const limpio = normalizarTelefono(fuente.valor);

        if (limpio.length >= 9 && limpio.length <= 12) {
            console.log(`[DEBUG] Fuente: ${fuente.nombre} → "${limpio}"`);
            return limpio.slice(-9);
        }
    }

    if (msg.from && !msg.from.includes('@lid')) {
        const fallback = normalizarTelefono(msg.from);
        if (fallback.length >= 9) {
            console.log(`[DEBUG] Fuente: fallback msg.from → "${fallback}"`);
            return fallback.length > 9 ? fallback.slice(-9) : fallback;
        }
    }

    console.log(`[DEBUG] No se pudo extraer telefono de ninguna fuente`);
    return null;
}

function registrarHandlerMensajes(c) {
    c.on('message', async msg => {
        try {
            if (msg.isGroup) return;
            if (msg.from.endsWith('@broadcast')) return;
            if (msg.from.endsWith('@newsletter')) return;
            if (!msg.body || msg.body.trim().length === 0) return;
            if (msg.body.length > 500) return;

            const contact = await msg.getContact();
            console.log(`[DEBUG] contact.number: "${contact.number}" | msg.from: "${msg.from}" | msg.author: "${msg.author}" | contact.name: "${contact.name}"`);

            const telefono = extraerTelefono(msg, contact);

            let telefonoEnvio = telefono;
            if (!telefono) {
                const raw = msg.from || '';
                telefonoEnvio = raw.replace('@lid', '').replace('@c.us', '').replace(/[^0-9]/g, '');
                if (telefonoEnvio.length < 9) {
                    console.log(`[LID] No se pudo extraer telefono ni LID valido`);
                    return;
                }
                console.log(`[LID] Enviando LID como telefono: ${telefonoEnvio}`);
            }

            console.log(`Mensaje de ${telefonoEnvio}: ${msg.body}`);

            const res = await axios.post(FASTAPI_URL, {
                telefono: telefonoEnvio,
                texto: msg.body
            });
            if (res.data.respuesta) {
                const delayMs = 2000 + Math.random() * 2000;
                await new Promise(resolve => setTimeout(resolve, delayMs));
                await msg.reply(res.data.respuesta);
            }
        } catch (err) {
            console.error('Error procesando mensaje:', err.message);
        }
    });
}

const http = require('http');
const BRIDGE_PORT = 8001;

const server = http.createServer(async (req, res) => {
    if (req.method === 'POST' && req.url === '/send') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', async () => {
            try {
                const { telefono, texto } = JSON.parse(body);
                const chatId = telefono.replace(/[^0-9]/g, '') + '@c.us';
                await client.sendMessage(chatId, texto);
                console.log(`[SCHEDULER] Mensaje enviado a ${telefono}: ${texto}`);
                res.writeHead(200, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ ok: true }));
            } catch (err) {
                console.error('Error enviando mensaje:', err.message);
                res.writeHead(500, { 'Content-Type': 'application/json' });
                res.end(JSON.stringify({ ok: false, error: err.message }));
            }
        });
    } else {
        res.writeHead(404);
        res.end();
    }
});

server.listen(BRIDGE_PORT, () => {
    console.log(`Bridge HTTP server en puerto ${BRIDGE_PORT}`);
});

process.on('uncaughtException', err => {
    console.error('[BRIDGE] Excepcion no capturada:', err.message);
    if (err.message.includes('Execution context') ||
        err.message.includes('Target closed') ||
        err.message.includes('Session closed')) {
        reconectar();
    }
});

process.on('unhandledRejection', reason => {
    console.error('[BRIDGE] Promesa rechazada:', reason);
});

client = crearClient();
client.initialize().catch(err => {
    console.error('[BRIDGE] Error al inicializar:', err.message);
    reconectar();
});
