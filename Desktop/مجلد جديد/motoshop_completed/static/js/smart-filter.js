(() => {
    "use strict";

    const root = document.querySelector("[data-smart-filter]");
    if (!root) return;

    const input = document.getElementById("smartBikeSearch");
    const suggestions = document.getElementById("smartSuggestions");
    const status = document.getElementById("smartFilterStatus");
    const normalSearch = document.getElementById("normalBikeSearch");
    const form = input ? input.closest("form") : null;
    const endpoint = root.dataset.smartFilterUrl || "/shop/smart-suggestions/";

    let timer = null;
    let controller = null;

    const closeSuggestions = () => {
        suggestions.innerHTML = "";
        suggestions.hidden = true;
    };

    const choose = (item) => {
        if (!normalSearch || !form) return;
        normalSearch.value = item.label;
        closeSuggestions();
        if (status) status.textContent = "✓";
        input.classList.remove("smart-loading");
        input.classList.add("smart-match");
        form.submit();
    };

    const render = (items, query) => {
        suggestions.innerHTML = "";
        if (!items.length) {
            suggestions.innerHTML = `<div class="smart-empty">لا توجد مطابقة قريبة. جرّب اسم الشركة أو اسم الموديل.</div>`;
            suggestions.hidden = false;
            return;
        }

        items.forEach((item) => {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "smart-suggestion";
            button.innerHTML = `
                <span class="smart-suggestion-icon"><i class="fas fa-motorcycle"></i></span>
                <span class="smart-suggestion-main">
                    <span class="smart-suggestion-title"></span>
                    <span class="smart-suggestion-meta"></span>
                </span>
                <span class="smart-suggestion-correction">هل تقصد؟</span>
            `;
            button.querySelector(".smart-suggestion-title").textContent = item.label;
            button.querySelector(".smart-suggestion-meta").textContent = `${item.year} • ${item.engine_cc} CC`;
            button.addEventListener("click", () => choose(item));
            suggestions.appendChild(button);
        });
        suggestions.hidden = false;
    };

    const fetchSuggestions = async (query) => {
        if (controller) controller.abort();
        controller = new AbortController();
        status.textContent = "…";
        input.classList.add("smart-loading");
        input.classList.remove("smart-match");

        try {
            const response = await fetch(`${endpoint}?q=${encodeURIComponent(query)}`, {
                method: "GET",
                headers: { "Accept": "application/json" },
                signal: controller.signal,
            });
            if (!response.ok) throw new Error("smart-filter-request-failed");
            const data = await response.json();
            render(data.suggestions || [], query);
            status.textContent = data.suggestions?.length ? "✨" : "";
        } catch (error) {
            if (error.name !== "AbortError") {
                closeSuggestions();
                status.textContent = "";
            }
        } finally {
            input.classList.remove("smart-loading");
        }
    };

    input.addEventListener("input", () => {
        const query = input.value.trim();
        closeSuggestions();
        input.classList.remove("smart-match", "smart-loading");
        status.textContent = "";

        if (timer) clearTimeout(timer);
        if (query.length < 2) return;
        timer = setTimeout(() => fetchSuggestions(query), 220);
    });

    input.addEventListener("keydown", (event) => {
        if (event.key === "Escape") closeSuggestions();
        if (event.key === "Enter") {
            event.preventDefault();
            const first = suggestions.querySelector(".smart-suggestion");
            if (first) first.click();
            else if (normalSearch && form) {
                normalSearch.value = input.value.trim();
                form.submit();
            }
        }
    });

    document.addEventListener("click", (event) => {
        if (!root.contains(event.target)) closeSuggestions();
    });
})();
