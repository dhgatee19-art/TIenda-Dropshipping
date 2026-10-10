#!/usr/bin/env python3
"""Genera las secciones cb-*.liquid del tema Catboing (markup + schema JSON validado)."""
import json, sys, os

OUT = sys.argv[1]


def comunes(align='left', h=44, b=17, pt=80, pb=80, fondo='#FAF6F0', texto='#2B2A30', con_align=True, con_h=True):
    s = [{"type": "header", "content": "Tipografía"}]
    if con_align:
        s.append({"type": "select", "id": "text_align", "label": "Alineación del texto",
                  "options": [{"value": "left", "label": "Izquierda"}, {"value": "center", "label": "Centro"},
                              {"value": "right", "label": "Derecha"}], "default": align})
    if con_h:
        s.append({"type": "range", "id": "heading_size", "label": "Tamaño del título", "min": 20, "max": 80,
                  "step": 2, "unit": "px", "default": h})
    s.append({"type": "range", "id": "body_size", "label": "Tamaño del texto", "min": 13, "max": 26, "step": 1,
              "unit": "px", "default": b})
    s += [{"type": "header", "content": "Colores"},
          {"type": "color", "id": "color_fondo", "label": "Fondo de la sección", "default": fondo},
          {"type": "color", "id": "color_texto", "label": "Color del texto", "default": texto},
          {"type": "header", "content": "Espaciado"},
          {"type": "range", "id": "padding_top", "label": "Espacio superior", "min": 0, "max": 160, "step": 8,
           "unit": "px", "default": pt},
          {"type": "range", "id": "padding_bottom", "label": "Espacio inferior", "min": 0, "max": 160, "step": 8,
           "unit": "px", "default": pb}]
    return s


def T(id, label, default=None, info=None):
    d = {"type": "text", "id": id, "label": label}
    if default: d["default"] = default
    if info: d["info"] = info
    return d


def TA(id, label, default=None, info=None):
    d = {"type": "textarea", "id": id, "label": label}
    if default: d["default"] = default
    if info: d["info"] = info
    return d


def IRT(id, label, default=None, info="Pon palabras en cursiva para que salgan en color, o en negrita para subrayarlas."):
    d = {"type": "inline_richtext", "id": id, "label": label}
    if default is not None: d["default"] = default
    if info: d["info"] = info
    return d


def IMG(id, label, info=None):
    d = {"type": "image_picker", "id": id, "label": label}
    if info: d["info"] = info
    return d


def URL(id, label, info=None):
    d = {"type": "url", "id": id, "label": label}  # OJO: los url NO admiten default
    if info: d["info"] = info
    return d


def CHK(id, label, default=True):
    return {"type": "checkbox", "id": id, "label": label, "default": default}


def RANGE(id, label, mn, mx, step, default, unit=None):
    d = {"type": "range", "id": id, "label": label, "min": mn, "max": mx, "step": step, "default": default}
    assert (mx - mn) / step <= 101, id
    if unit: d["unit"] = unit
    return d


def H(content):
    return {"type": "header", "content": content}


def write(name, markup, schema):
    # comprobaciones básicas del contrato
    ids = [s["id"] for s in schema.get("settings", []) if "id" in s]
    assert len(ids) == len(set(ids)), (name, "ids repetidos")
    for s in schema.get("settings", []):
        if s.get("type") in ("url", "image_picker"):
            assert "default" not in s, (name, s["id"])
        if s.get("type") == "range":
            assert (s["max"] - s["min"]) / s["step"] <= 101, (name, s["id"])
    for b in schema.get("blocks", []):
        for s in b.get("settings", []):
            if s.get("type") in ("url", "image_picker"):
                assert "default" not in s, (name, b["type"], s["id"])
    assert len(schema["name"]) <= 25, (name, "nombre largo", schema["name"])
    for pr in schema.get("presets", []):
        assert len(pr["name"]) <= 25, (name, "preset largo")
    for b in schema.get("blocks", []):
        assert len(b["name"]) <= 25, (name, "bloque largo")
    def chk(lst):
        for x in lst:
            assert x.get("default", "x") != "", (name, x.get("id"), "default vacío")
            if "label" in x: assert len(x["label"]) <= 100 if isinstance(x["label"], str) else True
    chk(schema.get("settings", []))
    for b in schema.get("blocks", []): chk(b.get("settings", []))
    path = os.path.join(OUT, "sections", name + ".liquid")
    with open(path, "w") as f:
        f.write(markup.strip() + "\n\n{% schema %}\n" + json.dumps(schema, ensure_ascii=False, indent=2) + "\n{% endschema %}\n")
    print("OK", path)


ICONOS = [{"value": v, "label": l} for v, l in
          [("gancho", "Gancho"), ("regla", "Regla"), ("raton", "Ratón"), ("pata", "Huella"), ("estrella", "Estrella"),
           ("reloj", "Reloj"), ("camion", "Camión"), ("escudo", "Escudo"), ("candado", "Candado")]]

