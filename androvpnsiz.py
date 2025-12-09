import requests
import os
import json
import time
import concurrent.futures
from urllib.parse import quote
import sys

def test_proxy_speed(proxy_url, test_url="https://httpbin.org/ip", timeout=3):
    """Proxy hızını test et"""
    try:
        start_time = time.time()
        response = requests.get(test_url, timeout=timeout, 
                              proxies={"http": proxy_url, "https": proxy_url})
        if response.status_code == 200:
            speed = time.time() - start_time
            return proxy_url, speed, True
    except:
        pass
    return proxy_url, 10, False

def get_fastest_proxies():
    """Hızlı proxy'leri bul - GitHub için optimize edilmiş"""
    print("⚡ GitHub Actions için proxy test ediliyor...")
    
    # GitHub Actions için özel proxy listesi
    proxy_list = [
        # Cloudflare Workers (GitHub'ta çalışır)
        "https://corsproxy.io/?",
        "https://api.codetabs.com/v1/proxy?quest=",
        "https://proxy.ponelat.workers.dev/",
        "https://cors.gerhut.workers.dev/?",
        
        # Güvenilir public proxy'ler
        "http://20.210.113.32:80",
        "http://20.206.106.192:80",
        
        # Türkiye proxy'leri
        "http://88.255.102.10:8080",
        "http://176.235.99.12:9090",
        "http://95.0.219.201:8080",
    ]
    
    # Workers proxy'leri
    workers = [
        ("CF-Proxy", "https://withered-shape-3305.vadimkantorov.workers.dev/?"),
        ("Rapid-Proxy", "https://rapid-wave-c8e3.redfor14314.workers.dev/"),
        ("Cors-Free", "https://proxy.freecdn.workers.dev/?url="),
        ("Hello-World", "https://hello-world-aged-resonance-fc8f.bokaflix.workers.dev/?apiUrl="),
        ("AllOrigins", "https://api.allorigins.win/raw?url="),  # Yeni ekle
    ]
    
    fast_proxies = []
    
    # Sadece workers proxy'lerini kullan (GitHub'ta daha güvenilir)
    for name, url in workers:
        fast_proxies.append(url)
        print(f"   ✅ {name} eklendi")
    
    # GitHub Actions ortam kontrolü
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("🚀 GitHub Actions ortamında çalışıyor")
        # GitHub'ta daha fazla workers ekleyelim
        extra_workers = [
            "https://cors-anywhere.herokuapp.com/",
            "https://thingproxy.freeboard.io/fetch/",
            "https://yacdn.org/proxy/",
        ]
        fast_proxies.extend(extra_workers)
    
    # Direkt erişimi de ekle
    fast_proxies.append("direct")
    
    return fast_proxies[:10]

def check_url_with_proxy(url, proxies, timeout=5):
    """URL'i proxy ile kontrol et"""
    # Önce doğrudan dene
    try:
        response = requests.head(url, timeout=timeout)
        if response.status_code == 200:
            return url, "direct"
    except:
        pass
    
    # Proxy'lerle dene
    for proxy in proxies:
        if proxy == "direct":
            continue
            
        try:
            if proxy.endswith("?") or "?url=" in proxy or "?quest=" in proxy or "apiUrl=" in proxy or "/raw?url=" in proxy:
                # Worker proxy formatı
                if "allorigins.win" in proxy:
                    proxy_url = f"{proxy}{quote(url, safe='')}"
                else:
                    proxy_url = f"{proxy}{url}"
            elif "/proxy/" in proxy or "/fetch/" in proxy:
                # Diğer proxy formatları
                proxy_url = f"{proxy}{url}"
            elif proxy.startswith("http://") or proxy.startswith("https://"):
                # Normal proxy formatı
                proxy_url = url
                proxies_dict = {"http": proxy, "https": proxy}
                response = requests.head(proxy_url, timeout=timeout, proxies=proxies_dict)
                if response.status_code == 200:
                    return proxy_url, proxy
                continue
            else:
                continue
                
            response = requests.head(proxy_url, timeout=timeout)
            if response.status_code == 200:
                return proxy_url, proxy.split("//")[-1].split("/")[0]
        except Exception as e:
            continue
    
    return None, None

