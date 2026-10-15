(() => {
  "use strict";
  const list = document.querySelector("#veille-auto-list");
  const status = document.querySelector("#veille-auto-status");
  const updated = document.querySelector("#veille-auto-date");
  if (!list || !status) return;

  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const formatDate = (value) => {
    if (!value) return "Date non précisée";
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? value : new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium", timeZone: "UTC" }).format(date);
  };

  fetch("veille-data.json", { cache: "no-store" })
    .then((response) => {
      if (!response.ok) throw new Error("Flux indisponible");
      return response.json();
    })
    .then((data) => {
      list.replaceChildren();
      const items = Array.isArray(data.items) ? data.items : [];
      items.slice(0, 20).forEach((item) => {
        const article = element("article", "card");
        article.append(element("p", "meta", (item.source || "Source") + " · " + formatDate(item.date)));
        article.append(element("h3", "", item.title || "Publication de sécurité"));
        if (item.kind) article.append(element("p", "small", item.kind));
        if (item.summary) article.append(element("p", "", item.summary));
        if (item.action) article.append(element("p", "", "Action recommandée : " + item.action));
        if (item.dueDate) article.append(element("p", "small", "Échéance indiquée par CISA : " + item.dueDate));
        if (item.url && /^https:\/\//i.test(item.url)) {
          const link = element("a", "link", "Consulter la source");
          link.href = item.url;
          link.target = "_blank";
          link.rel = "noopener noreferrer";
          article.append(link);
        }
        list.append(article);
      });
      if (!items.length) throw new Error("Le flux ne contient aucune entrée");
      status.textContent = items.length + " entrées récupérées automatiquement depuis les sources officielles.";
      if (updated && data.generatedAt) updated.textContent = "Dernière génération : " + formatDate(data.generatedAt);
      if (data.warnings && data.warnings.length) status.textContent += " Une source est temporairement indisponible ; les données disponibles sont conservées.";
    })
    .catch(() => {
      status.textContent = "Impossible de charger la veille en direct. Réessaie plus tard ; les sources officielles restent accessibles ci-dessous.";
    });
})();
