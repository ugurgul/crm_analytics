
###############################################################
# RFM ile Müşteri Segmentasyonu (Customer Segmentation with RFM)
###############################################################

###############################################################
# İş Problemi (Business Problem)
###############################################################
# FLO müşterilerini segmentlere ayırıp bu segmentlere göre pazarlama stratejileri belirlemek istiyor.
# Buna yönelik olarak müşterilerin davranışları tanımlanacak ve bu davranış öbeklenmelerine göre gruplar oluşturulacak..

###############################################################
# Veri Seti Hikayesi
###############################################################

# Veri seti son alışverişlerini 2020 - 2021 yıllarında OmniChannel(hem online hem offline alışveriş yapan) olarak yapan müşterilerin geçmiş alışveriş davranışlarından
# elde edilen bilgilerden oluşmaktadır.

# master_id: Eşsiz müşteri numarası
# order_channel : Alışveriş yapılan platforma ait hangi kanalın kullanıldığı (Android, ios, Desktop, Mobile, Offline)
# last_order_channel : En son alışverişin yapıldığı kanal
# first_order_date : Müşterinin yaptığı ilk alışveriş tarihi
# last_order_date : Müşterinin yaptığı son alışveriş tarihi
# last_order_date_online : Muşterinin online platformda yaptığı son alışveriş tarihi
# last_order_date_offline : Muşterinin offline platformda yaptığı son alışveriş tarihi
# order_num_total_ever_online : Müşterinin online platformda yaptığı toplam alışveriş sayısı
# order_num_total_ever_offline : Müşterinin offline'da yaptığı toplam alışveriş sayısı
# customer_value_total_ever_offline : Müşterinin offline alışverişlerinde ödediği toplam ücret
# customer_value_total_ever_online : Müşterinin online alışverişlerinde ödediği toplam ücret
# interested_in_categories_12 : Müşterinin son 12 ayda alışveriş yaptığı kategorilerin listesi

###############################################################
# GÖREVLER
###############################################################

# GÖREV 1: Veriyi Anlama (Data Understanding) ve Hazırlama
           # 1. flo_data_20K.csv verisini okuyunuz.
           # 2. Veri setinde
                     # a. İlk 10 gözlem,
                     # b. Değişken isimleri,
                     # c. Betimsel istatistik,
                     # d. Boş değer,
                     # e. Değişken tipleri, incelemesi yapınız.
           # 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir. Herbir müşterinin toplam
           # alışveriş sayısı ve harcaması için yeni değişkenler oluşturun.
           # 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.
           # 5. Alışveriş kanallarındaki müşteri sayısının, ortalama alınan ürün sayısının ve ortalama harcamaların dağılımına bakınız.
           # 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.
           # 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.
           # 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.

#1
import pandas as pd
import datetime as dt
pd.set_option('display.max_columns', None)
df_ = pd.read_csv('datasets/flo_data_20k.csv')
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option("display.width", 500)
df = df_.copy()

#2

#a
df.head(10)
#b
df.columns
#c
df.describe().T
#d
df.isnull().sum()
#e
df.columns.dtype.type

#3
df["order_num_total_ever_offline"]
df["order_num_total_ever_online"]

df["customer_value_total_ever_offline"]
df["customer_value_total_ever_online"]

df["total_order"] = df["order_num_total_ever_offline"] + df["order_num_total_ever_online"]

df["total_order_value"] = df["customer_value_total_ever_offline"] + df["customer_value_total_ever_online"]

#4
print(df.dtypes)

df["first_order_date"] = pd.to_datetime(df['first_order_date'])
df["last_order_date"] = pd.to_datetime(df['last_order_date'])
df["last_order_date_online"] = pd.to_datetime(df['last_order_date_online'])
df["last_order_date_offline"] = pd.to_datetime(df['last_order_date_offline'])

#5
df.groupby('order_channel').agg({
    'master_id': pd.Series.nunique,  # Benzersiz müşteri sayısı
    'total_order': 'sum',  # Online toplam ürün sayısı
    'total_order_value': 'sum',  # Online toplam harcamalar
}).reset_index()

#6
df.groupby('master_id').agg({'total_order_value': "sum"}).sort_values(by='total_order_value', ascending=False).head(10)

