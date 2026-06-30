// =============================================
//  EVENTBOT AI — api.js
//  Conexión fetch() → FastAPI Backend
//  Base URL: http://127.0.0.1:8000
// =============================================

const API_BASE = "http://127.0.0.1:8000";

async function apiFetch(endpoint, method = "GET", body = null) {
    const options = { method, headers: { "Content-Type": "application/json" } };
    if (body) options.body = JSON.stringify(body);
    try {
        const res = await fetch(`${API_BASE}${endpoint}`, options);
        if (!res.ok) throw new Error(`Error ${res.status}`);
        return await res.json();
    } catch (err) {
        console.error(`API Error [${method} ${endpoint}]:`, err);
        throw err;
    }
}

// ── CLIENTES ──────────────────────────────────
const ApiClientes = {
    listar:     ()          => apiFetch("/api/clientes"),
    obtener:    (id)        => apiFetch(`/api/clientes/${id}`),
    crear:      (data)      => apiFetch("/api/clientes", "POST", data),
    actualizar: (id, data)  => apiFetch(`/api/clientes/${id}`, "PUT", data),
    eliminar:   (id)        => apiFetch(`/api/clientes/${id}`, "DELETE")
};

// ── EVENTOS ───────────────────────────────────
const ApiEventos = {
    listar:     ()          => apiFetch("/api/eventos"),
    obtener:    (id)        => apiFetch(`/api/eventos/${id}`),
    crear:      (data)      => apiFetch("/api/eventos", "POST", data),
    actualizar: (id, data)  => apiFetch(`/api/eventos/${id}`, "PUT", data),
    eliminar:   (id)        => apiFetch(`/api/eventos/${id}`, "DELETE")
};

// ── RESERVAS ──────────────────────────────────
const ApiReservas = {
    listar:        ()           => apiFetch("/api/reservas"),
    obtener:       (id)         => apiFetch(`/api/reservas/${id}`),
    porCliente:    (clienteId)  => apiFetch(`/api/clientes/${clienteId}/reservas`),
    crear:         (data)       => apiFetch("/api/reservas", "POST", data),
    actualizar:    (id, data)   => apiFetch(`/api/reservas/${id}`, "PUT", data),
    eliminar:      (id)         => apiFetch(`/api/reservas/${id}`, "DELETE")
};

// ── PAGOS ─────────────────────────────────────
const ApiPagos = {
    listar:        ()           => apiFetch("/api/pagos"),
    obtener:       (id)         => apiFetch(`/api/pagos/${id}`),
    porReserva:    (reservaId)  => apiFetch(`/api/reservas/${reservaId}/pagos`),
    crear:         (data)       => apiFetch("/api/pagos", "POST", data),
    actualizar:    (id, data)   => apiFetch(`/api/pagos/${id}`, "PUT", data),
    eliminar:      (id)         => apiFetch(`/api/pagos/${id}`, "DELETE")
};

// ── PAQUETES ──────────────────────────────────
const ApiPaquetes = {
    listar:     ()          => apiFetch("/api/paquetes"),
    obtener:    (id)        => apiFetch(`/api/paquetes/${id}`),
    crear:      (data)      => apiFetch("/api/paquetes", "POST", data),
    actualizar: (id, data)  => apiFetch(`/api/paquetes/${id}`, "PUT", data),
    eliminar:   (id)        => apiFetch(`/api/paquetes/${id}`, "DELETE")
};

// ── PAQUETES-EVENTOS ──────────────────────────
const ApiPaquetesEventos = {
    listar:     ()      => apiFetch("/api/paquetes-eventos"),
    porEvento:  (id)    => apiFetch(`/api/eventos/${id}/paquetes`),
    crear:      (data)  => apiFetch("/api/paquetes-eventos", "POST", data),
    eliminar:   (id)    => apiFetch(`/api/paquetes-eventos/${id}`, "DELETE")
};

// ── DETALLE RESERVA ───────────────────────────
const ApiDetalleReserva = {
    listar:     ()      => apiFetch("/api/detalle-reserva"),
    porReserva: (id)    => apiFetch(`/api/reservas/${id}/detalle`),
    crear:      (data)  => apiFetch("/api/detalle-reserva", "POST", data)
};

// ── RECORDATORIOS (pendiente de implementar en backend) ───
const ApiRecordatorios = {
    listar:  async () => [],
    crear:   async () => {}
};

// ── CONVERSACIONES / MENSAJES (pendiente de implementar en backend) ──
const ApiMensajes = {
    listar:     async () => [],
    porCliente: async () => []
};

// ── USUARIOS (pendiente de implementar en backend) ────────
const ApiUsuarios = {
    listar: async () => [],
    crear:  async () => {},
    login:  async (data) => {
        // Login local mientras no existe el endpoint en el backend
        if (data.email === "admin@eventbot.pe" && data.password === "admin123") {
            return { idUsuario: 1, nombre: "Admin Sistema", email: data.email, rol: "admin", estado: "activo" };
        }
        return null;
    }
};

// ── STATUS ────────────────────────────────────
const ApiStatus = {
    check: async () => apiFetch("/api/clientes")
};

// ── HELPERS ───────────────────────────────────
function showToast(msg, tipo = "info") {
    const icons = { success: "✅", error: "❌", warning: "⚠️", info: "ℹ️" };
    const existing = document.querySelector(".eb-toast");
    if (existing) existing.remove();
    const el = document.createElement("div");
    el.className = "eb-toast";
    el.innerHTML = `<span>${icons[tipo]}</span><span>${msg}</span>`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 3500);
}

function formatMoney(n) {
    return "S/." + Number(n || 0).toLocaleString("es-PE", { minimumFractionDigits: 0 });
}
function formatDate(d) {
    if (!d) return "—";
    return new Date(d).toLocaleDateString("es-PE");
}
function getInitials(name) {
    if (!name) return "??";
    return name.split(" ").map(w => w[0]).join("").substring(0, 2).toUpperCase();
}