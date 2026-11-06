#include <stdio.h>
#include <conio.h>
#include <iostream>
using namespace std;

int main()
{
    char a[30] = "---BELAJAR TIPE DATA---";
    short b;
    int c;
    long d;
    float e;
    double f;
    int g = 1;
    int h = 2;

    b = 10000;
    c = 1000000;
    d = 1000000000;
    e = 3.12;
    f = 3.12345;

    cout << a << endl;
    cout << "Tipe data short : " << b << endl;
    cout << "Tipe data int : " << c << endl;
    cout << "Tipe data long : " << d << endl;
    cout << "Tipe data float : " << e << endl;
    cout << "Tipe data double : " << f << endl;
    cout << endl;
    cout << "Berikut Hasil Boolean : " << endl;
    cout << (g > h); // akan menghasilkan nilai 0 (false), karena 1 kurang dari 2
    cout << endl;
    cout << (g < h); // akan menghasilkan nilai 1 (true), karena 1 kurang dari 2
    cout << endl;
    cout << (g == h); // akan menghasilkan nilai 0 (false), karena 1 tidak sama dengan 2
    cout << endl;
    cout << (g != h); // akan menghasilkan nilai 1 (true), karena 1 tidak sama dengan 2
}