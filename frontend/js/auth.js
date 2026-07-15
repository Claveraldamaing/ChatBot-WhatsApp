// =============================================
//  EVENTBOT AI — auth.js
//  Manejo de sesión y login (con expiración y token)
// =============================================

const SESSION_KEY = "eb_usuario";
const SESSION_LIFETIME_MS = 8 * 60 * 60 * 1000;   // 8 horas de vida máxima de sesión
const INACTIVITY_LIMIT_MS = 20 * 60 * 1000;       // 20 min sin actividad → cierre automático

const Auth = {

    // Guardar sesión. `usuario` = datos del backend, `token` = token emitido por el backend al hacer login.
    // IMPORTANTE: el backend debe validar credenciales y emitir este token de forma real.
    // Sin eso, esto solo mejora la higiene del frontend, no reemplaza la validación server-side.
    setSession(usuario, token) {
        const session = {
            usuario,
            token: token || null,
            iat: Date.now(),
            exp: Date.now() + SESSION_LIFETIME_MS
        };
        localStorage.setItem(SESSION_KEY, JSON.stringify(session));
        this._reiniciarInactividad();
    },

    // Obtener sesión. Si expiró, la limpia y devuelve null (fuerza login de nuevo).
    getSession() {
        const raw = localStorage.getItem(SESSION_KEY);
        if (!raw) return null;
        let session;
        try {
            session = JSON.parse(raw);
        } catch {
            localStorage.removeItem(SESSION_KEY);
            return null;
        }
        if (!session.exp || Date.now() > session.exp) {
            localStorage.removeItem(SESSION_KEY);
            return null;
        }
        return session;
    },

    // Devuelve solo los datos del usuario (compatibilidad con el resto de vistas)
    getUsuario() {
        const s = this.getSession();
        return s ? s.usuario : null;
    },

    // Token para enviar en las peticiones a la API (Authorization: Bearer ...)
    getToken() {
        const s = this.getSession();
        return s ? s.token : null;
    },

    // Cerrar sesión
    logout(mensaje) {
        if (!mensaje && !confirm("¿Estás seguro de cerrar sesión?")) return;
        localStorage.removeItem(SESSION_KEY);
        clearTimeout(this._inactividadTimer);
        const destino = "../views/login.html" + (mensaje ? `?msg=${encodeURIComponent(mensaje)}` : "");
        window.location.href = destino;
    },

    // Verificar si está logueado y la sesión no expiró. Si no, redirige a login.
    require() {
        const session = this.getSession();
        if (!session) {
            sessionStorage.setItem("eb_redirect", window.location.pathname);
            window.location.href = "../views/login.html";
            return null;
        }
        this._reiniciarInactividad();
        return session.usuario;
    },

    // Verifica si el usuario actual tiene alguno de los roles permitidos.
    // Uso: if (!Auth.hasRole(["admin"])) { Auth.logout(); }
    hasRole(rolesPermitidos) {
        const usuario = this.getUsuario();
        if (!usuario) return false;
        return rolesPermitidos.includes(usuario.rol);
    },

    // Iniciales del usuario
    getInitials() {
        const u = this.getUsuario();
        if (!u || !u.nombre) return "AD";
        return u.nombre.split(" ").map(w => w[0]).join("").substring(0, 2).toUpperCase();
    },

    // Nombre del usuario
    getNombre() {
        const u = this.getUsuario();
        return u ? u.nombre : "Admin";
    },

    // Rol del usuario
    getRol() {
        const u = this.getUsuario();
        return u ? u.rol : null;
    },

    // ── Cierre de sesión automático por inactividad ──────────────
    _inactividadTimer: null,
    _reiniciarInactividad() {
        clearTimeout(this._inactividadTimer);
        this._inactividadTimer = setTimeout(() => {
            this.logout("Tu sesión se cerró por inactividad");
        }, INACTIVITY_LIMIT_MS);
    },
    _iniciarListenersInactividad() {
        ["mousemove", "keydown", "click", "scroll"].forEach(evento => {
            window.addEventListener(evento, () => {
                if (this.getSession()) this._reiniciarInactividad();
            }, { passive: true });
        });
    }
};

Auth._iniciarListenersInactividad();

// Verificar API al cargar
async function verificarAPI() {
    const el = document.getElementById("apiStatus");
    if (!el) return;
    try {
        await ApiClientes.listar();
        el.className = "api-status online";
        el.innerHTML = '<span class="dot"></span> Sistema en línea ✅';
    } catch {
        el.className = "api-status offline";
        el.innerHTML = '<span class="dot"></span> Sin conexión ❌';
    }
}

// Cargar sidebar con usuario activo
function cargarUsuarioSidebar() {
    const avatar = document.getElementById("sidebarAvatar");
    const nombre = document.getElementById("sidebarNombre");
    const rol = document.getElementById("sidebarRol");
    const headerAvatar = document.getElementById("headerAvatar");

    if (avatar) avatar.textContent = Auth.getInitials();
    if (nombre) nombre.textContent = Auth.getNombre();
    if (rol) rol.textContent = Auth.getRol() || "—";
    if (headerAvatar) headerAvatar.textContent = Auth.getInitials();
}

// Marcar nav item activo
function marcarNavActivo() {
    const pagina = window.location.pathname.split("/").pop().replace(".html", "");
    document.querySelectorAll(".eb-nav-item").forEach(item => {
        item.classList.remove("active");
        if (item.dataset.page === pagina) item.classList.add("active");
    });
}