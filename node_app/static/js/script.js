const navbarToggle = document.querySelector('.navbar-toggle');
const navbarMenu = document.querySelector('.navbar-menu');
let yearMode = false;


navbarToggle.addEventListener('click', () => {
    navbarToggle.classList.toggle('active');
    navbarMenu.classList.toggle('active');
});

// document.querySelector('.toggle-password').addEventListener('click', function () {
//   const input = document.getElementById('password');
//   const showing = input.type === 'text';

//   input.type = showing ? 'password' : 'text';
//   this.classList.toggle('showing', !showing);
//   this.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
// });

document.querySelectorAll('.toggle-password').forEach(button => {
  button.addEventListener('click', function () {
    const field = this.closest('.password-field');
    const input = field.querySelector('input');
    const showing = input.type === 'text';

    input.type = showing ? 'password' : 'text';
    this.classList.toggle('showing', !showing);
    this.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
  });
});

// This is an IIIFE function - Immediately Invoked Function Expression.
(function () {
  const cal = document.getElementById("cal");
  if (!cal) return;

  const colors = ["#1bbe1b", "#a10f0f", "#df8c11", "#c5b73b", "#e0e0e0"];
  const dayNames = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
  let year, month;
  let yearMode = false;
  let currentYear = new Date().getFullYear();

  function load() {
    const saved = localStorage.getItem("calendar-colors");
    return saved ? JSON.parse(saved) : {};
  }
  function save(data) {
    localStorage.setItem("calendar-colors", JSON.stringify(data));
  }

  function render() {
    const title = document.getElementById("title");
    title.textContent = new Date(year, month).toLocaleString(undefined, { month: "long", year: "numeric" });

    cal.innerHTML = "";
    dayNames.forEach(d => {
      const el = document.createElement("div");
      el.className = "day-name";
      el.textContent = d;
      cal.appendChild(el);
    });

    const first = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const daysInPrev = new Date(year, month, 0).getDate();
    const data = load();

    for (let i = 0; i < 42; i++) {
      const el = document.createElement("div");
      el.className = "day";
      let date, key, isOther = false;

      if (i < first) {
        date = daysInPrev - first + 1 + i;
        isOther = true;
      } else if (i >= first + daysInMonth) {
        date = i - first - daysInMonth + 1;
        isOther = true;
      } else {
        date = i - first + 1;
        key = `${year}-${month + 1}-${date}`;
      }

      el.textContent = date;
      if (isOther) {
        el.classList.add("other");
      } else {
        el.style.background = data[key] || "#e0e0e0";
        el.onclick = () => {
          const current = data[key] || "#e0e0e0";
          const next = colors[(colors.indexOf(current) + 1) % colors.length];
          data[key] = next;
          save(data);
          el.style.background = next;

          fetch("/admin/calendar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ day: key, color: next })
          });
        };
      }
      cal.appendChild(el);
    }
  }

  document.getElementById("prev").onclick = () => {
    month--;
    if (month < 0) { month = 11; year--; }
    render();
  };
  document.getElementById("next").onclick = () => {
    month++;
    if (month > 11) { month = 0; year++; }
    render();
  };
  document.getElementById("clear").onclick = () => {
    localStorage.removeItem("calendar-colors");
    render();
  };
  document.getElementById("year-btn").addEventListener("click", async () => {
    yearMode = !yearMode;
    const yearView = document.getElementById("year-view");
    const monthView = document.getElementById("month-view"); // your existing calendar

    if (yearMode) {
      monthView.style.display = "none";
      yearView.style.display = "block";
      await renderYear(currentYear);
    } else {
      yearView.style.display = "none";
      monthView.style.display = "block";
    }
  });

  const now = new Date();
  year = now.getFullYear();
  month = now.getMonth();
  render();
})();

async function showYear(year) {
  const res = await fetch(`/admin/calendar/year/${year}`);
  const days = await res.json();
  const map = Object.fromEntries(days.map(d => [d.day, d.color]));

  const container = document.getElementById("year-view");
  container.innerHTML = "";

  for (let m = 0; m < 12; m++) {
    const monthEl = document.createElement("div");
    monthEl.className = "year-month";

    const title = document.createElement("div");
    title.textContent = new Date(year, m).toLocaleString(undefined, { month: "short" });
    monthEl.appendChild(title);

    const daysInMonth = new Date(year, m + 1, 0).getDate();
    for (let d = 1; d <= daysInMonth; d++) {
      const key = `${year}-${String(m + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
      const cell = document.createElement("div");
      cell.className = "year-day";
      cell.textContent = d;
      if (map[key]) cell.style.background = map[key];
      monthEl.appendChild(cell);
    }
    container.appendChild(monthEl);
  }

  document.getElementById("month-view").hidden = true;
  container.hidden = false;
}

async function renderYear(year) {
  const res = await fetch(`/admin/calendar/year/${year}`);
  const colors = await res.json();
  const colorMap = Object.fromEntries(colors.map(r => [r.day, r.color]));

  const yearView = document.getElementById("year-view");
  yearView.innerHTML = "";

  for (let row = 0; row < 3; row++) {
    const rowDiv = document.createElement("div");
    rowDiv.className = "year-row";

    for (let col = 0; col < 4; col++) {
      const month = row * 4 + col;
      rowDiv.appendChild(renderMonth(year, month, colorMap));
    }
    yearView.appendChild(rowDiv);
  }
}

function renderMonth(year, month, colorMap) {
  const div = document.createElement("div");
  div.className = "year-month";
  const name = new Date(year, month).toLocaleString("default", { month: "long" });
  div.innerHTML = `<h3>${name}</h3><div class="year-days"></div>`;
  const daysDiv = div.querySelector(".year-days");

  const first = new Date(year, month, 1);
  const last = new Date(year, month + 1, 0).getDate();
  const startPad = first.getDay(); // 0 = Sunday

  for (let i = 0; i < startPad; i++) {
    daysDiv.appendChild(document.createElement("div"));
  }
  for (let d = 1; d <= last; d++) {
    const dayEl = document.createElement("div");
    dayEl.className = "year-day";
    const dateStr = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
    dayEl.textContent = d;
    dayEl.style.background = colorMap[dateStr] || "#9ca3af";  // medium gray when missing
    daysDiv.appendChild(dayEl);
  }
  return div;
}