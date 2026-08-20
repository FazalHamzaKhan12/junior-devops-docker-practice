import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Main {
    private static long toMegabytes(long bytes) {
        return bytes / (1024 * 1024);
    }

    public static void main(String[] args) {
        Runtime runtime = Runtime.getRuntime();
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
        boolean runningInDocker = Files.exists(Path.of("/.dockerenv"));

        System.out.println("========================================");
        System.out.println("       Simple Java Docker App");
        System.out.println("========================================");
        System.out.println("Current time : " + LocalDateTime.now().format(formatter));
        System.out.println("Operating OS : " + System.getProperty("os.name"));
        System.out.println("Java version : " + System.getProperty("java.version"));
        System.out.println("CPU cores    : " + runtime.availableProcessors());
        System.out.println("Max memory   : " + toMegabytes(runtime.maxMemory()) + " MB");
        System.out.println("Total memory : " + toMegabytes(runtime.totalMemory()) + " MB");
        System.out.println("Free memory  : " + toMegabytes(runtime.freeMemory()) + " MB");
        System.out.println(
            "Docker status: " +
            (runningInDocker
                ? "Java application is running inside Docker."
                : "Docker environment was not detected.")
        );
        System.out.println("========================================");
    }
}