#7
df["total_order"] = df["total_order"].astype(int)
df.groupby('master_id').agg({'total_order': "sum"}).sort_values(by="total_order",ascending=False).head(10)

#8
def data_prep(dataframe,first_ten=False):
    dataframe["total_order"] = dataframe["order_num_total_ever_offline"] + dataframe["order_num_total_ever_online"]
    dataframe["total_order_value"] = dataframe["customer_value_total_ever_offline"] + dataframe["customer_value_total_ever_online"]

    dataframe["first_order_date"] = pd.to_datetime(dataframe['first_order_date'])
    dataframe["last_order_date"] = pd.to_datetime(dataframe['last_order_date'])
    dataframe["last_order_date_online"] = pd.to_datetime(dataframe['last_order_date_online'])
    dataframe["last_order_date_offline"] = pd.to_datetime(dataframe['last_order_date_offline'])

    prep_df = dataframe.groupby('order_channel').agg({
        'master_id': pd.Series.nunique,  # Benzersiz müşteri sayısı
        'total_order': 'sum',  # Online toplam ürün sayısı
        'total_order_value': 'sum',  # Online toplam harcamalar
    }).reset_index()

    if first_ten:
        prep_df = dataframe.groupby('master_id').agg({'total_order_value': "sum"}).sort_values(by='total_order_value', ascending=False).head(
            10)
        prep_df = dataframe["total_order"] = dataframe["total_order"].astype(int)
        prep_df = dataframe.groupby('master_id').agg({'total_order': "sum"}).sort_values(by="total_order", ascending=False).head(10)

    return prep_df


# GÖREV 2: RFM Metriklerinin Hesaplanması

#1 & 2

today_date = dt.datetime(2021, 6, 2)


df.groupby("master_id").agg({"last_order_date": lambda last_order_date: (today_date - last_order_date.max()).days,
                             "total_order": lambda total_order: total_order,
                             "total_order_value": lambda total_order_value: total_order_value.sum()})

#3
rfm = df.groupby("master_id").agg({"last_order_date": lambda last_order_date: (today_date - last_order_date.max()).days,
                             "total_order": lambda total_order: total_order,
                             "total_order_value": lambda total_order_value: total_order_value.sum()})

#4
rfm.columns = ['recency', 'frequency', 'monetary']


# GÖREV 3: RF ve RFM Skorlarının Hesaplanması

rfm["recency_score"] = pd.qcut(rfm["recency"], q=5, labels=[5, 4, 3, 2, 1])

rfm["frequency_score"] = pd.qcut(rfm["frequency"].rank(method="first"), q=5, labels=[1, 2, 3, 4, 5])

rfm["monetary_score"] = pd.qcut(rfm["monetary"], q=5, labels=[1, 2, 3, 4, 5])

rfm["RFM_SCORE"] = (rfm['recency_score'].astype(str) +
                    rfm['frequency_score'].astype(str))


# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması

seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'new_customers',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm['segment'] = rfm['RFM_SCORE'].replace(seg_map, regex=True)


# GÖREV 5: Aksiyon zamanı!
           # 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.
           # 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulun ve müşteri id'lerini csv ye kaydediniz.
                   # a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
                   # tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Sadık müşterilerinden(champions,loyal_customers),
                   # ortalama 250 TL üzeri ve kadın kategorisinden alışveriş yapan kişiler özel olarak iletişim kuralacak müşteriler. Bu müşterilerin id numaralarını csv dosyasına
                   # yeni_marka_hedef_müşteri_id.cvs olarak kaydediniz.
                   # b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşteri olan ama uzun süredir
                   # alışveriş yapmayan kaybedilmemesi gereken müşteriler, uykuda olanlar ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
                   # olarak kaydediniz.

#1################################################
rfm[["segment", "recency", "frequency", "monetary"]].groupby("segment").agg(["mean", "count"])


rfm[(rfm["segment"] == "champions") & (rfm["segment"] == "loyal_customers")]

filtered_rfm = rfm[rfm['segment'].isin(['champions', 'loyal_customers'])]

filtered_df = df[df['interested_in_categories_12'].str.contains('KADIN')]

merged_df = pd.merge(filtered_rfm, filtered_df, on='master_id')

merged_df["master_id"]

merged_df['master_id'].to_csv("customer_rfm_id.csv", index=False)


#2##########################################################################

