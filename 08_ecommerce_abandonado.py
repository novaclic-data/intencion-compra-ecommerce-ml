import pandas as pd

# 1. CARGA (Tu carpeta sagrada de 'datos' 📂)
df = pd.read_csv("datos/intencion_compra.csv")

# 2. DETECTOR DE "SUCIEDAD" WEB
print("--- BUSCANDO HUECOS (NULOS) ---")
print(df.isnull().sum())

print("\n--- BUSCANDO SESIONES REPETIDAS (DUPLICADOS) ---")
print(df.duplicated().sum())

# 3. LIMPIEZA AUTOMÁTICA (Si hay pocos nulos, los borramos; si hay duplicados, se van)
# En este dataset de UCI, los nulos suelen ser poquitos.
df = df.dropna()
df = df.drop_duplicates()

print("\n✅ ¡TIENDA LIMPIA! Registros finales:", len(df))

# 4. EL BALANCE REAL (REVENUE)
# True = Compró | False = Abandonó el carrito
balance = df['Revenue'].value_counts()
porcentaje = df['Revenue'].value_counts(normalize=True) * 100

print("\n--- RESULTADOS DE VENTAS ---")
print(balance)
print(f"\n--- % DE CONVERSIÓN REAL ---")
print(porcentaje)

# --- INVESTIGACIÓN DE TEMPORALIDAD Y COMPORTAMIENTO ---

# 1. ¿Fines de semana (Weekend) vs Días de semana?
# True = Fin de semana | False = Lunes a Viernes
duelo_finde = pd.crosstab(df['Weekend'], df['Revenue'], normalize='index') * 100

print("--- % DE COMPRA: FIN DE SEMANA vs SEMANA ---")
print(duelo_finde)

# 2. El "Efecto Mes": ¿Cuál es el mes de las ventas de oro?
duelo_mes = pd.crosstab(df['Month'], df['Revenue'], normalize='index') * 100
print("\n--- % DE COMPRA POR MES (RANKING) ---")
print(duelo_mes.sort_values(by=True, ascending=False))

# --- DUELO DE LEALTAD: ¿NUEVO O CONOCIDO? ---

# 1. Analizamos la conversión por tipo de visitante
duelo_lealtad = pd.crosstab(df['VisitorType'], df['Revenue'], normalize='index') * 100

print("--- % DE CONVERSIÓN POR LEALTAD ---")
print(duelo_lealtad.sort_values(by=True, ascending=False))

# 2. El "Radar de Abandono": ¿Quién se va más rápido?
# ExitRates: Mientras más alto, más rápido cerraron la pestaña
abandono_promedio = df.groupby('VisitorType')['ExitRates'].mean()
print("\n--- TASA DE SALIDA PROMEDIO POR VISITANTE ---")
print(abandono_promedio)

# --- EL PODER DEL CONTENIDO: PAGE VALUES ---

# 1. ¿Cuánto vale la navegación de un comprador (True) vs un mirón (False)?
valor_promedio = df.groupby('Revenue')['PageValues'].mean()

print("--- VALOR DE PÁGINA PROMEDIO ---")
print("False = Se fue | True = COMPRÓ")
print(valor_promedio)

# 2. El "Radar de Decisión": ¿Cuántas páginas mira alguien antes de irse?
# Administrative: Páginas de cuenta/gestión
# Informational: Páginas de contacto/quiénes somos
# ProductRelated: Páginas de PRODUCTO (Las que traen el dinero)

paginas_por_compra = df.groupby('Revenue')[['Administrative', 'Informational', 'ProductRelated']].mean()
print("\n--- PROMEDIO DE PÁGINAS VISITADAS ---")
print(paginas_por_compra)

import matplotlib.pyplot as plt

# 1. Creamos la tabla de conversión por Mes
mes_ventas = pd.crosstab(df['Month'], df['Revenue'], normalize='index') * 100

# 2. Graficamos el éxito de ventas por mes
plt.figure(figsize=(12, 6))
mes_ventas[True].sort_values(ascending=False).plot(kind='bar', color='#f39c12')

plt.title('Ranking de Conversión: ¿En qué mes se compra más?', fontsize=14)
plt.xlabel('Mes del Año')
plt.ylabel('% de Compras Reales (Revenue = True)')
plt.xticks(rotation=45)

# 3. Guardamos el primer tesoro del Caso E-commerce
plt.savefig("01_conversion_por_mes.png")
plt.close()

print("\n✅ ¡Gráfico de Estacionalidad guardado!")

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. Seleccionamos las "Pistas del Comprador"
pistas_web = ['Administrative', 'Informational', 'ProductRelated', 
               'ExitRates', 'PageValues', 'Month', 'VisitorType']
X = df[pistas_web]
y = df['Revenue']

# 2. El TRADUCTOR UNIVERSAL (Dummies)
X = pd.get_dummies(X, drop_first=True)

# 3. DIVIDIMOS (80% Entrenamiento / 20% Examen)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. ENTRENAMOS AL "VENDEDOR VIRTUAL" (Random Forest)
# Usamos 'balanced' porque las compras (True) son poquitas (15%)
modelo_tienda = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
modelo_tienda.fit(X_train, y_train)

# 5. EL VEREDICTO
print("\n--- REPORTE DE PREDICCIÓN DE VENTAS ---")
predicciones = modelo_tienda.predict(X_test)
print(classification_report(y_test, predicciones))

# --- ¿QUÉ DELATA AL COMPRADOR? (IMPORTANCIA) ---

# 1. Extraemos el peso de cada pista
importancia = pd.Series(modelo_tienda.feature_importances_, index=X.columns)

# 2. Creamos el gráfico elegante
plt.figure(figsize=(10, 6))
importancia.sort_values(ascending=True).tail(10).plot(kind='barh', color='#2ecc71')

plt.title('¿Qué pistas delatan una compra inminente?', fontsize=14)
plt.xlabel('Importancia (Peso en la Decisión)')
plt.tight_layout()

# 3. Guardamos la Evidencia #2
plt.savefig("02_importancia_pistas_ecommerce.png")
plt.close()

print("✅ ¡Gráfico de Pistas de Venta guardado!")