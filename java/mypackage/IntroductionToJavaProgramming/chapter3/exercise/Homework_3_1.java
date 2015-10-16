package chapter3.exercise;

import java.util.Scanner;

public class Homework_3_1 {
    public static void solution(double a, double b, double c) {
        double d = b * b - 4.0 * a * c;
        double e = -b / 2.0 / a;
        if (d < 0.0) {
            System.out.println("The equation had no real roots");
        }
        else if (d == 0.0) {
            System.out.println("The equation had one root" + e);
        }
        else {
            double f = Math.pow(d, 0.5) / 2.0 / a;
            System.out.println("The equation had one root" + (e + f) + " and " + (e - f));
        }
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        System.out.println("Enter a, b, c: ");

        double a = input.nextDouble();
        double b = input.nextDouble();
        double c = input.nextDouble();

        solution(a, b, c);
    }

}
