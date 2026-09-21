<script>
 let { voices = [] } = $props();
</script>
{#each voices as p (p.generation_id + p.round)}
 <details class="openrouter-provenance">
  <summary>OpenRouter · {p.round} · Herkunft und Abrechnung</summary>
  <dl>
   <dt>Angefordertes Modell</dt><dd>{p.requested_model}</dd>
   <dt>Gemeldetes Modell</dt><dd>{p.reported_model}</dd>
   <dt>Upstream / Endpunkt</dt><dd>{p.upstream_provider} / {p.endpoint}</dd>
   <dt>Quantisierung / Präzision laut Endpunkt</dt><dd>{p.quantization === 'unknown' ? 'Nicht ausgewiesen' : p.quantization}</dd>
   <dt>Generation</dt><dd>{p.generation_id}</dd>
   <dt>Abschluss / nativer Abschluss</dt><dd>{p.finish_reason} / {p.native_finish_reason}</dd>
   <dt>Verbrauch</dt><dd><pre>{JSON.stringify(p.usage, null, 2)}</pre></dd>
   <dt>Kosten</dt><dd>{p.cost} USD · {p.cost_basis === 'billed' ? 'abgerechnet; Antwort und Generationsmetadaten abgeglichen' : 'nicht als abgerechnet bestätigt'}</dd>
   <dt>Rohbelege</dt><dd>{p.raw_artifact} · {p.generation_artifact}</dd>
  </dl>
 </details>
{/each}
<style>
 dl { display: grid; grid-template-columns: minmax(8rem, 1fr) 2fr; gap: .4rem 1rem; }
 dd { margin: 0; overflow-wrap: anywhere; }
 pre { white-space: pre-wrap; }
</style>
