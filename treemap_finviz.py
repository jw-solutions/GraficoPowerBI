import pandas as pd
import matplotlib.pyplot as plt
import squarify
import seaborn as sns

# Datos de ejemplo
data = {
    "Categoria": ["Tech", "Tech", "Finance", "Finance", "Healthcare", "Healthcare"],
    "Subcategoria": ["Software", "Hardware", "Banks", "Insurance", "Pharma", "Biotech"],
    "Valor": [5, -3, 2, -4, 3, -1]
}

df = pd.DataFrame(data)

# Crear una nueva columna combinando las categorías
df["Label"] = df["Categoria"] + " - " + df["Subcategoria"]

# Definir colores
norm = plt.Normalize(df["Valor"].min(), df["Valor"].max())
colors = [plt.cm.RdYlGn(norm(value)) for value in df["Valor"]]  # Rojo a verde degradado

# Crear el treemap
plt.figure(figsize=(16, 9))
squarify.plot(
    sizes=df["Valor"].abs(), 
    label=df["Label"], 
    color=colors, 
    alpha=0.8, 
    pad=True
)

plt.axis('off')
plt.title('Treemap estilo Finviz', fontsize=20)
plt.show()
