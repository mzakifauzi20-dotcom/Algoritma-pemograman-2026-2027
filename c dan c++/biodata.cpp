#include <iostream>
#include <string>
using namespace std;

int main() {
    string nama, kota, hobi;
    int umur;
    cout << "Nama : ";
    getline(cin, nama);
    cout << "Umur : ";
    cin >> umur;
    cin.ignore(); // buang '\n' sisa setelah angka
    cout << "Kota : ";
    getline(cin, kota);
    cout << "Hobi : "; // baru
    getline(cin, hobi); // baru
    cout << nama << ", " << umur << " tahun, dari " << kota << '\n';
    cout << "Tahun depan umur " << umur + 1 << '\n';
    cout << "Hobi: " << hobi << '\n'; // baru

}