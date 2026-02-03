// Função global para carregar reservas
window.carregarReserva = function(tipo) {
    console.log('Carregando reserva:', tipo);
    const url = `/dashboard/content/reserva/${tipo}`;
    
    fetch(url)
        .then(response => response.text())
        .then(data => {
            console.log('Dados carregados');
            document.getElementById('solicitar-content-area').innerHTML = data;

            if (tipo === 'sala' && typeof window.inicializarReservaSalaForm === 'function') {
                window.inicializarReservaSalaForm();
            }

            if (tipo === 'veiculo' && typeof window.inicializarReservaVeiculoForm === 'function') {
                window.inicializarReservaVeiculoForm();
            }
        })
        .catch(error => console.error('Erro:', error));
};

// Inicializa interações da tela de Perfil (parcial carregado via SPA)
window.inicializarPerfil = function() {
    const container = document.getElementById('content-area');
    if (!container) return;

    const readonlyEl = container.querySelector('#perfil-readonly');
    const editEl = container.querySelector('#perfil-edit');
    const btnEditar = container.querySelector('#btn-editar-perfil');
    const btnCancelar = container.querySelector('#btn-cancelar-perfil');

    if (btnEditar && readonlyEl && editEl) {
        btnEditar.addEventListener('click', function() {
            readonlyEl.style.display = 'none';
            editEl.style.display = 'block';
        });
    }

    if (btnCancelar && readonlyEl && editEl) {
        btnCancelar.addEventListener('click', function() {
            editEl.style.display = 'none';
            readonlyEl.style.display = 'block';
        });
    }
};

window.inicializarAvisos = function() {
    const container = document.getElementById('content-area');
    if (!container) return;

    const form = container.querySelector('#avisos-form');
    const msgEl = container.querySelector('#avisos-msg');

    const setMsg = (text, type) => {
        if (!msgEl) return;
        msgEl.style.display = 'block';
        msgEl.textContent = text;
        msgEl.classList.remove('alert-success', 'alert-error', 'alert-warning');
        if (type) msgEl.classList.add(`alert-${type}`);
    };

    // Form de criação (somente aprovador)
    if (form && form.dataset.initialized !== '1') {
        form.dataset.initialized = '1';
        form.addEventListener('submit', async function(e) {
        e.preventDefault();
        setMsg('Publicando...', 'warning');

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                credentials: 'same-origin',
                body: new FormData(form),
            });

            const payload = await readJsonPayload(response);
            if (payload.ok) {
                setMsg(payload.message || 'Aviso publicado.', 'success');
                const link = document.querySelector('.sidebar a[data-page="avisos"]');
                if (link) link.click();
            } else {
                setMsg(payload.message || 'Não foi possível publicar.', 'error');
                if (response.status === 401) window.location.href = '/';
            }
        } catch (err) {
            console.error(err);
            setMsg('Erro ao publicar. Tente novamente.', 'error');
        }
        });
    }

    // Ações por aviso (editar/apagar) - somente se os botões existirem
    container.querySelectorAll('.aviso-card').forEach(card => {
        if (card.dataset.initialized === '1') return;
        card.dataset.initialized = '1';

        const avisoId = card.dataset.avisoId;
        const btnEditar = card.querySelector('.js-editar-aviso');
        const btnApagar = card.querySelector('.js-apagar-aviso');

        if (btnEditar) {
            btnEditar.addEventListener('click', async () => {
                const tituloAtual = card.dataset.avisoTitulo || '';
                const mensagemAtual = card.dataset.avisoMensagem || '';
                const tipoAtual = (card.dataset.avisoTipo || 'info').toLowerCase();

                const novoTitulo = window.prompt('Título do aviso:', tituloAtual);
                if (novoTitulo === null) return;

                const novaMensagem = window.prompt('Mensagem do aviso:', mensagemAtual);
                if (novaMensagem === null) return;

                const novoTipo = window.prompt(
                    'Tipo (info / important / warning / success):',
                    tipoAtual
                );
                if (novoTipo === null) return;

                setMsg('Atualizando...', 'warning');
                try {
                    const response = await fetch(`/dashboard/api/avisos/${avisoId}/editar`, {
                        method: 'POST',
                        credentials: 'same-origin',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            titulo: novoTitulo,
                            mensagem: novaMensagem,
                            tipo: novoTipo,
                        }),
                    });
                    const payload = await readJsonPayload(response);
                    if (payload.ok) {
                        setMsg(payload.message || 'Aviso atualizado.', 'success');
                        const link = document.querySelector('.sidebar a[data-page="avisos"]');
                        if (link) link.click();
                    } else {
                        setMsg(payload.message || 'Não foi possível atualizar.', 'error');
                        if (response.status === 401) window.location.href = '/';
                    }
                } catch (err) {
                    console.error(err);
                    setMsg('Erro ao atualizar. Tente novamente.', 'error');
                }
            });
        }

        if (btnApagar) {
            btnApagar.addEventListener('click', async () => {
                const ok = window.confirm('Tem certeza que deseja apagar este aviso?');
                if (!ok) return;

                setMsg('Apagando...', 'warning');
                try {
                    const response = await fetch(`/dashboard/api/avisos/${avisoId}/apagar`, {
                        method: 'POST',
                        credentials: 'same-origin',
                    });
                    const payload = await readJsonPayload(response);
                    if (payload.ok) {
                        setMsg(payload.message || 'Aviso apagado.', 'success');
                        const link = document.querySelector('.sidebar a[data-page="avisos"]');
                        if (link) link.click();
                    } else {
                        setMsg(payload.message || 'Não foi possível apagar.', 'error');
                        if (response.status === 401) window.location.href = '/';
                    }
                } catch (err) {
                    console.error(err);
                    setMsg('Erro ao apagar. Tente novamente.', 'error');
                }
            });
        }
    });
};

