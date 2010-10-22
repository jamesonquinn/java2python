

package test.java2python;

import test.java2python.Class6;

// tests basic class member lookup; python code changes 'x' to 'self.x' and 'y' to 'self.y'
class Class7 extends Class6 {
    int y = 43;

    public void spam2() {
        System.out.println( x );
        System.out.println( y );
    };

    public static void main(String[] args) {
        Class7 c = new Class7();
        c.spam();
        c.spam2();
    }
}
