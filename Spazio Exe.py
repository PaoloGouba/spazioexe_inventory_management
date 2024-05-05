# RIPARAZIONI
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
df = pd.read_csv("/Users/angelopillon/Documents/Spazio exe/reparations.csv")
print("Total Number of Orders:", len(df))
average_price = df['price'].mean().round(2)
average_price_str = f"€{average_price:,.2f}"
print("Average Price of Devices:", average_price_str)
popular_brands = df['brand'].value_counts().head(5) 
print("Top 5 Popular Brands:")  # Remove the extra formatting 
for brand, count in popular_brands.items():
    print(f"{brand}: {count}")
orders_by_state = df['state'].value_counts()
print("Orders by State:")
for state, count in orders_by_state.items():
    print(f"{state}: {count}")
plt.figure(figsize=(10, 6))
sns.barplot(x=orders_by_state.index, y=orders_by_state.values)
plt.xlabel('State')
plt.ylabel('Number of Orders')
plt.title('Orders Distribution by State')
plt.xticks(rotation=45)
plt.show()
plt.figure(figsize=(8, 8))
plt.pie(popular_brands.values, labels=popular_brands.index, autopct="%1.1f%%")
plt.title('Top 5 Popular Brands')
plt.show()


# Inventario
# Dispositivi
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df = pd.read_csv("/Users/angelopillon/Documents/Spazio exe/devices.csv")
# Handling missing values
df.fillna(method='ffill', inplace=True)  # Example: Forward-fill missing values
# Converting dates to datetime format
df['selling_date'] = pd.to_datetime(df['selling_date'])
# Creating new columns if needed
df['Margine_profitto'] = df['sell_price'] - df['price']
n_dispositivi_per_tipo = df["device_type"].value_counts()
for tipo_dispositivo, numero_dispositivi in n_dispositivi_per_tipo.items():
    print(f"- {tipo_dispositivo}: {numero_dispositivi}")
    
plt.figure(figsize=(8, 6))
n_dispositivi_per_tipo.plot(kind="bar", color=['tab:blue', 'tab:orange', 'tab:green', 'tab:purple'])
plt.title("Distribuzione dei tipi di dispositivo in magazzino")
plt.xlabel("Tipo di dispositivo")
plt.ylabel("Numero di dispositivi")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
# Conta il numero di dispositivi per ogni stato
n_dispositivi_per_stato = df["status"].value_counts()
plt.figure(figsize=(8, 6))
n_dispositivi_per_stato.plot(kind="bar")
plt.title("Distribuzione degli stati dei dispositivi")
plt.xlabel("Stato")
plt.ylabel("Numero di dispositivi")
plt.show()
# Conta il numero di dispositivi per ogni brand
n_dispositivi_per_brand = df["brand"].value_counts()

# Ordina i brand in base al numero di dispositivi
n_dispositivi_per_brand = n_dispositivi_per_brand.sort_values(ascending=False)

# Seleziona i primi 10 brand
top_10_brand = n_dispositivi_per_brand.head(10)

# Crea un grafico a barre per visualizzare i primi 10 brand con il maggior numero di dispositivi
plt.figure(figsize=(12, 6))
top_10_brand.plot(kind="bar")
plt.title("Top 10 brand con il maggior numero di dispositivi")
plt.xlabel("Brand")
plt.ylabel("Numero di dispositivi")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()
# ## Analisi del grado del dispositivo

# Conta il numero di dispositivi per ogni grado
n_dispositivi_per_grado = df["grade"].value_counts()

# Crea un grafico a torta per visualizzare la distribuzione dei gradi dei dispositivi
plt.figure(figsize=(8, 6))
n_dispositivi_per_grado.plot(kind="pie", autopct="%1.1f%%")
plt.title("Distribuzione dei gradi dei dispositivi")
plt.show()
# Accessori
df = pd.read_csv("/Users/angelopillon/Documents/Spazio exe/accessories.csv")
# Conta il numero di accessori per ogni tipologia
n_accessori_per_tipologia = df["typology"].value_counts()

# Crea un grafico a torta per visualizzare la distribuzione delle tipologie di accessori
plt.figure(figsize=(8, 6))
n_accessori_per_tipologia.plot(kind="pie", autopct="%1.1f%%", colors=['tab:blue', 'tab:orange', 'tab:green', 'tab:purple'])
plt.title("Distribuzione delle tipologie di accessori")
plt.show()