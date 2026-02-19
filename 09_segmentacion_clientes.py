import pandas as pd

# 1. CARGA CON "ANTIDOTO" PARA EL ERROR (encoding)
# Usamos 'latin1' para que no nos de el error Unicode
df = pd.read_csv("datos/retail_ventas.csv", encoding='latin1')

# 2. RADIOGRAFÍA INICIAL
print("--- RADIOGRAFÍA DEL GIGANTE DE RETAIL ---")
df.info()

# 3. ¿DÓNDE ESTÁ LA SUCIEDAD? (Limpieza estratégica)
print("\n--- CONTEO DE NULOS ---")
print(df.isnull().sum())

# --- LIMPIEZA ESTRATÉGICA DE RETAIL ---

# 1. Borramos nulos en CustomerID (Sin ID no hay cliente que segmentar)
df = df.dropna(subset=['CustomerID'])

# 2. Convertimos el ID a entero (para que no tenga el .0 al final)
df['CustomerID'] = df['CustomerID'].astype(int)

# 3. CONVERSIÓN DE FECHA: De texto a "Tiempo Real" de Python
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# 4. CREAMOS LA COLUMNA DE DINERO: Cantidad x Precio
df['TotalSum'] = df['Quantity'] * df['UnitPrice']

# 5. Quitamos devoluciones (Cantidades negativas que ensucian el dinero)
df = df[df['Quantity'] > 0]

print(f"--- LIMPIEZA COMPLETADA ---")
print(f"Registros finales limpios: {len(df)}")
print(f"Rango de fechas: de {df['InvoiceDate'].min()} hasta {df['InvoiceDate'].max()}")

# --- CÁLCULO DEL MODELO RFM ---

# 1. Aseguramos la limpieza (Por si acaso)
df = df.dropna(subset=['CustomerID'])
df = df[df['Quantity'] > 0]
df['TotalSum'] = df['Quantity'] * df['UnitPrice']

# 2. Definimos una "Fecha de Referencia" (Un día después de la última compra del dataset)
snapshot_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

# 3. Agrupamos por Cliente y calculamos R, F y M
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days, # Días desde la última compra
    'InvoiceNo': 'count',                                   # Cantidad de facturas
    'TotalSum': 'sum'                                       # Total de dinero
})

# 4. Renombramos las columnas para que se vean profesionales
rfm.rename(columns={
    'InvoiceDate': 'Recency',
    'InvoiceNo': 'Frequency',
    'TotalSum': 'MonetaryValue'
}, inplace=True)

print("--- TABLA RFM GENERADA ---")
print(rfm.head())
print(f"\nTotal de clientes únicos segmentados: {len(rfm)}")

# --- CLASIFICACIÓN DE CLIENTES (RANKING 1 a 4) ---

# 1. Creamos etiquetas (1 es el mejor, 4 es el peor)
# Para Recency: Menos días es MEJOR (1)
r_labels = range(1, 5)
# Para Frecuencia y Dinero: Más es MEJOR (1)
f_labels = range(4, 0, -1)
m_labels = range(4, 0, -1)

# 2. Dividimos a los clientes en 4 grupos iguales para cada métrica
rfm['R'] = pd.qcut(rfm['Recency'], q=4, labels=r_labels)
rfm['F'] = pd.qcut(rfm['Frequency'], q=4, labels=f_labels)
rfm['M'] = pd.qcut(rfm['MonetaryValue'], q=4, labels=m_labels)

# 3. Sumamos los puntos para crear el "Segmento"
# Un cliente '111' es perfecto en todo.
rfm['RFM_Score'] = rfm['R'].astype(str) + rfm['F'].astype(str) + rfm['M'].astype(str)

print("--- CLIENTES CLASIFICADOS ---")
print(rfm.head())

import matplotlib.pyplot as plt

# Graficamos cuánto dinero gastan los grupos de clientes
plt.figure(figsize=(10, 6))
rfm.groupby('RFM_Score')['MonetaryValue'].mean().sort_values(ascending=False).head(10).plot(kind='bar', color='gold')

plt.title('Top 10 Segmentos de Clientes por Gasto Promedio', fontsize=14)
plt.xlabel('Puntaje RFM (111 es el mejor)')
plt.ylabel('Gasto Promedio ($)')
plt.savefig("01_segmentos_gasto.png")
plt.close()

print("\n✅ ¡Gráfico de segmentos de oro guardado!")

import matplotlib.pyplot as plt

# --- MAPA ESTRATÉGICO DE ALTA DEFINICIÓN ---

plt.figure(figsize=(12, 7)) # Lo hacemos un poco más ancho para que respire

# Usamos 'plasma' (Violeta -> Rosa -> Amarillo) que es muy estético
# Limitamos los datos visualmente para que no se aplasten (Zoom)
scatter = plt.scatter(rfm['Recency'], rfm['Frequency'], 
            c=rfm['MonetaryValue'], 
            cmap='plasma', 
            s=60, # Burbujas un poco más grandes
            alpha=0.6,
            edgecolors='white', # Un borde blanco para que no se vean pixelados
            linewidth=0.5)

# --- EL TRUCO DEL ZOOM (AMPLIACIÓN) ---
# Eje X: Le damos un poco de aire después de los 373 días
plt.xlim(-20, 450) 

# Eje Y: Limitamos a 600 para ver el "corazón" de los clientes sin que el VIP de 8000 lo aplaste
plt.ylim(-10, 600) 

plt.title('Segmentación de Clientes: Comportamiento y Valor', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Días desde la última compra (Recency)', fontsize=12)
plt.ylabel('Cantidad de compras (Frequency)', fontsize=12)

# Barra de color elegante
cbar = plt.colorbar(scatter)
cbar.set_label('Valor Monetario Total ($)', fontsize=12, labelpad=15)

plt.grid(True, linestyle='--', alpha=0.3) # Una rejilla suave para guiar la vista
plt.tight_layout()

plt.savefig("02_mapa_calor_clientes.png")
plt.close()

print("✅ ¡Mapa de Alta Definición guardado con éxito!")