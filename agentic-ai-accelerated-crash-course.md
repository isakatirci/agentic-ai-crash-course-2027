# Agentic AI Engineering 2027: Sıfırdan Production'a Hızlandırılmış Uygulamalı Kurs (Accelerated Crash Course)

> **Hedef Kitle:** Yazılım ve yapay zekâ dünyasına sıfırdan başlayan **Junior Developer**'lar.
> **Tahmini Uzunluk:** ~30–35 A4 Sayfası (40 sayfa sınırının altında, yoğun ve gereksiz tekrardan arındırılmış).
> **Çalışma Modeli:** Her modülde önce *Neden?* sorusunu sade bir benzetmeyle kavrayacak, kritik İngilizce terimleri öğrenecek, mekanizmayı adım adım görecek ve hemen ardından `labs/` klasöründeki eksiksiz Python kodunu çalıştıracaksınız.

---

## İçindekiler
- [Modül 0: Kurulum ve Zihinsel Model (Setup & Mental Model)](#modül-0-kurulum-ve-zihinsel-model-setup--mental-model)
- [Modül 1: LLM Engineering Temelleri](#modül-1-llm-engineering-temelleri)
- [Modül 2: Tool Use & Function Calling](#modül-2-tool-use--function-calling)
- [Modül 3: Agent Memory & State Management](#modül-3-agent-memory--state-management)
- [Modül 4: RAG, Vector Databases & Agentic RAG](#modül-4-rag-vector-databases--agentic-rag)
- [Modül 5: Model Context Protocol (MCP)](#modül-5-model-context-protocol-mcp)
- [Modül 6: Planning & Multi-Agent Orchestration (Mimari Trade-off'lar)](#modül-6-planning--multi-agent-orchestration-mimari-trade-offlar)
- [Modül 7: Production-Ready Engineering & 3 Kritik Tuzak](#modül-7-production-ready-engineering--3-kritik-tuzak)
- [Modül 8: Hemen Uygulanabilir Capstone Mini-Project & 14 Günlük Pratik Planı](#modül-8-hemen-uygulanabilir-capstone-mini-project--14-günlük-pratik-planı)
- [Master Glossary (Terimler Sözlüğü)](#master-glossary-terimler-sözlüğü)

---

## Modül 0: Kurulum ve Zihinsel Model (Setup & Mental Model)

### 1. Ne Öğreneceğiz & Neden Önemli?
Bir **LLM** (*Large Language Model*) API'sine soru sorup yanıt almak bugün yalnızca birkaç satır kod sürer. Ancak gerçek bir şirkette çalışan sistemler tek bir soru-cevapla bitmez. Müşterinin siparişini veritabanından sorgulamalı, önceki mesajları hatırlamalı, hata aldığında planını güncellemeli ve gerekirse başka yazılımlarla konuşmalıdır.

Bunu günlük hayattan bir örnekle düşünelim.
- **Klasik Prompt-and-Response yaklaşımı**, masasında sadece ansiklopedi bulunan bir danışmana benzer. Ona bir soru sorarsınız. Bildiği kadarıyla tek seferde cevap verir. Telefon açamaz, bilgisayardan sipariş kontrol edemez ve iki dakika sonra adınızı unutur.
- **Agentic AI yaklaşımı**, elinde telefonu, takvimi, not defteri ve şirket veritabanı ekranı olan bir operasyon uzmanına benzer. Hedefi anlar. Plan yapar. Gerekli araçları (*Tools*) kullanır. Sonucu kontrol eder. Eksik varsa ikinci bir adım atar ve işi bitirip size net bir rapor verir.

Bu modülde bilgisayarınızı temiz bir şekilde hazırlayacak ve tüm kurs boyunca kullanacağınız zihinsel modeli oturtacaksınız.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **LLM (Large Language Model):** Çok büyük metin verileriyle eğitilmiş, metin anlama ve üretme yeteneğine sahip yapay zekâ modelidir.
- **Prompt-and-Response:** Kullanıcının modele tek bir girdi (*Prompt*) gönderdiği ve modelin tek bir yanıt (*Response*) döndürdüğü statik etkileşim biçimidir.
- **Agentic AI:** Yalnızca metin üretmekle kalmayıp hedefe ulaşmak için plan yapan, harici araçlar (*Tools*) çağıran, bellek (*Memory*) tutan ve kendi çıktılarını değerlendirip adım adım ilerleyen yazılım mimarisidir.
- **Production:** Yazılımın geliştirici bilgisayarından çıkıp gerçek kullanıcıların hizmetine sunulduğu canlı çalışma ortamıdır.
- **Virtual Environment (`venv`):** Python projelerinin kütüphanelerini birbirinden izole eden sanal çalışma alanıdır. Bir projedeki paket sürümünün başka bir projeyi bozmasını engeller.
- **API Key:** Bir dış servise (örneğin OpenAI veya Anthropic) kimliğinizi doğrulayarak istek göndermenizi sağlayan gizli erişim anahtarıdır.
- **Thread-Safety:** Aynı kod parçasına birden fazla iş parçacığı (*Thread*) aynı anda eriştiğinde verinin bozulmaması ve sistemin tutarlı kalması özelliğidir.

### 3. Adım Adım Teknik Anlatım
Klasik bir LLM çağrısı ile bir *Agent* arasındaki yapısal farkı aşağıdaki akışta görebilirsiniz:

```text
[KLASİK PROMPT-AND-RESPONSE]
Kullanıcı ---> Prompt ---> LLM ---> Tek Cevap ---> Bitiş

[AGENTIC AI MİMARİSİ]
Kullanıcı ---> Hedef ---> [ Agent Loop ]
                            |-> 1. Planlama (Planning)
                            |-> 2. Bellekten Bağlam Okuma (Agent Memory & State)
                            |-> 3. Araç Çağırma (Tool Use / MCP / RAG)
                            |-> 4. Sonucu Gözlemleme (Observe)
                            |-> Hedef tamamlandı mı?
                                  |-- Hayır --> 1. adıma dön (max_steps sınırı içinde)
                                  |-- Evet  --> Kullanıcıya Nihai Yanıt
```

Buradaki en kritik nokta şudur: **Agent sihirli bir yapay zekâ türü değildir.** *Agent*, bir *LLM*'in etrafına iyi kurgulanmış bir yazılım döngüsü (*Agent Loop*), bellek (*State*) ve araç erişimi (*Tool Use*) eklenerek inşa edilen bir **Software Architecture** desenidir. Yani iyi bir *Agentic AI* mühendisi olmak, önce iyi bir yazılım mühendisi olmak demektir.

### 4. Hands-On Lab (Hemen Çalıştırılabilir Kurulum)
Bu kursun tüm laboratuvar dosyaları `agentic-ai-crash-course-2027/labs/` klasöründe bulunur ve **harici ücretli API anahtarı gerektirmeden** Python 3.10+ ile doğrudan çalışır.

PowerShell terminalini açın ve aşağıdaki adımları sırayla çalıştırın:

```powershell
# 1. Kurs klasörüne geçin (PowerShell: $env:USERPROFILE | CMD: %USERPROFILE%)
cd $env:USERPROFILE\agentic-ai-crash-course-2027

# 2. İzole bir Python Virtual Environment oluşturun
python -m venv .venv

# 3. Sanal ortamı aktif edin
.\.venv\Scripts\Activate.ps1

# 4. Python sürümünü doğrulayın (3.10 veya üzeri olmalı)
python --version

# 5. (Opsiyonel) Gerçek LLM API denemeleri için ortam dosyasını kopyalayın
Copy-Item .env.example .env
```

**Beklenen Çıktı:**
```text
Python 3.11.x (veya 3.10+ herhangi bir sürüm)
```

> **Güvenlik Kuralı:** `.env` dosyasına gerçek `OPENAI_API_KEY` eklerseniz bu dosyayı asla GitHub'a yüklemeyin. `.gitignore` dosyasına `.env` satırını mutlaka ekleyin.

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** Sanal ortam (`venv`) açmadan paketleri doğrudan sistem Python'ına kurmak. Bu durum zamanla sürüm çakışmalarına yol açar.
- **Sık Yapılan Hata 2:** *API Key* bilgisini doğrudan `.py` dosyasının içine sabit metin (*Hardcoded*) olarak yazmak. Anahtarınız sızarsa yüksek fatura riski doğar.
- **Mini Challenge:** `.env.example` dosyasını inceleyin ve kendi projenizde kullanmak üzere `APP_ENV=development` satırını ekleyin. Ardından Python ile `os.getenv("APP_ENV", "local")` çağrısını terminalde test edin.

---

## Modül 1: LLM Engineering Temelleri

### 1. Ne Öğreneceğiz & Neden Önemli?
Bir *Agent* inşa etmeden önce onun motorunu, yani *LLM*'i nasıl kontrol edeceğimizi bilmeliyiz. Pek çok Junior geliştirici *LLM*'i sadece sohbet kutusu gibi kullanır. Oysa yazılımda serbest metinle işlem yapmak çok zordur. Örneğin bir destek biletini otomatik yönlendirecekseniz modelin "Bence bu bir fatura sorunu gibi görünüyor" demesi işe yaramaz. Kodunuzun net, makine tarafından okunabilir bir JSON çıktısına ihtiyacı vardır.

Bunu bir restoran mutfağına benzetebilirsiniz. Müşteri siparişi ne kadar dağınık anlatırsa anlatsın, garson mutfağa **standart bir sipariş fişi** verir. *LLM Engineering* de dağınık insan dilini yazılımın güvenle işleyebileceği standart veri yapılarına dönüştürme disiplinidir.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **Tokenization:** Metnin *LLM* tarafından işlenebilmesi için kelime veya kelime parçalarına (*Token*) bölünmesi sürecidir. API maliyetleri ve hız sınırları kelimeye göre değil, *Token* sayısına göre hesaplanır.
- **Context Window:** Modelin tek bir istekte hafızasında tutabildiği maksimum *Token* kapasitesidir (girdi + çıktı toplamı). Bu sınır aşılırsa istek hata verir veya eski bilgiler kaybolur.
- **System Prompt:** Modele rolünü, kurallarını, sınırlarını ve çıktı biçimini öğreten en yüksek öncelikli yönergedir.
- **Temperature:** Modelin yanıt üretirken ne kadar rastgele veya yaratıcı olacağını belirleyen sayısal parametredir (`0.0` en tutarlı/deterministik, `1.0` daha yaratıcı).
- **Structured Outputs:** Modelin serbest metin yerine önceden tanımlanmış bir JSON şemasına (*Schema*) birebir uyan çıktı üretmesini sağlayan tekniktir.

### 3. Adım Adım Teknik Anlatım
Sağlam bir *LLM* çağrısı 4 aşamalı bir güvenlik hattından geçer:

```text
Kullanıcı Metni
   |
   v
[1. Token & Context Window Kontrolü] --> Limit aşımı varsa API'ye gitmeden durdur
   |
   v
[2. System Prompt + Temperature=0.0] --> Modele rolünü ve JSON kurallarını ver
   |
   v
[3. LLM Çağrısı] --> Ham JSON metni döner
   |
   v
[4. Schema Validation] --> Alanlar, veri tipleri ve izin verilen değerler doğrulanır
   |
   v
Güvenli Python Nesnesi (Immutable Dataclass)
```

Neden *Temperature* değerini `0.0` seçiyoruz? Çünkü sınıflandırma, JSON üretimi veya araç çağırma gibi mühendislik görevlerinde yaratıcılık değil, **tutarlılık (*Determinism*)** isteriz. Aynı destek bileti iki kez geldiğinde sistem her seferinde aynı kategoriyi üretmelidir.

### 4. Hands-On Lab (Hemen Çalıştırılabilir Uygulama)
Dosya: `labs/mod01_structured_llm.py`

Aşağıdaki komutu PowerShell'de çalıştırın:
```powershell
python labs/mod01_structured_llm.py
```

Kodun kritik bölümleri ve satır satır açıklaması:

```python
_WORD_PATTERN = re.compile(r"\w+|[^\w\s]", re.UNICODE)

@dataclass(frozen=True, slots=True)
class LLMRequestConfig:
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_context_tokens: int = 4096
    system_prompt: str = (
        "Sen bir destek bileti (Support Ticket) sınıflandırma uzmanısın. "
        "Yalnızca geçerli JSON döndür."
    )
```
- **`re.compile(...)`:** Regex desenini her fonksiyon çağrısında yeniden derlemek yerine uygulama başında bir kez derleriz. Bu yaklaşım *High Efficiency* sağlar.
- **`frozen=True`:** Yapılandırma nesnesini değiştirilemez (*Immutable*) yapar. Böylece birden fazla *Thread* bu ayarları aynı anda okuduğunda hiçbir *Race Condition* oluşmaz (*Thread-Safe*).
- **`slots=True`:** Python'ın her nesne için gereksiz sözlük (`__dict__`) oluşturmasını engeller ve bellek tüketimini düşürür.
- **`validate_ticket_schema(raw_json)`:** Modelden gelen JSON metnini doğrudan güvenip kullanmaz; `category`, `priority` ve `summary` alanlarını sıkı bir doğrulamadan geçirir.

**Beklenen Çıktı:**
```text
Ham JSON Çıktısı: {"category": "billing", "priority": "high", "summary": "Kullanıcı ödeme veya fatura sorunu bildiriyor."}
Doğrulanmış Nesne: TicketClassification(category='billing', priority='high', summary='Kullanıcı ödeme veya fatura sorunu bildiriyor.')
Tahmini Token Sayısı: 18
```

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** *LLM*'den gelen JSON yanıtını doğrulama (*Schema Validation*) yapmadan doğrudan veritabanına yazmak. Model bazen eksik alan veya beklenmeyen bir değer döndürebilir.
- **Sık Yapılan Hata 2:** Türkçe metinlerde `1 kelime = 1 token` varsaymak. Türkçe eklemeli bir dil olduğu için genellikle İngilizceye göre daha fazla *Token* tüketir.
- **Mini Challenge:** `labs/mod01_structured_llm.py` dosyasındaki `allowed_categories` kümesine `"refund"` (iade) kategorisini ekleyin ve "Ürünü iade etmek istiyorum" metni için çalışan yeni bir kural yazıp testi tekrar çalıştırın.

---

## Modül 2: Tool Use & Function Calling

### 1. Ne Öğreneceğiz & Neden Önemli?
Bir *LLM*, eğitim tarihinden sonraki bilgileri bilmez. Şirketinizin veritabanındaki güncel sipariş durumunu göremez. Ayrıca büyük sayılarla kesin matematik hesaplamaları yaparken hata yapabilir. İşte bu yüzden modele eller ve gözler vermemiz gerekir. Yazılımda bu ellere **Tool** (*Araç*) denir.

Bunu bir pilot ve kokpit göstergeleri gibi düşünebilirsiniz. Pilot kendi gözüyle uçağın yüksekliğini tahmin etmez. Altimetre aracına bakar, kesin veriyi alır ve kararını bu veriye göre verir. **Tool Use** sayesinde *LLM*, tahminde bulunmak yerine sizin yazdığınız güvenilir Python fonksiyonunu çağırır ve gerçek veriyi kullanarak cevap üretir.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **Tool:** Bir *Agent*'ın dış dünyayla etkileşime girmek veya kesin işlem yapmak için çağırabildiği yazılım fonksiyonudur (örneğin veritabanı sorgusu, hava durumu API'si, hesap makinesi).
- **Function Calling:** *LLM*'in serbest metin cevabı üretmek yerine, hangi fonksiyonu hangi parametrelerle çağırması gerektiğini yapılandırılmış bir formatta bildirmesidir.
- **Agent Loop (ReAct / Think-Act-Observe):** *Agent*'ın önce düşündüğü (*Think*), sonra bir araç çağırdığı (*Act*), aracın sonucunu incelediği (*Observe*) ve hedefe ulaşana kadar bu döngüyü tekrarladığı çalışma modelidir.
- **Max Steps (Step Limit):** Bir *Agent*'ın sonsuz döngüye girip API bütçenizi tüketmesini önlemek için konulan maksimum adım sınırıdır.
- **Tool Registry:** Tüm araçların isim, açıklama ve çalıştırılabilir fonksiyonlarıyla birlikte merkezi ve güvenli biçimde kaydedildiği yapıdır.

### 3. Adım Adım Teknik Anlatım
Bir *Tool* çağrısı gerçekleşirken **LLM kodu kendi içinde çalıştırmaz**. Bu çok önemli bir ayrıntıdır. Kodunuzu her zaman sizin uygulamanız çalıştırır:

```text
1. Kullanıcı: "ORD-101 siparişim nerede?"
2. Agent (Think): "Sipariş bilgisini bilmiyorum. get_order_status('ORD-101') aracını çağırmalıyım."
3. Uygulamanız (Act): ThreadSafeToolRegistry üzerinden Python fonksiyonunu çalıştırır.
4. Veritabanı Yanıtı (Observe): {"status": "Kargoda", "eta_days": 2}
5. Agent (Final Response): "Siparişiniz (ORD-101) şu an 'Kargoda' durumunda. Tahmini teslimat: 2 gün."
```

Ayrıca *Production* ortamında onlarca kullanıcı aynı anda istek atabilir. Bu yüzden `ToolRegistry` yapımız `threading.RLock()` ile korunur. Ancak dikkat edin: **Lock yalnızca aracı sözlükten okurken tutulur, aracın kendisi çalışırken serbest bırakılır.** Böylece yavaş bir API çağrısı diğer kullanıcıların isteklerini kilitlemez.

### 4. Hands-On Lab (Hemen Çalıştırılabilir Uygulama)
Dosya: `labs/mod02_tool_use_agent.py`

Çalıştırmak için:
```powershell
python labs/mod02_tool_use_agent.py
```

Kodun kritik mimari parçası:
```python
class ThreadSafeToolRegistry:
    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._tools: dict[str, ToolDefinition] = {}

    def execute(self, name: str, **kwargs: Any) -> dict[str, Any]:
        with self._lock:
            tool = self._tools.get(name)
        if tool is None:
            return {"ok": False, "error": f"Bilinmeyen tool: {name}"}
        try:
            result = tool.handler(**kwargs)
            return {"ok": True, "data": result}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
```
- **Hata İzolasyonu (`try / except`):** Bir araç hata verirse tüm *Agent* çökmez. Hata mesajı düzenli bir sözlük (`{"ok": False, "error": ...}`) olarak *Agent*'a geri döner. Böylece *Agent* kullanıcıya nazik ve anlaşılır bir açıklama yapabilir.
- **`max_steps=3`:** Döngü en fazla 3 adım ilerler. Beklenmeyen bir durumda sistem kendini güvenle durdurur.

**Beklenen Çıktı:**
```text
Siparişiniz (ORD-101) şu an 'Kargoda' durumunda. Tahmini teslimat: 2 gün.
Kargo hesaplaması tamamlandı: {'free_shipping': True, 'shipping_fee': 0.0}
```

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** *Agent Loop* içine `max_steps` sınırı koymamak. Hatalı bir *Tool* çağrısı sonsuz döngüye girerek dakikalar içinde yüksek API maliyeti oluşturabilir.
- **Sık Yapılan Hata 2:** Aracın açıklamasını (*description*) belirsiz yazmak. *LLM* hangi aracı seçeceğine tam olarak o açıklamayı okuyarak karar verir.
- **Mini Challenge:** `labs/mod02_tool_use_agent.py` içine `cancel_order(order_id: str)` adında yeni bir *Tool* ekleyin. Eğer sipariş durumu `"Teslim Edildi"` ise iptal işlemini reddeden güvenli bir kural yazın.

---

## Modül 3: Agent Memory & State Management

### 1. Ne Öğreneceğiz & Neden Önemli?
*LLM* API'leri doğası gereği **Stateless** (durumsuz) çalışır. Yani ikinci mesajınızı gönderdiğinizde model, beş saniye önce ne konuştuğunuzu hatırlamaz. Her yeni istek, model için tamamen yabancı bir başlangıçtır.

Bunu bir doktor muayenehanesine benzetelim. Doktor her randevuda hastanın tüm geçmişini aklında tutamaz. Bunun yerine iki şey kullanır: Masadaki güncel muayene notları (**Short-Term Memory**) ve hastanın kronik alerjilerinin yazılı olduğu hasta dosyası (**Long-Term Memory**). Bir *Agent*'ı tutarlı yapan şey, konuşma geçmişini ve çalışma durumunu (**State**) doğru yönetmesidir.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **Stateless:** Önceki isteklerin bilgisini otomatik olarak saklamayan sistem özelliğidir.
- **State Management:** Bir oturum veya çok adımlı iş akışı boyunca değişen verilerin (mesajlar, ara sonuçlar, adım sayısı) düzenli ve güvenli biçimde tutulmasıdır.
- **Short-Term Memory:** Aktif konuşma penceresindeki son mesajları tutan kısa süreli bellektir.
- **Long-Term Memory:** Oturumlar kapansa bile saklanan, kullanıcı tercihleri veya geçmiş kararlar gibi kalıcı bellek katmanıdır.
- **Bounded Memory (Sınırlı Bellek):** Bellek kullanımının ve *Context Window* maliyetinin sonsuza kadar büyümesini önlemek için yalnızca son `N` mesajı saklayan yapıdır.
- **Session Isolation:** A kullanıcısının konuşma verilerinin B kullanıcısının oturumuna kesinlikle karışmamasını sağlayan veri ayrımıdır.

### 3. Adım Adım Teknik Anlatım
Bellek yönetiminde en kritik mühendislik kararı şudur: **Tüm konuşma geçmişini sınırsız bir listede tutarsanız hem RAM şişer hem de *Context Window* patlar.** Bunun yerine sabit boyutlu bir kuyruk (*Bounded Queue* — Python'da `collections.deque(maxlen=N)`) kullanırız.

```text
Yeni Mesaj Gelir (Session: user-junior-01)
   |
   v
[ThreadSafeMemoryManager (RLock)]
   |--> Short-Term Memory: deque(maxlen=4) -> En eski mesaj otomatik düşer!
   |--> Long-Term Memory:  {"preferred_language": "Python", "experience_level": "Junior"}
   |
   v
[Snapshot Oluştur] --> Dışarıya orijinal referans değil, güvenli kopya verilir.
```

Neden dışarıya doğrudan iç listeyi değil de **Snapshot** (kopya) döndürüyoruz? Çünkü başka bir fonksiyon o listeyi değiştirirse (*Mutation*), bellek yöneticisinin iç durumu bozulur. Kopya döndürmek *Thread-Safety* açısından altın standarttır.

### 4. Hands-On Lab (Hemen Çalıştırılabilir Uygulama)
Dosya: `labs/mod03_memory_and_state.py`

Çalıştırmak için:
```powershell
python labs/mod03_memory_and_state.py
```

Kodun kritik noktaları:
- `deque(maxlen=4)` yapısı sayesinde 6 mesaj eklense bile bellekte her zaman **en güncel 4 mesaj** kalır. Eski mesajlar O(1) karmaşıklığında otomatik silinir (*High Efficiency*).
- `long_term_facts` sözlüğü, kısa süreli mesajlar düşse bile kullanıcının `"preferred_language": "Python"` bilgisini kalıcı olarak korur.
- `self._sessions` sözlüğü her kullanıcıyı kendi `session_id` anahtarı altında izole eder.

**Beklenen Çıktı:**
```text
Long-Term Facts: {'preferred_language': 'Python', 'experience_level': 'Junior'}
Short-Term Mesaj Sayısı (maxlen=4): 4
  - [user] Soru 3: Agent Memory nasıl çalışır?
  - [user] Soru 4: Agent Memory nasıl çalışır?
  - [user] Soru 5: Agent Memory nasıl çalışır?
  - [user] Soru 6: Agent Memory nasıl çalışır?
```

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** Tüm kullanıcıların mesajlarını tek bir global Python listesinde (`messages = []`) tutmak. İki kullanıcı aynı anda sisteme girdiğinde cevaplar birbirine karışır ve veri sızıntısı yaşanır.
- **Sık Yapılan Hata 2:** Konuşma uzadıkça tüm geçmişi her seferinde *LLM*'e göndermek. Bu hem maliyeti katlar hem de modelin dikkatinin dağılmasına (*Context Rot*) yol açar.
- **Mini Challenge:** `ThreadSafeMemoryManager` sınıfına `clear_short_term(session_id: str)` adında bir metot ekleyin. Bu metot kısa süreli mesajları temizlesin ama `long_term_facts` bilgisine dokunmasın.

---

## Modül 4: RAG, Vector Databases & Agentic RAG

### 1. Ne Öğreneceğiz & Neden Önemli?
Şirketinizin 500 sayfalık iç dokümantasyonu, ürün kılavuzları ve güncel iade politikaları var. Bu 500 sayfanın tamamını her soruda *LLM*'in *Context Window*'ına yapıştıramazsınız. Hem sığmaz hem de çok pahalı olur. Peki *Agent* bu özel şirket bilgilerine nasıl ulaşacak? Cevap: **RAG** (*Retrieval-Augmented Generation*).

Bunu açık kitap sınavına benzetebilirsiniz. Öğrencinin 500 sayfalık kitabı ezberlemesine gerek yoktur. Soru geldiğinde kitabın içindekiler kısmından ilgili 2 paragrafı bulur (*Retrieval*), o 2 paragrafı okuyarak cevabı yazar (*Generation*). **Agentic RAG** ise bir adım daha ileri gider: Eğer öğrenci ilk aramada doğru sayfayı bulamazsa pes etmez; soruyu farklı kelimelerle yeniden arar (**Query Rewrite**) ve doğru paragrafı bulana kadar aramayı iyileştirir.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **RAG (Retrieval-Augmented Generation):** *LLM*'in yanıt üretmeden önce harici bir bilgi tabanından ilgili metin parçalarını çekip *Prompt*'a eklemesi mimarisidir.
- **Chunking:** Uzun dokümanların, arama motorunun verimli bulabileceği daha küçük ve anlamlı metin parçalarına (*Chunk*) bölünmesidir.
- **Embeddings:** Metinlerin anlamsal içeriğini sayısal vektörlere (sayı dizilerine) dönüştüren matematiksel temsillerdir. Anlamca yakın cümlelerin vektörleri birbirine yakındır.
- **Vector Database:** *Embedding* vektörlerini saklayan ve gelen sorguya en yakın vektörleri milisaniyeler içinde bulan özel veritabanıdır (örneğin Qdrant, Pinecone, pgvector).
- **Cosine Similarity:** İki vektör arasındaki açıyı ölçerek anlamsal benzerliği `0.0` ile `1.0` arasında puanlayan matematiksel yöntemdir.
- **Agentic RAG:** Klasik tek seferlik aramanın ötesine geçip, dönen sonuçların yeterli olup olmadığını kontrol eden, yetersizse sorguyu yeniden yazarak (*Query Rewrite*) aramayı tekrarlayan akıllı RAG mimarisidir.

### 3. Adım Adım Teknik Anlatım
Klasik *RAG* ile *Agentic RAG* arasındaki farkı akış şemasında inceleyelim:

```text
[KLASİK RAG]
Soru --> Vektöre Çevir --> Vector DB'de Ara --> İlk Sonucu Al --> LLM Cevabı (Sonuç alakasız olsa bile!)

[AGENTIC RAG]
Soru --> Vector DB'de Ara --> Benzerlik Skoru >= Eşik (min_score) mi?
                                 |-- EVET --> Güvenilir Bağlamla LLM Cevabı
                                 |-- HAYIR --> Sorguyu İyileştir (Query Rewrite)
                                                 |--> Tekrar Ara --> Doğru Bağlamı Bul --> LLM Cevabı
```

Bu kontrol katmanı sayesinde kullanıcı teknik terim bilmeden ("beğenmezsem geri verebilir miyim?") sorduğunda bile sistem bunu şirket politikası diline ("iade politikası süre gün kargo") genişleterek doğru maddeyi yakalar.

### 4. Hands-On Lab (Hemen Çalıştırılabilir Uygulama)
Dosya: `labs/mod04_agentic_rag.py`

Çalıştırmak için:
```powershell
python labs/mod04_agentic_rag.py
```

Kodun işleyişi:
- `add_document(...)`: Metni `chunk_size=120` karakterlik parçalara böler (*Chunking*), her parçayı normalize edilmiş vektöre çevirir ve *Thread-Safe* bir kilit altında saklar.
- `cosine_similarity(vec_a, vec_b)`: Daha kısa olan vektör üzerinde döngü kurarak gereksiz çarpma işlemlerinden kaçınır (*High Efficiency*).
- `agentic_rag_search(...)`: İlk aramada skor `0.25` eşiğinin altında kalırsa otomatik olarak **Query Rewrite** adımını tetikler ve ikinci aramayı yapar.

**Beklenen Çıktı:**
```text
Sorgu 1 (Net): [İlk Aramada Bulundu | Skor: 0.49] -> Müşteriler teslimattan itibaren 14 gün içinde ücretsiz kargo ile iade politikası kapsamında ürün iade edebilir.
Sorgu 2 (Belirsiz): [Agentic Query Rewrite Uygulandı | Yeni Skor: 0.40] -> Müşteriler teslimattan itibaren 14 gün içinde ücretsiz kargo ile iade politikası kapsamında ürün iade edebilir.
```

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** *Chunk* boyutunu çok küçük (10 kelime) veya çok büyük (5 sayfa) seçmek. Çok küçük *Chunk* bağlamı koparır; çok büyük *Chunk* ise alakasız gürültü taşır.
- **Sık Yapılan Hata 2:** Arama sonucunun benzerlik skorunu (*Similarity Score*) hiç kontrol etmeden *LLM*'e vermek. Alakasız bir parça verilirse *LLM* halüsinasyon (*Hallucination*) üretebilir.
- **Mini Challenge:** `labs/mod04_agentic_rag.py` içindeki `ThreadSafeVectorStore`'a yeni bir `"kargo"` dokümanı ekleyin ("500 TL üzeri siparişlerde kargo ücretsizdir.") ve belirsiz bir soruyla (*"teslimat parası öder miyim?"*) *Agentic RAG* davranışını test edin.

---

## Modül 5: Model Context Protocol (MCP)

### 1. Ne Öğreneceğiz & Neden Önemli?
Modül 2'de kendi *Tool* fonksiyonumuzu yazdık. Şimdi gerçek bir şirketi düşünelim: Şirkette GitHub, Slack, PostgreSQL, Jira ve Google Drive var. Ayrıca 3 farklı AI uygulamanız var (örneğin bir geliştirici asistanı, bir müşteri destek *Agent*'ı ve bir raporlama botu). Eskiden her AI uygulaması için her araca özel bağlantı kodu yazmak gerekiyordu. 3 uygulama x 5 araç = 15 ayrı entegrasyon bakımı!

Bunu eski telefon şarj kablolarına benzetebilirsiniz. Eskiden her telefon markasının kendi prizi vardı. Sonra **USB-C** standardı geldi; artık tek bir kabloyu her cihaza takabiliyorsunuz. **Model Context Protocol (MCP)**, *Agentic AI* dünyasının USB-C standardıdır. Bir aracı *MCP Server* olarak bir kez yazarsınız; *MCP* destekleyen her *Agent* onu anında keşfedip kullanabilir.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **Model Context Protocol (MCP):** AI uygulamalarının (*MCP Client / Host*) harici veri kaynaklarına ve araçlara (*MCP Server*) tek bir standart protokol üzerinden bağlanmasını sağlayan açık standarttır.
- **MCP Server:** Araçları (*Tools*), veri kaynaklarını (*Resources*) ve şablonları (*Prompts*) dış dünyaya standart *JSON-RPC 2.0* formatında sunan servis katmanıdır.
- **MCP Client:** *Agent* tarafında yaşayan, *MCP Server*'a bağlanıp hangi araçların mevcut olduğunu keşfeden (`tools/list`) ve onları çağıran (`tools/call`) istemci bileşenidir.
- **JSON-RPC 2.0:** Uzaktaki bir fonksiyonu JSON mesajlarıyla çağırmak için kullanılan hafif, standart iletişim protokolüdür.
- **Tool Discovery (Araç Keşfi):** *Agent*'ın sabit kodlanmış (*Hardcoded*) araç listesi yerine, çalışma zamanında *MCP Server*'a sorarak mevcut araçları ve şemalarını otomatik öğrenmesidir.

### 3. Adım Adım Teknik Anlatım
*MCP* mimarisinde *Agent* ile dış servis arasında temiz bir sınır bulunur:

```text
[AI Uygulaması / MCP Client]
       |
       |--- 1. Keşif (JSON-RPC): {"method": "tools/list"}
       |<-- 2. Yanıt: [{"name": "check_inventory", "inputSchema": {...}}]
       |
       |--- 3. Çalıştırma (JSON-RPC): {"method": "tools/call", "params": {"name": "check_inventory", "arguments": {"sku": "SKU-LAPTOP-01"}}}
       |<-- 4. Yanıt: {"sku": "SKU-LAPTOP-01", "in_stock": 12}
       |
[Warehouse MCP Server] ---> Gerçek Depo Veritabanı
```

Bu ayrımın en büyük avantajı **Loose Coupling** (gevşek bağlılık) sağlamasıdır. Depo veritabanınız değişse bile *Agent* kodunuzu değiştirmezsiniz; yalnızca *MCP Server* içindeki tek bir fonksiyonu güncellersiniz.

### 4. Hands-On Lab (Hemen Çalıştırılabilir Uygulama)
Dosya: `labs/mod05_mcp_client_server.py`

Çalıştırmak için:
```powershell
python labs/mod05_mcp_client_server.py
```

Kodun kritik noktaları:
- `SimpleMCPServer`, gerçek *MCP* standardının kalbindeki `tools/list` (keşif) ve `tools/call` (çağrı) *JSON-RPC 2.0* metodlarını uygular.
- `MCPToolSpec` içinde `input_schema` (JSON Schema) yer alır. Böylece herhangi bir *LLM*, aracın hangi parametreleri beklediğini tahmin etmeden kesin olarak bilir.
- `self._lock` ile araç kayıt defteri *Thread-Safe* tutulur.

**Beklenen Çıktı:**
```text
MCP tools/list Yanıtı: {"jsonrpc": "2.0", "id": 1, "result": {"tools": [{"name": "check_inventory", "description": "Depo stok durumunu SKU koduna göre sorgular.", "inputSchema": {"type": "object", "properties": {"sku": {"type": "string"}}, "required": ["sku"]}}]}}
MCP tools/call Yanıtı: {"jsonrpc": "2.0", "id": 2, "result": {"sku": "SKU-LAPTOP-01", "in_stock": 12}}
```

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** Tek bir *MCP Server* içine 50 farklı alakasız araç doldurmak. Çok fazla araç açıklaması *LLM*'in *Context Window*'ını şişirir ve yanlış araç seçme oranını artırır.
- **Sık Yapılan Hata 2:** *MCP Server* üzerinden tehlikeli işlemlere (örneğin `DELETE FROM users`) yetkilendirme (*Authorization*) koymadan erişim vermek.
- **Mini Challenge:** `labs/mod05_mcp_client_server.py` içindeki `SimpleMCPServer`'a `reserve_inventory` adında ikinci bir *MCP Tool* ekleyin ve `tools/list` çıktısında iki aracın da göründüğünü doğrulayın.

---

## Modül 6: Planning & Multi-Agent Orchestration (Mimari Trade-off'lar)

### 1. Ne Öğreneceğiz & Neden Önemli?
Tek bir *Agent*'a hem araştırma yap, hem makale yaz, hem dil bilgisi denetle hem de veritabanına kaydet dediğinizde sonuç genellikle bozulur. Çünkü tek bir *Prompt* içinde çok fazla sorumluluk birleşince model odak kaybeder.

Bunu bir yazılım ekibine benzetebilirsiniz. Tek bir kişi aynı anda hem ürün yöneticisi, hem yazılımcı hem de kalite kontrol (QA) uzmanı olursa hata kaçırması kolaylaşır. Bunun yerine **Planner** (planlayıcı), **Writer** (üretici) ve **Reviewer** (denetleyici) rollerini ayırırsınız. Eğer *Reviewer* bir eksik bulursa iş *Writer*'a geri döner. İşte bu iş birliğini yöneten yapıya **Multi-Agent Orchestration** denir.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **Planning:** Büyük ve karmaşık bir hedefin, yürütülebilir küçük alt adımlara bölünmesi sürecidir.
- **Multi-Agent Orchestration:** Farklı uzmanlık rollerine sahip birden fazla *Agent*'ın hangi sırayla ve hangi kurallarla birlikte çalışacağını yöneten koordinasyon katmanıdır.
- **Stateful Workflow (Graph):** Adımların düğüm (*Node*), geçişlerin kenar (*Edge*) olarak modellendiği ve ortak bir durum (*State*) nesnesinin düğümler arasında aktarıldığı akış mimarisidir.
- **Conditional Edge (Koşullu Geçiş):** Bir düğümün çıktısına bakarak sıradaki adımın dinamik olarak seçilmesidir (örneğin "Onaylandıysa bitir, reddedildiyse tekrar yaz").
- **Trade-off (Mimari Ödünleşim):** Bir teknik kararın getirdiği avantajlar karşılığında vazgeçilen diğer özelliklerdir. Yazılımda "her iş için en iyi tek araç" yoktur; projeye en uygun *Trade-off* vardır.

### 3. Adım Adım Teknik Anlatım
2027 ekosisteminde öne çıkan başlıca *Orchestration* araçlarının Junior seviyesinde net karar matrisi şöyledir:

| Framework / Araç | Temel Yaklaşım | En Güçlü Olduğu Senaryo | Trade-off (Dikkat Edilecek Nokta) |
| :--- | :--- | :--- | :--- |
| **LangGraph** | Graf tabanlı *Stateful Workflow* (*Node* & *Edge*) | Karmaşık döngüler, koşullu dallanma, *Production* kontrolü | Başlangıçta graf kavramını öğrenmek biraz daha disiplin ister. |
| **CrewAI** | Rol tabanlı ekip simülasyonu (*Role / Goal / Backstory*) | Hızlı prototip, içerik üretimi ve araştırma ekipleri | Çok ince *State* kontrolü gereken kurumsal akışlarda esnekliği azalabilir. |
| **OpenAI Agents SDK** | Hafif, minimalist *Handoff* ve *Tool* döngüsü | Hızlı, sade ve düşük soyutlamalı *Agent* sistemleri | Çok karmaşık graf dallanmalarını elle yönetmeniz gerekebilir. |
| **AutoGen** | Ajanlar arası sohbet (*Conversational Multi-Agent*) | Kod yazma-test etme gibi tartışmalı görevler | Sohbet döngüsü iyi sınırlanmazsa yüksek *Token* tüketebilir. |
| **n8n** | Görsel *Low-Code Workflow Automation* | CRM, e-posta, Slack gibi iş süreçlerini hızlıca bağlama | Ağır yazılım mühendisliği ve özel *Concurrency* mantığı için kod tabanlı çözümler daha uygundur. |

Aşağıda `LangGraph` mantığının saf Python ile nasıl çalıştığını gösteren akış yer alıyor:

```text
[START] -> (planner_node) -> (writer_node) -> (reviewer_node)
                                  ^                  |
                                  |   [Reddedildi]   |
                                  +------------------+
                                                     | [Onaylandı veya max_revisions]
                                                     v
                                                   [END]
```

### 4. Hands-On Lab (Hemen Çalıştırılabilir Uygulama)
Dosya: `labs/mod06_stateful_workflow.py`

Çalıştırmak için:
```powershell
python labs/mod06_stateful_workflow.py
```

Kodun kritik tasarım kararları:
- `WorkflowState` sınıfı `@dataclass(frozen=True, slots=True)` ile **Immutable** tanımlanmıştır. Hiçbir düğüm (*Node*) gelen *State*'i yerinde değiştirmez; `dataclasses.replace(...)` ile yeni bir *State* üretir. Bu sayede yan etkiler (*Side Effects*) ortadan kalkar ve sistem %100 *Thread-Safe* olur.
- `reviewer_node`, ilk taslağı kısa bulduğu için reddeder ve graf motoru akışı otomatik olarak `writer_node`'a geri çevirir.
- `max_revisions=3` sınırı sayesinde *Reviewer* ile *Writer* arasında sonsuz tartışma döngüsü oluşması engellenir.

**Beklenen Çıktı:**
```text
[GRAPH] Çalıştırılan Node: planner
[GRAPH] Çalıştırılan Node: writer
[GRAPH] Çalıştırılan Node: reviewer
[GRAPH] Reviewer reddetti -> Writer düğümüne geri dönülüyor.
[GRAPH] Çalıştırılan Node: writer
[GRAPH] Çalıştırılan Node: reviewer

--- SONUÇ ---
Onay Durumu: True
Revizyon Sayısı: 2
Nihai Taslak: Agentic AI State Management kapsamlı özet -> Agentic AI State Management nedir? | Neden Production ortamında kritik önem taşır? | Basit bir uygulama örneği. Örnek: State izole edilmelidir.
```

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** Tek bir *LLM* çağrısıyla çözülebilecek basit bir işe gereksiz yere 4 ajanlık *Multi-Agent* mimarisi kurmak. Her ekstra ajan hem gecikmeyi (*Latency*) hem de maliyeti artırır.
- **Sık Yapılan Hata 2:** Düğümler arasında paylaşılan *State* nesnesini rastgele değiştirmek (*Mutate*), hata ayıklamayı (*Debugging*) imkânsız hâle getirir.
- **Mini Challenge:** `labs/mod06_stateful_workflow.py` içindeki `reviewer_node` fonksiyonuna yeni bir kalite kuralı ekleyin: Taslak içinde mutlaka `"Production"` kelimesi geçsin; geçmiyorsa taslağı reddedip `writer_node`'un düzeltmesini sağlayın.

---

## Modül 7: Production-Ready Engineering & 3 Kritik Tuzak

### 1. Ne Öğreneceğiz & Neden Önemli?
Kendi bilgisayarınızda çalışan bir *Agent* prototipi yapmak kolaydır. Zor olan, bu sistemi 1.000 gerçek kullanıcı aynı anda kullanırken ayakta tutmaktır (*Production*). Canlı ortamda *LLM* API'si aniden `429 Rate Limit` hatası verebilir, yanıt süresi 15 saniyeye çıkabilir veya model beklenmedik bir cevap üretebilir.

Bunu bir uçağın kara kutusuna ve yedek motoruna benzetebilirsiniz. **Observability** (kara kutu) olmadan bir hata yaşandığında nedenini asla bulamazsınız. **Retry & Fallback** (yedek motor) olmadan en ufak ağ kesintisinde uygulamanız çöker. **Evaluation** (test uçuşu) olmadan yaptığınız yeni bir *Prompt* değişikliğinin eski özellikleri bozup bozmadığını bilemezsiniz.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **Observability & Tracing (LangSmith Mantığı):** Bir *Agent*'ın her adımında ne düşündüğünü, hangi aracı çağırdığını, kaç milisaniye sürdüğünü ve ne kadar *Token* harcadığını adım adım kayıt altına alma disiplinidir.
- **Evaluation (Evals):** *Agent* yanıtlarının doğruluğunu, güvenliğini ve format uyumluluğunu otomatik test setleriyle ölçme sürecidir.
- **Retry & Exponential Backoff:** Geçici bir ağ veya API hatası alındığında isteği artan bekleme süreleriyle (örneğin 50ms, 100ms, 200ms) kontrollü biçimde yeniden deneme yöntemidir.
- **Fallback:** Birincil model veya servis tamamen başarısız olduğunda, sistemin çökmesi yerine yedek bir modele veya güvenli varsayılan cevaba geçmesidir.
- **LoRA / QLoRA (Fine-Tuning):** Dev bir *LLM*'in tüm ağırlıklarını baştan eğitmek yerine, yalnızca küçük bir adaptör katmanını düşük bellek maliyetiyle eğiten ince ayar tekniğidir.
- **Deployment:** Geliştirilen *Agent* uygulamasının *Docker*, bulut sunucusu veya API servisi (*FastAPI*) üzerinden canlıya alınması sürecidir.

### 3. Adım Adım Teknik Anlatım

#### A) Ne Zaman Prompt/RAG, Ne Zaman LoRA/QLoRA?
Junior geliştiricilerin en çok karıştırdığı sorulardan biri şudur: *"Kendi modelimi LoRA/QLoRA ile eğitmeli miyim?"*
- **Önce Prompt Engineering + RAG + Tool Use kullanın:** Güncel şirket bilgisi, doküman arama ve dış servis çağrıları için *Fine-Tuning* yapılmaz; çünkü bilgi her gün değişir.
- **LoRA/QLoRA ne zaman gerekir?** Modelin çok özel bir alan dilini (örneğin tıbbi rapor formatı), çok spesifik bir üslubu öğrenmesi gerekiyorsa veya çok yüksek trafikte daha küçük ve ucuz bir açık kaynak modeli (*Open-Weight Model*) hızlandırmak istiyorsanız tercih edilir.

#### B) Kaynak Dosyadaki 3 Kritik Tuzak ve Kaçınma Stratejileri
1. **Tuzak 1 — Temelleri Atlayıp Yalnızca Framework Ezberlemek:** *Python*, *HTTP API*, *Data Handling*, *Evaluation* ve *Software Architecture* bilmeden yalnızca *LangChain* veya *CrewAI* ezberlemek tehlikelidir. *Framework*'ler 6 ayda bir değişir; ancak *State Management*, *Thread-Safety* ve *Observability* prensipleri kalıcıdır.
2. **Tuzak 2 — Her Aracı Aynı Anda Öğrenmeye Çalışmak:** Aynı hafta *LangGraph*, *CrewAI*, *AutoGen*, *n8n* ve *QLoRA* öğrenmeye çalışmak zihinsel dağınıklık yaratır. Önce çekirdek mantığı (bu kurstaki Modül 1–5) kavrayın, ardından projenizin *Trade-off*'larına uyan **tek bir** *Orchestration* aracında derinleşin.
3. **Tuzak 3 — Kurs Biriktirmek (Tutorial Hell):** Pasif video izlemek sizi *AI Engineer* yapmaz. Öğrenme, klavyeye dokunup kendi *Agent*'ınızı kırıp onardığınızda başlar. Her modülün sonunda mutlaka kodu değiştirip yeni bir özellik ekleyin.

### 4. Hands-On Lab (Hemen Çalıştırılabilir Uygulama)
Dosya: `labs/mod07_production_guardrails.py`

Çalıştırmak için:
```powershell
python labs/mod07_production_guardrails.py
```

Kodun işleyişi:
- `unstable_primary()` fonksiyonu bilerek `429 Rate Limit Exceeded` hatası fırlatır.
- `call_with_retry_and_fallback(...)` önce kısa *Exponential Backoff* ile `max_retries=2` kez yeniden dener; hâlâ başarısızsa sistemi çökertmeden `reliable_fallback()` fonksiyonuna geçer.
- `ThreadSafeTracer`, her denemenin süresini (`duration_ms`) ve durumunu (`OK` / `ERROR`) kaydeder.
- `evaluate_response(...)`, dönen cevabın zorunlu anahtar kelimeleri (`"14 gün"`, `"ücretsiz"`) içerip içermediğini otomatik test eder.

**Beklenen Çıktı:**
```text
Nihai Cevap: İade süresi 14 gündür ve kargo ücretsizdir.
Evaluation Raporu: {'passed': True, 'missing_keywords': []}

--- OBSERVABILITY TRACE ---
  [ERROR] primary_llm (0.00 ms) -> attempt=1: 429 Rate Limit Exceeded
  [ERROR] primary_llm (0.01 ms) -> attempt=2: 429 Rate Limit Exceeded
  [ERROR] primary_llm (0.01 ms) -> attempt=3: 429 Rate Limit Exceeded
  [OK] fallback_llm (0.00 ms) -> fallback_triggered
```

### 5. Common Pitfalls & Mini Challenge
- **Sık Yapılan Hata 1:** *Production* ortamında `print()` ile log tutmaya çalışmak. Paralel isteklerde `print()` çıktıları birbirine karışır; bunun yerine yapılandırılmış *Trace* ve `Span` kayıtları (*LangSmith*, *OpenTelemetry*) kullanılmalıdır.
- **Sık Yapılan Hata 2:** Her hatada sınırsız *Retry* yapmak. `401 Invalid API Key` gibi kalıcı bir hatada *Retry* yapmak sadece zaman kaybettirir.
- **Mini Challenge:** `labs/mod07_production_guardrails.py` içindeki `unstable_primary` fonksiyonunu 2. denemede başarılı olacak şekilde güncelleyin ve *Fallback*'in tetiklenmediğini *Observability Trace* çıktısından doğrulayın.

---

## Modül 8: Hemen Uygulanabilir Capstone Mini-Project & 14 Günlük Pratik Planı

### 1. Ne Öğreneceğiz & Neden Önemli?
Şimdiye kadar tüm parçaları tek tek inşa ettik: *Structured Outputs*, *Tool Use*, *Memory & State*, *Agentic RAG*, *MCP*, *Stateful Workflow* ve *Observability*. Gerçek mühendislik becerisi, bu parçaları tek bir çalışan sistemde bir araya getirdiğinizde ortaya çıkar.

Bu bitirme projesinde (**Capstone Mini-Project**), aynı anda birden fazla müşteriye hizmet veren, sipariş sorgulayan (*Tool Use*), şirket politikalarını yanıtlayan (*RAG*), oturum bazlı bellek tutan (*Memory & State*), her adımın gecikmesini ölçen (*Observability*) ve **ThreadPoolExecutor** ile eşzamanlı (*Concurrent*) yük altında bile veri bozmayan (%100 *Thread-Safe*) bir **Production Support Agent** çalıştıracaksınız.

### 2. Key Terminology (Kritik Kavramlar ve Tanımlar)
- **Concurrency (Eşzamanlılık):** Birden fazla kullanıcı isteğinin aynı zaman aralığında paralel olarak işlenebilmesidir.
- **Race Condition:** İki veya daha fazla *Thread*'in aynı paylaşılan veriyi senkronizasyon olmadan değiştirmeye çalışması sonucu oluşan öngörülemez hatadır.
- **Routing (Yönlendirme):** Gelen kullanıcı isteğinin niyetine göre doğru işleme (*Tool Use*, *RAG* veya *Fallback*) yönlendirilmesi mekanizmasıdır.
- **Latency:** Bir isteğin sisteme girmesi ile yanıtın dönmesi arasında geçen toplam süredir (milisaniye cinsinden).

### 3. Adım Adım Teknik Anlatım
Bitirme projesinin uçtan uca mimarisi:

```text
4 Eşzamanlı Müşteri İsteği (ThreadPoolExecutor - 4 Worker Thread)
             |
             v
   [ProductionSupportAgent] (RLock ile Session & Trace Koruması)
             |
             +--> Session State Güncelle (Bounded deque maxlen=5)
             |
             +--> Akıllı Yönlendirme (Routing)
             |      |-- "ORD-" geçiyorsa --> Tool Use (Order Lookup)
             |      |-- "iade/garanti"   --> RAG Bilgi Bankası
             |      |-- Diğer            --> Güvenli Fallback
             |
             +--> TraceSpan Kaydet (session_id, step, latency_ms, outcome)
             |
             v
     İzole & Tutarlı Müşteri Yanıtı
```

### 4. Hands-On Lab (Hemen Çalıştırılabilir Capstone Uygulaması)
Dosya: `labs/mod08_capstone_agent.py`

Çalıştırmak için:
```powershell
python labs/mod08_capstone_agent.py
```

**Beklenen Çıktı:**
```text
[sess-1] Soru: ORD-500 siparişim ne durumda?
[sess-1] Yanıt: [Tool:OrderLookup] ORD-500 durumu -> Hazırlanıyor (Tahmini kargo: Yarın)

[sess-2] Soru: Ürünü beğenmezsem iade süresi kaç gün?
[sess-2] Yanıt: [RAG:Policy] Teslimattan itibaren 14 gün içinde ücretsiz iade hakkınız vardır.

[sess-3] Soru: Kulaklıkların garanti süresi ne kadar?
[sess-3] Yanıt: [RAG:Policy] Tüm elektronik ürünlerde 24 ay resmi distribütör garantisi bulunur.

[sess-1] Soru: Teşekkürler, peki ORD-501 nerede?
[sess-1] Yanıt: [Tool:OrderLookup] ORD-501 durumu -> Kargoda (Takip No: TR998877)

--- CAPSTONE OBSERVABILITY TRACES ---
  sess-1 | tool_order_lookup | 0.026 ms | SUCCESS
  sess-2 | rag_policy_search | 0.009 ms | SUCCESS
  sess-3 | rag_policy_search | 0.008 ms | SUCCESS
  sess-1 | tool_order_lookup | 0.009 ms | SUCCESS
```

### 5. Common Pitfalls, Mini Challenge & 14 Günlük Pratik Planı
- **Sık Yapılan Hata:** Tek kullanıcılı testte çalışan bir *Agent*'ı paralel yük testi (`ThreadPoolExecutor`) yapmadan canlıya almak.
- **Capstone Mini Challenge:** `labs/mod08_capstone_agent.py` içine Modül 5'teki *MCP* sunucusundan stok sorgulayan yeni bir rota (`"stok"` kelimesi geçtiğinde) ve Modül 7'deki `evaluate_response` doğrulama adımını ekleyin.

#### Hemen Başlayabileceğiniz 14 Günlük Uygulama Takvimi
- **Gün 1–2:** Modül 0 & Modül 1'i çalıştırın. Kendi JSON şemanızı (örneğin iş ilanı özetleyici) tasarlayın.
- **Gün 3–4:** Modül 2'yi çalıştırın. Kendi 2 yeni *Tool* fonksiyonunuzu (örneğin döviz çevirici, tarih hesaplayıcı) yazın.
- **Gün 5–6:** Modül 3'ü çalıştırın. `ThreadSafeMemoryManager`'ı JSON dosyasına kaydedip geri yükleyecek (*Persistence*) şekilde geliştirin.
- **Gün 7–8:** Modül 4'ü çalıştırın. Kendi PDF veya `.txt` notlarınızı `chunk_size` değerleriyle oynayarak test edin.
- **Gün 9–10:** Modül 5'i çalıştırın. İki farklı aracı tek bir *MCP Server* üzerinden dışarı açın.
- **Gün 11–12:** Modül 6'yı çalıştırın. `LangGraph` veya saf Python graf motoruyla 3 düğümlü kendi onay akışınızı kurun.
- **Gün 13–14:** Modül 7 & 8'i birleştirin. Gerçek bir *LLM API* (veya yerel *Ollama*) bağlayıp *Observability* + *Evaluation* testleriyle GitHub portföyünüze yükleyin.

---

## Master Glossary (Terimler Sözlüğü)

- **Agent Loop:** *Agent*'ın hedefe ulaşana kadar *Think → Act → Observe* adımlarını tekrarladığı kontrollü yürütme döngüsüdür.
- **Agent Memory:** *Agent*'ın konuşma geçmişini (*Short-Term*) ve kalıcı bilgileri (*Long-Term*) saklama mekanizmasıdır.
- **Agentic AI:** Planlama, araç kullanımı, bellek yönetimi ve öz-değerlendirme yapabilen hedef odaklı yapay zekâ sistem mimarisidir.
- **Agentic RAG:** Arama sonuçlarının kalitesini değerlendirip gerekirse sorguyu yeniden yazarak (*Query Rewrite*) tekrar arama yapan gelişmiş *RAG* mimarisidir.
- **Chunking:** Büyük metin dokümanlarını vektör aramasına uygun küçük parçalara bölme işlemidir.
- **Concurrency:** Birden fazla görevin aynı zaman aralığında paralel olarak yürütülmesidir.
- **Context Window:** Bir *LLM*'in tek bir istekte işleyebileceği maksimum *Token* kapasitesidir.
- **Cosine Similarity:** İki vektör arasındaki anlamsal yakınlığı ölçen `0.0–1.0` arası benzerlik metriğidir.
- **Deployment:** Geliştirilen uygulamanın gerçek kullanıcıların erişebileceği canlı sunucuya taşınmasıdır.
- **Embeddings:** Metinleri anlamsal olarak karşılaştırılabilir sayısal vektörlere dönüştüren temsillerdir.
- **Evaluation (Evals):** *Agent* çıktılarının doğruluk, format ve güvenlik kriterlerine göre otomatik test edilmesidir.
- **Fallback:** Birincil servis veya model başarısız olduğunda devreye giren güvenli yedek çalışma planıdır.
- **Function Calling:** *LLM*'in bir fonksiyonu belirli argümanlarla çağırmak için yapılandırılmış talimat üretmesidir.
- **Latency:** İsteğin gönderilmesi ile yanıtın alınması arasındaki bekleme süresidir.
- **LLM (Large Language Model):** Büyük ölçekli metin verileriyle eğitilmiş dil modelidir.
- **LoRA / QLoRA:** Büyük dil modellerini düşük donanım maliyetiyle belirli bir alana uyarlayan ince ayar (*Fine-Tuning*) teknikleridir.
- **Model Context Protocol (MCP):** AI uygulamaları ile harici araç/veri kaynakları arasında standart iletişim kuran açık protokoldür.
- **Multi-Agent Orchestration:** Birden fazla uzman *Agent*'ın belirli kurallar ve durum geçişleriyle koordineli çalıştırılmasıdır.
- **Observability:** Sistemin iç çalışma adımlarını, gecikmelerini ve hatalarını *Trace* kayıtlarıyla şeffaf biçimde izleyebilme yeteneğidir.
- **Planning:** Karmaşık bir kullanıcı hedefini sıralı ve doğrulanabilir alt görevlere ayırma sürecidir.
- **Prompt-and-Response:** Tek seferlik girdi-çıktı mantığına dayanan, araçsız ve durumsuz klasik LLM kullanımıdır.
- **Race Condition:** Eşzamanlı çalışan *Thread*'lerin paylaşılan veriyi kontrolsüz değiştirmesi sonucu oluşan tutarsızlık hatasıdır.
- **RAG (Retrieval-Augmented Generation):** Modelin yanıt üretmeden önce harici bilgi tabanından ilgili veriyi çekip kullanmasıdır.
- **Retry & Exponential Backoff:** Geçici hatalarda isteği artan bekleme süreleriyle kontrollü olarak tekrar deneme stratejisidir.
- **State Management:** Çok adımlı iş akışlarında verinin yaşam döngüsü boyunca tutarlı ve izole biçimde yönetilmesidir.
- **Structured Outputs:** Model çıktısının katı bir JSON şemasına uyarak makine tarafından güvenle okunabilmesidir.
- **System Prompt:** Modelin davranış sınırlarını, rolünü ve kurallarını belirleyen en üst düzey yönergedir.
- **Temperature:** Modelin yanıt üretimindeki rastgelelik derecesini belirleyen parametredir.
- **Thread-Safety:** Paylaşılan kaynaklara çoklu *Thread* erişiminde veri bütünlüğünün korunmasıdır.
- **Tokenization:** Metnin *LLM* tarafından işlenebilen küçük sayısal parçalara (*Token*) ayrılmasıdır.
- **Tool Use:** *Agent*'ın veritabanı, API veya hesaplama gibi dış fonksiyonları çağırarak gerçek dünya verisiyle işlem yapmasıdır.
- **Trade-off:** Bir mühendislik seçiminde elde edilen fayda karşılığında kabul edilen maliyet veya kısıttır.
- **Vector Database:** *Embedding* vektörlerini saklayıp hızlı benzerlik araması yapan özel veritabanı türüdür.
