// =============================================
//  EVENTBOT AI — sidebar.js
//  Sidebar compartido para todas las páginas
// =============================================

function renderSidebar() {
    const pagina = window.location.pathname.split("/").pop().replace(".html", "");
    
    const nav = [
        { section: "Principal" },
        { page: "dashboard", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`, label: "Dashboard" },
        { section: "Gestión" },
        { page: "clientes", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87"/><path d="M16 3.13a4 4 0 010 7.75"/></svg>`, label: "Clientes" },
        { page: "eventos", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>`, label: "Eventos" },
        { page: "reservas", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/><rect x="9" y="3" width="6" height="4" rx="1"/><line x1="9" y1="12" x2="15" y2="12"/><line x1="9" y1="16" x2="13" y2="16"/></svg>`, label: "Reservas" },
        { page: "pagos", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><rect x="1" y="4" width="22" height="16" rx="2"/><line x1="1" y1="10" x2="23" y2="10"/></svg>`, label: "Pagos" },
        { section: "Seguimiento" },
        { page: "recordatorios", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>`, label: "Recordatorios" },
        { page: "conversaciones", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>`, label: "Conversaciones" },
        { section: "Sistema" },
        { page: "reportes", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`, label: "Reportes" },
        { page: "usuarios", icon: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>`, label: "Usuarios" },
    ];

    let navHTML = "";
    nav.forEach(item => {
        if (item.section) {
            navHTML += `<div class="eb-nav-section">${item.section}</div>`;
        } else {
            const isActive = pagina === item.page ? "active" : "";
            navHTML += `
                <a href="${item.page}.html" class="eb-nav-item ${isActive}" data-page="${item.page}">
                    ${item.icon}
                    ${item.label}
                </a>`;
        }
    });

    const html = `
        <aside class="eb-sidebar">
            <div class="eb-sidebar-logo">
                <h2>⚡ EventBot AI</h2>
                <span>Gestión de Eventos · Trujillo 2026</span>
            </div>
            <nav class="eb-nav">${navHTML}</nav>
            <div class="eb-sidebar-footer">
                <div class="eb-user">
                    <div class="eb-avatar" id="sidebarAvatar">AD</div>
                    <div class="eb-user-info">
                        <div class="eb-user-name" id="sidebarNombre">Admin</div>
                        <div class="eb-user-role" id="sidebarRol">admin</div>
                    </div>
                    <button onclick="Auth.logout()" title="Salir" class="eb-sidebar-logout">
                        <svg width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                    </button>
                </div>
            </div>
        </aside>`;

    const container = document.getElementById("sidebar");
    if (container) container.innerHTML = html;
}

// Inicializar todo al cargar la página
document.addEventListener("DOMContentLoaded", () => {
    renderSidebar();
    cargarUsuarioSidebar();
    verificarAPI();
});