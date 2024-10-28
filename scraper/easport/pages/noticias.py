
class NoticiasEASport:
	@classmethod
	def scrap(cls, html_data):
		container = html_data.find('ea-grid')

		lista_noticias = []

		for noticia in container.css.select('ea-container  ea-tile[slot="tile"]'):
			extra = noticia.find_all('div')

			lista_noticias.append({
				'imagen': noticia.get('media'),
				'titulo': noticia.get('title-text'),
				'etiqueta': extra[0].string.strip(),
				'fecha': extra[1].string.strip(),
				'descripcion': noticia.find('ea-tile-copy').string.strip()
			})

		return lista_noticias
