public class Solution {
    public int addDigits(int num) {
        int sum = 0;
        for(char c : String.valueOf(num).toCharArray()) {
            sum += Character.getNumericValue(c);
        }
        sum = sum > 10 ? addDigits(sum) : sum;
        return sum;
    }
}