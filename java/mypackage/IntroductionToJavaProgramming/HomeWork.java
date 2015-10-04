package mypackage.IntroductionToJavaProgramming;

import java.util.Scanner;

public class HomeWork {
    public static void HomeWork_1_3() {
        String java = "    J\n" +
                      "    J  aaa   v   v  aaa\n" +
                      "J   J  a a    v v   a a\n" +
                      " J J   aaaa    v    aaaa\n";
        System.out.print(java);
    }

    public static void HomeWork_2_8() {
        ShowCurrentTime t = new ShowCurrentTime();
        Scanner input = new Scanner(System.in);
        System.out.print("Enter the time zone offset to GMT: ");
        long offset = input.nextLong();
        t.SetOffsetGMT(offset);
    }

    public static void HomeWork_2_15() {
        Scanner input = new Scanner(System.in);
        System.out.println("Enter x1 and y1:");
        double x1 = input.nextDouble();
        double y1 = input.nextDouble();
        System.out.println("Enter x2 and y2:");
        double x2 = input.nextDouble();
        double y2 = input.nextDouble();
        double distance = Math.sqrt((x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2));
        System.out.println("The distance between the two points is :" + distance);
    }


}
