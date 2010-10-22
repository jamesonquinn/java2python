// tests basic subclassing
class Base {
    static int x = 42;
}


class Class5 extends Base {
    static int y = 43;
    public static void main(String[] args) {
        System.out.println("extends, by "+x +" - that's almost " + y);
    }
}
