package chapter3.exercise;

import java.util.Random;
import java.util.Scanner;

public class Homework_3_17 {
    public static void solution2 (int computer_number, int you_number) {
        int check_value = -1;
        String[] numbers = {"scissor", "rock", "paper"};
        if (computer_number == 2)
            check_value = 2;

        String result = "Computer won";
        if (computer_number == you_number)
            result = "It is a draw";
        else if (computer_number == (you_number + check_value))
            result = "You won";

        String computer_result = numbers[computer_number];
        String you_result = numbers[you_number];
        System.out.format("The computer is %s. You are %s. %s", computer_result, you_result, result);
    }

    public static void main(String[] args) {
        Random random = new Random();
        int computer_num = random.nextInt(3);
        System.out.println("scissor(0), rock(1), paper(2): " + computer_num);
        Scanner input = new Scanner(System.in);
        solution2(computer_num, input.nextInt());
    }
}
