"""
Utility functions untuk API synchronization
"""
import logging
from typing import Dict, List, Optional
from decouple import config
import requests

logger = logging.getLogger(__name__)

class APIClient:
    """
    Client untuk menangani komunikasi dengan API eksternal
    """
    
    def __init__(self):
        self.base_url = config('API_BASE_URL')
        self.username = config('API_USERNAME')
        self.password = config('API_PASSWORD')
        self.token = None
    
    def get_token(self) -> Optional[str]:
        """
        Mendapatkan token autentikasi dari API
        """
        try:
            data = {
                'act': 'GetToken',
                'username': self.username,
                'password': self.password
            }
            
            response = requests.post(self.base_url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            print(result)
            # API menggunakan 'success': 'true' (string) bukan 'status': 'success'
            if result.get('success') == 'true':
                self.token = result.get('token')
                return self.token
            else:
                logger.error(f"API Error: {result.get('message', 'Unknown error')}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while getting token: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while getting token: {e}")
            return None
    
    def get_dosen_data(self) -> List[Dict]:
        """
        Mengambil data dosen dari API dengan pagination
        """
        if not self.token:
            if not self.get_token():
                return []
        
        all_data = []
        page = 1
        rows_per_page = 100  # Ambil lebih banyak data per request
        total_expected_records = None  # Track total records dari API
        
        while True:
            try:
                # Headers sesuai dengan curl command
                headers = {
                    'rows': str(rows_per_page),
                    'page': str(page)
                }
                
                data = {
                    'act': 'ListDosen',
                    'token': self.token
                }
                
                response = requests.post(self.base_url, headers=headers, data=data, timeout=30)
                response.raise_for_status()
                
                result = response.json()
                
                # Debug response structure (hanya untuk halaman pertama)
                if page == 1:
                    print(f"API Response keys: {list(result.keys())}")
                
                # API menggunakan 'success': 'true' (string) bukan 'status': 'success'
                if result.get('success') == 'true':
                    # Data dosen ada di key 'rows'
                    page_data = result.get('rows', [])
                    total_records = result.get('records', 0)
                    
                    # Set total expected records dari response pertama
                    if total_expected_records is None:
                        total_expected_records = total_records
                        print(f"Total records available in API: {total_expected_records}")
                    
                    print(f"Page {page}: received {len(page_data)} records")
                    
                    # Debug: print sample data dari halaman pertama
                    if page == 1 and page_data:
                        print(f"Sample data: {page_data[0]}")
                    
                    if not page_data:  # Tidak ada data lagi
                        print("No more data available, stopping pagination")
                        break
                    
                    all_data.extend(page_data)
                    
                    # Validasi: jika total data yang sudah diterima >= total records dari API
                    if len(all_data) >= total_expected_records:
                        print(f"Received all expected records ({len(all_data)}/{total_expected_records}), stopping pagination")
                        break
                    
                    # Jika data kurang dari rows_per_page, berarti sudah halaman terakhir
                    if len(page_data) < rows_per_page:
                        print("Received less data than requested, reached last page")
                        break
                    
                    page += 1
                    
                    # Safety check: hindari infinite loop jika ada masalah
                    if page > 100:  # Maksimal 100 halaman (10,000 records dengan 100 per halaman)
                        print("Reached maximum page limit (100), stopping for safety")
                        break
                        
                else:
                    logger.error(f"API Error: {result.get('message', 'Unknown error')}")
                    print(f"Failed response: {result}")
                    break
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Network error while getting dosen data page {page}: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error while getting dosen data page {page}: {e}")
                break
        
        print(f"Total dosen data fetched: {len(all_data)}")
        if total_expected_records:
            print(f"Data completeness: {len(all_data)}/{total_expected_records} ({(len(all_data)/total_expected_records*100):.1f}%)")
        
        return all_data
    
    def get_mahasiswa_profile(self, nim: str) -> Optional[Dict]:
        """
        Mendapatkan profil mahasiswa berdasarkan NIM
        
        Args:
            nim (str): Nomor Induk Mahasiswa
            session_cookie (str): Session cookie untuk autentikasi (opsional)
            
        Returns:
            Dict: Data profil mahasiswa atau None jika gagal
        """
        if not self.token:
            if not self.get_token():
                logger.error("Failed to get token for mahasiswa profile request")
                return None
        
        try:
            # Setup headers
            headers = {}
            # Data form sesuai dengan curl command
            data = {
                'act': 'Mhs',
                'token': self.token,
                'nim': nim
            }
            
            response = requests.post(self.base_url, headers=headers, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Debug response
            logger.info(f"Mahasiswa profile response keys: {list(result.keys())}")
            
            # Periksa apakah request berhasil
            if result.get('success') == 'true':
                mahasiswa_data = result.get('data', {})
                logger.info(f"Successfully retrieved profile for NIM: {nim}")
                return mahasiswa_data
            else:
                error_message = result.get('message', 'Unknown error')
                logger.error(f"API Error for NIM {nim}: {error_message}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while getting mahasiswa profile for NIM {nim}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while getting mahasiswa profile for NIM {nim}: {e}")
            return None
    
    def get_mahasiswa_data(self, prodi: str = None, angkatan: str = None) -> List[Dict]:
        """
        Mengambil data mahasiswa dari API berdasarkan prodi dan angkatan
        
        Args:
            prodi (str): Kode program studi (opsional)
            angkatan (str): Tahun angkatan (opsional)
            
        Returns:
            List[Dict]: List data mahasiswa yang sesuai dengan filter
        """
        if not self.token:
            if not self.get_token():
                return []
        
        try:
            # Data form sesuai dengan format yang diminta
            data = {
                'act': 'ListMahasiswa',
                'token': self.token
            }
            
            # Tambahkan filter jika disediakan
            if prodi:
                data['prodi'] = prodi
            if angkatan:
                data['angkatan'] = angkatan
            
            response = requests.post(self.base_url, data=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            # Debug response structure
            print(f"Mahasiswa API Response keys: {list(result.keys())}")
            
            # API menggunakan 'success': 'true' (string) bukan 'status': 'success'
            if result.get('success') == 'true':
                # Data mahasiswa ada di key 'rows'
                mahasiswa_data = result.get('rows', [])
                total_records = result.get('records', 0)
                
                print(f"Total mahasiswa records found: {total_records}")
                print(f"Received {len(mahasiswa_data)} mahasiswa records")
                
                # Debug: print sample data jika ada
                if mahasiswa_data:
                    print(f"Sample mahasiswa data: {mahasiswa_data[0]}")
                
                return mahasiswa_data
                        
            else:
                error_message = result.get('message', 'Unknown error')
                logger.error(f"Mahasiswa API Error: {error_message}")
                print(f"Failed mahasiswa response: {result}")
                return []
                    
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while getting mahasiswa data: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error while getting mahasiswa data: {e}")
            return []
    

def validate_dosen_data(data: Dict) -> bool:
    """
    Validasi data dosen yang diterima dari API
    """
    # Field yang diterima dari API
    required_fields = ['nama', 'email', 'uniid']
    
    # Cek apakah semua field yang diperlukan ada
    if not all(field in data for field in required_fields):
        return False
    
    # Cek apakah field tidak kosong
    if not all(str(data.get(field, '')).strip() for field in required_fields):
        return False
    
    # Validasi iddsn tidak boleh kosong (digunakan sebagai nik)
    iddsn = str(data.get('iddsn', '')).strip()
    if not iddsn:
        return False
    
    # Validasi format email sederhana
    email = data.get('email', '')
    if '@' not in email or '.' not in email:
        return False
    
    # Validasi NIDN (optional field, bisa kosong)
    nidn = data.get('nidn', '')
    if nidn and nidn != '-' and nidn != '':
        # NIDN biasanya 10 digit, tapi ada yang berbeda format
        pass
    
    return True

def normalize_dosen_data(data: Dict) -> Dict:
    """
    Normalisasi data dosen sebelum disimpan ke database
    """
    normalized = {}
    
    # Mapping dari field API ke field database
    # Gunakan iddsn sebagai nik karena itu identifier unik
    normalized['nik'] = str(data.get('iddsn', '')).strip()
    normalized['uniid'] = str(data.get('uniid', '')).strip()
    normalized['nama_dosen'] = str(data.get('nama', '')).strip().title()  # Title case untuk nama
    normalized['email'] = str(data.get('email', '')).strip().lower()  # Lowercase untuk email
    
    return normalized

def validate_mahasiswa_data(data: Dict) -> bool:
    """
    Validasi data mahasiswa yang diterima dari API
    """
    # Field yang diperlukan untuk mahasiswa
    required_fields = ['nim', 'nama']
    
    # Cek apakah semua field yang diperlukan ada
    if not all(field in data for field in required_fields):
        logger.warning(f"Missing required fields in mahasiswa data: {data}")
        return False
    
    # Cek apakah field tidak kosong
    if not all(str(data.get(field, '')).strip() for field in required_fields):
        logger.warning(f"Empty required fields in mahasiswa data: {data}")
        return False
    
    # Validasi format NIM (biasanya numeric atau alphanumeric)
    nim = str(data.get('nim', '')).strip()
    if len(nim) < 5:  # NIM biasanya minimal 5 karakter
        logger.warning(f"Invalid NIM format: {nim}")
        return False
    
    return True

def normalize_mahasiswa_data(data: Dict) -> Dict:
    """
    Normalisasi data mahasiswa sebelum disimpan ke database
    """
    normalized = {}
    
    # Mapping dari field API ke field database
    normalized['nim'] = str(data.get('nim', '')).strip().upper()
    normalized['nama_mahasiswa'] = str(data.get('nama', '')).strip().title()
    
    # Field dari API response
    normalized['email'] = str(data.get('email', '')).strip().lower() if data.get('email') else f"{normalized['nim'].lower()}@student.ums.ac.id"
    
    # Field angkatan dari API atau extract dari NIM
    if 'angkatan' in data and data.get('angkatan'):
        try:
            normalized['angkatan'] = int(data.get('angkatan'))
        except (ValueError, TypeError):
            # Fallback: extract dari NIM
            nim = normalized['nim']
            if len(nim) >= 7 and nim[1:5].isdigit():
                normalized['angkatan'] = int(nim[1:5])
            else:
                normalized['angkatan'] = 2024  # Default
    else:
        # Extract dari NIM (format: L200170149 -> angkatan = 2017)
        nim = normalized['nim']
        if len(nim) >= 7 and nim[1:5].isdigit():
            normalized['angkatan'] = int(nim[1:5])
        else:
            normalized['angkatan'] = 2024  # Default
    
    # Field kode_prodi dari API
    normalized['prodi'] = str(data.get('kode_prodi', '')).strip() if data.get('kode_prodi') else ''
    
    # Field opsional lainnya dengan default values
    normalized['semester'] = int(data.get('semester', 1)) if data.get('semester') and str(data.get('semester')).isdigit() else 1
    normalized['fakultas'] = str(data.get('fakultas', '')).strip() if data.get('fakultas') else ''
    normalized['status'] = str(data.get('status', '')).strip() if data.get('status') else 'Aktif'
    normalized['no_hp'] = str(data.get('no_hp', '')).strip() if data.get('no_hp') else ''
    normalized['alamat'] = str(data.get('alamat', '')).strip() if data.get('alamat') else ''
    
    return normalized
