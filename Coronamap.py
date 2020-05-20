"""
Created on Wed May 17 11:29:39 2020
@author: Omer
"""

#Gerekli kütüphanelerimizi ekledik
import pandas as pd
import geopandas as gpd
import PIL
import io

def tarihDuzelt(tarih): # Tarih MM/DD/YYYY şeklindeydi ve biz bunu kendimize uyarladık
    tarihS = tarih.split('/') # İlk / leri kaldırıp listeye aldık
    ###############
    temp = tarihS[0]
    tarihS[0] = tarihS[1] ### Yer değiştirme yaptık
    tarihS[1] = temp
    ###############
    return "/".join(tarihS) # Ve tekrardan düzgün halini / ile birleştirip return ettik

#İnternet üzerinden githubdaki verilere ulaşıp data adlı değişkene atadık
veriler = pd.read_html('https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

for veri in veriler:
#    print(veri) #Aldığımız dataları yazdırık
    veri = veri.groupby('Country/Region').sum()   # Bu kısımda aslında bir nevi veritabanı işlemi
                                                  # olan group by metodunu kullanıyoruz ve Ülke isimlerine
                                                  # göre bu verileri toparlıyoruz

veri = veri.drop(columns = ['Lat','Long','Unnamed: 0']) # Burada gereksiz olan sütunları kaldırdık
                                                        # Enlem boylam bilgisi tam olarak doğru olmadığı
                                                        # için onu da kaldırdık ki doğrusunu ekleyelim

transpoz_veri = veri.T    #Bu satırda verimizin transpozunu aldık ki günlere göre işlem yapabilelim

dunya = gpd.read_file(r'C:\Users\Omer\Desktop\Yedekler\Projeler\Python\Projeler\CoronApp\World_Countries\World_Countries.shp')
#Dunya haritası ile alakalı verilerimizi bu yolla aldık
#İstersersek dunya.plot() ile bunu görselleştirebiliriz


######################################## İki listede olup isimleri aynı olmayanları değiştirdik
dunya.replace('Myanmar','Burma' , inplace = True)
dunya.replace('Cape Verde','Cabo Verde' , inplace = True)
dunya.replace('United States', 'US', inplace = True)
dunya.replace('Czech Republic', 'Czechia', inplace = True)
dunya.replace('Democratic Republic of the Congo','Congo (Brazzaville)' , inplace = True)
dunya.replace('Ivory Coast','Cote d\'Ivoire' , inplace = True)
dunya.replace('Swaziland','Eswatini' , inplace = True)
dunya.replace('South Korea','Korea, South' , inplace = True)
dunya.replace('St. Kitts and Nevis','Saint Kitts and Nevis' , inplace = True)
dunya.replace('St. Lucia','Saint Lucia' , inplace = True)
dunya.replace('St. Vincent and the Grenadines','Saint Vincent and the Grenadines' , inplace = True)
dunya.replace('Taiwan','Taiwan*' , inplace = True)
dunya.replace('East Timor','Timor-Leste' , inplace = True)
dunya.replace('Palestine','West Bank and Gaza' , inplace = True)
##########################################


for index,row in veri.iterrows():
    if index not in dunya['COUNTRY'].to_list(): # Bu döngü ile birlikte iki listede de olan
        print(index+" listede yok ")            # ülke adlarının var olup olmadıklarını kontrol ettik
    else:                                       # ki birleştirirken sorun yaşamayalım ve düzeltelim
        pass



birlesim = dunya.join(veri,on = 'COUNTRY' , how = 'right') # Bu kısımda iki tablomuzu 
                                                           # doğru coğrafik konumlar ile vaka sayısını
                                                           # bir tabloda toplamak amacıyla birleştiriyoruz  

image_frames = []
for tarih in birlesim.columns.to_list()[2:]: # Tarihleri sütunlardan aldık ve tarihler 2. sütundan başlıyor
    tablo = birlesim.plot(column = tarih ,   
                          cmap = 'OrRd', # Renk skalasını seçtik Orange/Red
                          legend = True, # Sol tarafta bulunan göstergeyi açtık
                          scheme = 'user_defined', # Şema kısmını kendimiz ayarlayacağımızı söyledik
                          classification_kwds = {'bins':[10, 20, 50, 100, 500, 1000, 5000, 10000, 500000]},
                          edgecolor = 'black', # Kenar rengini seçtik
                          linewidth = 0.3,     # Sınırların kalınlığını seçtik
                          )
    
    tablo.set_title(tarihDuzelt(tarih)+' Tarihindeki Toplam Coronavirüs Vakaları', fontdict = 
                 {'fontsize':20}, pad = 0)  # Üstte bulunan başlığımızı ekledik ve ayarladık
    
    tablo.set_axis_off() # Yanda ve Üstte bulunan çizgileri yoketmek için
    
    tablo.get_legend().set_bbox_to_anchor((0.1, 0.7)) # Legend sol taraftaki çizelgemiz
                                                      # Ve burada onun konumunu ayarlıyoruz
    
    img = tablo.get_figure() # Resmi burada figüre dönüştürüp değişkene atarız
    
    
    f = io.BytesIO()
    img.savefig(f, format = 'png', bbox_inches = 'tight',pad_inches=0.4) # Figürümüzü kaydederiz
    f.seek(0)
    image_frames.append(PIL.Image.open(f)) # Ve kayıtlı figürü framelerimizin içine attık 


# Burada GIF Oluşturduk 
image_frames[0].save('Coronamap.gif', format = 'GIF',   # Dosya ismi , formatı
            append_images = image_frames[1:],           # Ekleyeceğimiz resimler
            save_all = True, duration = 300,            # Hızı
            loop = 2)                                   # Ve tekrar sayısı

f.close()


        