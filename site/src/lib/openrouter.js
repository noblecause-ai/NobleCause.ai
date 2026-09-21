// Only structured new-record provenance enables this procedure text.
export const openRouterProcedure = {
 de: 'Die Ratsmodelle werden über das API-Gateway OpenRouter aufgerufen — je Sitz ein festes Modell bei einem fest gewählten Upstream-Anbieter, ohne automatische Ausweichwege. Der Rekord führt je Votum das angeforderte und das gemeldete Modell, den Upstream-Anbieter und die tatsächlich abgerechneten Kosten. Fällt ein Endpunkt aus, ist der Ausfall sichtbar; es antwortet kein stilles Ersatzmodell.',
 en: 'Council models are called through the OpenRouter API gateway — one fixed model per seat at one fixed upstream provider, with no automatic alternate routes. For each vote, the record lists the requested and reported model, the upstream provider, and the actually billed cost. If an endpoint fails, the failure is visible; no silent substitute model answers.'
};
export function openRouterVoices(session, model) {
 return (session?.rounds ?? []).flatMap(round => [...(round.votes ?? []), ...(round.exchanges ?? [])]
  .filter(v => (!model || v.model === model) && v.provenance?.transport === 'openrouter_api')
  .map(v => ({ round: round.kind, ...v.provenance })));
}
export const hasOpenRouter = session => openRouterVoices(session).length > 0;
