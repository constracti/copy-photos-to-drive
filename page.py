class Page:

	def __init__(self, title):
		self.title = title
		self.body_tags = []

	def add_body_tag(self, tag):
		self.body_tags.append(tag)

	def get_html(self):
		html = '<html>\n'
		html += '<head>\n'
		html += f'<title>{self.title}</title>\n'
		html += '</head>\n'
		html += '<body>\n'
		html += f'<h1>{self.title}</h1>\n'
		for tag in self.body_tags:
			html += tag
		html += '</body>\n'
		html += '</html>\n'
		return html
