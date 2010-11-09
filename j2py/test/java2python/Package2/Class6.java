package test.java2python.Package2;


// tests basic class member lookup; python code changes 'x' to 'self.x'
public class Class6 {
    int x = 42;

    public void spam() {
        System.out.println( x );
    };

    public static void main(String[] args) {
        Class6 c = new Class6();
        c.spam();
    }
}
