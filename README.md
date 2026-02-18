# 🛒 Inteligencia de Ventas: Predicción de Intención de Compra en E-commerce

![Status](https://img.shields.io)
![IA-Accuracy](https://img.shields.io)
![Sector](https://img.shields.io)

### 🕵️ El Desafío del Negocio
¿Por qué el 84% de los usuarios abandona la tienda sin comprar? Analizamos **12,330 sesiones de navegación** para identificar los patrones que convierten a un "visitante mirón" en un "comprador real". El objetivo es optimizar la tasa de conversión (CRO) y reducir el abandono de carrito.

### 🔍 Hallazgos Estratégicos (Insights):
1.  **El Mes de Oro:** **Noviembre** lidera la intención de compra, impulsado por eventos globales de descuentos. 👑🗓️
2.  **La Paradoja del Visitante:** Sorprendentemente, los **Nuevos Visitantes** tienen una tasa de conversión del **24.9%**, casi el doble que los recurrentes (14%). ¡La primera impresión es la que vende! 😍💸
3.  **El Valor de la Página:** Los compradores reales navegan por páginas con un `PageValue` **14 veces superior** al de los que abandonan.

### 📊 Evidencias Visuales de Conversión:

#### 1. Estacionalidad de Ventas por Mes
![Conversión por Mes](01_conversion_por_mes.png)

#### 2. ¿Qué "mira" la IA antes de una compra? (Feature Importance)
![Importancia de Pistas](02_importancia_pistas_ecommerce.png)

*Análisis Técnico: El **PageValues** y el **ExitRates** dominan el 70% de la decisión. El modelo detecta cuándo el usuario está a punto de abandonar o cerrar la transacción.*

---

### 💡 Recomendación de Negocio (ROI)
**Se recomienda implementar disparadores de ofertas (Exit-Intent Popups) cuando la IA detecte niveles altos de ExitRates en páginas de alto valor. Además, enfocar el presupuesto de marketing en la captación de tráfico nuevo durante Noviembre para maximizar el retorno de inversión.**

---

### ⚙️ Especificaciones Técnicas
*   **Motor de IA:** Random Forest Classifier con balanceo de clases.
*   **Métricas:** 89% Accuracy Global.
