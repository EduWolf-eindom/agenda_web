document.addEventListener("DOMContentLoaded", init);

/* ====================================================
   DOM ELEMENTOS
==================================================== */
const el = {
  calendar: document.getElementById("calendar"),
  modal: document.getElementById("eventModal"),
  modalTitle: document.getElementById("modalTitle"),

  eventId: document.getElementById("eventId"),
  cliente: document.getElementById("eventCliente"),
  contrato: document.getElementById("eventContrato"),
  assunto: document.getElementById("eventAssunto"),
  fase: document.getElementById("eventFase"),
  situacao: document.getElementById("eventSituacao"),
  descricao: document.getElementById("eventDescricao"),
  start: document.getElementById("eventStart"),

  btnSave: document.getElementById("saveEvent"),
  btnDelete: document.getElementById("deleteEvent"),
  btnCancel: document.getElementById("cancelEvent"),

  dropdown: document.getElementById("clienteDropdown"),

  listView: document.getElementById("listView"),
  listContent: document.getElementById("listContent"),
  listTitle: document.getElementById("listTitle"),

  btnCalendar: document.getElementById("btnCalendar"),
  btnListDay: document.getElementById("btnListDay"),
  btnListWeek: document.getElementById("btnListWeek")
};

let calendar;

/* ====================================================
   UTILIDADES
==================================================== */
function debounce(fn, delay = 400) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(null, args), delay);
  };
}

function show(el) { el.classList.remove("hidden"); }
function hide(el) { el.classList.add("hidden"); }

function fetchJSON(url) {
  return fetch(url).then(r => r.json());
}

/* ====================================================
   CATÁLOGOS (ASSUNTO / FASE / SITUAÇÃO)
==================================================== */
function loadCatalog(url, selectEl) {
  fetchJSON(url).then(items => {
    selectEl.innerHTML = "<option value=''>SELECIONE</option>";
    items.forEach(i => {
      const opt = document.createElement("option");
      opt.value = i.id;
      opt.textContent = i.nome;
      selectEl.appendChild(opt);
    });
  });
}

/* ====================================================
   AUTOCOMPLETE DE CONTRATOS
==================================================== */
function renderDropdown(contratos) {
  el.dropdown.innerHTML = "";

  if (!contratos.length) {
    el.dropdown.innerHTML =
      "<div class='autocomplete-empty'>Nenhum contrato encontrado</div>";
    show(el.dropdown);
    return;
  }

  contratos.forEach(c => {
    const item = document.createElement("div");
    item.className = "autocomplete-item";
    item.textContent = c;
    item.onclick = () => {
      el.contrato.innerHTML = `<option value="${c}" selected>${c}</option>`;
      hide(el.dropdown);
    };
    el.dropdown.appendChild(item);
  });

  show(el.dropdown);
}

const buscarContratos = debounce(() => {
  const cliente = el.cliente.value.trim().toUpperCase();
  if (cliente.length < 3) return hide(el.dropdown);

  fetchJSON(`/api/agenda/contratos?cliente=${encodeURIComponent(cliente)}`)
    .then(renderDropdown);
});

/* ====================================================
   MODAL
==================================================== */
function openModal(data = {}) {
  el.eventId.value = data.id || "";
  el.cliente.value = data.cliente || "";
  el.start.value = data.start || "";
  el.assunto.value = data.assunto_id || "";
  el.fase.value = data.fase_id || "";
  el.situacao.value = data.situacao_id || "";
  el.descricao.value = data.descricao || "";

  el.contrato.innerHTML = "<option value=''>SELECIONE</option>";

  el.modalTitle.textContent = data.id
    ? "Editar Compromisso"
    : "Novo Compromisso";

  el.btnDelete.style.display = data.id ? "inline-block" : "none";
  show(el.modal);

  if (data.cliente) {
    fetchJSON(`/api/agenda/contratos?cliente=${encodeURIComponent(data.cliente)}`)
      .then(contratos => {
        renderDropdown(contratos);
        setTimeout(() => {
          el.contrato.value = data.contrato;
        }, 300);
      });
  }
}

function closeModal() {
  hide(el.modal);
}

