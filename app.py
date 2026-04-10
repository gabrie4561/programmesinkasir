import streamlit as st

# Menyimpan data keranjang agar tidak terhapus saat halaman dimuat ulang
if 'keranjang' not in st.session_state:
    st.session_state.keranjang = []
    st.session_state.total = 0

# Dictionary untuk menyimpan daftar menu dan harga agar kode lebih rapi
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

# Bagian Input Pesanan
st.subheader('Tambah Pesanan')
pilihan_menu = st.selectbox('Pilih menu:', list(menu_dict.keys()))
qty = st.number_input('Masukkan jumlah pesanan:', min_value=1, value=1)

if st.button('Tambah ke Keranjang'):
    harga = menu_dict[pilihan_menu]
    subtotal = harga * qty
    
    # Masukkan ke keranjang
    st.session_state.keranjang.append({
        'menu': pilihan_menu, 'harga': harga, 'qty': qty, 'subtotal': subtotal
    })
    st.session_state.total += subtotal
    st.success(f'Ditambahkan: {pilihan_menu} x {qty} = Rp {subtotal}')

st.markdown('---')

# Bagian Struk dan Pembayaran
if st.session_state.keranjang:
    st.subheader('Daftar Pesanan Saat Ini')
    for i, item in enumerate(st.session_state.keranjang):
        st.write(f"{i+1}. {item['menu']} x{item['qty']} @Rp{item['harga']} = Rp{item['subtotal']}")
    
    st.write(f"**Total Keseluruhan: Rp {st.session_state.total}**")
    
    bayar = st.number_input('Masukkan uang pembayaran (Rp):', min_value=0, step=1000)
    
    if st.button('Bayar'):
        if bayar >= st.session_state.total:
            kembalian = bayar - st.session_state.total
            st.success('Pembayaran Berhasil!')
            
            st.code(f"""
=========== STRUK PEMBAYARAN ===========
Total           : Rp {st.session_state.total}
Uang dibayar    : Rp {bayar}
Kembalian       : Rp {kembalian}
----------------------------------------
Terima kasih telah membeli
========================================
            """)
            
            # Tombol untuk mereset pesanan
            if st.button('Selesaikan & Buat Pesanan Baru'):
                st.session_state.keranjang = []
                st.session_state.total = 0
                st.rerun()
        else:
            st.error('Uang pembayaran kurang!')
