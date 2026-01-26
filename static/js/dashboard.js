// Função global para carregar reservas
window.carregarReserva = function(tipo) {
    console.log('Carregando reserva:', tipo);
    const url = `/dashboard/content/reserva/${tipo}`;
    
    fetch(url)
        .then(response => response.text())
        .then(data => {
            console.log('Dados carregados');
            document.getElementById('solicitar-content-area').innerHTML = data;
        })
        .catch(error => console.error('Erro:', error));
};

document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('.sidebar');
    const contentArea = document.getElementById('content-area');

    sidebar.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && e.target.dataset.page) {
            e.preventDefault();
            
            const page = e.target.dataset.page;
            const url = `/dashboard/content/${page}`;
            
            // Remover ativa de todos os links
            sidebar.querySelectorAll('a').forEach(link => {
                link.classList.remove('active');
            });
            
            // Adicionar ativa ao link clicado
            e.target.classList.add('active');
            
            // Carregar conteúdo
            fetch(url)
                .then(response => response.text())
                .then(data => {
                    contentArea.innerHTML = data;
                    
                    // Se for a página de solicitação de reserva, inicializar o script
                    if (page === 'solicitar_reserva' && typeof inicializarSolicitarReserva !== 'undefined') {
                        inicializarSolicitarReserva();
                    }
                })
                .catch(error => console.error('Erro ao carregar página:', error));
        }
    });

    // Carregar home por padrão
    const homeLink = sidebar.querySelector('a[data-page="home"]');
    if (homeLink) {
        homeLink.click();
    }
});