def get_active_base_url(proxies):
    """Aktif base URL'yi bul"""
    print("\n🔍 Aktif domain aranıyor...")
    
    # Öncelikli domainler
    priority_domains = [
        "https://andro.226503.xyz/checklist/",
        "https://androiptv.fun/checklist/",
        "https://birazcikspor.xyz/checklist/",
        "https://androstream.live/checklist/",
    ]
    
    test_channels = [
        "androstreamlivebs1",
        "androstreamlivess1",
        "androstreamlivets"
    ]
    
    for domain in priority_domains:
        for channel in test_channels:
            test_url = f"{domain}{channel}.m3u8"
            stream_url, used_proxy = check_url_with_proxy(test_url, proxies, timeout=3)
            if stream_url:
                print(f"✅ Aktif domain: {domain} (via {used_proxy})")
                return domain
    
    # Alternatif domainleri tarama
    print("⚠  Öncelikli domainler çalışmıyor, alternatifler taranıyor...")
    
    for i in range(1, 30):
        domain = f"https://birazcikspor{i}.xyz/checklist/"
        test_url = f"{domain}androstreamlivebs1.m3u8"
        try:
            response = requests.head(test_url, timeout=2)
            if response.status_code == 200:
                print(f"✅ Alternatif domain: {domain}")
                return domain
        except:
            continue
    
    # Son çare
    default_domain = "https://andro.226503.xyz/checklist/"
    print(f"⚠  Varsayılan domain: {default_domain}")
    return default_domain

def get_DeaTHLesS_streams():
    """DeaTHLesS IPTV stream'lerini al"""
    
    print("=" * 60)
    print("🚀 DeaTHLesS IPTV Bot - GitHub Actions Optimize")
    print("=" * 60)
    
    # GitHub Actions kontrolü
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        print("📦 GitHub Actions ortamında çalışıyor")
        print("🔧 Proxy ayarları optimize ediliyor...")
    
    # 1. Proxy'leri al
    proxies = get_fastest_proxies()
    print(f"📊 Kullanılacak proxy sayısı: {len(proxies)}")
    
    # 2. Aktif domain'i bul
    base_url = get_active_base_url(proxies)
    
    # 3. Kanal listesi oluştur
    print(f"\n📡 Kanal listesi oluşturuluyor: {base_url}")
    
    channels = get_channel_list()
    
    m3u_content = "#EXTM3U\n"
    m3u_content += "# DeaTHLesS IPTV - GitHub Actions\n"
    m3u_content += f"# Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
    m3u_content += f"# Base URL: {base_url}\n\n"
    
    successful = 0
    total = len(channels)
    
    for name, channel_id in channels:
        url = f"{base_url}{channel_id}.m3u8"
        stream_url, proxy_used = check_url_with_proxy(url, proxies)
        
        if stream_url:
            logo_url = "https://i.hizliresim.com/8xzjgqv.jpg"
            m3u_content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="TR:{name}" tvg-logo="{logo_url}" group-title="TURKIYE",{name}\n'
            
            # GitHub Actions'ta farklı format
            if os.environ.get('GITHUB_ACTIONS') == 'true':
                # Direkt URL veya basit proxy kullan
                if proxy_used and proxy_used != "direct":
                    m3u_content += f"{stream_url}\n"
                else:
                    m3u_content += f"{url}\n"
            else:
                m3u_content += f"{stream_url}\n"
            
            successful += 1
            print(f"✅ {name}")
        else:
            print(f"❌ {name}")
    
    print(f"\n📊 Sonuç: {successful}/{total} kanal bulundu")
    
    # Çok az kanal bulunduysa, alternatif yaklaşım dene
    if successful < 5:
        print("\n⚠  Çok az kanal bulundu, alternatif yöntem deneniyor...")
        alt_content = try_alternative_method(base_url)
        if alt_content:
            m3u_content += alt_content
            print("✅ Alternatif yöntemle kanallar eklendi")
    
    return m3u_content