# ---------------------------------------------------------------- HERO
write("cb-hero", r"""
{%- render 'cb-section-style', section: section -%}
{%- liquid
  assign s = section.settings
  assign p = s.producto
  assign v = p.selected_or_first_available_variant
  assign url = s.boton_url | default: p.url | default: routes.all_products_collection_url
-%}
{% style %}
  #shopify-section-{{ section.id }} .cb-hero__inner { min-height: {{ s.altura }}vh; }
  #shopify-section-{{ section.id }} .cb-hero__veil { opacity: {{ s.velo | divided_by: 100.0 }}; }
  #shopify-section-{{ section.id }} .cb-hero__media img { object-position: {{ s.foco_movil }}% center; }
  @media (min-width: 990px) { #shopify-section-{{ section.id }} .cb-hero__media img { object-position: center; } }
{% endstyle %}
<section class="cb-section cb-hero">
  <div class="cb-hero__inner">
    <div class="cb-hero__media" data-cb-parallax="{{ s.parallax }}">
      {% render 'cb-img', img: s.imagen, fallback: 'cb-hero.jpg', alt: 'Gato saltando para atrapar el ratón Catboing colgado de una puerta', width: 2400, eager: true %}
    </div>
    <div class="cb-hero__veil" aria-hidden="true"></div>
    <div class="cb-hero__content cb-container">
      <div class="cb-hero__box cb-align">
        {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-eyebrow--pill cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
        <h2 class="cb-h1 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
        {%- if s.texto != blank -%}<div class="cb-body cb-reveal" style="--cb-i:2">{{ s.texto | newline_to_br }}</div>{%- endif -%}
        {%- if s.mostrar_precio and p != blank -%}
          <div class="cb-hero__price cb-reveal" style="--cb-i:3">
            <span class="cb-hero__price-now">{{ v.price | money }}</span>
            {%- if v.compare_at_price > v.price -%}
              <span class="cb-hero__price-old">{{ v.compare_at_price | money }}</span>
              {%- assign ahorro = v.compare_at_price | minus: v.price | times: 100 | divided_by: v.compare_at_price -%}
              <span class="cb-hero__save">-{{ ahorro }}%</span>
            {%- endif -%}
          </div>
        {%- endif -%}
        {%- if s.boton_texto != blank -%}
          <div class="cb-reveal" style="--cb-i:4"><a href="{{ url }}" class="cb-btn">{{ s.boton_texto }}{% render 'cb-icon', name: 'flecha' %}</a></div>
        {%- endif -%}
        {%- if s.ticks != blank -%}
          <ul class="cb-hero__ticks cb-reveal" style="--cb-i:5">
            {%- assign lineas = s.ticks | newline_to_br | split: '<br />' -%}
            {%- for l in lineas -%}{%- assign t = l | strip -%}{%- if t != blank -%}<li><span class="cb-check">{% render 'cb-icon', name: 'check' %}</span>{{ t }}</li>{%- endif -%}{%- endfor -%}
          </ul>
        {%- endif -%}
      </div>
    </div>
    {%- if s.mostrar_badge -%}
      <div class="cb-hero__badge" aria-hidden="true">
        <span class="cb-hero__badge-emoji">{{ s.badge_emoji }}</span>
        <span>{{ s.badge_titulo }}<small>{{ s.badge_sub }}</small></span>
      </div>
    {%- endif -%}
  </div>
</section>
""", {
    "name": "CB – Portada (hero)", "tag": "section", "class": "cb-wrap",
    "settings": [
        H("Imagen"),
        IMG("imagen", "Imagen de fondo", "Recomendado: horizontal, con el gato a la derecha y espacio libre a la izquierda."),
        RANGE("foco_movil", "Encuadre en móvil (0 = izquierda, 100 = derecha)", 0, 100, 5, 70, "%"),
        RANGE("altura", "Altura mínima (% de la pantalla)", 50, 100, 5, 85, "%"),
        RANGE("velo", "Intensidad del velo claro detrás del texto", 0, 100, 5, 100, "%"),
        RANGE("parallax", "Efecto de profundidad al bajar", 0, 30, 2, 10),
        H("Textos"),
        T("eyebrow", "Etiqueta superior", "🐾 El juguete que tu gato no va a soltar"),
        IRT("titulo", "Título", "Tu gato juega solo. <em>Tú, tranquilo.</em>"),
        TA("texto", "Texto", "Cuelga Catboing del marco de una puerta y mira cómo tu gato salta, persigue y caza su ratón… mientras tú trabajas, cocinas o descansas."),
        H("Producto y botón"),
        {"type": "product", "id": "producto", "label": "Producto (para mostrar el precio)"},
        CHK("mostrar_precio", "Mostrar precio", True),
        T("boton_texto", "Texto del botón", "Lo quiero para mi gato"),
        URL("boton_url", "Enlace del botón", "Si lo dejas vacío, lleva a la página del producto."),
        TA("ticks", "Ventajas bajo el botón (una por línea)", "Envío gratis con seguimiento\nSe instala en 1 minuto\nSin pilas ni enchufes"),
        H("Etiqueta flotante"),
        CHK("mostrar_badge", "Mostrar etiqueta flotante", True),
        T("badge_emoji", "Emoji", "😼"),
        T("badge_titulo", "Título", "¡Juega solo!"),
        T("badge_sub", "Subtítulo", "Tú, libre para lo tuyo"),
    ] + comunes(h=64, b=19, pt=0, pb=0),
    "presets": [{"name": "CB – Portada (hero)"}]
})

# ---------------------------------------------------------------- MARQUESINA
write("cb-marquesina", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
{% style %}
  #shopify-section-{{ section.id }} .cb-marquee__item { font-size: {{ s.tamano }}px; padding: {{ s.alto }}px 22px; }
  #shopify-section-{{ section.id }} .cb-marquee__track { --cb-vel: {{ s.velocidad }}s; }
  #shopify-section-{{ section.id }} .cb-marquee__sep { color: {{ s.color_icono }}; }
  {%- if s.inclinado %}
  #shopify-section-{{ section.id }} .cb-marquee { transform: rotate(-1.5deg); margin: 18px -2%; }
  {%- endif %}
{% endstyle %}
<div class="cb-section cb-marquee">
  <div class="cb-marquee__track">
    {%- for g in (1..2) -%}
      <div class="cb-marquee__group"{% if g == 2 %} aria-hidden="true"{% endif %}>
        {%- for r in (1..3) -%}
          {%- for block in section.blocks -%}
            <span class="cb-marquee__item" {% if g == 1 and r == 1 %}{{ block.shopify_attributes }}{% endif %}>
              {%- if s.icono != 'ninguno' -%}<span class="cb-marquee__sep">{% render 'cb-icon', name: s.icono %}</span>{%- endif -%}
              {{ block.settings.texto }}
            </span>
          {%- endfor -%}
        {%- endfor -%}
      </div>
    {%- endfor -%}
  </div>
</div>
""", {
    "name": "CB – Cinta animada", "tag": "section", "class": "cb-wrap", "max_blocks": 8,
    "settings": [
        RANGE("velocidad", "Duración de una vuelta (segundos; más = más lento)", 10, 80, 2, 34, "s"),
        RANGE("tamano", "Tamaño del texto", 14, 40, 1, 22, "px"),
        RANGE("alto", "Altura de la cinta", 6, 40, 2, 18, "px"),
        {"type": "select", "id": "icono", "label": "Icono separador",
         "options": [{"value": "pata", "label": "Huella"}, {"value": "estrella", "label": "Estrella"},
                     {"value": "ninguno", "label": "Ninguno"}], "default": "pata"},
        {"type": "color", "id": "color_icono", "label": "Color del icono", "default": "#FF5C7A"},
        CHK("inclinado", "Cinta ligeramente inclinada", False),
        H("Colores"),
        {"type": "color", "id": "color_fondo", "label": "Fondo", "default": "#2B2A30"},
        {"type": "color", "id": "color_texto", "label": "Texto", "default": "#FAF6F0"},
        H("Espaciado"),
        RANGE("padding_top", "Espacio superior", 0, 160, 8, 0, "px"),
        RANGE("padding_bottom", "Espacio inferior", 0, 160, 8, 0, "px"),
    ],
    "blocks": [{"type": "texto", "name": "Frase", "settings": [T("texto", "Texto", "Envío gratis")]}],
    "presets": [{"name": "CB – Cinta animada", "blocks": [
        {"type": "texto", "settings": {"texto": "Envío gratis con seguimiento"}},
        {"type": "texto", "settings": {"texto": "Se instala en 1 minuto"}},
        {"type": "texto", "settings": {"texto": "Tu gato juega solo"}},
        {"type": "texto", "settings": {"texto": "Sin pilas ni enchufes"}}]}]
})

# ---------------------------------------------------------------- SPLIT
write("cb-split", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
{% style %}
  #shopify-section-{{ section.id }} .cb-split__media { --cb-ratio: {{ s.proporcion }}; }
{% endstyle %}
<section class="cb-section">
  <div class="cb-container">
    <div class="cb-split{% if s.invertido %} cb-split--invertido{% endif %}">
      <div class="cb-split__media cb-reveal">
        {% render 'cb-img', img: s.imagen, fallback: 'cb-tu-tranquilo.jpg', alt: 'Persona relajada en el sofá mientras su gato juega solo con Catboing', width: 1400 %}
        {%- if s.sticker != blank -%}<span class="cb-split__sticker">{{ s.sticker }}</span>{%- endif -%}
      </div>
      <div class="cb-split__text cb-align">
        {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
        <h2 class="cb-h2 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
        {%- if s.texto != blank -%}<div class="cb-body cb-reveal" style="--cb-i:2">{{ s.texto | newline_to_br }}</div>{%- endif -%}
        {%- if s.lista != blank -%}
          <ul class="cb-lista cb-reveal" style="--cb-i:3">
            {%- assign lineas = s.lista | newline_to_br | split: '<br />' -%}
            {%- for l in lineas -%}{%- assign t = l | strip -%}{%- if t != blank -%}<li><span class="cb-check">{% render 'cb-icon', name: 'check' %}</span><span>{{ t }}</span></li>{%- endif -%}{%- endfor -%}
          </ul>
        {%- endif -%}
        {%- if s.boton_texto != blank -%}
          <div class="cb-reveal" style="--cb-i:4"><a href="{{ s.boton_url | default: routes.all_products_collection_url }}" class="cb-btn{% if s.boton_oscuro %} cb-btn--oscuro{% endif %}">{{ s.boton_texto }}{% render 'cb-icon', name: 'flecha' %}</a></div>
        {%- endif -%}
      </div>
    </div>
  </div>
</section>
""", {
    "name": "CB – Imagen con texto", "tag": "section", "class": "cb-wrap",
    "settings": [
        H("Imagen"),
        IMG("imagen", "Imagen"),
        CHK("invertido", "Imagen a la derecha", False),
        {"type": "select", "id": "proporcion", "label": "Forma de la imagen",
         "options": [{"value": "4/3", "label": "Horizontal"}, {"value": "1/1", "label": "Cuadrada"},
                     {"value": "4/5", "label": "Vertical"}], "default": "4/3"},
        T("sticker", "Pegatina sobre la imagen (vacío = sin pegatina)", "¡Juega solo!"),
        H("Textos"),
        T("eyebrow", "Etiqueta superior", "El problema"),
        IRT("titulo", "Título", "Un gato aburrido es un gato <em>travieso</em>"),
        TA("texto", "Texto", "Arañazos en el sofá, carreras a las 3 de la madrugada, energía acumulada… Los gatos de casa necesitan cazar cada día, pero tú no siempre puedes estar con la varita en la mano."),
        TA("lista", "Lista de ventajas (una por línea)", "Juega solo mientras teletrabajas, cocinas o descansas\nGasta energía y se aburre menos en casa\nSin pilas, sin enchufes y sin ruidos"),
        T("boton_texto", "Texto del botón (vacío = sin botón)"),
        URL("boton_url", "Enlace del botón"),
        CHK("boton_oscuro", "Botón oscuro", True),
    ] + comunes(h=46, b=18, pt=96, pb=96),
    "presets": [{"name": "CB – Imagen con texto"}]
})