async function readJsonPayload(response) {
    const contentType = response.headers.get('content-type') || '';
    if (contentType.includes('application/json')) {
        return await response.json();
    }
    const text = await response.text();
    return {
        ok: response.ok,
        message: text || `Erro ${response.status}`,
    };
}

window.inicializarSolicitacoesPendentes = function() {
    const container = document.getElementById('content-area');
    if (!container) return;

    const msgEl = document.getElementById('solicitacoes-msg');
    const setMsg = (text, type) => {
        if (!msgEl) return;
        msgEl.style.display = 'block';
        msgEl.textContent = text;
        msgEl.classList.remove('alert-success', 'alert-error', 'alert-warning');
        if (type) msgEl.classList.add(`alert-${type}`);
    };

    container.querySelectorAll('.solicitacao-card').forEach(card => {
        if (card.dataset.initialized === '1') return;
        card.dataset.initialized = '1';

        const tipo = card.dataset.tipo;
        const id = card.dataset.id;

        const btnAprovar = card.querySelector('.js-aprovar');
        const btnRejeitar = card.querySelector('.js-rejeitar');

        if (btnAprovar) {
            btnAprovar.addEventListener('click', async () => {
                setMsg('Aprovando...', 'warning');
                try {
                    const response = await fetch(`/dashboard/api/reservas/${tipo}/${id}/aprovar`, {
                        method: 'POST',
                        credentials: 'same-origin',
                    });
                    const payload = await readJsonPayload(response);
                    if (payload.ok) {
                        setMsg(payload.message || 'Aprovado.', 'success');
                        const link = document.querySelector('.sidebar a[data-page="solicitacoes_pendentes"]');
                        if (link) link.click();
                    } else {
                        setMsg(payload.message || 'Não foi possível aprovar.', 'error');
                        if (response.status === 401) window.location.href = '/';
                    }
                } catch (err) {
                    console.error(err);
                    setMsg('Erro ao aprovar. Tente novamente.', 'error');
                }
            });
        }

        if (btnRejeitar) {
            btnRejeitar.addEventListener('click', async () => {
                const motivo = window.prompt('Informe o motivo da rejeição:');
                if (!motivo) {
                    setMsg('Rejeição cancelada (motivo vazio).', 'warning');
                    return;
                }

                setMsg('Rejeitando...', 'warning');
                try {
                    const response = await fetch(`/dashboard/api/reservas/${tipo}/${id}/rejeitar`, {
                        method: 'POST',
                        credentials: 'same-origin',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ motivo }),
                    });
                    const payload = await readJsonPayload(response);
                    if (payload.ok) {
                        setMsg(payload.message || 'Rejeitado.', 'success');
                        const link = document.querySelector('.sidebar a[data-page="solicitacoes_pendentes"]');
                        if (link) link.click();
                    } else {
                        setMsg(payload.message || 'Não foi possível rejeitar.', 'error');
                        if (response.status === 401) window.location.href = '/';
                    }
                } catch (err) {
                    console.error(err);
                    setMsg('Erro ao rejeitar. Tente novamente.', 'error');
                }
            });
        }
    });
};

