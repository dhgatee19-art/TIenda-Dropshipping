# ESTADO del proyecto

- Tienda: kvqu7z-ms.myshopify.com (nombre interno; el panel es admin.shopify.com/store/curioshop-2843)
- Nombre de la tienda: CatGravity (dominio catboing.com)
- Panel: https://admin.shopify.com/store/curioshop-2843
- Carpeta del proyecto: raíz de este repositorio (tema completo)
- Tema base: Dawn (Shopify/dawn @ 258f00f, descargado 2026-10-10)

## Fases
- [x] Fase 0 — Entorno: Node 22 + Shopify CLI 4.9.3 instalados (entorno en la nube)
- [x] Fase 1 — Conexión + sondeo: sesión del tema + sesión de datos (store auth) OK.
      Notas del entorno en la nube: usar NODE_USE_ENV_PROXY=1 con el CLI; falta xdg-open
      (stub en scratchpad/bin); la vuelta de store auth (127.0.0.1:13387) la pega el usuario
      y la reenvío con curl. Usar SIEMPRE --store kvqu7z-ms.myshopify.com.
      Temas actuales en la tienda: Horizon (live, 195273720185), Horizon (unpublished, 195090219385).
- [x] Fase 2 — Proyecto: tema base Dawn copiado
- [ ] Fase 3 — Brief
- [ ] Fase 4 — Secciones
- [ ] Fase 5 — Producto y páginas
- [ ] Fase 6 — Publicación

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

## Secciones creadas
(ninguna todavía)

## Decisiones de diseño
(pendientes)
