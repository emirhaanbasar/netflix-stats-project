# Gerekli kütüphaneler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.stats import t, chi2

# 1. Veri yükleme
veri = pd.read_csv("C:/Users/emirh/OneDrive/Desktop/archive/netflix_titles.csv", encoding='ISO-8859-1')
yillar = veri['release_year'].dropna().astype(int).tolist()

# 2. Tanımlayıcı istatistikler
adet = len(yillar)
ortalama = sum(yillar) / adet

sirali = sorted(yillar)

if adet % 2 == 0:
    medyan = (sirali[adet // 2 - 1] + sirali[adet // 2]) / 2
else:
    medyan = sirali[adet // 2]

varyans = sum((x - ortalama) ** 2 for x in yillar) / (adet - 1)
sapma = math.sqrt(varyans)
shata = sapma / math.sqrt(adet)

print("Ortalama (Mean):", round(ortalama, 3))
print("Medyan:", medyan)
print("Varyans:", round(varyans, 3))
print("Standart Sapma:", round(sapma, 3))
print("Standart Hata:", round(shata, 3))

# 3. Aykırı Değer Tespiti (IQR yöntemi)
q1 = pd.Series(yillar).quantile(0.25)
q3 = pd.Series(yillar).quantile(0.75)
iqr = q3 - q1
alt_sinir = q1 - 1.5 * iqr
ust_sinir = q3 + 1.5 * iqr
aykirilar = [x for x in yillar if x < alt_sinir or x > ust_sinir]
print("\nAykırı Değer Sayısı:", len(aykirilar))

# 4. %95 Güven Aralığı - Ortalama
z = 1.96
guven_alt = ortalama - z * shata
guven_ust = ortalama + z * shata
print("\nOrtalama için %95 Güven Aralığı: [{:.3f}, {:.3f}]".format(guven_alt, guven_ust))

# 5. %95 Güven Aralığı - Varyans
alfa = 0.05
chi2_alt = chi2.ppf(alfa / 2, df=adet - 1)
chi2_ust = chi2.ppf(1 - alfa / 2, df=adet - 1)
var_guven_alt = (adet - 1) * varyans / chi2_ust
var_guven_ust = (adet - 1) * varyans / chi2_alt
print("Varyans için %95 Güven Aralığı: [{:.3f}, {:.3f}]".format(var_guven_alt, var_guven_ust))

# 6. Hipotez Testi (H0: ortalama = 2015)
pop_ort = 2015
t_sayi = (ortalama - pop_ort) / shata
p_deger = 2 * (1 - t.cdf(abs(t_sayi), df=adet - 1))

print("\nHipotez Testi (H0: Ortalama = 2015)")
print("t-değeri:", round(t_sayi, 3))
print("p-değeri:", round(p_deger, 5))
if p_deger < 0.05:
    print("Sonuç: H0 reddedildi. Ortalama 2015'ten farklıdır.")
else:
    print("Sonuç: H0 kabul edilir. Ortalama 2015 olabilir.")

# 7. Örneklem Büyüklüğü (%90 güven, ±0.1 hata)
z90 = 1.645
hata_payi = 0.1
gerekli_ornek_sayisi = math.ceil((z90 * sapma / hata_payi) ** 2)
print("\n±0.1 hata payı ile, %90 güven düzeyinde gereken örneklem sayısı:", gerekli_ornek_sayisi)

# 8. Grafikler 
yillar_df = pd.Series(yillar)

plt.figure(figsize=(14, 6))

# Histogram 
plt.subplot(1, 2, 1)
sns.histplot(yillar_df, bins=30, kde=True, color='skyblue', edgecolor='black')
plt.title("Yayın Yılı Dağılımı (Histogram)")
plt.xlabel("Yayın Yılı")
plt.ylabel("Frekans")
plt.grid(True, linestyle='--', alpha=0.5)

# Boxplot
plt.subplot(1, 2, 2)
sns.boxplot(x=yillar_df, color='lightgreen')
plt.title("Yayın Yılı Dağılımı (Boxplot)")
plt.xlabel("Yayın Yılı")
plt.grid(True, axis='x', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()
