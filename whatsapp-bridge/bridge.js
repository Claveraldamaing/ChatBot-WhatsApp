const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const axios = require('axios');
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { headless: true }
});
const FASTAPI_URL = 'http://127.0.0.1:8000/webhook-local';
client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
    console.log('Escanea el QR con tu WhatsApp');
});
client.on('ready', () => {
    console.log('WhatsApp conectado!');
});
client.on('message', async msg => {
    if (msg.from.endsWith('@broadcast') || msg.from.endsWith('@g.us')) return;
    const contact = await msg.getContact();
    if (contact.isMyContact) {
        console.log(`Ignorado (contacto guardado): ${msg.from}`);
        return;
    }
    const telefono = msg.from.replace('@c.us', '').replace('@lid', '');
    const texto = msg.body;
    console.log(`Mensaje de ${telefono}: ${texto}`);
    try {
        const res = await axios.post(FASTAPI_URL, {
            telefono: telefono,
            texto: texto
        });
        if (res.data.respuesta) {
            await msg.reply(res.data.respuesta);
        }
    } catch (err) {
        console.error('Error conectando con FastAPI:', err.message);
    }
});
client.initialize();