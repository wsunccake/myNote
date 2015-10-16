package chpater2.exercise;

import java.util.Scanner;

public class HomeWork_2_8 {
    public static void main() {
        listing.ShowCurrentTime t = new listing.ShowCurrentTime();
        Scanner input = new Scanner(System.in);
        System.out.print("Enter the time zone offset to GMT: ");
        long offset = input.nextLong();
        t.SetOffsetGMT(offset);
    }
}
