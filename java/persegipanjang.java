import java.util.Locale;
import java.util.Scanner;

public class persegipanjang {
    public static void main(String[] args) {
        var in = new Scanner(System.in).useLocale(Locale.US);

        System.out.print("Panjang : ");
        double p = in.nextDouble();
        System.out.print("Lebar : ");
        double l = in.nextDouble();

        System.out.printf(Locale.US, "Luas : %.2f%n", p * l);
        System.out.printf(Locale.US, "Keliling : %.2f%n", 2 * (p + l));
     }
}