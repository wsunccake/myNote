package chapter6.exercise;

import java.util.Scanner;

public class Homework_6_5 {
    public static void displaySortedNumber(double num1, double num2, double num3) {
        double greater_num = num1 > num2 ? num1 : num2;
        double less_num = num1 < num2 ? num1 : num2;
        if (num3 > greater_num) {
            System.out.format("%f, %f, %f", num3, greater_num, less_num);
        }
        else {
            if (num3 > less_num)
                System.out.format("%f, %f, %f", greater_num, num3, less_num);
            else
                System.out.format("%f, %f, %f", greater_num, less_num, num3);
        }
    }

    public static void main() {
        Scanner input = new Scanner(System.in);

        System.out.println("input three numbers: ");
        double num1 = input.nextDouble();
        double num2 = input.nextDouble();
        double num3 = input.nextDouble();
        displaySortedNumber(num1, num2, num3);
    }
}