window.inicializarReservaVeiculoForm = function() {
    const form = document.getElementById('reserva-veiculo-form');
    const msgEl = document.getElementById('reserva-veiculo-msg');
    if (!form) return;
    if (form.dataset.initialized === '1') return;
    form.dataset.initialized = '1';

    const setMsg = (text, type) => {
        if (!msgEl) return;
        msgEl.style.display = 'block';
        msgEl.textContent = text;
        msgEl.classList.remove('alert-success', 'alert-error', 'alert-warning');
        if (type) msgEl.classList.add(`alert-${type}`);
    };

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        setMsg('Enviando...', 'warning');

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                credentials: 'same-origin',
                body: new FormData(form),
            });

            const payload = await readJsonPayload(response);
            if (payload.ok) {
                setMsg(payload.message, 'success');
                form.reset();
            } else {
                setMsg(payload.message || 'Não foi possível enviar a solicitação.', 'error');
                if (response.status === 401) {
                    window.location.href = '/';
                }
            }
        } catch (err) {
            console.error(err);
            setMsg('Erro ao enviar. Tente novamente.', 'error');
        }
    });
};

window.inicializarReservaSalaForm = function() {
    const form = document.getElementById('reserva-sala-form');
    const msgEl = document.getElementById('reserva-sala-msg');
    if (!form) return;
    if (form.dataset.initialized === '1') return;
    form.dataset.initialized = '1';

    const setMsg = (text, type) => {
        if (!msgEl) return;
        msgEl.style.display = 'block';
        msgEl.textContent = text;
        msgEl.classList.remove('alert-success', 'alert-error', 'alert-warning');
        if (type) msgEl.classList.add(`alert-${type}`);
    };

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        setMsg('Enviando...', 'warning');

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                credentials: 'same-origin',
                body: new FormData(form),
            });

            const payload = await readJsonPayload(response);
            if (payload.ok) {
                setMsg(payload.message, 'success');
                form.reset();
            } else {
                setMsg(payload.message || 'Não foi possível enviar a solicitação.', 'error');
                if (response.status === 401) {
                    window.location.href = '/';
                }
            }
        } catch (err) {
            console.error(err);
            setMsg('Erro ao enviar. Tente novamente.', 'error');
        }
    });
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

                    if (page === 'solicitacoes_pendentes' && typeof window.inicializarSolicitacoesPendentes === 'function') {
                        window.inicializarSolicitacoesPendentes();
                    }

                    if (page === 'perfil' && typeof window.inicializarPerfil === 'function') {
                        window.inicializarPerfil();
                    }

                    if (page === 'avisos' && typeof window.inicializarAvisos === 'function') {
                        window.inicializarAvisos();
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
