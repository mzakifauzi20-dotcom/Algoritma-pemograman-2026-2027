import java.util.Locale;
import java.util.Scanner;

public class lingkaran {
    public static void main(String[] args) {
        var in = new Scanner(System.in).useLocale(Locale.US);
        
        System.out.print("Jari-jari : ");
        double r = in.nextDouble();

        double luas = Math.PI * r * r;
        double keliling = 2 * Math.PI * r;
        System.out.printf(Locale.US, "Luas : %.2f%n", luas);
        System.out.printf(Locale.US, "Keliling : %.2f%n", keliling);
        double diameter = 2 * r;
        System.out.printf(Locale.US, "Diameter : %.2f%n", diameter);
    }
}