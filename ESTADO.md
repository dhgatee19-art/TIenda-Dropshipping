# ESTADO del proyecto

- Tienda: kvqu7z-ms.myshopify.com (nombre interno; el panel es admin.shopify.com/store/curioshop-2843)
- Nombre de la tienda: CatGravity (dominio catboing.com)
- Panel: https://admin.shopify.com/store/curioshop-2843
- Carpeta del proyecto: raíz de este repositorio (tema completo)
- Tema base: Dawn (Shopify/dawn @ 258f00f, descargado 2026-10-10)

## Contexto del negocio (contado por el usuario)
- Dropshipping desde julio 2026; 2 productos anteriores sin ventas (precio alto para LATAM, web mal configurada).
- Tráfico orgánico con vídeos IA (Higgsfield): vídeos de 70-80k vistas con el primer producto; >60% del tráfico era de México.
- Estrategia actual: Catboing para México, Chile, Colombia y España, sin restringir países; precio ~299 MXN (compra impulsiva).
- Pagos: tarjetas + PayPal; sin OXXO (preocupación del usuario).
- Stock del proveedor: 61 uds. Política de inventario cambiada a DENY (deja de vender en 0) el 2026-10-11.
  Reactivar CONTINUE solo con proveedor de reserva.
- Siguiente paso del usuario: ideas de vídeos y prompts para anuncios.

## Fases
- [x] Fase 0 — Entorno: Node 22 + Shopify CLI 4.9.3 (entorno en la nube)
- [x] Fase 1 — Conexión + sondeo (sesión de tema + store auth). Ver notas técnicas abajo.
- [x] Fase 2 — Proyecto: tema base Dawn
- [x] Fase 3 — Brief: el usuario delegó el estilo ("el que más convierta"), tienda en español
- [x] Fase 3b — Fotos IA (gpt-image-2): 12 imágenes generadas, gasto aprox. 1,3 $ de 5 $
- [x] Fase 4 — Secciones propias (prefijo cb-)
- [~] Fase 5 — Producto asignado (templateSuffix "cb"), galería y descripción OK. Pendiente: políticas legales (panel), página de contacto
- [x] Fase 6 — Tema PUBLICADO por el usuario (Catboing v1 = live). Push con --allow-live (permiso explícito del usuario).

## Tema de trabajo
- ID: 200400142713 ("Catboing v1", sin publicar)
- Previsualización: https://kvqu7z-ms.myshopify.com/?preview_theme_id=200400142713
- Editor: https://kvqu7z-ms.myshopify.com/admin/themes/200400142713/editor
- Subir: `NODE_USE_ENV_PROXY=1 shopify theme push --store kvqu7z-ms.myshopify.com --path . --theme 200400142713 --json`
- Tema publicado actual: Horizon (195273720185) — se mantiene como copia de seguridad

## Pendiente del lado del usuario (panel de Shopify)
- [x] Idioma principal: español (cambiado por el usuario).
  (El tema ya muestra sus textos en español: locales/en.default.json lleva las traducciones de es.json.)
- Título/descripción de la portada en Google = "AuriClean…" (antiguo) → Tienda online → Preferencias.
- Nombre de la tienda = "CatGravity" (sale en la pestaña) → Configuración → Detalles de la tienda.
- [x] Menú principal en español (Inicio · Catboing · Preguntas frecuentes · Contacto).
- [x] 6 políticas reescritas para Catboing (base, revisar con un profesional). Páginas Contacto (con formulario) y Sobre nosotros reescritas.
- Moneda base USD; en la vista previa se ve en MXN (Markets convierte por país).

## Notas técnicas del entorno en la nube
- Revisión visual: herramientas/pruebas/shots.mjs y test-compra.mjs (Playwright, contraseña en TIENDA_PASS).
- El CLI necesita NODE_USE_ENV_PROXY=1 (proxy de red) y un `xdg-open` falso en el PATH.
- store auth redirige a 127.0.0.1:13387: el usuario pega la URL de vuelta y se reenvía con curl.
- La clave de OpenAI NO está en el repositorio (vive en el scratchpad de la sesión; pedirla de nuevo si hace falta).
- `herramientas/generar-secciones.py` regenera todas las secciones cb-* (markup + schema validado):
  `python3 herramientas/generar-secciones.py .`

## Producto leído
Producto principal ACTUAL (cambiado por el usuario el 2026-10-10):
- id: gid://shopify/Product/15856931602809
- handle: juguete-colgante-puerta-gatos
- título: Catboing™ | Juguete colgante para puerta para gatos con cuerda elástica
- estado: ACTIVE pero SIN publicar en el canal Tienda online (publishedAt null) → la
  vista previa da error. Hay que marcar el canal "Tienda online" en el producto.
- precio: 16.99 (antes 29.99), 1 variante "Gris oscuro", stock 61, vende sin stock (CONTINUE)
- descripción (ES): ratón de peluche con cuerda elástica que se cuelga del marco de la
  puerta; el gato juega solo; instalación en 1 min (3 pasos); cuerda ~180 cm hasta ~380 cm
  estirada; en el otro extremo se pueden colgar otros juguetes; gancho para marcos delgados
  (en gruesos puede quedar justo); usar con supervisión. Envío gratis con seguimiento:
  México 6-11, Chile 7-10, Colombia 8-16, España 7-14 días hábiles.
- SEO ya escrito por el usuario (título/descr.). Dominio: catboing.com (tienda con contraseña).
- fotos: 6 en fotos-producto/ (de proveedor, con textos en inglés encima; 2-3 de ambiente)

Producto anterior (ahora DRAFT): CatGravity™ bebedero por gravedad
(gid://shopify/Product/15804628599161), fotos en fotos-producto-catgravity/.

## Secciones creadas (sections/)
- cb-hero — portada con foto, título, precio dinámico, botón, ventajas y etiqueta flotante
- cb-marquesina — cinta animada de frases
- cb-split — imagen + texto + lista (bloque "el problema")
- cb-pasos — 3 pasos de instalación
- cb-bandas — bandas alternas imagen/texto (por qué les encanta)
- cb-galeria — galería en mosaico
- cb-comparativa — tabla Catboing vs varita vs juguete suelto
- cb-detalles — ficha técnica + aviso de medir la puerta
- cb-faq — preguntas frecuentes (ancla /#faq)
- cb-cta — llamada final con precio y añadir al carrito
- cb-producto — página de producto (galería del catálogo, variantes, cantidad, barra fija móvil)
- cb-footer — pie de página propio (en footer-group.json)
- header.liquid (Dawn) — añadido logo por sección + logo de texto "Cat" + "boing"
- Plantillas: templates/index.json, templates/product.cb.json (asignada al producto)
- layout/theme.liquid: carga cb-styles.css / cb-scripts.js, favicon de respaldo, clase cb-js

## Decisiones de diseño
- Tono: divertido y cercano ("gato feliz, dueño tranquilo"). Idioma: español.
- Paleta: crema #FAF6F0, crema 2 #F3EADD, carbón #2B2A30, coral #FF5C7A (botones), amarillo #FFD36B.
- Fuentes: las del tema (Nunito 800 títulos / Nunito 400 texto), editables en Ajustes del tema.
- Esquinas redondeadas (24px), botones píldora, animaciones de entrada y rebote.
- Sin reseñas inventadas: añadir una app de reseñas cuando haya opiniones reales.
- Fotos IA en fotos-ia/ (copias en assets/cb-*.jpg). 6 subidas a la galería del producto (primeras).
- Moneda de la tienda: USD (vende a MX/CL/CO/ES) — recomendado revisar Markets.