rfm["segment"].value_counts()
"cant_loose","about_to_sleep","new_customers"

filtered_rfm = rfm[rfm["segment"].isin(['cant_loose', 'about_to_sleep', "new_customers"])]

filtered_df = df[df['interested_in_categories_12'].str.contains('ERKEK', "COCUK")]

merged_df = pd.merge(filtered_rfm, filtered_df, on="master_id")

merged_df['master_id'].to_csv("customer_rfm.csv", index=False)


# GÖREV 6: Tüm süreci fonksiyonlaştırınız.





###############################################################
# GÖREV 1: Veriyi  Hazırlama ve Anlama (Data Understanding)
###############################################################


# 2. Veri setinde
        # a. İlk 10 gözlem,
        # b. Değişken isimleri,
        # c. Boyut,
        # d. Betimsel istatistik,
        # e. Boş değer,
        # f. Değişken tipleri, incelemesi yapınız.



# 3. Omnichannel müşterilerin hem online'dan hemde offline platformlardan alışveriş yaptığını ifade etmektedir.
# Herbir müşterinin toplam alışveriş sayısı ve harcaması için yeni değişkenler oluşturunuz.



# 4. Değişken tiplerini inceleyiniz. Tarih ifade eden değişkenlerin tipini date'e çeviriniz.


# df["last_order_date"] = df["last_order_date"].apply(pd.to_datetime)



# 5. Alışveriş kanallarındaki müşteri sayısının, toplam alınan ürün sayısı ve toplam harcamaların dağılımına bakınız.



# 6. En fazla kazancı getiren ilk 10 müşteriyi sıralayınız.




# 7. En fazla siparişi veren ilk 10 müşteriyi sıralayınız.




# 8. Veri ön hazırlık sürecini fonksiyonlaştırınız.


###############################################################
# GÖREV 2: RFM Metriklerinin Hesaplanması
###############################################################

# Veri setindeki en son alışverişin yapıldığı tarihten 2 gün sonrasını analiz tarihi



# customer_id, recency, frequnecy ve monetary değerlerinin yer aldığı yeni bir rfm dataframe


###############################################################
# GÖREV 3: RF ve RFM Skorlarının Hesaplanması (Calculating RF and RFM Scores)
###############################################################

#  Recency, Frequency ve Monetary metriklerini qcut yardımı ile 1-5 arasında skorlara çevrilmesi ve
# Bu skorları recency_score, frequency_score ve monetary_score olarak kaydedilmesi




# recency_score ve frequency_score’u tek bir değişken olarak ifade edilmesi ve RF_SCORE olarak kaydedilmesi


###############################################################
# GÖREV 4: RF Skorlarının Segment Olarak Tanımlanması
###############################################################

# Oluşturulan RFM skorların daha açıklanabilir olması için segment tanımlama ve  tanımlanan seg_map yardımı ile RF_SCORE'u segmentlere çevirme


###############################################################
# GÖREV 5: Aksiyon zamanı!
###############################################################

# 1. Segmentlerin recency, frequnecy ve monetary ortalamalarını inceleyiniz.



# 2. RFM analizi yardımı ile 2 case için ilgili profildeki müşterileri bulunuz ve müşteri id'lerini csv ye kaydediniz.

# a. FLO bünyesine yeni bir kadın ayakkabı markası dahil ediyor. Dahil ettiği markanın ürün fiyatları genel müşteri tercihlerinin üstünde. Bu nedenle markanın
# tanıtımı ve ürün satışları için ilgilenecek profildeki müşterilerle özel olarak iletişime geçeilmek isteniliyor. Bu müşterilerin sadık  ve
# kadın kategorisinden alışveriş yapan kişiler olması planlandı. Müşterilerin id numaralarını csv dosyasına yeni_marka_hedef_müşteri_id.cvs
# olarak kaydediniz.



# b. Erkek ve Çoçuk ürünlerinde %40'a yakın indirim planlanmaktadır. Bu indirimle ilgili kategorilerle ilgilenen geçmişte iyi müşterilerden olan ama uzun süredir
# alışveriş yapmayan ve yeni gelen müşteriler özel olarak hedef alınmak isteniliyor. Uygun profildeki müşterilerin id'lerini csv dosyasına indirim_hedef_müşteri_ids.csv
# olarak kaydediniz.
