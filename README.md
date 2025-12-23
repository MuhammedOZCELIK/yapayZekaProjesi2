Karınca Kolonisi Algoritması ile Rota Optimizasyonu (Senaryo 3)

Bu proje, Yapay Zeka dersi kapsamında verilen Senaryo 3 ödevi için geliştirilmiştir. Projede, Karınca Kolonisi Optimizasyonu (Ant Colony Optimization – ACO) algoritması kullanılarak gerçek dünya verileri üzerinde bir rota optimizasyonu problemi çözülmektedir.

Çalışmanın amacı; bir aracın bir merkez noktadan (depo) başlayarak Bursa iline dağılmış 12 liseyi ziyaret etmesi ve tekrar başlangıç noktasına dönmesi durumunda, toplam yol süresini veya mesafesini en aza indiren rotayı bulmaktır.

Projenin Temel Mantığı

Uygulama, kullanıcıdan alınan adres bilgilerini kullanarak çalışır. Girilen adresler önce Google Geocoding API yardımıyla koordinatlara dönüştürülür. Daha sonra Google Distance Matrix API kullanılarak noktalar arasındaki gerçek sürüş mesafeleri veya süreleri hesaplanır.

Elde edilen bu bilgilerle oluşturulan maliyet matrisi, Karınca Kolonisi Algoritmasına girdi olarak verilir. Algoritma, farklı iterasyonlar boyunca en kısa rotayı bulmaya çalışır ve zamanla daha iyi çözümlere yakınsar.

Kullanılan Yöntem ve Teknolojiler

Projede aşağıdaki teknolojiler kullanılmıştır:

Python programlama dili

Streamlit ile web tabanlı kullanıcı arayüzü

Google Maps Geocoding API

Google Maps Distance Matrix API

Karınca Kolonisi Optimizasyonu (ACO) algoritması

Harita üzerinde görselleştirme

Google Distance Matrix API’nin istek sınırları dikkate alınarak, mesafe hesaplamaları parçalı (chunked) şekilde yapılmıştır. Bu sayede API limit hataları önlenmiştir.

Uygulama Özellikleri

Kullanıcı, depo adresini ve 12 adet okul adresini sisteme girebilir

Optimizasyon kriteri olarak mesafe veya süre seçilebilir

Karınca sayısı, iterasyon sayısı ve diğer ACO parametreleri kullanıcı tarafından ayarlanabilir

En uygun rota tablo halinde gösterilir

Toplam mesafe veya süre bilgisi hesaplanır

Bulunan rota harita üzerinde görsel olarak çizilir

Algoritmanın iterasyonlar boyunca gelişimi grafikle gösterilir

Sonuç

Bu proje ile, meta-sezgisel bir optimizasyon yöntemi olan Karınca Kolonisi Algoritması’nın, gerçek harita verileri kullanılarak rota optimizasyon problemlerinde etkin bir şekilde kullanılabildiği gösterilmiştir. Geliştirilen sistem, hem algoritmik hem de görsel açıdan kullanıcıya anlaşılır ve etkileşimli bir çözüm sunmaktadır.

Muhammed Emin ÖZÇELİK 2212721063
