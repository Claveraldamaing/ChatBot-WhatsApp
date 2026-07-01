// =============================================
//  EVENTBOT AI — auth.js
//  Manejo de sesión y login
// =============================================

const Auth = {

    // Guardar sesión
    setSession(usuario) {
        localStorage.setItem("eb_usuario", JSON.stringify(usuario));
    },

    // Obtener sesión
    getSession() {
        const data = localStorage.getItem("eb_usuario");
        return data ? JSON.parse(data) : null;
    },

    // Cerrar sesión
    logout() {
        localStorage.removeItem("eb_usuario");
        window.location.href = "../views/login.html";
    },

    // Verificar si está logueado
    require() {
        const session = this.getSession();
        if (!session) {
            window.location.href = "../views/login.html";
            return null;
        }
        return session;
    },

    // Iniciales del usuario
    getInitials() {
        const s = this.getSession();
        if (!s || !s.nombre) return "AD";
        return s.nombre.split(" ").map(w => w[0]).join("").substring(0, 2).toUpperCase();
    },

    // Nombre del usuario
    getNombre() {
        const s = this.getSession();
        return s ? s.nombre : "Admin";
    },

    // Rol del usuario
    getRol() {
        const s = this.getSession();
        return s ? s.rol : "admin";
    }
};

// Verificar API al cargar
async function verificarAPI() {
    const el = document.getElementById("apiStatus");
    if (!el) return;
    try {
        await ApiClientes.listar();
        el.className = "api-status online";
        el.innerHTML = '<span class="dot"></span> FastAPI online ✅';
    } catch {
        el.className = "api-status offline";
        el.innerHTML = '<span class="dot"></span> FastAPI offline ❌';
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
    if (rol) rol.textContent = Auth.getRol();
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