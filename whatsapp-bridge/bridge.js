const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
console.log('Iniciando WhatsApp Bridge...');
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    }
});
const FASTAPI_URL = 'http://127.0.0.1:8000/webhook-local';
client.on('loading_screen', (percent, message) => {
    console.log(`Cargando WhatsApp Web: ${percent}% - ${message}`);
});
client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('Escanea el QR con tu WhatsApp');
});
client.on('authenticated', () => {
    console.log('Autenticado correctamente');
});
client.on('auth_failure', msg => {
    console.error('Error de autenticacion:', msg);
});
client.on('ready', () => {
    console.log('WhatsApp conectado!');
});
client.on('error', err => {
    console.error('Error en el bridge:', err.message);
});

function normalizarTelefono(num) {
    return num.replace('@c.us', '').replace('@lid', '').replace('@g.us', '').replace(/[^0-9]/g, '');
}

function esTelefonoValido(num) {
    const limpio = normalizarTelefono(num);
    return limpio.length >= 9 && limpio.length <= 12;
}

function esLid(valor) {
    return valor && valor.endsWith('@lid');
}

client.on('message', async msg => {
    if (msg.isGroup) return;
    if (msg.from.endsWith('@broadcast')) return;
    if (msg.from.endsWith('@newsletter')) return;
    if (!msg.body || msg.body.trim().length === 0) return;
    if (msg.body.length > 500) return;

    const contact = await msg.getContact();
    console.log(`[DEBUG] contact.number: "${contact.number}" | msg.from: "${msg.from}" | msg.author: "${msg.author}" | contact.name: "${contact.name}"`);

    let telefonoRaw = null;

    if (contact.number && esTelefonoValido(contact.number)) {
        telefonoRaw = contact.number;
        console.log(`[DEBUG] Fuente: contact.number`);
    }

    if (!telefonoRaw && msg.author && !esLid(msg.author)) {
        const authorLimpio = normalizarTelefono(msg.author);
        if (authorLimpio.length >= 9 && authorLimpio.length <= 12) {
            telefonoRaw = authorLimpio;
            console.log(`[DEBUG] Fuente: msg.author`);
        }
    }

    if (!telefonoRaw && msg.from && !esLid(msg.from)) {
        const fromLimpio = normalizarTelefono(msg.from);
        if (fromLimpio.length >= 9 && fromLimpio.length <= 12) {
            telefonoRaw = fromLimpio;
            console.log(`[DEBUG] Fuente: msg.from`);
        }
    }

    if (!telefonoRaw) {
        telefonoRaw = msg.from;
        console.log(`[DEBUG] Fuente: msg.from (fallback final)`);
    }

    let telefono;
    if (telefonoRaw && !esLid(telefonoRaw) && normalizarTelefono(telefonoRaw).length >= 9) {
        telefono = normalizarTelefono(telefonoRaw).slice(-9);
    } else {
        telefono = normalizarTelefono(telefonoRaw);
        if (telefono.length > 9) {
            telefono = telefono.slice(-9);
        }
    }

    console.log(`[DEBUG] telefonoRaw: "${telefonoRaw}" | telefono (9 digitos): "${telefono}"`);

    if (telefono.length < 9) {
        console.log(`Ignorado (telefono muy corto): "${telefono}" de raw "${telefonoRaw}"`);
        return;
    }

    const texto = msg.body;
    console.log(`Mensaje de ${telefono}: ${texto}`);

    try {
        const res = await axios.post(FASTAPI_URL, {
            telefono: telefono,
            texto: texto
        });
        if (res.data.respuesta) {
            const delayMs = 2000 + Math.random() * 2000;
            await new Promise(resolve => setTimeout(resolve, delayMs));
            await msg.reply(res.data.respuesta);
        }
    } catch (err) {
        console.error('Error conectando con FastAPI:', err.message);
    }
});

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

client.initialize();