/* ====================================================
   CALENDÁRIO
==================================================== */
function initCalendar() {
  calendar = new FullCalendar.Calendar(el.calendar, {
    locale: "pt-br",
    timeZone: "local",

    initialView: "dayGridMonth",

    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay"
    },

    slotDuration: "00:10:00",
    snapDuration: "00:10:00",
    allDaySlot: false,
    nowIndicator: true,
    editable: true,

    events: "/api/agenda",

    dateClick(info) {
      openModal({
        start: info.dateStr.length === 10
          ? info.dateStr + "T08:00"
          : info.date.toISOString().slice(0, 16)
      });
    },

    eventClick(info) {
      openModal({
        id: info.event.id,
        start: info.event.startStr.slice(0, 16),
        cliente: info.event.extendedProps?.cliente_nome,
        contrato: info.event.extendedProps?.contrato_numero,
        assunto_id: info.event.extendedProps?.assunto_id,
        fase_id: info.event.extendedProps?.fase_id,
        situacao_id: info.event.extendedProps?.situacao_id,
        descricao: info.event.extendedProps?.descricao
      });
    },

    eventDrop(info) {
      fetch(`/api/agenda/${info.event.id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          start_time: info.event.startStr
        })
      }).catch(() => info.revert());
    }
  });

  calendar.render();
}

/* ====================================================
   LIST VIEW (DIÁRIA / SEMANAL)
==================================================== */
function renderList(mode) {
  const events = calendar.getEvents();
  el.listContent.innerHTML = "";

  hide(el.calendar);
  show(el.listView);

  const today = calendar.getDate();
  const start = new Date(today);
  const end = new Date(today);

  if (mode === "day") {
    el.listTitle.textContent = "📋 LISTA DIÁRIA";
  } else {
    el.listTitle.textContent = "📋 LISTA SEMANAL";
    end.setDate(start.getDate() + 6);
  }

  const filtered = events.filter(ev => {
    const d = ev.start;
    return mode === "day"
      ? d.toDateString() === today.toDateString()
      : d >= start && d <= end;
  });

  if (!filtered.length) {
    el.listContent.innerHTML = "<p>SEM COMPROMISSOS.</p>";
    return;
  }

  const grouped = {};
  filtered.forEach(e => {
    const key = e.start.toDateString();
    grouped[key] = grouped[key] || [];
    grouped[key].push(e);
  });

  Object.entries(grouped).forEach(([day, items]) => {
    const box = document.createElement("div");
    box.className = "list-day";

    const title = document.createElement("h3");
    title.textContent = day;
    box.appendChild(title);

    items.sort((a, b) => a.start - b.start).forEach(ev => {
      const item = document.createElement("div");
      item.className = "list-item";
      item.innerHTML = `
        <span class="list-time">
          ${ev.start.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
        </span>
        ${ev.title}
      `;
      item.onclick = () =>
        openModal({ id: ev.id, start: ev.startStr.slice(0, 16) });
      box.appendChild(item);
    });

    el.listContent.appendChild(box);
  });
}

/* ====================================================
   INIT
==================================================== */
function init() {
  loadCatalog("/api/catalogos/assuntos", el.assunto);
  loadCatalog("/api/catalogos/fases", el.fase);
  loadCatalog("/api/catalogos/situacoes", el.situacao);

  el.cliente.addEventListener("input", buscarContratos);
  el.btnCancel.onclick = closeModal;

  el.btnCalendar.onclick = () => {
    hide(el.listView);
    show(el.calendar);
  };

  el.btnListDay.onclick = () => renderList("day");
  el.btnListWeek.onclick = () => renderList("week");

  document.addEventListener("click", e => {
    if (!e.target.closest(".autocomplete-wrapper")) {
      hide(el.dropdown);
    }
  });

  el.btnSave.onclick = () => {
    const payload = {
      cliente_nome: el.cliente.value,
      contrato_numero: el.contrato.value,
      assunto_id: el.assunto.value || null,
      fase_id: el.fase.value || null,
      situacao_id: el.situacao.value || null,
      descricao: el.descricao.value,
      start_time: el.start.value
    };

    const id = el.eventId.value;
    const method = id ? "PUT" : "POST";
    const url = id ? `/api/agenda/${id}` : "/api/agenda";

    fetch(url, {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(() => {
      calendar.refetchEvents();
      closeModal();
    });
  };

  el.btnDelete.onclick = () => {
    if (!el.eventId.value) return;
    if (!confirm("Excluir este compromisso?")) return;

    fetch(`/api/agenda/${el.eventId.value}`, { method: "DELETE" })
      .then(() => {
        calendar.refetchEvents();
        closeModal();
      });
  };

  initCalendar();
}
