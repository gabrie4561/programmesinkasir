import streamlit as st

# Inisialisasi session state
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []
    st.session_state.total = 0
if 'bayar_berhasil' not in st.session_state:
    st.session_state.bayar_berhasil = False
if 'struk' not in st.session_state:
    st.session_state.struk = ""
if 'kembalian' not in st.session_state:
    st.session_state.kembalian = 0
if 'uang_bayar' not in st.session_state:
    st.session_state.uang_bayar = 0

menu_dict = {
    'Matcha': 13000, 'Taro': 13000, 'Coklat': 13000, 'Red Velvet': 13000, 'Kopi': 13000,
    'Americano': 13000, 'Lemon Tea': 13000, 'Coffucino': 13000, 'Kopi Latte': 13000, 'Strawberry Tea': 13000,
    'Kopi Susu': 15000, 'Lotus': 15000, 'Gula Aren': 15000,
    'Vanila Coff': 16000, 'Tiramisu': 16000, 'Kopi Caramel': 16000,
    'Visixty': 20000, 'Japanesh': 20000,
    'Kopi Hitam': 8000, 'Sanger': 14000
}

st.title('☕ Program Mesin Kasir')
st.markdown('---')

# Tampilan Input Pesanan (Hanya muncul jika belum bayar)
if not st.session_state.bayar_berhasil:
    st.subheader('Tambah Pesanan')
    pilihan_menu = st.selectbox('Pilih menu:', list(menu_dict.keys()))
    qty = st.number_input('Masukkan jumlah pesanan:', min_value=1, value=1)

    if st.button('Tambah ke Keranjang'):
        harga = menu_dict[pilihan_menu]
        subtotal = harga * qty
        
        st.session_state.keranjang.append({
            'menu': pilihan_menu, 'harga': harga, 'qty': qty, 'subtotal': subtotal
        })
        st.session_state.total += subtotal
        st.success(f'Ditambahkan: {pilihan_menu} x {qty} = Rp {subtotal}')

    st.markdown('---')

    # Tampilan Keranjang
    if st.session_state.keranjang:
        st.subheader('Daftar Pesanan Saat Ini')
        struk_sementara = ""
        for i, item in enumerate(st.session_state.keranjang):
            baris = f"{i+1}. {item['menu']} x{item['qty']} @Rp{item['harga']} = Rp{item['subtotal']}"
            st.write(baris)
            struk_sementara += baris + "\n"
        
        st.write(f"**Total Keseluruhan: Rp {st.session_state.total}**")
        
        # Simpan struk sementara ke session_state agar bisa dicetak nanti
        st.session_state.struk = struk_sementara
        
        bayar = st.number_input('Masukkan uang pembayaran (Rp):', min_value=0, step=1000)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button('Bayar', use_container_width=True):
                if bayar >= st.session_state.total:
                    st.session_state.kembalian = bayar - st.session_state.total
                    st.session_state.uang_bayar = bayar
                    st.session_state.bayar_berhasil = True # Ubah status menjadi berhasil
                    st.rerun() # Refresh halaman untuk menampilkan mode struk
                else:
                    st.error('Uang pembayaran kurang!')
        with col2:
            # Tombol untuk mereset/mengosongkan keranjang sebelum bayar
            if st.button('Kosongkan Keranjang', type='secondary', use_container_width=True):
                st.session_state.keranjang = []
                st.session_state.total = 0
                st.rerun()

# Tampilan Struk (Hanya muncul jika pembayaran berhasil)
else:
    st.success('Pembayaran Berhasil!')
    
    st.code(f"""
=========== STRUK PEMBAYARAN ===========
{st.session_state.struk.strip()}
----------------------------------------
Total           : Rp {st.session_state.total}
Uang dibayar    : Rp {st.session_state.uang_bayar}
Kembalian       : Rp {st.session_state.kembalian}
----------------------------------------
Terima kasih telah membeli
========================================
""")
    
    # Tombol reset setelah pembayaran selesai
    if st.button('Selesaikan & Buat Pesanan Baru', type='primary'):
        st.session_state.keranjang = []
        st.session_state.total = 0
        st.session_state.bayar_berhasil = False
        st.session_state.struk = ""
        st.session_state.kembalian = 0
        st.session_state.uang_bayar = 0
        st.rerun()
