import pandas as pd

def extract_features_for_rating_prediction(df: pd.DataFrame) -> pd.DataFrame:
	"""
	Recebe um DataFrame com colunas: Título, Preço, Avaliação, Disponibilidade, Categoria, Imagem
	Retorna um DataFrame apenas com as features relevantes para treinar um modelo de predição de avaliação:
	- Preço (float)
	- Disponibilidade (int: quantidade disponível extraída do texto)
	- Categoria (str)
	- Avaliação (target, convertida para número)
	"""
	
	df = df.copy()
	df['Preço'] = df['Preço'].replace('[£$]', '', regex=True).astype(float)

	# Converter disponibilidade para 1 (em estoque) ou 0 (fora de estoque)
	def in_stock(text):
		return 1 if 'in stock' in str(text).lower() else 0
	df['Disponibilidade'] = df['Disponibilidade'].apply(in_stock)

	# Converter avaliação textual para número
	rating_map = {
		'Zero': 0, 'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5
	}
	df['Avaliação'] = df['Avaliação'].map(rating_map)

	# Selecionar apenas as colunas relevantes
	features = df[['Preço', 'Disponibilidade', 'Categoria', 'Avaliação']].dropna()
	return features