def get_channel_list():
    """Kanal listesini döndür"""
    return [
        ["beIN Sport 1 HD", "androstreamlivebs1"],
        ["beIN Sport 2 HD", "androstreamlivebs2"],
        ["beIN Sport 3 HD", "androstreamlivebs3"],
        ["beIN Sport 4 HD", "androstreamlivebs4"],
        ["beIN Sport 5 HD", "androstreamlivebs5"],
        ["S Sport 1 HD", "androstreamlivess1"],
        ["S Sport 2 HD", "androstreamlivess2"],
        ["Tivibu Sport HD", "androstreamlivets"],
        ["Tivibu Sport 1 HD", "androstreamlivets1"],
        ["Tivibu Sport 2 HD", "androstreamlivets2"],
        ["Tabii HD", "androstreamlivetb"],
        ["Tabii 1 HD", "androstreamlivetb1"],
        ["Exxen HD", "androstreamliveexn"],
        ["Exxen 1 HD", "androstreamliveexn1"],
        ["Facebook beIN Sport 1", "facebooklivebs1"],
        ["Facebook S Sport 1", "facebooklivess1"],
    ]

def try_alternative_method(base_url):
    """Alternatif yöntemle kanal bul"""
    content = ""
    
    # Basit bir yaklaşım: tüm olası kanalları ekle
    channels = [
        ("beIN Sport 1", "androstreamlivebs1"),
        ("beIN Sport 2", "androstreamlivebs2"),
        ("S Sport 1", "androstreamlivess1"),
        ("Tivibu Sport", "androstreamlivets"),
    ]
    
    for name, channel_id in channels:
        url = f"{base_url}{channel_id}.m3u8"
        content += f'#EXTINF:-1 tvg-id="sport.tr" tvg-name="{name}",{name}\n'
        content += f"{url}\n"
    
    return content

def save_m3u_file(content):
    """M3U dosyasını kaydet"""
    try:
        file_name = "androvpnsiz.m3u"
        
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(content)
        
        channel_count = content.count('#EXTINF')
        
        print("\n" + "=" * 60)
        print("✅ İŞLEM TAMAMLANDI!")
        print("=" * 60)
        print(f"📂 Dosya: {file_name}")
        print(f"📊 Toplam Kanal: {channel_count}")
        print(f"💾 Boyut: {len(content.encode('utf-8'))} bytes")
        
        # GitHub Actions için ek bilgi
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            print("\n🚀 GitHub Actions: M3U dosyası oluşturuldu")
            print("📤 Otomatik commit yapılacak")
        
        return file_name
        
    except Exception as e:
        print(f"❌ Dosya kaydetme hatası: {e}")
        return None

if __name__ == "__main__":
    try:
        print(f"Python {sys.version}")
        print(f"Çalışma dizini: {os.getcwd()}")
        
        m3u_data = get_DeaTHLesS_streams()
        
        if m3u_data and m3u_data.count('#EXTINF') > 0:
            saved_file = save_m3u_file(m3u_data)
            
            # Örnek çıktı
            print("\n📋 İlk 5 kanal:")
            lines = m3u_data.split('\n')
            count = 0
            for line in lines:
                if line.startswith('#EXTINF') and count < 5:
                    name = line.split(',')[-1] if ',' in line else line
                    print(f"  {count+1}. {name}")
                    count += 1
            
        else:
            print("\n❌ HATA: Hiç kanal bulunamadı!")
            print("Lütfen scripti yeniden çalıştırın veya proxy ayarlarını kontrol edin.")
            
    except KeyboardInterrupt:
        print("\n⏹ İşlem durduruldu")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}")
        import traceback
        traceback.print_exc()
