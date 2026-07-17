// =============================================
//  EVENTBOT AI — api.js
//  Conexión fetch() → FastAPI Backend
//  Base URL: http://127.0.0.1:8000
// =============================================

const API_BASE = localStorage.getItem("api_base") || "http://127.0.0.1:8000";

async function apiFetch(endpoint, method = "GET", body = null) {
    const headers = { "Content-Type": "application/json" };

    // Adjunta el token de sesión a toda petición (una vez que el backend lo valide, esto
    // habilita que cada endpoint pueda rechazar peticiones sin sesión o con sesión inválida).
    if (typeof Auth !== "undefined") {
        const token = Auth.getToken();
        if (token) headers["Authorization"] = `Bearer ${token}`;
    }

    const options = { method, headers };
    if (body) options.body = JSON.stringify(body);

    try {
        const res = await fetch(`${API_BASE}${endpoint}`, options);

        // Si el backend responde 401/403, la sesión ya no es válida del lado del servidor
        // (token vencido, revocado, etc.) → cerrar sesión local en vez de seguir como si nada.
        if ((res.status === 401 || res.status === 403) && typeof Auth !== "undefined") {
            Auth.logout("Tu sesión expiró o no es válida. Vuelve a iniciar sesión.");
            throw new Error(`No autorizado (${res.status})`);
        }

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
    eliminar:      (id)         => apiFetch(`/api/reservas/${id}`, "DELETE"),
    finalizarPago: (id)         => apiFetch(`/api/reservas/${id}/finalizar-pago`, "POST")
};

// ── PAGOS ─────────────────────────────────────
const ApiPagos = {
    listar:        ()           => apiFetch("/api/pagos"),
    obtener:       (id)         => apiFetch(`/api/pagos/${id}`),
    porReserva:    (reservaId)  => apiFetch(`/api/reservas/${reservaId}/pagos`),
    crear:         (data)       => apiFetch("/api/pagos", "POST", data),
    actualizar:    (id, data)   => apiFetch(`/api/pagos/${id}`, "PUT", data),
    confirmar:     (id)         => apiFetch(`/api/pagos/${id}/confirmar`, "PUT"),
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

// ── RECORDATORIOS ──────────────────────────────
const ApiRecordatorios = {
    listar:     ()          => apiFetch("/api/recordatorios"),
    obtener:    (id)        => apiFetch(`/api/recordatorios/${id}`),
    crear:      (data)      => apiFetch("/api/recordatorios", "POST", data),
    actualizar: (id, data)  => apiFetch(`/api/recordatorios/${id}`, "PUT", data),
    eliminar:   (id)        => apiFetch(`/api/recordatorios/${id}`, "DELETE"),
    generar:    (reservaId) => apiFetch(`/api/recordatorios/generar-para-reserva/${reservaId}`, "POST"),
    pendientes: ()          => apiFetch("/api/recordatorios/pendientes-para-enviar")
};

// ── MENSAJES IA ────────────────────────────────
const ApiMensajes = {
    listar:        ()         => apiFetch("/api/mensajes-ia"),
    porCliente:    (id)       => apiFetch(`/api/clientes/${id}/mensajes`),
    estadisticas:  async ()   => ({})
};

// ── USUARIOS ───────────────────────────────────
const ApiUsuarios = {
    listar:     ()          => apiFetch("/api/usuarios"),
    crear:      (data)      => apiFetch("/api/usuarios", "POST", data),
    actualizar: (id, data)  => apiFetch(`/api/usuarios/${id}`, "PUT", data),

    // CRÍTICO: el login ya NO valida nada en el frontend. Se envía email/contraseña
    // al backend, y es el backend quien debe:
    //   1) buscar el usuario por email
    //   2) comparar la contraseña contra el hash guardado (bcrypt/argon2, nunca texto plano)
    //   3) si es válido, emitir un token (JWT firmado, con expiración corta)
    //   4) devolver { usuario: {...sin password...}, token: "..." }
    // Mientras ese endpoint no exista en el backend, el login fallará (comportamiento correcto:
    // "cerrado por defecto" en vez de aceptar cualquier contraseña).
    login: (data) => apiFetch("/api/auth/login", "POST", data)
};

// ── FORMULARIOS (pendiente de implementar en backend) ─────
const ApiFormularios = {
    listar: async () => []
};

// ── DASHBOARD ──────────────────────────────────
const ApiDashboard = {
    stats: () => apiFetch("/api/dashboard/stats")
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
    const spanIcon = document.createElement("span");
    spanIcon.textContent = icons[tipo] || "";
    const spanMsg = document.createElement("span");
    spanMsg.textContent = msg;
    el.appendChild(spanIcon);
    el.appendChild(spanMsg);
    document.body.appendChild(el);
    setTimeout(() => {
        el.classList.add("eb-toast--out");
        setTimeout(() => el.remove(), 250);
    }, 3500);
}

function formatMoney(n) {
    return "S/." + Number(n || 0).toLocaleString("es-PE", { minimumFractionDigits: 0 });
}
function formatDate(d) {
    if (!d) return "—";
    const date = new Date(d);
    if (isNaN(date.getTime())) return "—";
    return date.toLocaleDateString("es-PE");
}
function getInitials(name) {
    if (!name) return "??";
    return name.split(" ").map(w => w[0]).join("").substring(0, 2).toUpperCase();
}