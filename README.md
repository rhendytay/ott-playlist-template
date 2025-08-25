# OTT Playlist (Auto Filter MNC Group)

Repo ini otomatis mengambil playlist dari `bit.ly/KITKATTV`, menyaring channel MNC Group (RCTI, MNCTV, GTV, iNews), dan menyimpan hasilnya ke `kitkat_clean.m3u` di branch default.

## Cara pakai (ringkas)

1. **Public repository** disarankan (agar link bisa diakses player).
2. Upload file ini dan `update_playlist.py` ke repo.
3. Aktifkan **GitHub Pages**: Settings → Pages → _Deploy from a branch_ → Branch: `main` (root).
4. Jalankan workflow di tab **Actions** → _Run workflow_.
5. Akses playlist di:
   ```
   https://<username>.github.io/<nama-repo>/iptv_channel.m3u
   ```

## Ubah daftar channel yang diblokir

Edit env `BLOCK_KEYWORDS` di workflow:

```
BLOCK_KEYWORDS: RCTI,MNCTV,GTV,iNews
```

Pisahkan dengan koma, case-insensitive.

## Jalankan lokal (opsional)

```bash
pip install requests
python update_playlist.py
```
