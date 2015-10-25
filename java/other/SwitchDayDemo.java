package other;

public class SwitchDayDemo {
    enum Day {
        Monday, Tuesday, Wednesday, Thursday,
        Friday, Saturday, Sunday;
    }

    public static void main() {
        Day day = Day.Monday;

        switch (day) {
            case Monday:
            case Tuesday:
            case Wednesday:
            case Thursday:
            case Friday:
                System.out.println("Today is working day");
                break;
            case Saturday:
            case Sunday:
                System.out.println("Today is weekend");
                break;
        }
    }
}
