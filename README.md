
# 🕷️ Explorador de llocs web per detectar errors 4XX

Aquest projecte és una eina per analitzar un lloc web i detectar enllaços interns que produeixen errors **HTTP 4XX** (com ara *404 No Found*). El procés es fa de manera **automàtica**, **paral·lela** i amb suport de navegació dinàmica mitjançant **Selenium**.

## ✅ Objectius

- Rastrejar un lloc web a partir d'una URL inicial.
- Detectar errors **client-side** (4XX) en les pàgines visitades.
- Emmagatzemar els resultats en un fitxer **CSV** per facilitar-ne l'anàlisi posterior.

## ⚙️ Llenguatge i tecnologies utilitzades

- **Python 3**
- **Selenium WebDriver** (amb Firefox en mode headless)
- **Requests** per fer peticions HTTP eficients
- **Concurrent.futures** per optimitzar el rastreig amb paral·lelisme
- **CSV** per generar informes reutilitzables

## 📌 Decisions de disseny

### 🔹 Navegació amb Selenium

S’utilitza **Selenium** per extreure dinàmicament tots els enllaços (`<a href="...">`) de cada pàgina visitada, garantint compatibilitat amb llocs amb JavaScript.

### 🔹 Paral·lelisme amb ThreadPoolExecutor

S'utilitza `ThreadPoolExecutor` per llançar múltiples rastrejos alhora i així **accelerar l’exploració** sense sobrecarregar el lloc web.

### 🔹 Control de dominis

Només es continuen rastrejant URL que pertanyin al **mateix domini** d'origen per evitar sortir del lloc analitzat.

### 🔹 Sessió persistent amb Requests

S'utilitza una única instància de `requests.Session()` per millorar el rendiment mitjançant connexions reutilitzables.

### 🔹 Control de profunditat

S’ha afegit un límit configurable (`max_urls`) per evitar que el rastreig sigui massa profund o infinit.

## 🧪 Exemple d’ús

```python
domini = "https://www.exemple.com/"
max_urls = 50
errors_trobats = detectar_errors_4xx(domini, max_urls)
generar_informe(errors_trobats)
```

### Resultat

Un fitxer `informe_errors.csv` amb estructura:

```
URL amb error, Codi d'error HTTP, Pàgina d'origen
https://exemple.com/error404, 404, https://exemple.com/inici
...
```

## 🔐 Consideracions de seguretat

- El rastreig es limita al domini d’origen.
- Es fa en **mode headless** per evitar obrir finestres del navegador.
- Totes les excepcions són capturades per evitar bloquejos.

## 📌 Millores futures

- Afegir suport per detectar errors 5XX (servidor).
- Permetre analitzar recursos com imatges, scripts, CSS, etc.
- Exportar l’informe a altres formats: JSON, HTML.
