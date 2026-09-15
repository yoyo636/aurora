// MathUtils.java — Java 数学工具类示例
// 编译: javac MathUtils.java
// 运行: java MathUtils
// Aurora 调用: std.java.call("MathUtils", "add", 3, 4)

public class MathUtils {

    // 基本运算
    public static int add(int a, int b) {
        return a + b;
    }

    public static int subtract(int a, int b) {
        return a - b;
    }

    public static int multiply(int a, int b) {
        return a * b;
    }

    public static double divide(double a, double b) {
        if (b == 0) throw new ArithmeticException("Division by zero");
        return a / b;
    }

    // 数组操作
    public static int sum(int[] numbers) {
        int total = 0;
        for (int n : numbers) total += n;
        return total;
    }

    public static double average(int[] numbers) {
        if (numbers.length == 0) return 0;
        return (double) sum(numbers) / numbers.length;
    }

    public static int max(int[] numbers) {
        int m = numbers[0];
        for (int n : numbers) if (n > m) m = n;
        return m;
    }

    public static int min(int[] numbers) {
        int m = numbers[0];
        for (int n : numbers) if (n < m) m = n;
        return m;
    }

    // 字符串操作
    public static String greet(String name) {
        return "Hello, " + name + "!";
    }

    public static String reverse(String str) {
        return new StringBuilder(str).reverse().toString();
    }

    // 主方法
    public static void main(String[] args) {
        System.out.println("Java MathUtils Module");
        System.out.println("add(3, 4) = " + add(3, 4));
        System.out.println("multiply(5, 6) = " + multiply(5, 6));
        System.out.println("greet(\"Aurora\") = " + greet("Aurora"));
        int[] nums = {1, 2, 3, 4, 5};
        System.out.println("sum([1,2,3,4,5]) = " + sum(nums));
        System.out.println("average([1,2,3,4,5]) = " + average(nums));
    }
}