# ---------------------------------------------------------------- PASOS
write("cb-pasos", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
<section class="cb-section cb-pasos">
  <div class="cb-container">
    <div class="cb-pasos__head cb-align">
      {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
      <h2 class="cb-h2 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
      {%- if s.texto != blank -%}<div class="cb-body cb-reveal" style="--cb-i:2">{{ s.texto | newline_to_br }}</div>{%- endif -%}
    </div>
    <div class="cb-pasos__grid">
      {%- for block in section.blocks -%}
        <div class="cb-paso cb-reveal" style="--cb-i:{{ forloop.index }}" {{ block.shopify_attributes }}>
          <span class="cb-paso__icon">{% render 'cb-icon', name: block.settings.icono %}</span>
          <div class="cb-paso__num">{{ forloop.index }}</div>
          <h3 class="cb-h3" style="font-size: {{ s.paso_titulo }}px">{{ block.settings.titulo }}</h3>
          <div class="cb-texto" style="line-height:1.55;opacity:.8">{{ block.settings.texto | newline_to_br }}</div>
        </div>
      {%- endfor -%}
    </div>
    {%- if s.nota != blank -%}
      <div class="cb-align" style="margin-top:6px"><span class="cb-pasos__nota cb-reveal">{% render 'cb-icon', name: 'reloj' %}{{ s.nota }}</span></div>
    {%- endif -%}
  </div>
</section>
{% style %}
  #shopify-section-{{ section.id }} .cb-pasos__nota svg { width: 20px; height: 20px; color: var(--cb-coral); }
{% endstyle %}
""", {
    "name": "CB – Pasos", "tag": "section", "class": "cb-wrap", "max_blocks": 6,
    "settings": [
        T("eyebrow", "Etiqueta superior", "Así de fácil"),
        IRT("titulo", "Título", "Listo para jugar en <em>1 minuto</em>"),
        TA("texto", "Texto", "Sin herramientas, sin tornillos y sin agujeros en la pared."),
        RANGE("paso_titulo", "Tamaño del título de cada paso", 16, 34, 1, 23, "px"),
        T("nota", "Nota final (vacío = sin nota)", "Funciona mejor en marcos de puerta delgados"),
    ] + comunes(align='center', h=46, b=18, pt=96, pb=96, fondo='#F3EADD'),
    "blocks": [{"type": "paso", "name": "Paso", "settings": [
        T("titulo", "Título", "Paso"),
        TA("texto", "Texto", "Descripción del paso"),
        {"type": "select", "id": "icono", "label": "Icono decorativo", "options": ICONOS, "default": "pata"}]}],
    "presets": [{"name": "CB – Pasos", "blocks": [
        {"type": "paso", "settings": {"titulo": "Engancha", "texto": "Pasa el soporte por encima del marco de la puerta, en la parte de arriba.", "icono": "gancho"}},
        {"type": "paso", "settings": {"titulo": "Comprueba", "texto": "Asegúrate de que queda firme antes de soltarlo.", "icono": "regla"}},
        {"type": "paso", "settings": {"titulo": "Ajusta y ¡a jugar!", "texto": "Regula la cuerda para que el ratón cuelgue a la altura de tu gato… y disfruta del espectáculo.", "icono": "raton"}}]}]
})

# ---------------------------------------------------------------- BANDAS
write("cb-bandas", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
{%- assign respaldos = 'cb-banda-1.jpg,cb-banda-2.jpg,cb-banda-3.jpg' | split: ',' -%}
<section class="cb-section cb-bandas">
  <div class="cb-container">
    {%- if s.titulo != blank -%}
      <div class="cb-bandas__head cb-align">
        {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
        <h2 class="cb-h2 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
      </div>
    {%- endif -%}
    <div class="cb-bandas__list">
      {%- for block in section.blocks -%}
        {%- assign idx = forloop.index0 | modulo: 3 -%}
        <div class="cb-banda" {{ block.shopify_attributes }}>
          <div class="cb-banda__media cb-reveal">
            <span class="cb-banda__blob" aria-hidden="true"></span>
            {% render 'cb-img', img: block.settings.imagen, fallback: respaldos[idx], alt: block.settings.titulo, width: 1200 %}
          </div>
          <div class="cb-banda__text">
            {%- if block.settings.tag != blank -%}<span class="cb-banda__tag cb-reveal">{{ block.settings.tag }}</span>{%- endif -%}
            <h3 class="cb-h2 cb-reveal" style="--cb-i:1; font-size: clamp(26px, 4vw, {{ s.banda_titulo }}px)">{{ block.settings.titulo }}</h3>
            <div class="cb-body cb-reveal" style="--cb-i:2">{{ block.settings.texto | newline_to_br }}</div>
          </div>
        </div>
      {%- endfor -%}
    </div>
  </div>
</section>
""", {
    "name": "CB – Bandas", "tag": "section", "class": "cb-wrap", "max_blocks": 6,
    "settings": [
        T("eyebrow", "Etiqueta superior", "Por qué les encanta"),
        IRT("titulo", "Título general (vacío = sin título)", "Diseñado para el <em>cazador</em> que lleva dentro"),
        RANGE("banda_titulo", "Tamaño del título de cada banda", 22, 60, 2, 38, "px"),
    ] + comunes(align='center', h=46, b=18, pt=96, pb=96),
    "blocks": [{"type": "banda", "name": "Banda", "settings": [
        IMG("imagen", "Imagen", "Se recorta en forma redondeada."),
        T("tag", "Etiqueta", "Ventaja"),
        T("titulo", "Título", "Título de la banda"),
        TA("texto", "Texto", "Texto de la banda")]}],
    "presets": [{"name": "CB – Bandas", "blocks": [
        {"type": "banda", "settings": {"tag": "Instinto de caza", "titulo": "Despierta al cazador que lleva dentro", "texto": "Un ratón de peluche suave que se mueve con cada zarpazo. Tu gato acecha, se agazapa y salta, igual que haría si estuviera cazando de verdad."}},
        {"type": "banda", "settings": {"tag": "Rebote elástico", "titulo": "Nunca se queda quieto", "texto": "La cuerda elástica hace que el ratón rebote y cambie de dirección con cada golpe. Cada partida es distinta, así que el juego sigue siendo interesante."}},
        {"type": "banda", "settings": {"tag": "Gato cansado, gato feliz", "titulo": "Gasta energía y se aburre menos", "texto": "Unos minutos de juego intenso ayudan a liberar la energía acumulada de los gatos de casa. Menos aburrimiento, menos travesuras… y siestas más largas."}}]}]
})

# ---------------------------------------------------------------- GALERIA
write("cb-galeria", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
{%- assign respaldos = 'cb-galeria-1.jpg,cb-galeria-2.jpg,cb-detalle.jpg,cb-producto-estudio.jpg,cb-banda-2.jpg' | split: ',' -%}
{% style %}
  #shopify-section-{{ section.id }} .cb-galeria__grid { gap: {{ s.separacion }}px; }
{% endstyle %}
<section class="cb-section cb-galeria">
  <div class="cb-container">
    <div class="cb-galeria__head cb-align">
      {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
      <h2 class="cb-h2 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
      {%- if s.texto != blank -%}<div class="cb-body cb-reveal" style="--cb-i:2">{{ s.texto | newline_to_br }}</div>{%- endif -%}
    </div>
    <div class="cb-galeria__grid">
      {%- for block in section.blocks -%}
        {%- assign idx = forloop.index0 | modulo: 5 -%}
        <figure class="cb-galeria__item cb-reveal" style="--cb-i:{{ forloop.index0 }};margin:0" {{ block.shopify_attributes }}>
          {% render 'cb-img', img: block.settings.imagen, fallback: respaldos[idx], alt: block.settings.texto, width: 1000 %}
          {%- if block.settings.texto != blank -%}<figcaption class="cb-galeria__cap">{{ block.settings.texto }}</figcaption>{%- endif -%}
        </figure>
      {%- endfor -%}
    </div>
  </div>
</section>
""", {
    "name": "CB – Galería", "tag": "section", "class": "cb-wrap", "max_blocks": 9,
    "settings": [
        T("eyebrow", "Etiqueta superior", "En acción"),
        IRT("titulo", "Título", "Saltos, zarpazos y <em>mucha diversión</em>"),
        TA("texto", "Texto", ""),
        RANGE("separacion", "Separación entre fotos", 0, 40, 2, 16, "px"),
    ] + comunes(align='center', h=46, b=18, pt=96, pb=96),
    "blocks": [{"type": "foto", "name": "Foto", "settings": [IMG("imagen", "Imagen"), T("texto", "Texto sobre la foto (opcional)")]}],
    "presets": [{"name": "CB – Galería", "blocks": [
        {"type": "foto", "settings": {"texto": "¡Salto olímpico!"}},
        {"type": "foto", "settings": {"texto": "Se instala en 1 minuto"}},
        {"type": "foto", "settings": {"texto": "Peluche suave"}},
        {"type": "foto", "settings": {"texto": "Cuerda elástica"}},
        {"type": "foto", "settings": {"texto": ""}}]}]
})

# ---------------------------------------------------------------- COMPARATIVA
write("cb-comparativa", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
<section class="cb-section cb-comp">
  <div class="cb-container">
    <div class="cb-comp__head cb-align">
      {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
      <h2 class="cb-h2 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
      {%- if s.texto != blank -%}<div class="cb-body cb-reveal" style="--cb-i:2">{{ s.texto | newline_to_br }}</div>{%- endif -%}
    </div>
    <div class="cb-reveal" style="--cb-i:3">
      <table class="cb-comp__table">
        <thead>
          <tr>
            <th scope="col"><span class="visually-hidden">Característica</span></th>
            <th scope="col" class="cb-comp__nuestro">{{ s.col_1 }}</th>
            <th scope="col">{{ s.col_2 }}</th>
            {%- if s.col_3 != blank -%}<th scope="col">{{ s.col_3 }}</th>{%- endif -%}
          </tr>
        </thead>
        <tbody>
          {%- for block in section.blocks -%}
            <tr {{ block.shopify_attributes }}>
              <td>{{ block.settings.texto }}</td>
              <td class="cb-comp__nuestro">{% if block.settings.c1 %}<span class="cb-si" title="Sí">{% render 'cb-icon', name: 'check' %}</span>{% else %}<span class="cb-no" title="No">{% render 'cb-icon', name: 'x' %}</span>{% endif %}</td>
              <td>{% if block.settings.c2 %}<span class="cb-si" title="Sí">{% render 'cb-icon', name: 'check' %}</span>{% else %}<span class="cb-no" title="No">{% render 'cb-icon', name: 'x' %}</span>{% endif %}</td>
              {%- if s.col_3 != blank -%}<td>{% if block.settings.c3 %}<span class="cb-si" title="Sí">{% render 'cb-icon', name: 'check' %}</span>{% else %}<span class="cb-no" title="No">{% render 'cb-icon', name: 'x' %}</span>{% endif %}</td>{%- endif -%}
            </tr>
          {%- endfor -%}
        </tbody>
      </table>
    </div>
  </div>
</section>
""", {
    "name": "CB – Comparativa", "tag": "section", "class": "cb-wrap", "max_blocks": 10,
    "settings": [
        T("eyebrow", "Etiqueta superior", "Compáralo"),
        IRT("titulo", "Título", "¿Por qué <em>Catboing</em>?"),
        TA("texto", "Texto", ""),
        T("col_1", "Columna 1 (la vuestra)", "Catboing"),
        T("col_2", "Columna 2", "Varita con pluma"),
        T("col_3", "Columna 3 (vacío = sin columna)", "Juguete suelto"),
    ] + comunes(align='center', h=46, b=18, pt=96, pb=96, fondo='#F3EADD'),
    "blocks": [{"type": "fila", "name": "Fila", "settings": [
        T("texto", "Característica", "Característica"),
        CHK("c1", "Columna 1 la cumple", True), CHK("c2", "Columna 2 la cumple", False), CHK("c3", "Columna 3 la cumple", False)]}],
    "presets": [{"name": "CB – Comparativa", "blocks": [
        {"type": "fila", "settings": {"texto": "Tu gato juega aunque tú no estés", "c1": True, "c2": False, "c3": True}},
        {"type": "fila", "settings": {"texto": "Se mueve y rebota con cada golpe", "c1": True, "c2": False, "c3": False}},
        {"type": "fila", "settings": {"texto": "Movimiento que despierta su instinto", "c1": True, "c2": True, "c3": False}},
        {"type": "fila", "settings": {"texto": "No acaba perdido debajo del sofá", "c1": True, "c2": True, "c3": False}}]}]
})

# ---------------------------------------------------------------- DETALLES
write("cb-detalles", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
<section class="cb-section cb-detalles">
  <div class="cb-container">
    <div class="cb-split{% if s.invertido %} cb-split--invertido{% endif %}">
      <div class="cb-split__media cb-reveal" style="--cb-ratio: 1/1">
        {% render 'cb-img', img: s.imagen, fallback: 'cb-detalle.jpg', alt: 'Detalle del ratón de peluche Catboing', width: 1200 %}
      </div>
      <div class="cb-align">
        {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
        <h2 class="cb-h2 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
        {%- if s.texto != blank -%}<div class="cb-body cb-reveal" style="--cb-i:2">{{ s.texto | newline_to_br }}</div>{%- endif -%}
        {%- if s.specs != blank -%}
          <ul class="cb-specs cb-reveal cb-texto" style="--cb-i:3">
            {%- assign lineas = s.specs | newline_to_br | split: '<br />' -%}
            {%- for l in lineas -%}
              {%- assign t = l | strip -%}
              {%- if t != blank -%}
                {%- assign partes = t | split: '|' -%}
                <li><span>{{ partes[0] | strip }}</span><span>{{ partes[1] | strip }}</span></li>
              {%- endif -%}
            {%- endfor -%}
          </ul>
        {%- endif -%}
        {%- if s.aviso != blank -%}
          <div class="cb-aviso cb-reveal cb-texto" style="--cb-i:4"><span class="cb-aviso__icono" aria-hidden="true">📏</span><div>{{ s.aviso | newline_to_br }}</div></div>
        {%- endif -%}
      </div>
    </div>
  </div>
</section>
""", {
    "name": "CB – Detalles", "tag": "section", "class": "cb-wrap",
    "settings": [
        IMG("imagen", "Imagen"),
        CHK("invertido", "Imagen a la derecha", True),
        T("eyebrow", "Etiqueta superior", "Detalles"),
        IRT("titulo", "Título", "Pequeño, suave y <em>muy resistente al juego</em>"),
        TA("texto", "Texto", ""),
        TA("specs", "Ficha técnica (una por línea: Nombre | Valor)", "Juguete | Ratón de peluche con cuerda elástica\nCuerda | Unos 180 cm (hasta 380 cm estirada)\nColor | Gris oscuro\nInstalación | En el marco de la puerta\nExtra | Cuelga otros juguetes en el otro extremo"),
        TA("aviso", "Aviso destacado (vacío = sin aviso)", "Mide el grosor del marco de tu puerta antes de comprar: el gancho está pensado para marcos delgados y en marcos gruesos puede quedar justo.\nÚsalo siempre con tu gato supervisado y guárdalo al terminar de jugar."),
    ] + comunes(h=42, b=16, pt=96, pb=96),
    "presets": [{"name": "CB – Detalles"}]
})

# ---------------------------------------------------------------- FAQ
write("cb-faq", r"""
{%- render 'cb-section-style', section: section -%}
{%- assign s = section.settings -%}
{%- assign contacto = 'mailto:' | append: shop.email -%}
<section class="cb-section cb-faq" id="{{ s.ancla | default: 'faq' | handleize }}" style="scroll-margin-top: 90px">
  <div class="cb-container">
    <div class="cb-faq__wrap">
      <div class="cb-faq__aside cb-align">
        {%- if s.eyebrow != blank -%}<span class="cb-eyebrow cb-reveal">{{ s.eyebrow }}</span>{%- endif -%}
        <h2 class="cb-h2 cb-reveal" style="--cb-i:1">{{ s.titulo }}</h2>
        {%- if s.texto != blank -%}<div class="cb-body cb-reveal" style="--cb-i:2">{{ s.texto | newline_to_br }}</div>{%- endif -%}
        {%- if s.boton_texto != blank -%}
          <div class="cb-reveal" style="--cb-i:3"><a href="{{ s.boton_url | default: contacto }}" class="cb-btn cb-btn--oscuro">{{ s.boton_texto }}</a></div>
        {%- endif -%}
      </div>
      <div>
        {%- for block in section.blocks -%}
          <details class="cb-faq__item cb-reveal" style="--cb-i:{{ forloop.index0 }}" {{ block.shopify_attributes }}{% if forloop.first and s.abrir_primera %} open{% endif %}>
            <summary>{{ block.settings.pregunta }}</summary>
            <div class="cb-faq__answer cb-texto">{{ block.settings.respuesta }}</div>
          </details>
        {%- endfor -%}
      </div>
    </div>
  </div>
</section>
""", {
    "name": "CB – Preguntas", "tag": "section", "class": "cb-wrap", "max_blocks": 16,
    "settings": [
        T("eyebrow", "Etiqueta superior", "Dudas"),
        IRT("titulo", "Título", "Preguntas <em>frecuentes</em>"),
        TA("texto", "Texto", "¿No encuentras lo que buscas? Escríbenos y te respondemos encantados."),
        T("boton_texto", "Texto del botón (vacío = sin botón)", "Contactar"),
        URL("boton_url", "Enlace del botón", "Si lo dejas vacío, abre un email a la dirección de la tienda."),
        CHK("abrir_primera", "Primera pregunta abierta", True),
        T("ancla", "Nombre del ancla (para enlazar con /#nombre)", "faq"),
    ] + comunes(h=46, b=16, pt=96, pb=96),
    "blocks": [{"type": "pregunta", "name": "Pregunta", "settings": [
        T("pregunta", "Pregunta", "¿Pregunta?"),
        {"type": "richtext", "id": "respuesta", "label": "Respuesta", "default": "<p>Respuesta.</p>"}]}],
    "presets": [{"name": "CB – Preguntas", "blocks": [
        {"type": "pregunta", "settings": {"pregunta": "¿Sirve para cualquier puerta?", "respuesta": "<p>El gancho está pensado para marcos de puerta delgados. En marcos gruesos puede quedar justo, así que te recomendamos medir el grosor del marco antes de comprar.</p>"}},
        {"type": "pregunta", "settings": {"pregunta": "¿Necesito herramientas para instalarlo?", "respuesta": "<p>No. Solo tienes que enganchar el soporte en la parte de arriba del marco, comprobar que queda firme y ajustar la cuerda a la altura de tu gato. Se instala en un minuto.</p>"}},
        {"type": "pregunta", "settings": {"pregunta": "¿Es seguro para mi gato?", "respuesta": "<p>Úsalo siempre con tu gato supervisado y guárdalo cuando termine de jugar. Con el uso intenso la cuerda puede desgastarse, así que revísala de vez en cuando.</p>"}},
        {"type": "pregunta", "settings": {"pregunta": "¿Puedo colgar otros juguetes?", "respuesta": "<p>Sí. En el otro extremo de la cuerda puedes colgar otros juguetes favoritos de tu gato.</p>"}},
        {"type": "pregunta", "settings": {"pregunta": "¿Cuánto tarda el envío?", "respuesta": "<p>El envío es gratis y con número de seguimiento: México 6-11 días hábiles, Chile 7-10, Colombia 8-16 y España 7-14.</p>"}},
        {"type": "pregunta", "settings": {"pregunta": "¿Y si tengo algún problema con mi pedido?", "respuesta": "<p>Escríbenos y lo resolvemos. Puedes consultar todas las condiciones en nuestra <a href=\"/policies/refund-policy\">política de devoluciones</a>.</p>"}}]}]
})

# ---------------------------------------------------------------- CTA FINAL
write("cb-cta", r"""
{%- render 'cb-section-style', section: section -%}
{%- liquid
  assign s = section.settings
  assign p = s.producto
  assign v = p.selected_or_first_available_variant
-%}
{% style %}
  #shopify-section-{{ section.id }} .cb-cta__card { background: {{ s.color_tarjeta }}; color: {{ s.color_texto_tarjeta }}; }
{% endstyle %}
<section class="cb-section cb-cta">
  <div class="cb-container">
    <div class="cb-cta__card cb-reveal">
      <div class="cb-cta__media">
        {% render 'cb-img', img: s.imagen, fallback: 'cb-cierre.jpg', alt: 'Gatito sujetando el ratón Catboing', width: 1200 %}
      </div>
      <div class="cb-cta__body cb-align">
        {%- if s.eyebrow != blank -%}<span class="cb-eyebrow" style="color: var(--cb-amarillo)">{{ s.eyebrow }}</span>{%- endif -%}
        <h2 class="cb-h2">{{ s.titulo }}</h2>
        {%- if s.texto != blank -%}<div class="cb-body">{{ s.texto | newline_to_br }}</div>{%- endif -%}
        {%- if p != blank -%}
          <div class="cb-hero__price">
            <span class="cb-hero__price-now">{{ v.price | money }}</span>
            {%- if v.compare_at_price > v.price -%}
              <span class="cb-hero__price-old">{{ v.compare_at_price | money }}</span>
              {%- assign ahorro = v.compare_at_price | minus: v.price | times: 100 | divided_by: v.compare_at_price -%}
              <span class="cb-hero__save">-{{ ahorro }}%</span>
            {%- endif -%}
          </div>
          {%- if p.has_only_default_variant and s.anadir_directo -%}
            {%- form 'product', p, class: 'cb-cta__form' -%}
              <input type="hidden" name="id" value="{{ v.id }}">
              <button type="submit" name="add" class="cb-btn"{% unless v.available %} disabled{% endunless %}>
                {%- render 'cb-icon', name: 'carrito' -%}
                {%- if v.available -%}{{ s.boton_texto }}{%- else -%}{{ s.agotado_texto }}{%- endif -%}
              </button>
            {%- endform -%}
          {%- else -%}
            <a href="{{ p.url }}" class="cb-btn">{{ s.boton_texto }}{% render 'cb-icon', name: 'flecha' %}</a>
          {%- endif -%}
        {%- endif -%}
        {%- if s.garantias != blank -%}
          <div class="cb-garantias">
            {%- assign iconos = 'camion,candado,reloj,escudo' | split: ',' -%}
            {%- assign lineas = s.garantias | newline_to_br | split: '<br />' -%}
            {%- assign n = 0 -%}
            {%- for l in lineas -%}{%- assign t = l | strip -%}{%- if t != blank -%}{%- assign i = n | modulo: 4 -%}<span>{% render 'cb-icon', name: iconos[i] %}{{ t }}</span>{%- assign n = n | plus: 1 -%}{%- endif -%}{%- endfor -%}
          </div>
        {%- endif -%}
      </div>
    </div>
  </div>
</section>
""", {
    "name": "CB – Llamada a comprar", "tag": "section", "class": "cb-wrap",
    "settings": [
        IMG("imagen", "Imagen"),
        {"type": "product", "id": "producto", "label": "Producto"},
        CHK("anadir_directo", "El botón añade directamente al carrito", True),
        T("eyebrow", "Etiqueta superior", "Oferta de lanzamiento"),
        IRT("titulo", "Título", "Dale a tu gato <em>su nuevo juguete favorito</em>"),
        TA("texto", "Texto", "Diversión para él, tranquilidad para ti. Pídelo hoy y recíbelo en casa con envío gratis."),
        T("boton_texto", "Texto del botón", "Añadir al carrito"),
        T("agotado_texto", "Texto si está agotado", "Agotado"),
        TA("garantias", "Garantías (una por línea)", "Envío gratis con seguimiento\nPago 100% seguro\nInstalación en 1 minuto"),
        {"type": "color", "id": "color_tarjeta", "label": "Fondo de la tarjeta", "default": "#2B2A30"},
        {"type": "color", "id": "color_texto_tarjeta", "label": "Texto de la tarjeta", "default": "#FAF6F0"},
    ] + comunes(h=48, b=18, pt=64, pb=96),
    "presets": [{"name": "CB – Llamada a comprar"}]
})

# ---------------------------------------------------------------- PRODUCTO
write("cb-producto", r"""
{%- render 'cb-section-style', section: section -%}
{%- liquid
  assign s = section.settings
  assign v = product.selected_or_first_available_variant
  assign media_sel = v.featured_media | default: product.featured_media
-%}
<section class="cb-section cb-producto" data-cb-producto data-money-format="{{ shop.money_format | escape }}" data-add-label="{{ s.boton_texto | escape }}" data-sold-label="{{ s.agotado_texto | escape }}">
  <div class="cb-container">
    <div class="cb-producto__grid">
      {%- comment -%} Galería: sigue a las fotos del catálogo {%- endcomment -%}
      <div class="cb-galeria-p">
        <div class="cb-galeria-p__main">
          {%- if v.compare_at_price > v.price and s.mostrar_descuento -%}
            {%- assign ahorro = v.compare_at_price | minus: v.price | times: 100 | divided_by: v.compare_at_price -%}
            <span class="cb-galeria-p__badge">-{{ ahorro }}%</span>
          {%- endif -%}
          {%- if media_sel != blank -%}
            {%- assign img_main = media_sel.preview_image -%}
            {%- assign alt_main = media_sel.alt | default: product.title | escape -%}
            <img data-cb-main-img src="{{ img_main | image_url: width: 1400 }}"
              srcset="{{ img_main | image_url: width: 700 }} 700w, {{ img_main | image_url: width: 1100 }} 1100w, {{ img_main | image_url: width: 1400 }} 1400w"
              sizes="(max-width: 989px) 100vw, 55vw" width="1400" height="{{ 1400 | divided_by: img_main.aspect_ratio | round }}"
              alt="{{ alt_main }}" loading="eager" fetchpriority="high">
          {%- else -%}
            {{ 'product-1' | placeholder_svg_tag }}
          {%- endif -%}
        </div>
        {%- if product.media.size > 1 -%}
          <div class="cb-galeria-p__thumbs" role="list">
            {%- for m in product.media -%}
              <button type="button" class="cb-galeria-p__thumb" role="listitem" data-cb-thumb data-media-id="{{ m.id }}"
                data-src="{{ m.preview_image | image_url: width: 1400 }}"
                data-srcset="{{ m.preview_image | image_url: width: 700 }} 700w, {{ m.preview_image | image_url: width: 1100 }} 1100w, {{ m.preview_image | image_url: width: 1400 }} 1400w"
                data-alt="{{ m.alt | default: product.title | escape }}"
                aria-label="Ver foto {{ forloop.index }}" aria-current="{% if m.id == media_sel.id %}true{% else %}false{% endif %}">
                {{ m.preview_image | image_url: width: 160 | image_tag: loading: 'lazy', alt: '' }}
              </button>
            {%- endfor -%}
          </div>
        {%- endif -%}
      </div>

      {%- comment -%} Columna de compra {%- endcomment -%}
      <div class="cb-compra" data-cb-buy-zone>
        {%- if s.eyebrow != blank -%}<span class="cb-eyebrow">{{ s.eyebrow }}</span>{%- endif -%}
        <h1 class="cb-h1" style="font-size: clamp(28px, 4vw, {{ s.heading_size }}px)">{{ s.titulo_corto | default: product.title }}</h1>
        <div class="cb-compra__price">
          <span class="cb-hero__price-now" data-cb-price>{{ v.price | money }}</span>
          <span class="cb-hero__price-old" data-cb-compare{% unless v.compare_at_price > v.price %} hidden{% endunless %}>{% if v.compare_at_price > v.price %}{{ v.compare_at_price | money }}{% endif %}</span>
          {%- if v.compare_at_price > v.price and s.mostrar_descuento -%}
            <span class="cb-hero__save">{{ s.texto_descuento }}</span>
          {%- endif -%}
        </div>
        {%- if s.intro != blank -%}<p class="cb-compra__intro cb-texto">{{ s.intro | newline_to_br }}</p>{%- endif -%}
        {%- if s.bullets != blank -%}
          <ul class="cb-compra__bullets cb-texto">
            {%- assign lineas = s.bullets | newline_to_br | split: '<br />' -%}
            {%- for l in lineas -%}{%- assign t = l | strip -%}{%- if t != blank -%}<li><span class="cb-check">{% render 'cb-icon', name: 'check' %}</span><span>{{ t }}</span></li>{%- endif -%}{%- endfor -%}
          </ul>
        {%- endif -%}

        {%- form 'product', product, id: 'cb-form-producto', novalidate: 'novalidate' -%}
          <input type="hidden" name="id" value="{{ v.id }}">
          {%- unless product.has_only_default_variant -%}
            {%- for option in product.options_with_values -%}
              {%- assign oi = forloop.index0 -%}
              <fieldset class="cb-opcion" data-cb-option style="border:0;padding:0;margin:0 0 18px">
                <legend class="cb-opcion__label">{{ option.name }}: <span style="font-weight:600">{{ option.selected_value }}</span></legend>
                <div class="cb-opcion__values">
                  {%- for value in option.values -%}
                    <input type="radio" id="cb-opt-{{ section.id }}-{{ oi }}-{{ forloop.index0 }}" name="cb-opt-{{ oi }}" value="{{ value | escape }}"{% if option.selected_value == value %} checked{% endif %}>
                    <label for="cb-opt-{{ section.id }}-{{ oi }}-{{ forloop.index0 }}">{{ value }}</label>
                  {%- endfor -%}
                </div>
              </fieldset>
            {%- endfor -%}
            <script type="application/json" data-cb-variants>
              [{%- for x in product.variants -%}{"id":{{ x.id }},"available":{{ x.available | json }},"price":{{ x.price }},"compare_at_price":{{ x.compare_at_price | default: 0 }},"options":{{ x.options | json }},"featured_media_id":{{ x.featured_media.id | default: 'null' }}}{%- unless forloop.last -%},{%- endunless -%}{%- endfor -%}]
            </script>
          {%- endunless -%}

          {%- if s.mostrar_stock and v.available -%}
            <p class="cb-compra__stock"><span class="cb-compra__dot" aria-hidden="true"></span>{{ s.stock_texto }}</p>
          {%- endif -%}

          <div class="cb-compra__row">
            {%- if s.mostrar_cantidad -%}
              <div class="cb-cantidad">
                <button type="button" data-cb-qty-btn="-1" aria-label="Quitar uno">−</button>
                <input type="number" name="quantity" value="1" min="1" data-cb-qty aria-label="Cantidad">
                <button type="button" data-cb-qty-btn="1" aria-label="Añadir uno">+</button>
              </div>
            {%- endif -%}
            <button type="submit" name="add" class="cb-btn" data-cb-add{% unless v.available %} disabled{% endunless %}>
              {%- render 'cb-icon', name: 'carrito' -%}
              <span data-cb-add-label>{%- if v.available -%}{{ s.boton_texto }}{%- else -%}{{ s.agotado_texto }}{%- endif -%}</span>
            </button>
          </div>
          {%- if s.mostrar_pago_rapido -%}{{ form | payment_button }}{%- endif -%}
        {%- endform -%}

        {%- if s.confianza != blank -%}
          <div class="cb-confianza">
            {%- assign iconos = 'camion,candado,reloj,escudo' | split: ',' -%}
            {%- assign lineas = s.confianza | newline_to_br | split: '<br />' -%}
            {%- assign n = 0 -%}
            {%- for l in lineas -%}{%- assign t = l | strip -%}{%- if t != blank -%}{%- assign i = n | modulo: 4 -%}<div class="cb-confianza__item">{% render 'cb-icon', name: iconos[i] %}{{ t }}</div>{%- assign n = n | plus: 1 -%}{%- endif -%}{%- endfor -%}
          </div>
        {%- endif -%}

        <div class="cb-acordeon">
          {%- if s.mostrar_descripcion and product.description != blank -%}
            <details open><summary>{{ s.titulo_descripcion }}</summary><div class="cb-acordeon__body cb-texto">{{ product.description }}</div></details>
          {%- endif -%}
          {%- for block in section.blocks -%}
            <details {{ block.shopify_attributes }}><summary>{{ block.settings.titulo }}</summary><div class="cb-acordeon__body cb-texto">{{ block.settings.texto }}</div></details>
          {%- endfor -%}
        </div>
      </div>
    </div>
  </div>

  {%- if s.barra_movil -%}
    <div class="cb-sticky-atc" data-cb-sticky>
      <div class="cb-sticky-atc__info">{{ s.titulo_corto | default: product.title }}<small data-cb-price>{{ v.price | money }}</small></div>
      <button type="button" class="cb-btn" data-cb-sticky-submit data-cb-add{% unless v.available %} disabled{% endunless %}><span data-cb-add-label>{%- if v.available -%}{{ s.boton_texto }}{%- else -%}{{ s.agotado_texto }}{%- endif -%}</span></button>
    </div>
  {%- endif -%}
</section>
""", {
    "name": "CB – Producto", "tag": "section", "class": "cb-wrap", "max_blocks": 8,
    "settings": [
        H("Encabezado"),
        T("eyebrow", "Etiqueta superior", "🐾 Juguete interactivo para gatos"),
        T("titulo_corto", "Título visible (vacío = título del catálogo)", "Catboing™ – Juguete colgante de puerta"),
        CHK("mostrar_descuento", "Mostrar etiqueta de descuento", True),
        T("texto_descuento", "Texto de la etiqueta de descuento", "Oferta de lanzamiento"),
        H("Texto de venta"),
        TA("intro", "Introducción", "Cuélgalo del marco de una puerta y tu gato tendrá su propio ratón para saltar, perseguir y cazar… mientras tú haces tus cosas."),
        TA("bullets", "Ventajas (una por línea)", "Juega solo, sin que tengas que estar con él\nEl rebote elástico mantiene el juego interesante\nSe instala en 1 minuto, sin herramientas"),
        H("Compra"),
        CHK("mostrar_stock", "Mostrar aviso de disponibilidad", True),
        T("stock_texto", "Texto de disponibilidad", "En stock · Envío gratis con seguimiento"),
        CHK("mostrar_cantidad", "Mostrar selector de cantidad", True),
        T("boton_texto", "Texto del botón", "Añadir al carrito"),
        T("agotado_texto", "Texto si está agotado", "Agotado"),
        CHK("mostrar_pago_rapido", "Mostrar botones de pago rápido (Shop Pay, PayPal…)", False),
        CHK("barra_movil", "Barra de compra fija en móvil", True),
        TA("confianza", "Garantías (una por línea, máx. 3 recomendado)", "Envío gratis\nPago seguro\nInstala en 1 min"),
        H("Información desplegable"),
        CHK("mostrar_descripcion", "Mostrar la descripción del catálogo", True),
        T("titulo_descripcion", "Título de la descripción", "Descripción"),
    ] + comunes(h=40, b=16, pt=40, pb=72, con_align=False),
    "blocks": [{"type": "desplegable", "name": "Desplegable", "settings": [
        T("titulo", "Título", "Título"),
        {"type": "richtext", "id": "texto", "label": "Contenido", "default": "<p>Contenido</p>"}]}],
    "presets": [{"name": "CB – Producto"}],
    "enabled_on": {"templates": ["product"]}
})

# ---------------------------------------------------------------- FOOTER
write("cb-footer", r"""
{%- assign s = section.settings -%}
{% style %}
  #shopify-section-{{ section.id }} { padding-top: {{ s.padding_top }}px; padding-bottom: {{ s.padding_bottom }}px; background: {{ s.color_fondo }}; }
  #shopify-section-{{ section.id }} .cb-footer { background: {{ s.color_fondo }}; color: {{ s.color_texto }}; font-size: {{ s.body_size }}px; }
{% endstyle %}
<footer class="cb-section cb-footer">
  <div class="cb-container">
    <div class="cb-footer__grid">
      <div>
        {%- if s.logo != blank -%}
          <img src="{{ s.logo | image_url: width: 600 }}" alt="{{ s.logo.alt | default: shop.name | escape }}" width="{{ s.logo_width }}" height="{{ s.logo_width | divided_by: s.logo.aspect_ratio | round }}" loading="lazy" style="width:{{ s.logo_width }}px;height:auto;margin-bottom:14px">
        {%- else -%}
          <div class="cb-footer__logo-text">{{ s.logo_texto }}<span class="cb-acento">{{ s.logo_acento }}</span></div>
        {%- endif -%}
        {%- if s.lema != blank -%}<p class="cb-footer__text">{{ s.lema | newline_to_br }}</p>{%- endif -%}
        {%- if s.instagram != blank or s.tiktok != blank or s.facebook != blank -%}
          <div class="cb-footer__social">
            {%- if s.instagram != blank -%}<a href="{{ s.instagram }}" target="_blank" rel="noopener" aria-label="Instagram">{% render 'cb-icon', name: 'instagram' %}</a>{%- endif -%}
            {%- if s.tiktok != blank -%}<a href="{{ s.tiktok }}" target="_blank" rel="noopener" aria-label="TikTok">{% render 'cb-icon', name: 'tiktok' %}</a>{%- endif -%}
            {%- if s.facebook != blank -%}<a href="{{ s.facebook }}" target="_blank" rel="noopener" aria-label="Facebook">{% render 'cb-icon', name: 'facebook' %}</a>{%- endif -%}
          </div>
        {%- endif -%}
      </div>
      <div>
        <p class="cb-footer__title">{{ s.nav_titulo }}</p>
        <ul class="cb-footer__links">
          {%- for i in (1..5) -%}
            {%- assign k_label = 'nav_' | append: i | append: '_texto' -%}
            {%- assign k_url = 'nav_' | append: i | append: '_url' -%}
            {%- if s[k_label] != blank -%}<li><a href="{{ s[k_url] | default: '#' }}">{{ s[k_label] }}</a></li>{%- endif -%}
          {%- endfor -%}
        </ul>
      </div>
      <div>
        <p class="cb-footer__title">{{ s.ayuda_titulo }}</p>
        {%- if s.ayuda_texto != blank -%}<p class="cb-footer__text">{{ s.ayuda_texto | newline_to_br }}</p>{%- endif -%}
        {%- assign email = s.email | default: shop.email -%}
        {%- if email != blank -%}<p class="cb-footer__text"><a href="mailto:{{ email }}">✉️ {{ email }}</a></p>{%- endif -%}
      </div>
    </div>
    <div class="cb-footer__bottom">
      <span>© {{ 'now' | date: '%Y' }} {{ s.logo_texto }}{{ s.logo_acento }}. {{ s.copyright }}</span>
      <nav class="cb-footer__legal" aria-label="Legal">
        <a href="/policies/privacy-policy">Privacidad</a>
        <a href="/policies/terms-of-service">Términos</a>
        <a href="/policies/refund-policy">Devoluciones</a>
        <a href="/policies/shipping-policy">Envíos</a>
        {%- if s.legal_extra_texto != blank -%}<a href="{{ s.legal_extra_url | default: '#' }}">{{ s.legal_extra_texto }}</a>{%- endif -%}
      </nav>
      {%- if s.mostrar_pagos -%}
        <ul class="cb-footer__pagos" aria-label="Métodos de pago">
          {%- for type in shop.enabled_payment_types -%}<li>{{ type | payment_type_svg_tag: class: 'icon icon--full-color' }}</li>{%- endfor -%}
        </ul>
      {%- endif -%}
    </div>
  </div>
</footer>
""", {
    "name": "CB – Pie de página", "tag": "section", "class": "cb-wrap",
    "settings": [
        H("Marca"),
        IMG("logo", "Logo (imagen; vacío = logo de texto)"),
        RANGE("logo_width", "Ancho del logo", 60, 300, 5, 150, "px"),
        T("logo_texto", "Logo de texto: primera parte", "Cat"),
        T("logo_acento", "Logo de texto: parte en color", "boing"),
        TA("lema", "Frase de la marca", "Juguetes que hacen felices a los gatos (y tranquilos a sus humanos)."),
        URL("instagram", "Instagram (enlace)"), URL("tiktok", "TikTok (enlace)"), URL("facebook", "Facebook (enlace)"),
        H("Columna de enlaces"),
        T("nav_titulo", "Título", "Tienda"),
        T("nav_1_texto", "Enlace 1: texto", "Inicio"), URL("nav_1_url", "Enlace 1: dirección"),
        T("nav_2_texto", "Enlace 2: texto", "Catboing"), URL("nav_2_url", "Enlace 2: dirección"),
        T("nav_3_texto", "Enlace 3: texto", "Preguntas frecuentes"), URL("nav_3_url", "Enlace 3: dirección"),
        T("nav_4_texto", "Enlace 4: texto", "Contacto"), URL("nav_4_url", "Enlace 4: dirección"),
        T("nav_5_texto", "Enlace 5: texto (vacío = oculto)"), URL("nav_5_url", "Enlace 5: dirección"),
        H("Columna de ayuda"),
        T("ayuda_titulo", "Título", "¿Necesitas ayuda?"),
        TA("ayuda_texto", "Texto", "Escríbenos y te respondemos lo antes posible."),
        T("email", "Email de contacto (vacío = el de la tienda)"),
        H("Barra inferior"),
        T("copyright", "Texto tras el copyright", "Todos los derechos reservados."),
        T("legal_extra_texto", "Enlace legal extra: texto (p. ej. Aviso legal)"), URL("legal_extra_url", "Enlace legal extra: dirección"),
        CHK("mostrar_pagos", "Mostrar iconos de métodos de pago", True),
        H("Estilo"),
        RANGE("body_size", "Tamaño del texto", 12, 20, 1, 15, "px"),
        {"type": "color", "id": "color_fondo", "label": "Fondo", "default": "#2B2A30"},
        {"type": "color", "id": "color_texto", "label": "Texto", "default": "#FAF6F0"},
        RANGE("padding_top", "Espacio superior", 0, 160, 8, 64, "px"),
        RANGE("padding_bottom", "Espacio inferior", 0, 160, 8, 32, "px"),
    ],
    "presets": [{"name": "CB – Pie de página"}],
    "enabled_on": {"groups": ["footer"]}
})
