package chapter3.exercise;

import java.util.Random;

public class Homework_3_4 {
    public static void solution1() {
//        Math.random()*(n-m)+m;
        int num = (int) (Math.random() * 12 + 1);
        String month = "";
        switch (num) {
            case 1:
                month = "January";
                break;
            case 2:
                month = "February";
                break;
            case 3:
                month = "March";
                break;
            case 4:
                month = "April";
                break;
            case 5:
                month = "May";
                break;
            case 6:
                month = "June";
                break;
            case 7:
                month = "July";
                break;
            case 8:
                month = "August";
                break;
            case 9:
                month = "September";
                break;
            case 10:
                month = "October";
                break;
            case 11:
                month = "November";
                break;
            case 12:
                month = "December";
                break;
        }
        System.out.println(month);
    }

    public static void solution2() {
        String[] months = {"January", "February", "March", "April", "May", "June",
                           "July", "August", "September", "October", "November", "December"};
        Random random = new Random();
        System.out.println(months[random.nextInt(12)]);
    }

    public static void main(String[] args) {
        solution1();
        solution2();
    }
}
