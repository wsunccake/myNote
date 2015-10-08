package listing;

public class ShowCurrentTime {
    long currentSecond;
    long currentMinute;
    long currentHour;

    public ShowCurrentTime() {
        long totalMilliseconds = System.currentTimeMillis();
        long totalSeconds = totalMilliseconds / 1000;
        currentSecond = totalSeconds % 60;
        long totalMinutes = totalSeconds / 60;
        currentMinute = totalMinutes % 60;
        long totalHours = totalMinutes / 60;
        currentHour = totalHours % 24;

        System.out.println("Current time is " + currentHour + ":" + currentMinute + ":" + currentSecond + " GMT");
        System.out.format("Current time is %d:%d:%d GMT\n", currentHour, currentMinute, currentSecond);
    }

    public void SetOffsetGMT(long offset) {
        System.out.format("Current time is %d:%d:%d", currentHour + offset, currentMinute, currentSecond);
    }

    public static void main(String[] args) {
        ShowCurrentTime t = new ShowCurrentTime();
    }
}
