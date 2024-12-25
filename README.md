source .venv/bin/activate
source .venv/bin/activate.fish

query: Var olan vektörlerden belirli koşulları (örneğin, metadata değerleri) sağlayanları döndürür.
search: Elinizdeki vektöre en yakın olan vektörleri ve ilgili verileri döndürür.

1. create_collection() – Koleksiyon Oluşturma
    > Bu fonksiyon, şema tanımlaması yaparak veri tiplerini ve koleksiyon özelliklerini belirtmenizi sağlar.

2. insert() – Veri Ekleme
    > Bu fonksiyon, koleksiyona vektörler ve diğer metadata'yı ekler. Genellikle vektörler için ID, vector verisi ve ek bilgileri (metin, etiket vb.) içeren bir liste alır.

3. search() – Vektör Araması
    > Bu fonksiyon, sorgu vektörüne en benzer olan verileri arar. nprobe parametresi, aramanın doğruluğunu ve hızını etkiler. limit parametresi ise döndürülecek en yakın komşu sayısını belirler.

4. query() – Veri Sorgulama
    > query fonksiyonu, vektörler arası benzerlik araması yapmaz; bunun yerine, metadata üzerinden belirli koşullara uyan verileri döndürür.

5. delete() – Veri Silme
    > Bu fonksiyon, koleksiyon içindeki belirli koşullara uyan verileri silmek için kullanılır. 

6. drop_collection() – Koleksiyon Silme
    > Koleksiyonu tamamen siler, içindeki tüm veriler kaybolur.

7. has_collection() – Koleksiyon Var mı?
    > Bu fonksiyon, koleksiyonun sistemde mevcut olup olmadığını kontrol eder.

8. list_collections() – Koleksiyonları Listeleme
    >  Sistemdeki mevcut tüm koleksiyonların isimlerini döndürür.

9. get_collection_info() – Koleksiyon Bilgisi
    > Koleksiyon hakkında yapı bilgilerini döndürür (örn. koleksiyonun boyutu, veri tipleri vb.).

10. load_collection() – Koleksiyonu Yükleme
    > Bu fonksiyon, arama işlemleri yapılabilmesi için koleksiyonu bellek üzerine yükler. Koleksiyon belleğe yüklendikten sonra veri aramaları yapılabilir.

11. release_collection() – Koleksiyonu Serbest Bırakma
    >Açıklama: Bellekte yüklenen koleksiyonu serbest bırakır. Bu işlem, belleği serbest bırakmak için gereklidir.


QT Install
    sudo apt-get install python3-pyqt5